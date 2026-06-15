from pyats.topology import Testbed, Device

tb = Testbed("lab")

r1 = Device(
    name="R1",
    os="iosxe",
    type="router"
)

tb.add_device(r1)
