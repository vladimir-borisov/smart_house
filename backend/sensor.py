from bleak import BleakClient, BleakError
import struct
import asyncio

class XiaomiSensor:
    """
        Class for work with Xiaomi LYWSD03MMC
        Bluetooth Temperature Humidity sensor
    """


    # Bluetooth characteristics addresses (UUID)
    BATTERY_LEVEL = "00002a19-0000-1000-8000-00805f9b34fb"
    TEMPERATURE_HUMIDITY = "ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6"


    def __init__(self, name: str, mac_address: str):
        """
            Initialize one Xiaomi sensor

            Input:
                name: a name of the device
                mac_address: MAC address of sensor (can be received via Xiaomi Home application for mobile)
                             sample of a correct MAC address: A4:C1:38:F0:16:49
            Output:
                XiaomiSensor object
        """

        self.name = name
        self.mac_address = mac_address
        self.client = BleakClient(self.mac_address, use_cached=False, timeout=50)


    def is_connected(self):
        return self.client.is_connected

    async def connect(self):
        try:
            # asynchronous connection to a device
            print(f'Connecting to "{self.name}" sensor ...')
            await self.client.connect()
            print(f'Sensor {self.name} is connected')
        except Exception as err:
            print(err)

    async def disconnect(self):
        try:
            # asynchronous disconnection from a device
            await self.client.disconnect()
            print(f'Device {self.name} is disconnected')
        except Exception as err:
            print(err)


    async def get_data_by_uuid(self, uuid: str):
        try:
            return await self.client.read_gatt_char(uuid)
        except BleakError as error:
            print(error)
            return None

    async def get_humidity(self):
        """
            Get current humidity of a sensor

            Input:
                -
            Output:
                current relative humidity measured by sensor in range 0-100%
        """
        temp_humidity_data = await self.get_data_by_uuid(self.TEMPERATURE_HUMIDITY)

        humidity = temp_humidity_data[2]

        return humidity


    async def get_temperature(self):

        """
            Get current temperature of a sensor

            Input:
                -
            Output:
                current temperature measured by sensor in Celsius degree
        """

        temp_humidity_data = await self.get_data_by_uuid(self.TEMPERATURE_HUMIDITY)

        if (temp_humidity_data is None):
            return -1

        temperature = struct.unpack("<h", temp_humidity_data[0:2])[0] / 100.0

        return temperature




async def main():
    #sensor = XiaomiSensor(name = "kitchen", mac_address='A4:C1:38:F0:16:49')
    sensor = XiaomiSensor(name = "kitchen", mac_address='A4:C1:38:CE:8F:2F')

    #print(sensor.client.)
    await sensor.connect()

    print(await sensor.get_temperature(), await sensor.get_humidity())

    await sensor.disconnect()

#asyncio.run(main())

