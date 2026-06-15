from pyats.topology import loader
from pprint import pprint

from mikrotik_parsers.system_resource import ShowSystemResource


def main():

    # Carrega o testbed
    testbed = loader.load("testbed.yaml")

    # Seleciona o MikroTik
    device = testbed.devices["MT1"]

    print(f"Conectando em {device.name}...")

    device.connect(
        learn_hostname=True,
        log_stdout=False
    )

    print("Conectado!\n")

    # Instancia o parser
    parser = ShowSystemResource(device=device)

    # Executa o parser
    data = parser.cli()

    print("Resultado parseado:")
    print("-" * 60)

    pprint(data)

    print("-" * 60)

    print(f"Versão: {data.get('version')}")
    print(f"Uptime : {data.get('uptime')}")
    print(f"CPU    : {data.get('cpu_load')}")

    device.disconnect()

    print("\nDesconectado.")


if __name__ == "__main__":
    main()
