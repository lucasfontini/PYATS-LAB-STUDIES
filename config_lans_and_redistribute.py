from pyats import aetest
from genie.testbed import load
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


class ConfigureP2P(aetest.Testcase):

    @aetest.test
    def configure_devices(self, r1, mt1):

        r1_cfg = """
        interface GigabitEthernet3
         ip address 10.20.20.1 255.255.255.252
         description LAN_CISCO
         no shutdown
        router ospf 1
        network 10.20.20.0 0.0.0.3 area 0

        """

        mt_cfg = """
        ip address add address=10.30.30.1/30 interface=ether15
        /routing ospf interface-template add area=backbone interfaces=ether15 networks=10.30.30.0/30
        """

        r1.configure(r1_cfg)
        mt1.execute(mt_cfg)

        time.sleep(5)


class ValidateCiscoConfig(aetest.Testcase):

    @aetest.test
    def validate_interface(self, r1, steps):

        interfaces = r1.parse("show ip interface brief")

        with steps.start("Validate GigabitEthernet6 IP") as step:

            ip = interfaces["interface"]["GigabitEthernet3"]["ip_address"]

            if ip == "10.20.20.1":
                step.passed(
                    f"Interface configured with {ip}"
                )
            else:
                step.failed(
                    f"Expected 10.20.20.1 got {ip}"
                )


class ValidateConnectivity(aetest.Testcase):

    @aetest.test
    def ping_mikrotik(self, r1):
      time.sleep(10)
      ping = r1.parse("ping 10.30.30.1")

      success = int(ping["ping"]["statistics"]["success_rate_percent"])

      if success == 100:
        self.passed("Ping OK")
      elif success > 80:
        self.passx("Ping but with packet loss")
      else:
        self.failed(f"Success rate {success}%")


class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect(self, r1, mt1):

        r1.disconnect()
        mt1.disconnect()




if __name__ == "__main__":
  aetest.main()
