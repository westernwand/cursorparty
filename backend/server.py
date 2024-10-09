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
        mouse_positions[websocket.id] = (float(tmp["x"]), float(tmp["y"]))
    except:
        print(f"Illegal message received from {websocket.id}, closing connection\n\t{message}")
        raise IllegalMessageException

# log current application state
def log_application_state():
    output = f"{len(connections)} connections: "
    for websocket in connections:
        output += f"\n\t{websocket.id} - {websocket.remote_address[0]}:{websocket.remote_address[1]} - ({mouse_positions[websocket.id][0]},{mouse_positions[websocket.id][0]})"
    print(output)

# sends a mouse connection update to each active, connected client
def broadcast_update():
    for websocket in connections:
        # skip sending to inactive websockets
        if mouse_positions[websocket.id] == (-1, -1):
            continue
        # rebuild mouse_positions dict without current mouse position
        new_dict = {}
        for key in mouse_positions:
            # skip if mouse_positions has not been updated yet (indicating inactive connection)
            if mouse_positions[key] == (-1, -1):
                continue
            # skip if sending current websocket's position to current websocket
            if key == websocket.id:
                continue
            # add valid positions to new_dict (adding str because json.dumps is having issues with UUIDs as keys)
            new_dict[str(key)] = mouse_positions[key]
        # async send message to client (only if new_dict is not empty)
        if new_dict:
            asyncio.create_task(websocket.send(json.dumps(new_dict, default=str)))

async def main():
    async with websockets.serve(register, "0.0.0.0", 8081):
        while True:
            log_application_state()
            broadcast_update()
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())