# api/main.py

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from emulator.cpu import CPU
from api.ws_manager import manager

app = FastAPI(title="6502 Emulator API")

# CORS — allows the browser frontend (a different origin) to talk to this server.
# Without this, the browser blocks requests from a different port.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

cpu = CPU()


# --- Request models ---

class LoadRequest(BaseModel):
    program: list[int]
    start_address: int = 0x0600

class RunRequest(BaseModel):
    max_steps: int = 1000  # Safety cap — stops runaway programs


# --- HTTP endpoints (unchanged from Phase 5) ---

@app.post("/reset")
def reset():
    cpu.reset()
    cpu.memory.reset()
    return {"status": "ok", "state": cpu.get_state()}


@app.post("/load")
def load(request: LoadRequest):
    for i, byte in enumerate(request.program):
        if not (0 <= byte <= 0xFF):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid byte at index {i}: {byte}"
            )
    cpu.memory.load(request.start_address, request.program)
    return {
        "status": "ok",
        "bytes_loaded": len(request.program),
        "start_address": hex(request.start_address)
    }


@app.post("/step")
async def step():
    """HTTP step — executes one instruction and broadcasts state to all WS clients."""
    try:
        state = cpu.step()
        # Push to any connected WebSocket clients too
        await manager.broadcast({"type": "state", "data": state})
        return {"status": "ok", "state": state}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/state")
def state():
    return {"status": "ok", "state": cpu.get_state()}


@app.get("/memory")
def memory(start: int = 0x0600, length: int = 32):
    if length > 256:
        raise HTTPException(status_code=400, detail="Max length is 256")
    bytes_out = [cpu.memory.read(start + i) for i in range(length)]
    return {
        "start": hex(start),
        "bytes": [hex(b) for b in bytes_out]
    }


# --- WebSocket endpoint ---

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Send current state immediately on connect
        await manager.send_to(websocket, {
            "type": "state",
            "data": cpu.get_state()
        })

        # Listen for commands from the browser
        while True:
            message = await websocket.receive_json()
            command = message.get("command")

            if command == "step":
                try:
                    state = cpu.step()
                    await manager.broadcast({
                        "type": "state",
                        "data": state
                    })
                except ValueError as e:
                    await manager.send_to(websocket, {
                        "type": "error",
                        "message": str(e)
                    })

            elif command == "reset":
                cpu.reset()
                cpu.memory.reset()
                await manager.broadcast({
                    "type": "state",
                    "data": cpu.get_state()
                })

            elif command == "load":
                program = message.get("program", [])
                start   = message.get("start_address", 0x0600)
                cpu.memory.load(start, program)
                await manager.send_to(websocket, {
                    "type": "loaded",
                    "bytes_loaded": len(program)
                })

            elif command == "run":
                # Run up to max_steps instructions, broadcasting each one
                max_steps = message.get("max_steps", 1000)
                halted = False
                steps  = 0
                while not halted and steps < max_steps:
                    state  = cpu.step()
                    halted = state["halted"]
                    steps += 1
                    await manager.broadcast({
                        "type": "state",
                        "data": state
                    })
                await manager.send_to(websocket, {
                    "type": "run_complete",
                    "steps_executed": steps,
                    "halted": halted
                })

            else:
                await manager.send_to(websocket, {
                    "type": "error",
                    "message": f"Unknown command: {command}"
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket)