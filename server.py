import websockets
import asyncio
import json
import logging

logging.basicConfig()

CLIENTS = set()
VALUE = 0

def client_event():
    return json.dumps({"type": "users", "count": len(CLIENTS)})

def value_event():
    return json.dumps({"type": "value", "value": VALUE})

async def counter(websocket):
    global CLIENTS, VALUE
    try:
        # On initial connection
        # 1. add new client to set
        # 2. broadcast new client joined to all clients
        # 3. send current value to the newly joined client
        CLIENTS.add(websocket)
        websockets.broadcast(CLIENTS, client_event())
        await websocket.send(value_event())

        # Listen for events from the all the clients
        # Update the value based on the event
        # Broadcast newly updated value to all the clients
        async for message in websocket:
            event = json.loads(message)
            if event["action"] == "minus":
                VALUE -= 1
                websockets.broadcast(CLIENTS, value_event())
            elif event["action"] == "plus":
                VALUE += 1
                websockets.broadcast(CLIENTS, value_event())
            else:
                logging.error("Event not supported: %s", event)
    finally:
        # In case of connection closed remove the current client
        # Broadcast the info to all the remaining connected client
        CLIENTS.remove(websocket)
        websockets.broadcast(CLIENTS, client_event())

async def main():
    async with websockets.serve(counter, "localhost", 5678):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())