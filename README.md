# 6502 CPU Emulator + Visual Debugger

A fully functional emulator of the MOS Technology 6502 processor — the chip that powered the NES, Apple II, and Commodore 64 — with a real-time visual debugger built on top. Load raw hex programs, step through them instruction by instruction, and watch registers change, flags flip, and memory update live in the browser.

> Built as a portfolio project to understand CPU architecture, emulation, and real-time full-stack communication.

---

## What It Does

The emulator implements the full MOS 6502 instruction set — all 56 official instructions across 13 addressing modes. The visual debugger connects to it over WebSocket and gives you a live window into the CPU's state at every step:

- Step through programs one instruction at a time or run to completion
- Watch registers (PC, SP, A, X, Y, P) update in real time with change highlighting
- See all 7 status flags (N, V, B, D, I, Z, C) flip as instructions execute
- Hex memory viewer centered on the current Program Counter
- Execution log tracking every instruction that has run
- Mini disassembler showing the next upcoming instructions
- Stack peek showing the top of the hardware stack
- Binary bit display on every register
- Load programs as raw hex bytes directly from the browser

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Emulator Core | Python | CPU registers, memory model, fetch-decode-execute loop |
| Backend | FastAPI | REST endpoints + WebSocket server |
| Real-time Bridge | WebSockets | Push CPU state to browser on every step |
| Frontend | HTML / CSS / JS | Visual debugger UI |

---

## Project Structure

```
6502-emulator/
├── emulator/
│   ├── cpu.py          # 6502 CPU — registers, flags, instruction execution
│   ├── memory.py       # 64KB flat address space
│   └── opcodes.py      # Full opcode lookup table (mnemonic, mode, cycles)
├── api/
│   ├── main.py         # FastAPI app — HTTP endpoints + WebSocket
│   └── ws_manager.py   # WebSocket connection manager (broadcast to all clients)
├── frontend/
│   ├── index.html      # Debugger layout
│   ├── style.css       # Retrofuturism / retro-Japanese visual theme
│   └── debugger.js     # WebSocket client, state rendering, canvas animation
├── examples/
│   ├── count_to_10.txt # Simple counting loop
│   └── fibonacci.txt   # Fibonacci sequence
├── tests/
│   └── test_cpu.py
├── requirements.txt
└── README.md
```

---

## Getting Started

**Prerequisites:** Python 3.10+

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/6502-emulator.git
cd 6502-emulator

# 2. Create and activate virtual environment
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash
# source .venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the backend server
uvicorn api.main:app --reload

# 5. Open the debugger
# Open frontend/index.html directly in your browser
```

The status dot in the top-right corner turns green when the WebSocket connects successfully.

---

## How to Use

### Loading a program

Programs are entered as space-separated hex bytes in the **LOAD** panel on the right. Example — a simple counting loop:

```
A9 00 AA E8 E0 03 D0 FB 00
```

This program loads 0 into the accumulator, copies it to X, increments X until it reaches 3, then halts. Hit **LOAD INTO MEMORY** and the bytes are written to address `$0600` in the emulator's memory.

### Controls

| Control | Keyboard | What it does |
|---|---|---|
| STEP | `Space` | Execute one instruction |
| RUN | `G` | Run until BRK or 10,000 steps |
| RESET | `R` | Wipe CPU state and memory back to initial |

### Reading the debugger

**Registers panel (left)** — Shows all 6502 registers in hex. The PC row is always highlighted in red since it's the most important register. The row flashes when a value changes. The binary bits below each register show you the individual bit state.

**Flags panel (left)** — The 7 status flags light up red when set. These flip based on the result of arithmetic and logic instructions — Z goes high when a result is zero, N when bit 7 is set, C when arithmetic produces a carry, and so on.

**Current instruction (center)** — The large mnemonic shows the instruction at the current PC. The metadata row shows the raw opcode byte, addressing mode, and cycle count.

**Memory viewer (center)** — 128 bytes of memory shown as a hex dump. The byte at the current PC is highlighted red. Scrolls to follow execution automatically.

**Execution log (right)** — Every executed instruction with its address and total cycle count at that point.

---

## Architecture

```
Browser (frontend/)
    │
    │  WebSocket  ws://localhost:8000/ws
    │  HTTP       http://localhost:8000/...
    │
FastAPI Server (api/)
    │
    │  Direct Python calls
    │
Emulator Core (emulator/)
    ├── CPU — fetch / decode / execute loop
    └── Memory — 64KB flat address space
```

The emulator core is completely independent of the web layer. `cpu.step()` executes one instruction and returns the full CPU state as a Python dict. The FastAPI layer wraps this and broadcasts the state to all connected WebSocket clients after every step.

The WebSocket connection stays open for the browser session. Commands (`step`, `run`, `reset`, `load`) are sent as JSON from the browser. State updates are pushed back as JSON after every execution. Multiple browser tabs stay in sync because every broadcast goes to all active connections.

---

## The 6502

The MOS Technology 6502 (1975) is one of the most historically significant processors ever made. At $25 it was a fraction of the cost of competing chips and enabled the home computer revolution. It powered:

- **Nintendo Entertainment System (NES)** — the Ricoh 2A03 was a modified 6502
- **Apple II** — the machine that put Apple on the map
- **Commodore 64** — best-selling personal computer of all time
- **Atari 2600** — defined the home gaming market

The 6502 has 7 registers, a 64KB address space, and 56 official instructions across 13 addressing modes. Its simplicity and thorough documentation make it the standard starting point for learning CPU emulation.

---

## What I Built

The emulator implements:

- All 56 official 6502 instructions
- All 13 addressing modes including indirect indexed (IND_X, IND_Y) and relative branching (REL)
- Accurate flag behavior for N, V, B, D, I, Z, C
- Hardware stack at $0100–$01FF
- Full 64KB memory model
- Cycle-accurate counting
- Signed overflow detection for ADC/SBC
- JSR/RTS subroutine call and return with stack management

---

## What I Learned

Building this forced me to actually understand things I'd only vaguely known existed:

**Bitwise operations in practice.** You can't emulate hardware without them. Masking with `& 0xFF` to clamp to 8 bits, shifting with `>>` and `<<` to pack and unpack flag bytes, detecting overflow with the `~(A ^ value) & (A ^ result) & 0x80` formula — these stopped being abstract and became tools.

**How CPUs actually execute code.** The fetch-decode-execute loop sounds simple until you implement it. The moment that clicked for me was realizing that every instruction is just a carefully sequenced set of register reads, writes, and arithmetic operations. There's no magic.

**Little-endian byte ordering.** The 6502 stores 16-bit addresses low-byte first. `fetch_word()` taught me why byte order matters.

**WebSockets vs HTTP.** REST is request-response — the browser has to ask. WebSocket is persistent — the server can push. For a live debugger where you want state updates the moment they happen, the difference is fundamental.

**Why emulation is hard.** Getting the basic loop working is 20% of the work. The other 80% is edge cases — what happens when SP wraps from $00 to $FF, how indirect addressing actually resolves through two pointer hops, why SBC is implemented as ADC with an inverted operand.

---

## Roadmap

Things I'd add with more time:

- **Assembler input** — write assembly mnemonics directly instead of raw hex
- **NES ROM loading** — parse the iNES format and run actual NES games
- **Breakpoints** — pause execution when PC hits a specific address
- **Memory write watch** — highlight bytes that changed since the last step
- **Export/import** — save and load CPU state snapshots

---

## License

MIT — do whatever you want with it.
