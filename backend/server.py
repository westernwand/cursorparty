import asyncio
import websockets

async def reply_hello(websocket):
    await websocket.send("hello world from server!")

async def main():
    async with websockets.serve(reply_hello, "0.0.0.0", 8081):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())