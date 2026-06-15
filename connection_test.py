from pyats import aetest
from pyats.topology import loader

class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect(self):

        self.parent.parameters["testbed"] = loader.load(
            "testbed.yaml"
        )

        tb = self.parent.parameters["testbed"]

        device = tb.devices["R1"]

        device.connect(log_stdout=False)

        self.parent.parameters["device"] = device


class TestHostname(aetest.Testcase):

    @aetest.test
    def verify_hostname(self):

        device = self.parent.parameters["device"]

        version = device.parse("show version")

        hostname = version["version"]["hostname"]

        if hostname == "Router":
            self.passed()
        else:
            self.failed()





class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect(self):

        device = self.parent.parameters["device"]

        device.disconnect()




if __name__ == "__main__":
    aetest.main()
