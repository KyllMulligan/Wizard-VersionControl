# server/hexagon_math.py - Enhanced with Cube Coordinates

import math

def hex_to_cube(coords):
    """Converts (x, y) axial coordinates to cube coordinates (q, r, s)."""
    return {'q': coords['x'], 'r': coords['y'], 's': -(coords['x'] + coords['y'])}

def cube_to_hex(cube_coords):
    """Converts cube coordinates back to axial (x, y) format."""
    # We use q=x, r=y for simplicity in the client/server context
    return {'x': cube_coords['q'], 'y': cube_coords['r']}

def get_neighbors(current_hex):
    """Returns a list of 6 adjacent hex coordinates from a given hex."""
    # Directions are defined by the six principal axes in cube space (directions vector)
    directions = [
        {'q': 1, 'r': 0, 's': -1}, # E
        {'q': 1, 'r': -1, 's': 0}, # SE
        {'q': 0, 'r': -1, 's': 1}, # SW
        {'q': -1, 'r': 0, 's': 1}, # W
        {'q': -1, 'r': 1, 's': 0}, # NW
        {'q': 0, 'r': 1, 's': -1}  # N
    ]
    neighbors = []
    for direction in directions:
        neighbor_cube = {
            'q': current_hex['q'] + direction['q'],
            'r': current_hex['r'] + direction['r'],
            's': current_hex['s'] + direction['s']
        }
        # Convert back to axial for the return type consistency
        neighbors.append({'x': neighbor_cube['q'], 'y': neighbor_cube['r']})
    return neighbors

def hex_to_coords(hex_map):
    """Converts a simple dict {'x': N, 'y': N} into a usable coordinate object."""
    return {
        'x': hex_map.get('x', 0),
        'y': hex_map.get('y', 0)
    }