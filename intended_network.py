from pyats.topology import loader
from pprint import pprint
# Carrega o testbed
testbed = loader.load("testbed.yaml")

# Seleciona o dispositivo
device = testbed.devices["R1"]

# Conecta via SSH
device.connect()


output = device.parse("show version")
#print(output)
hostname = output["version"]["hostname"]

if hostname == device.custom["hostname"]:
  print("Test hostname .... PASS")
else:
  print("Test hostname .... FAIL ")
# Executa comando
interfaces = device.parse("show ip interface brief")
for loopback in device.custom["loopbacks"]:

    if loopback not in interfaces["interface"]:
        print(f"Test {loopback} .... FAIL")
    else:
        print(f"Test {loopback} .... PASS")
# Desconecta
device.disconnect()
