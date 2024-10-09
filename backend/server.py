import asyncio
import websockets
import json

# generic exception to throw when clients send bad data
class IllegalMessageException(Exception):
    pass

# create set for current connections
connections = set()
# create dict for mouse positions
mouse_positions = {}

# initial registration and closure handling
async def register(websocket):
    print(f"new connection received, id={websocket.id}")
    # add connection to connections set
    connections.add(websocket)
    mouse_positions[websocket.id] = (-1, -1)
    # start main loop
    while True:
        # handle and error check each message
        async for message in websocket:
            try:
                handle_message(message, websocket)
            except IllegalMessageException:
                await websocket.close()
        # handle closure for each connection
        try:
            await websocket.wait_closed()
        finally:
            # remove application state for closed websocket
            connections.remove(websocket)
            del mouse_positions[websocket.id]
            print(f"connection removed, id={websocket.id}")
            break

# handle and error check messages from clients
def handle_message(message, websocket):
    try:
        tmp = json.loads(message)
        mouse_positions[websocket.id] = (int(tmp["x"]), int(tmp["y"]))
    except:
        print(f"Illegal message received from {websocket.id}, closing connection")
        raise IllegalMessageException

# log current application state
def log_application_state():
    output = f"{len(connections)} connections: "
    for conn in connections:
        output += f"\n\t{conn.id} - {conn.remote_address[0]}:{conn.remote_address[1]} - ({mouse_positions[conn.id][0]},{mouse_positions[conn.id][0]})"
    print(output)

async def main():
    async with websockets.serve(register, "0.0.0.0", 8081):
        while True:
            # log application state every 5 seconds
            log_application_state()
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())