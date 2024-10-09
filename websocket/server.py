import asyncio
import websockets
import json


class IllegalMessageException(Exception):
    """ Generic exception to throw when clients send bad data """
    pass


# create set for current connections
connections = set()
# create limit on number of clients allowed to connect at once
MAX_NUM_CLIENTS = 100


def build_update_message(x, y, id):
    """ Create templated update message """
    message = {"id": str(id), "x":x, "y":y, "type":"update"}
    return json.dumps(message)

def build_remove_message(id):
    """ Create templated remove message """
    message = {"id":str(id), "type":"remove"}
    return json.dumps(message)

async def register(websocket):
    """ Handles initial registration and websocket closure """
    print(f"New connection received, id={websocket.id} ({websocket.remote_address[0]}:{websocket.remote_address[1]})")
    # reject connection if connection limit reached
    if len(connections) >= MAX_NUM_CLIENTS:
        print(f"Maximum concurrent connection limit reached, rejecting new connection")
        await websocket.close(4001)
        return
    # add connection to connections set
    connections.add(websocket)
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
            websockets.broadcast(connections, build_remove_message(websocket.id))
            print(f"Connection removed, id={websocket.id} ({websocket.remote_address[0]}:{websocket.remote_address[1]})")
            break


def handle_message(message, websocket):
    """ Handle and error check messages from clients """
    tmp = json.loads(message)
    x = None
    y = None
    try:
        x, y = float(tmp["x"]), float(tmp["y"])
    except:
        print(f"Illegal message received, id={websocket.id} ({websocket.remote_address[0]}:{websocket.remote_address[1]})")
        raise IllegalMessageException
    # send update to all other clients
    websockets.broadcast(connections - {websocket}, build_update_message(x, y, websocket.id))

def log_application_state():
    """ Prints current application state to stdout """
    if len(connections) == 0:
        print("0 websocket connections")
        return
    output = f"{len(connections)} websocket connections:"
    for websocket in connections:
        output += f"\n\tid={websocket.id} ({websocket.remote_address[0]}:{websocket.remote_address[1]})"
    print(output)


async def main():
    async with websockets.serve(register, host="0.0.0.0", port=80):
        while True:
            log_application_state()
            await asyncio.sleep(15)


if __name__ == "__main__":
    asyncio.run(main())
