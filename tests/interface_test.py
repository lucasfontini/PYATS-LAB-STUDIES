from pyats import aetest


class InterfaceTest(aetest.Testcase):

    @aetest.test
    def verify_interfaces(self, testbed, steps):

        device = testbed.devices["R1"]

        if not device.connected:
            device.connect(log_stdout=False)

        interfaces = device.parse("show ip interface brief")

        for intf, data in interfaces["interface"].items():

            with steps.start(f"Validando {intf}",
                             continue_=True) as step:

                status = data.get("status")

                if status != "up":
                    step.failed(f"{intf} is down")
                else:
                    step.passed(f"{intf} is up")


if __name__ == "__main__":
    aetest.main()
