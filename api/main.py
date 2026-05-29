from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from emulator.cpu import CPU

app = FastAPI(title="6502 Emulator API")

# single CPU instance
cpu = CPU()


class LoadRequest(BaseModel):
    program: list[int]
    start_address: int = 0x0600


# Endpoints

@app.post("/reset")
def reset():
    """Wipe the CPU back to its initial state."""
    cpu.reset()
    cpu.memory.reset()
    return {"status": "ok", "state": cpu.get_state()}

@app.post("/load")
def load(request: LoadRequest):
    """Load a program into memory."""
    # Validate every byte is actually a byte (0-255)
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
def step():
    """Execute one instruction and return the new CPU state."""
    try:
        state = cpu.step()
        return {"status": "ok", "state": state}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/state")
def state():
    """Return current CPU state without executing anything."""
    return {"status": "ok", "state": cpu.get_state()}


@app.get("/memory")
def memory(start: int = 0x0600, length: int = 32):
    """
    Return a slice of memory as a list of bytes.
    Default shows 32 bytes starting at $0600 — where programs load.
    """
    if length > 256:
        raise HTTPException(status_code=400, detail="Max length is 256")
    bytes_out = [cpu.memory.read(start + i) for i in range(length)]
    return {
        "start": hex(start),
        "bytes": [hex(b) for b in bytes_out]
    }