from pyats import aetest
from pyats.topology import loader


class InitialSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect(self):

        self.parent.parameters["testbed"] = loader.load(
            "testbed.yaml"
        )

        tb = self.parent.parameters["testbed"]

        device = tb.devices["R1"]

        device.connect(log_stdout=False)

        self.parent.parameters["device"] = device




class TestInterface(aetest.Testcase):
    @aetest.test
    def verify_interfaces(self, steps):

        device = self.parent.parameters["device"]

        interfaces = device.parse("show ip interface brief")

        for interface, data in interfaces["interface"].items():

            with steps.start(
                f"Checking {interface}",
                continue_=True
            ) as step:

                if data["status"] != "up":

                    step.failed(
                        f"{interface} is down"
                    )





class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect(self):

        device = self.parent.parameters["device"]

        device.disconnect()

if __name__ == "__main__":
    aetest.main()

