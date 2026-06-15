from genie.testbed import load
from genie.utils.diff import Diff

tb = load("testbed.yaml")

dev = tb.devices["R1"]

dev.connect()

print("Capturando snapshot inicial...")

pre = dev.parse("show ip interface brief")

config = """
interface Loopback10
 ip address 100.20.20.20 255.255.255.255
 no shut
"""

print("Aplicando configuração...")

dev.configure(config)

print("Capturando snapshot final...")

post = dev.parse("show ip interface brief")

print("Calculando diferenças...")

d = Diff(pre, post)

d.findDiff()

print("\n=== DIFF ===")
print(d)
