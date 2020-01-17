import logging
import os

from core import configservices
from core.configservice.manager import ConfigServiceManager
from core.emulator.coreemu import CoreEmu
from core.emulator.emudata import IpPrefixes, NodeOptions
from core.emulator.enumerations import EventTypes, NodeTypes

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # setup basic network
    prefixes = IpPrefixes(ip4_prefix="10.83.0.0/16")
    options = NodeOptions(model="nothing")
    # options.services = []
    coreemu = CoreEmu()
    session = coreemu.create_session()
    session.set_state(EventTypes.CONFIGURATION_STATE)
    switch = session.add_node(_type=NodeTypes.SWITCH)

    # node one
    node_one = session.add_node(options=options)
    interface = prefixes.create_interface(node_one)
    session.add_link(node_one.id, switch.id, interface_one=interface)

    # node two
    node_two = session.add_node(options=options)
    interface = prefixes.create_interface(node_two)
    session.add_link(node_two.id, switch.id, interface_one=interface)

    session.instantiate()

    # manager load config services
    manager = ConfigServiceManager()
    path = os.path.dirname(os.path.abspath(configservices.__file__))
    manager.load(path)

    clazz = manager.services["DefaultRoute"]
    dr_service = clazz(node_one)
    dr_service.set_config({"value1": "custom"})
    dr_service.start()

    clazz = manager.services["IPForward"]
    dr_service = clazz(node_one)
    dr_service.start()

    input("press enter to exit")
    session.shutdown()
