import unittest
from custom_components.eltako.sensor import *
from unittest import mock
from tests.mocks import *
from homeassistant.helpers.entity import Entity
from homeassistant.const import Platform
from custom_components.eltako.binary_sensor import EltakoBinarySensor
from eltakobus import *

# mock update of Home Assistant
Entity.schedule_update_ha_state = mock.Mock(return_value=None)
# EltakoBinarySensor.hass.bus.fire is mocked by class HassMock


class TestSensor_A5_14_09(unittest.TestCase):
    
    msg1 = Regular4BSMessage(address=b'\xFF\xFF\x00\x80', data=b'\xAA\x00\x00\xD0', status=0x00)

    def create_windowhandle_sensor(self) -> EltakoWindowHandleWithSupplyVoltage:
        gateway = GatewayMock()
        dev_id = AddressExpression.parse("FF-FF-00-80")
        dev_name = "dev name"
        dev_eep = EEP.find("A5-14-09")
        ewh = EltakoWindowHandleWithSupplyVoltage(Platform.SENSOR, gateway, dev_id, dev_name, dev_eep, SENSOR_DESC_WINDOWHANDLE)

        return ewh
    
    def create_battery_voltage_sensor(self) -> EltakoBatteryVoltageSensor:
        gateway = GatewayMock()
        dev_id = AddressExpression.parse("FF-FF-00-80")
        dev_name = "dev name"
        dev_eep = EEP.find("A5-14-09")
        ebs = EltakoBatteryVoltageSensor(Platform.SENSOR, gateway, dev_id, dev_name, dev_eep)

        return ebs
    

    def test_windowhandle_sensor(self):
        ewh_handle = self.create_windowhandle_sensor()
        
        ewh_handle.entity_description = SENSOR_DESC_WINDOWHANDLE
        ewh_handle._attr_native_value = -1
        
        ewh_handle.value_changed(self.msg1)
        self.assertEqual(ewh_handle.native_value, 'tilt')

        
    def test_battery_voltage_sensor(self):
        ebs_vlt = self.create_battery_voltage_sensor()

        ebs_vlt.value_changed(self.msg1)
        self.assertEqual(ebs_vlt.native_value, 3.3999999999999995)

