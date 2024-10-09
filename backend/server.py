import asyncio
import websockets
import json

class IllegalMessageException(Exception):
    pass

# create set for current connections
connections = set()
# create dict for mouse positions
mouse_positions = {}

# initial registration and closure handling
async def register(websocket):
    # add connection to connections set
    connections.add(websocket)
    mouse_positions[websocket.id] = (0, 0)
    # send message to each new connection
    await reply_hello(websocket)
    # start main loop
    while True:
        # handle and error check each message
        async for message in websocket:
            print(mouse_positions)
            try:
                handle_message(message, websocket)
            except IllegalMessageException:
                await websocket.close()
        # handle closure for each connection
        try:
            await websocket.wait_closed()
        finally:
            cleanup_connection(websocket)
            break

def cleanup_connection(websocket):
    connections.remove(websocket)
    del mouse_positions[websocket.id]
    print(f"connection removed, id={websocket.id}")
    pretty_print_connections()

def handle_message(message, websocket):
    try:
        tmp = json.loads(message)
        mouse_positions[websocket.id] = (int(tmp["x"]), int(tmp["y"]))
    except:
        print(f"Illegal message received from {websocket.id}, closing connection")
        raise IllegalMessageException

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

# runs every 10 seconds, logs all connections and mouse positions
async def log_connections():
    while True:
        pretty_print_connections()
        print(mouse_positions)
        await asyncio.sleep(10)

async def main():
    async with websockets.serve(register, "0.0.0.0", 8081):
        await log_connections()

if __name__ == "__main__":
    asyncio.run(main())