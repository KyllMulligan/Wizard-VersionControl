# server/auth_service.py - Authentication and Naming Service

import uuid
from datetime import datetime

class AuthService:
    """Manages user sessions, one-time codes, and persistent name registration."""

    def __init__(self):
        # In a real system, this would connect to the durable DB (Postgres)
        # For PoC, we use an in-memory store.
        self.user_sessions = {} # {session_code: {'is_active': bool, 'expires': timestamp}}
        self.registered_names = {} # {user_id: name}

    def generate_one_time_code(self, username):
        """Generates a secure, unique, time-limited code for login."""
        # Use UUID for high entropy and uniqueness
        token = str(uuid.uuid4()).upper()
        expiry = datetime.now().timestamp() + 3600 # Expires in 1 hour
        self.user_sessions[token] = {'username': username, 'is_active': True, 'expires': expiry}
        print(f"[AUTH] Generated code for {username}: {token}")
        return token

    def validate_session(self, token):
        """Checks if the provided token is valid and not expired."""
        session = self.user_sessions.get(token)
        if session and session['is_active'] and session['expires'] > datetime.now().timestamp():
            # Successful validation: Consume the token (optional, for security)
            return session['username'], True
        return None, False

    def register_sacred_name(self, user_id, desired_name):
        """
        Attempts to reserve a name. This simulates a transactional write 
        that must be ACID compliant against the global name registry table.
        Requires checking for uniqueness and preventing conflicts.
        """
        if self.registered_names.get(user_id) == desired_name:
            return {"success": False, "message": "Name already claimed."}

        # Simulate transaction/uniqueness check
        for user_data in self.registered_names.values():
            if user_data['username'] == desired_name and user_data['user_id'] != user_id:
                return {"success": False, "message": f"Name '{desired_name}' is already taken by another player."}

        # Successful transaction
        self.registered_names[user_id] = {'username': desired_name}
        print(f"[AUTH] Player {user_id} successfully claimed the Sacred Name: {desired_name}")
        return {"success": True, "message": f"Name '{desired_name}' reserved successfully."}

# Utility for testing/debugging visibility
def get_all_registered_names():
    return self.registered_names