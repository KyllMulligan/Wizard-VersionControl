// client/main.js

class PlayerCube {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        // Render logic using Canvas/WebGL here (e.g., Three.js cube rendering)
    }

    update_position(new_x, new_y) {
        // Smoothly animate the visual movement to (new_x, new_y)
        console.log(`[Render] Moving cube to ${new_x}, ${new_y}`);
    }
}

async function initializeConnection() {
    const ws = new WebSocket("ws://localhost:8001/shardzero");
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === "STATE_UPDATE") {
            // Receive and process state updates from the server
            console.log("Received State Update:", data.data);
        } else if (data.type === "ENTITY_DISCOVERY") {
             // Logic to render other visible players/entities in nearby shards
             console.log("Nearby Entities Found!");
        }
    };

    ws.onclose = () => console.error("Disconnected from Shard Zero.");
    await ws.send(JSON.stringify({type: "CONNECT", player_id: "temp_user"})); // Initial connection message
}

// Setup click listener for movement input
document.addEventListener('mousedown', (event) => {
    const targetX = event.offsetX; 
    const targetY = event.offsetY;
    console.log(`[Input] Player clicked at: (${targetX}, ${targetY}). Sending move request.`);

    // Simulate sending the movement input to the server
    // (Actual network send logic here)
});

initializeConnection();