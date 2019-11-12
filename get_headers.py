#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import collections
import os
import re
import subprocess
import xml.etree.ElementTree


# Rule object representing the rule of Bazel BUILD.
Rule = collections.namedtuple(
    "Rule", "type name package srcs hdrs textual_hdrs deps visibility testonly")


def get_elem_value(elem, name):
  """Returns the value of XML element with the given name."""
  for child in elem:
    if child.attrib.get("name") != name:
      continue
    if child.tag == "string":
      return child.attrib.get("value")
    if child.tag == "boolean":
      return child.attrib.get("value") == "true"
    if child.tag == "list":
      return [nested_child.attrib.get("value") for nested_child in child]
    raise "Cannot recognize tag: " + child.tag
  return None


def normalize_paths(paths):
  """Returns the list of normalized path."""
  # e.g. ["//absl/strings:dir/header.h"] -> ["absl/strings/dir/header.h"]
  return [path.lstrip("/").replace(":", "/") for path in paths]


def parse_rule(elem, package):
  """Returns a rule from bazel XML rule."""
  return Rule(
      type=elem.attrib["class"],
      name=get_elem_value(elem, "name"),
      package=package,
      srcs=normalize_paths(get_elem_value(elem, "srcs") or []),
      hdrs=normalize_paths(get_elem_value(elem, "hdrs") or []),
      textual_hdrs=normalize_paths(get_elem_value(elem, "textual_hdrs") or []),
      deps=get_elem_value(elem, "deps") or [],
      visibility=get_elem_value(elem, "visibility") or [],
      testonly=get_elem_value(elem, "testonly") or False)


def read_build(package):
  """Runs bazel query on given package file and returns all cc rules."""
  result = subprocess.check_output(
      ["bazel", "query", package + ":all", "--output", "xml"])
  root = xml.etree.ElementTree.fromstring(result)
  return [
      parse_rule(elem, package)
      for elem in root
      if elem.tag == "rule" and elem.attrib["class"].startswith("cc_")
  ]


def collect_rules(root_path):
  """Collects and returns all rules from root path recursively."""
  rules = []
  for cur, _, _ in os.walk(root_path):
    build_path = os.path.join(cur, "BUILD.bazel")
    if os.path.exists(build_path):
      rules.extend(read_build("//" + cur))
  return rules


def relevant_rule(rule):
  """Returns true if a given rule is relevant when generating a podspec."""
  return (
      # cc_library only (ignore cc_test, cc_binary)
      rule.type == "cc_library" and
      # ignore empty rule
      (rule.hdrs + rule.textual_hdrs + rule.srcs) and
      # ignore test-only rule
      not rule.testonly)


def is_public(rule):
  if "//visibility:public" in rule.visibility:
    return True
  if "//absl:__subpackages__" in rule.visibility:
    return False
  if "internal" in rule.package or "internal" in rule.name:
    return False
  return True


def main():
  rules = filter(relevant_rule, collect_rules("absl"))
  public_headers = set()
  for rule in rules:
    if not is_public(rule):
      continue
    public_headers.update(rule.hdrs)
  for h in sorted(public_headers):
    print("#include <{}>".format(h))

if __name__ == "__main__":
  main()
