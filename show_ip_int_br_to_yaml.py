from pyats.topology import loader
from pprint import pprint
import yaml
# Carrega o testbed
testbed = loader.load("testbed.yaml")

# Seleciona o dispositivo
device = testbed.devices["R1"]

# Conecta via SSH
device.connect(log_stdout=False)

# Executa comando
interface = device.parse("show ip interface brief")

interfacesyaml = yaml.dump(interface)

print(interfacesyaml)

with open('r1_interfaces.yaml' , 'w') as file:
  file.write(interfacesyaml)

# Desconecta
device.disconnect()
