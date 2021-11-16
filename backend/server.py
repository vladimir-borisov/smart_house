import asyncio
import websockets
from sensor import XiaomiSensor
import json

class WebSocketServer:
    """
        Realization of a web socket server for simple
        manage of connections between server and clients
        with respect to xiaomi sensors
    """

    # set of all currently connected users
    active_users = set()
    counter = 0

    def __init__(self, port: int, address: str):
        """
            WebSocketServer initialization

            Input:
                port: websocket port number (666, 1234, ...)
                address: websocket host address (192.168.0.1, socket.com, ...)
            Output:
                -
        """

        self.port = port
        self.address = address


        self.sensors = [#TODO: delete hard coded names and mac_addresses
                        XiaomiSensor(name="kitchen", mac_address='A4:C1:38:F0:16:49'),
                        XiaomiSensor(name="bedroom", mac_address='A4:C1:38:CE:8F:2F')
                       ]


    async def connect_sensors(self) -> None:
        """
            Check if all sensors are connected
            and trying to connect if some are not

            Input:
                -
            Output:
                -
        """

        for sensor in self.sensors:
            if (not sensor.is_connected()):
                await sensor.connect()


    async def consumer(self, message: str) -> None:
        """
            Input:
            Output:
        """
        return None

    async def consumer_handler(self, websocket, path) -> None:
        """

        """

        async for message in websocket:
            await self.consumer(message)

    async def producer(self) -> str:
        """
            Collect temperature and humidity data from connected sensors
            and return it


            Input:
                -
            Output:
                collected data from sensor in json format

        """

        sensors_info = {'sensors': []}

        for sensor in self.sensors:

            sensor_info = {'sensor_name': sensor.name, 'sensor_mac_address': sensor.mac_address}

            if (sensor.is_connected()):
                sensor_info['temperature'] = await sensor.get_temperature()
                sensor_info['humidity'] = await sensor.get_humidity()

            sensors_info['sensors'].append(sensor_info)

        return json.dumps(sensors_info)

    async def producer_handler(self, websocket, path) -> None:
        """
            Manage sending of messages from server

            Input:
                websocket: current websocket which server will use to send a message
                path:
            Output:
                -
        """

        while True:
            message = await self.producer()
            await websocket.send(message)
            await asyncio.sleep(10) # TODO: delete hard coded delay


    async def main(self, websocket, path) -> None:
        """
            Logic for one connection

            Input:
                websocket: websocket which is used by server for communication with clients
                path:
            Output:
                -

        """

        #consumer_task = asyncio.ensure_future(self.consumer_handler(websocket, path))
        producer_task = asyncio.ensure_future(self.producer_handler(websocket, path))

        done, pending = await asyncio.wait(
            [producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()


    async def start(self):
        """
            Just starting a websocket server

            Input:
                -
            Output:
                -
        """

        await self.connect_sensors()

        async with websockets.serve(self.main, self.address, self.port):
            print('Web server is started')
            await asyncio.Future()  # run forever


if (__name__ == '__main__'):
    websocket_server = WebSocketServer(port = 8899, address='192.168.1.3')
    asyncio.run(websocket_server.start())
