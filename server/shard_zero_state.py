# server/shard_zero_state.py - Final Revision (Incorporating Shard Transition)

import asyncio
from websockets import WebSocketClientProtocol
from .hexagon_math import get_neighbors, hex_to_cube # Import needed math functions
# Assume a global state dictionary for all shards exists: SHARD_STATES = {'ShardZero': StateManager(...), 'ShardA': StateManager(...) }

class ShardZeroStateManager:
    def __init__(self):
        # Initial player state at the origin (0, 0)
        initial_coords = {'x': 0, 'y': 0}
        self.players = {
            "system_origin": {
                'id': "system_origin",
                'coords': initial_coords,
                'shard_id': 'ShardZero', # Always starts here
                'is_player': False,
                'last_seen': asyncio.get_event_loop().time()
            }
        }
        self.connections = set()

    async def register(self, websocket):
        """Handles a new connection and assigns it an ID (simulated here)."""
        await self.connections.add(websocket)

    async def process_move_input(self, websocket: WebSocketClientProtocol, input_data):
        """Processes incoming movement requests."""
        player_id = "temp_user" # Simplified for PoC - Requires Auth Service integration later!
        target_hex = {'x': input_data['target_x'], 'y': input_data['target_y']}

        # 1. Validation check (Adjacency) remains the same...
        current_hex = self.players.get(player_id, {}).get('coords', initial_coords)
        neighbors = get_neighbors(current_hex)
        is_valid_move = any((neighbor['x'] == target_hex['x'] and neighbor['y'] == target_hex['y']) for neighbor in neighbors)

        if not is_valid_move:
            return {"status": "FAILURE", "message": "Movement failed. Target hex is not adjacent or outside bounds."}
        
        # 2. Shard Transition Check (NEW LOGIC)
        is_transition = self._check_for_shard_transition(current_hex, target_hex)

        if is_transition:
            new_shard_id = self._determine_target_shard(target_hex)
            # In a real system: send player to new shard's websocket/connection handler
            print(f"[TRANSITION] Player {player_id} attempting move into {new_shard_id}.")
            self.players[player_id]['coords'] = target_hex
            self.players[player_id]['shard_id'] = new_shard_id # Update shard ID!
        else:
            # Standard movement within current shard (ShardZero)
            self.players[player_id]['coords'] = target_hex

        self.players[player_id]['last_seen'] = asyncio.get_event_loop().time()
        print(f"[SUCCESS] {player_id} moved to ({target_hex['x']}, {target_hex['y']}) in {self.players[player_id]['shard_id']}")

        # 3. Broadcast the change (Simulates state commit/broadcast)
        await self.broadcast_state({"moved_players": [self.players[player_id]]})
        return {"status": "SUCCESS", "new_coords": target_hex, "new_shard": self.players[player_id]['shard_id']}

    def _check_for_shard_transition(self, current_hex, next_hex):
        """Simulated check: If a player moves too far from origin (0,0), they transition."""
        # Simplified logic: Any move beyond the radius 3 means entering an adjacent shard instance.
        distance = abs(next_hex['x']) + abs(next_hex['y']) # Using Manhattan distance as proxy for range check
        return distance > 2

    def _determine_target_shard(self, hex_coords):
        """Maps coordinates to a deterministic shard ID (e.g., ShardA, ShardB)."""
        # Based on the x-axis coordinate being significantly positive/negative
        if hex_coords['x'] > 2:
            return "ShardAlpha"
        elif hex_coords['y'] > 2:
            return "ShardBeta"
        else:
            return "ShardZero"

    async def broadcast_state(self, data):
        """Sends the updated state to all connected clients."""
        message = json.dumps({"type": "STATE_UPDATE", "data": data})
        for connection in list(self.connections): 
            try:
                await connection.send(message)
            except Exception as e:
                print(f"Could not send to a client: {e}")

    def get_nearby_visible_players(self, current_hex):
        """Retrieves visible players from all connected shards."""
        visible = []
        for player_id, data in self.players.items():
            if player_id == "system_origin": continue 
                
            distance = abs(data['coords']['x'] - current_hex['x']) + abs(data['coords']['y'] - current_hex['y'])
            
            if distance <= 3: # Expanded visibility radius to show cross-shard presence
                visible.append({"id": player_id, "coords": data['coords'], "shard": data['shard_id'], "dist": distance})
        return visible