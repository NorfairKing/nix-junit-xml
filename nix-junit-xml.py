import argparse
import subprocess
import json
from junit_xml import TestSuite, TestCase

parser = argparse.ArgumentParser(description="nix-junit-xml")
parser.add_argument("file", metavar="FILE")

args = parser.parse_args()

attribute_process = subprocess.run(["nix", "eval", "--expr", "builtins.attrNames ( import ./" + args.file + ")", "--impure", "--json"], capture_output=True)

attributes = json.loads(attribute_process.stdout)

test_cases = []

def test_attribute(attribute_name):
    completed_process = subprocess.run(["nix","build", "-f", args.file, attribute_name], capture_output=True)
    stdout = ''
    stderr = ''
    time = 1
    test_case = TestCase (
        name = attribute_name,
        elapsed_sec=time,
        file=args.file,
        stdout=completed_process.stdout,
        stderr=completed_process.stderr
    )
    if completed_process.returncode != 0:
        test_case.add_failure_info(message=completed_process.returncode)

    test_cases.append(test_case)

attributes = [ "succeeding", "failing" ]

for attribute in attributes:
    test_attribute(attribute)


ts = TestSuite("nix-build example.nix", test_cases)

# pretty printing is on by default but can be disabled using prettyprint=False
print(TestSuite.to_xml_string([ts]))

with open("junit.xml", "w") as f:
  f.write(TestSuite.to_xml_string([ts]))
