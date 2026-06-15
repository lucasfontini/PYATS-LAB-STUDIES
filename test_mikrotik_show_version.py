from pyats import aetest
from pyats.topology import loader

from mikrotik_parsers.system_resource import ShowSystemResource


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect(self, testbed):
        self.parent.device = testbed.devices["MT1"]
        self.parent.device.connect(
            learn_hostname=True,
            log_stdout=False
        )


class VerifySystemResource(aetest.Testcase):

    @aetest.test
    def verify_version(self):

        parser = ShowSystemResource(
            device=self.parent.device
        )

        data = parser.cli()

        

        version = data.get("version")

        if version:
            self.passed(
                f"Versão encontrada: {version}"
            )
        else:
            self.failed(
                "Versão não encontrada"
            )


class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect(self):

        self.parent.device.disconnect()


if __name__ == "__main__":

    testbed = loader.load("testbed.yaml")

    aetest.main(
        testbed=testbed
    )
