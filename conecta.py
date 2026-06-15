from pyats.topology import loader
from pprint import pprint
# Carrega o testbed
testbed = loader.load("testbed.yaml")

# Seleciona o dispositivo
device = testbed.devices["R1"]

# Conecta via SSH
device.connect()

# Executa comando
output = device.learn("interface")

pprint(output.info)

# Desconecta
device.disconnect()
