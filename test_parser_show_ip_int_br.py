from genie.testbed import load
from pprint import pprint

tb = load("testbed.yaml")

dev = tb.devices["R1"]

dev.connect()

print("=" * 50)
print("EXECUTE")
print("=" * 50)

output = dev.execute("show ip interface brief")

print(output)

print("=" * 50)
print("PARSE")
print("=" * 50)

parsed = dev.parse("show ip interface brief")

pprint(parsed)
