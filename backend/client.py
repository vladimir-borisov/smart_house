""" This file is using mainly for server debugging"""

import asyncio
import websockets

async def hello():

    uri = "ws://192.168.1.3:8899"

    async with websockets.connect(uri) as websocket:
        while(True):
            print('Test')
            server_message = await websocket.recv()
            print(f"{server_message}")

asyncio.get_event_loop().run_until_complete(hello())