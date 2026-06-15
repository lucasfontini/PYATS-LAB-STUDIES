from pyats import aetest


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect(self, testbed):
        testbed.connect(log_stdout=False)


class VersionTest(aetest.Testcase):

    @aetest.test
    def check_version(self, testbed):

        device = testbed.devices["R1"]

        output = device.parse("show version")

        version = output["version"]["version"]

        print(f"Versão encontrada: {version}")

        if "17." in version:
            self.passed()
        else:
            self.failed()


class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect(self, testbed):
        testbed.disconnect()
