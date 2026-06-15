from pyats import aetest
from genie.testbed import load
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
import time

console = Console()


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect_devices(self):

        console.print("[bold cyan]Conectando dispositivos...[/bold cyan]")

        tb = load("testbed.yaml")

        self.parent.parameters["tb"] = tb
        self.parent.parameters["r1"] = tb.devices["R1"]
        self.parent.parameters["mt1"] = tb.devices["MT1"]

        self.parent.parameters["r1"].connect(log_stdout=False)
        self.parent.parameters["mt1"].connect(log_stdout=False)

        console.print("[green]✓ Dispositivos conectados[/green]")


class ConfigureOSPF(aetest.Testcase):

    @aetest.test
    def configure_devices(self, r1, mt1):

        r1_cfg = """
router ospf 1
 router-id 1.1.1.1
 network 10.10.10.0 0.0.0.3 area 0
"""

        with Progress() as progress:

            task = progress.add_task(
                "[cyan]Configurando dispositivos...",
                total=2
            )

            with console.status(
                "[bold green]Configurando Cisco R1..."
            ):
                r1.configure(r1_cfg)

            progress.advance(task)

            with console.status(
                "[bold green]Configurando MikroTik MT1..."
            ):
                mt1.execute(
                    "/routing ospf instance add name=default-v2 router-id=2.2.2.2"
                )

                mt1.execute(
                    "/routing ospf area add name=backbone area-id=0.0.0.0 instance=default-v2"
                )

                mt1.execute(
                    "/routing ospf interface-template add interfaces=ether14 area=backbone"
                )

            progress.advance(task)

        console.print(
            "[green]✓ Configuração concluída[/green]"
        )

        time.sleep(5)


class ValidateCiscoConfig(aetest.Testcase):

    @aetest.test
    def validate_ospf(self, r1):

        table = Table(
            title="Cisco Validation Report"
        )

        table.add_column(
            "Device",
            style="cyan"
        )

        table.add_column(
            "Check",
            style="yellow"
        )

        table.add_column(
            "Status",
            style="green"
        )

        try:

            ospf = r1.parse("show ip ospf")

            if ospf:

                table.add_row(
                    "R1",
                    "OSPF Process",
                    "✅ PASS"
                )

                console.print(table)

                self.passed(
                    "OSPF CONFIGURED"
                )

            else:

                table.add_row(
                    "R1",
                    "OSPF Process",
                    "❌ FAIL"
                )

                console.print(table)

                self.failed(
                    "OSPF NOT CONFIGURED"
                )

        except Exception as e:

            table.add_row(
                "R1",
                "OSPF Process",
                f"❌ ERROR: {e}"
            )

            console.print(table)

            self.failed(
                f"Validation error: {e}"
            )


class ValidateNeighbor(aetest.Testcase):

    @aetest.test
    def validate_neighbor(self, r1):

        table = Table(
            title="OSPF Neighbor Validation"
        )

        table.add_column("Device")
        table.add_column("Neighbor")
        table.add_column("State")

        try:

            neighbors = r1.parse(
                "show ip ospf neighbor"
            )

            found = False

            for interface in neighbors.get(
                "interfaces", {}
            ):

                for nbr in neighbors["interfaces"][
                    interface
                ].get("neighbors", {}):

                    state = neighbors[
                        "interfaces"
                    ][interface]["neighbors"][
                        nbr
                    ].get(
                        "state",
                        "UNKNOWN"
                    )

                    table.add_row(
                        "R1",
                        nbr,
                        state
                    )

                    found = True

            if not found:

                table.add_row(
                    "R1",
                    "-",
                    "NO NEIGHBOR"
                )

            console.print(table)

        except Exception as e:

            console.print(
                f"[red]Erro ao validar vizinhos: {e}[/red]"
            )


class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect(self, r1, mt1):

        console.print(
            "[bold cyan]Desconectando dispositivos...[/bold cyan]"
        )

        if r1.is_connected():
            r1.disconnect()

        if mt1.is_connected():
            mt1.disconnect()

        console.print(
            "[green]✓ Cleanup concluído[/green]"
        )


if __name__ == "__main__":
    aetest.main()
