from genie.testbed import load

tb = load("testbed.yaml")

dev = tb.devices["R1"]

dev.connect() 

config = """ interface Loopback200
 ip address 200.200.200.200 255.255.255.255
 no shut 
""" 
dev.configure(config)

parsed = dev.parse("show ip interface brief")

print(parsed["interface"]["Loopback200"])
