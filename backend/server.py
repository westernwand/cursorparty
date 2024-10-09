import asyncio
import websockets

# create set for current connections
connections = set()

# initial registration and closure handling
async def register(websocket):
    # add connection to connections set
    connections.add(websocket)
    # send message to each new connection
    await reply_hello(websocket)
    # start main loop
    while True:
        async for message in websocket:
            print(message)
        # handle closure for each connection
        try:
            await websocket.wait_closed()
        finally:
            connections.remove(websocket)
            print(f"connection removed, id={websocket.id}")
            pretty_print_connections()
            break

# send initial response
async def reply_hello(websocket):
    print(f"new connection received, id={websocket.id}")
    pretty_print_connections()
    await websocket.send("welcome to cursorparty! :^)")

# helper for logging connections state
def pretty_print_connections():
    output = f"{len(connections)} connections: "
    for conn in connections:
        output += f"{{{conn.id}-{conn.remote_address[0]}:{conn.remote_address[1]}}} "
    print(output)


async def main():
    async with websockets.serve(register, "0.0.0.0", 8081):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())