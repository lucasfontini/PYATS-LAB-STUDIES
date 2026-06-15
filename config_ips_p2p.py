from genie.testbed import load
import time

tb = load("testbed.yaml")

dev = tb.devices["R1"]
mikrotik = tb.devices["MT1"]

dev.connect(log_stdout=False) 
mikrotik.connect()

config = """
interface GigabitEthernet6
ip address 10.10.10.2 255.255.255.252
description "P2P-MIKROTIK"
no shut 
""" 

config_mk="""
ip address add address=10.10.10.1/30 network=255.255.255.252 interface=ether10
"""

dev.configure(config)
mikrotik.execute(config_mk)

time.sleep(5)

interfaces = dev.parse("show ip interface brief")
for interface , data in interfaces["interface"].items():
  if interface == "GigabitEthernet6":
    if "10.10.10.2" in data["ip_address"]:
      print("Ip configured successfully")
    else:
      print("Error to configured ip address please, check manually")

ping = dev.parse("ping 10.10.10.1")
print(ping)




