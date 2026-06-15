from pyats.topology import loader

from rich.console import Console

console = Console()

# Carrega o testbed
testbed = loader.load("testbed.yaml")

# Seleciona o dispositivo
device = testbed.devices["R1"]

# Conecta via SSH
device.connect()

# Executa comando
output = device.parse("show ip ospf")
console.print(output)

output = device.parse("show ip ospf interface")
console.print(output)
# Desconecta
device.disconnect()
