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
    print(f"new connection received, id={str(websocket.id)}")
    # add connection to connections set
    connections.add(websocket)
    mouse_positions[str(websocket.id)] = (-1, -1)
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
            del mouse_positions[str(websocket.id)]
            print(f"connection removed, id={str(websocket.id)}")
            break

# handle and error check messages from clients
def handle_message(message, websocket):
    try:
        tmp = json.loads(message)
        mouse_positions[str(websocket.id)] = (float(tmp["x"]), float(tmp["y"]))
    except:
        print(f"Illegal message received from {str(websocket.id)}, closing connection\n\t{message}")
        raise IllegalMessageException

# log current application state
def log_application_state():
    output = f"{len(connections)} connections: "
    for conn in connections:
        output += f"\n\t{str(conn.id)} - {conn.remote_address[0]}:{conn.remote_address[1]} - ({mouse_positions[str(conn.id)][0]},{mouse_positions[str(conn.id)][0]})"
    print(output)

# broadcast mouse connection update
def broadcast_update():
    # TODO remove each connection's own position
    websockets.broadcast(connections, json.dumps(mouse_positions))

async def main():
    async with websockets.serve(register, "0.0.0.0", 8081):
        while True:
            # log application state every 1 seconds
            log_application_state()
            # broadcast mouse position updates
            broadcast_update()
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())