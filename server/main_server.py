# server/main_server.py - The Game Master Orchestrator
import asyncio
import websockets
from auth_service import AuthService
from shard_zero_state import ShardZeroStateManager

SHARD_ZERO_MANAGER = ShardZeroStateManager()
AUTH_SERVICE = AuthService()

async def client_handler(websocket: websockets.WebSocketClientProtocol, path: str):
    """
    Main websocket handler for all incoming player connections and commands.
    This function acts as the central switchboard connecting Auth to State Management.
    """
    await SHARD_ZERO_MANAGER.register(websocket)
    player_id = "temp_user" # Needs real auth integration

    try:
        async for message in websocket:
            data = json.loads(message)
            msg_type = data.get("type")

            if msg_type == "CONNECT":
                # Initial connection handling
                print(f"[SERVER] Received initial connect request from {player_id}.")
                await SHARD_ZERO_MANAGER.broadcast_state({"connected_players": [player_id]})

            elif msg_type == "MOVE_INPUT":
                # 1. Process the move input through Shard Zero's logic
                result = await SHARD_ZERO_MANAGER.process_move_input(websocket, data)
                if result['status'] != 'SUCCESS':
                    await websocket.send(json.dumps({"type": "ERROR", "message": result['message']}))

            elif msg_type == "AUTH_REQUEST":
                # Handle requests to authenticate (e.g., sending the one-time code)
                print("[SERVER] Received auth request.")
                await websocket.send(json.dumps({"type": "ACK", "status": "AUTH_NEEDED"}))


async def main():
    """Starts the WebSocket server that listens for client connections."""
    # Start the central hub on a specific port
    async with websockets.serve(client_handler, "localhost", 8001):
        print("--------------------------------------------------------")
        print("✨ HEXSHARD ONLINE SERVER STARTED ✨")
        print("Listening for WebSocket connections on ws://localhost:8001")
        print("Server ready to process player movement and shard transitions.")
        # Keep the main coroutine running indefinitely
        await asyncio.Future()

if __name__ == "__main__":
    import json # Ensure json is available in the execution scope
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[SERVER] Server gracefully shut down by user.")