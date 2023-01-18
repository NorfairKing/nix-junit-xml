import argparse
import json
import subprocess
import time
from junit_xml import TestSuite, TestCase

parser = argparse.ArgumentParser(description="nix-junit-xml")
parser.add_argument("file", metavar="FILE")

args = parser.parse_args()

attribute_process = subprocess.run(["nix", "eval", "--expr", "builtins.attrNames ( import ./" + args.file + ")", "--impure", "--json"], capture_output=True)

attributes = json.loads(attribute_process.stdout)

test_cases = []

def test_attribute(attribute_name):

    begin = time.time()
    completed_process = subprocess.run(["nix","build", "-f", args.file, attribute_name], capture_output=True)
    end = time.time()

    duration = end - begin

    test_case = TestCase (
        name = attribute_name,
        elapsed_sec=duration,
        file=args.file,
        stdout=completed_process.stdout,
        stderr=completed_process.stderr
    )
    if completed_process.returncode != 0:
        test_case.add_failure_info(message=completed_process.returncode)

    test_cases.append(test_case)

for attribute in attributes:
    test_attribute(attribute)


ts = TestSuite("nix-build " + args.file, test_cases)

with open("junit.xml", "w") as f:
  f.write(TestSuite.to_xml_string([ts]))
