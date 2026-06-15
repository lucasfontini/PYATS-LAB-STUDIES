from pyats import aetest
from genie.testbed import load
from genie.utils.diff import Diff
import time


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect_devices(self):

        tb = load("testbed.yaml")

        self.parent.parameters["tb"] = tb
        self.parent.parameters["r1"] = tb.devices["R1"]
        self.parent.parameters["mt1"] = tb.devices["MT1"]

        self.parent.parameters["r1"].connect()
        self.parent.parameters["mt1"].connect()


class ConfigureOSPF(aetest.Testcase):

    @aetest.test
    def configure_devices(self, r1, mt1):

        # Snapshot antes
        try:
            before = r1.learn("ospf")
            self.parent.parameters["ospf_before"] = before
        except Exception:
            self.parent.parameters["ospf_before"] = None

        r1_cfg = """
        router ospf 1
        router-id 1.1.1.1
        network 10.10.10.0 0.0.0.3 area 0
        """

        mt_cfg = """
        /ip address
        /routing ospf instance add name=default-v2 router-id=2.2.2.2
        /routing ospf area add name=backbone area-id=0.0.0.0 instance=default-v2
        /routing ospf interface-template add interfaces=ether14 area=backbone
        """

        r1.configure(r1_cfg)
        mt1.execute(mt_cfg)

        time.sleep(10)

        # Snapshot depois
        after = r1.learn("ospf")
        self.parent.parameters["ospf_after"] = after


class ValidateCiscoConfig(aetest.Testcase):

    @aetest.test
    def validate_ospf(self, r1):

        before = self.parent.parameters["ospf_before"]
        after = self.parent.parameters["ospf_after"]

        if before is None:
            self.passed("OSPF não existia antes e agora está configurado")
            return

        diff = Diff(before.to_dict(), after.to_dict())
        diff.findDiff()

        print(diff)

        if diff.diffs:
            self.passed("Mudanças OSPF detectadas")
        else:
            self.failed("Nenhuma mudança OSPF detectada")


class VerifyNeighbor(aetest.Testcase):

    @aetest.test
    def verify_neighbor(self, r1):

        neighbors = r1.parse("show ip ospf neighbor")

        if neighbors.get("interfaces"):
            self.passed("Vizinho OSPF encontrado")
        else:
            self.failed("Nenhum vizinho OSPF encontrado")


class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect(self, r1, mt1):

        r1.disconnect()
        mt1.disconnect()


if __name__ == "__main__":
    aetest.main()
