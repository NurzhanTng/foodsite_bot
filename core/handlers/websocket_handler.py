import asyncio
import websockets
import json


async def handle_websocket(uri: str):
    async with websockets.connect(uri) as websocket:
        # await websocket.send(json.dumps({"type": "hello"}))

        async for message in websocket:
            print("Received message:", message)
