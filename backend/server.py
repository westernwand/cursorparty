import asyncio
import websockets
import json


class IllegalMessageException(Exception):
    """ Generic exception to throw when clients send bad data """
    pass


# create set for current connections
connections = set()
# create dict for mouse positions
mouse_positions = {}


async def register(websocket):
    """ Handles initial registration and websocket closure """
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


def handle_message(message, websocket):
    """ Handle and error check messages from clients """
    try:
        tmp = json.loads(message)
        mouse_positions[websocket.id] = (float(tmp["x"]), float(tmp["y"]))
    except:
        print(f"Illegal message received from {
              websocket.id}, closing connection\n\t{message}")
        raise IllegalMessageException


def log_application_state():
    """ Prints current application state to stdout """
    output = f"{len(connections)} connections: "
    for websocket in connections:
        output += f"\n\t{websocket.id} - {websocket.remote_address[0]}:{
            websocket.remote_address[1]} - ({mouse_positions[websocket.id][0]},{mouse_positions[websocket.id][0]})"
    print(output)


def broadcast_update():
    """ Sends the current cursor state to each active, connected client """
    for websocket in connections:
        # skip sending to inactive websockets
        if mouse_positions[websocket.id] == (-1, -1):
            continue
        # create message to send to clients
        message = []
        for key in mouse_positions:
            # skip if mouse_positions has not been updated yet (indicating inactive connection)
            if mouse_positions[key] == (-1, -1):
                continue
            # skip if sending current websocket's position to current websocket
            if key == websocket.id:
                continue
            # add mouse position to message
            message.append({
                "id": str(key), 
                "x": mouse_positions[key][0], 
                "y": mouse_positions[key][1]
            })
        # async send message to client (only if message is not empty)
        if len(message) > 0:
            asyncio.create_task(websocket.send(
                json.dumps(message, default=str)))


async def main():
    async with websockets.serve(register, "0.0.0.0", 8081):
        while True:
            log_application_state()
            broadcast_update()
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
