# Core state machine for Shard Zero
import asyncio
from websockets import WebSocketClientProtocol

class ShardZeroStateManager:
    def __init__(self):
        # Stores player positions {player_id: {'x': 0, 'y': 0, 'z': 0, 'shard_id': 'ShardZero'}}
        self.players = {}
        # WebSocket connections for real-time updates
        self.connections = set()

    async def register(self, websocket):
        self.connections.add(websocket)

    def process_move_input(self, player_id, target_hex):
        """Processes incoming movement requests and validates them against shard rules."""
        # Logic to check if target is valid within Shard Zero boundaries
        if self.players.get(player_id):
            print(f"Processing move for {player_id} to {target_hex}")
            self.players[player_id]['current_hex'] = target_hex
            return {"status": "OK", "new_state": self.players[player_id]}
        return {"status": "ERROR", "message": "Player not found."}

    async def broadcast_state(self, state):
        """Sends the updated state to all connected clients."""
        for connection in list(self.connections):
            await connection.send(json.dumps({"type": "STATE_UPDATE", "data": state}))
