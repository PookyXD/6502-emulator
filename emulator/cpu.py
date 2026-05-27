# emulator's core cpu

from emulator.memory import Memory

class CPU:
    def __init__(self):
        self.memory = Memory()
        self.reset()

    def reset(self):
        self.PC = 0x0600
        self.SP = 0xFF
        self.A  = 0x00
        self.X  = 0x00
        self.Y  = 0x00
        self.N = 0
        self.V = 0
        self.B = 0
        self.D = 0
        self.I = 1
        self.Z = 0
        self.C = 0
        self.cycles = 0

    def set_zn_flags(self, value: int) -> None:
        self.Z = 1 if (value & 0xFF) == 0 else 0
        self.N = 1 if (value & 0x80) != 0 else 0

    def get_status_byte(self) -> int:
        return (
            (self.N << 7) |
            (self.V << 6) |
            (1     << 5) |
            (self.B << 4) |
            (self.D << 3) |
            (self.I << 2) |
            (self.Z << 1) |
            (self.C << 0)
        )

    def set_status_byte(self, value: int) -> None:
        self.N = (value >> 7) & 1
        self.V = (value >> 6) & 1
        self.B = (value >> 4) & 1
        self.D = (value >> 3) & 1
        self.I = (value >> 2) & 1
        self.Z = (value >> 1) & 1
        self.C = (value >> 0) & 1

    def fetch_byte(self) -> int:
        value = self.memory.read(self.PC)
        self.PC = (self.PC + 1) & 0xFFFF
        self.cycles += 1
        return value

    def fetch_word(self) -> int:
        low  = self.fetch_byte()
        high = self.fetch_byte()
        return (high << 8) | low

    def read_byte(self, address: int) -> int:
        self.cycles += 1
        return self.memory.read(address)

    def write_byte(self, address: int, value: int) -> None:
        self.cycles += 1
        self.memory.write(address, value)

    def stack_push(self, value: int) -> None:
        self.write_byte(0x0100 + self.SP, value)
        self.SP = (self.SP - 1) & 0xFF

    def stack_pop(self) -> int:
        self.SP = (self.SP + 1) & 0xFF
        return self.read_byte(0x0100 + self.SP)

    def get_state(self) -> dict:
        return {
            "PC": self.PC,
            "SP": self.SP,
            "A":  self.A,
            "X":  self.X,
            "Y":  self.Y,
            "P":  self.get_status_byte(),
            "flags": {
                "N": self.N, "V": self.V, "B": self.B,
                "D": self.D, "I": self.I, "Z": self.Z, "C": self.C
            },
            "cycles": self.cycles
        }
    
    def resolve_address(self, mode: str) -> int:
        """
        Given an addressing mode, fetch the operand bytes from memory
        and return the effective address the instruction should use.
        """
        if mode == "IMM":
            # Value is the next byte itself — return PC, then advance
            addr = self.PC
            self.PC = (self.PC + 1) & 0xFFFF
            self.cycles += 1
            return addr

        elif mode == "ZP":
            return self.fetch_byte()

        elif mode == "ZP_X":
            base = self.fetch_byte()
            self.cycles += 1
            return (base + self.X) & 0xFF   # Wraps within zero page

        elif mode == "ZP_Y":
            base = self.fetch_byte()
            self.cycles += 1
            return (base + self.Y) & 0xFF

        elif mode == "ABS":
            return self.fetch_word()

        elif mode == "ABS_X":
            base = self.fetch_word()
            return (base + self.X) & 0xFFFF

        elif mode == "ABS_Y":
            base = self.fetch_word()
            return (base + self.Y) & 0xFFFF

        else:
            raise ValueError(f"Unknown addressing mode: {mode}")
        

    def step(self) -> dict:
        """
        Execute one instruction and return the CPU state after it.
        This is the fetch-decode-execute cycle.
        """
        from emulator.opcodes import OPCODES

        # --- FETCH ---
        opcode_byte = self.fetch_byte()

        # --- DECODE ---
        if opcode_byte not in OPCODES:
            raise ValueError(f"Unknown opcode: {opcode_byte:#04x} at PC {self.PC - 1:#06x}")

        mnemonic, mode, base_cycles = OPCODES[opcode_byte]
        self.cycles += base_cycles - 1  # -1 because fetch_byte already added 1

        # --- EXECUTE ---

        # -- Loads --
        if mnemonic == "LDA":
            addr = self.resolve_address(mode)
            self.A = self.memory.read(addr)
            self.set_zn_flags(self.A)

        elif mnemonic == "LDX":
            addr = self.resolve_address(mode)
            self.X = self.memory.read(addr)
            self.set_zn_flags(self.X)

        elif mnemonic == "LDY":
            addr = self.resolve_address(mode)
            self.Y = self.memory.read(addr)
            self.set_zn_flags(self.Y)

        # -- Stores --
        elif mnemonic == "STA":
            addr = self.resolve_address(mode)
            self.memory.write(addr, self.A)

        elif mnemonic == "STX":
            addr = self.resolve_address(mode)
            self.memory.write(addr, self.X)

        elif mnemonic == "STY":
            addr = self.resolve_address(mode)
            self.memory.write(addr, self.Y)

        # -- Register transfers --
        elif mnemonic == "TAX":
            self.X = self.A
            self.set_zn_flags(self.X)

        elif mnemonic == "TAY":
            self.Y = self.A
            self.set_zn_flags(self.Y)

        elif mnemonic == "TXA":
            self.A = self.X
            self.set_zn_flags(self.A)

        elif mnemonic == "TYA":
            self.A = self.Y
            self.set_zn_flags(self.A)

        # -- Increment / Decrement --
        elif mnemonic == "INX":
            self.X = (self.X + 1) & 0xFF
            self.set_zn_flags(self.X)

        elif mnemonic == "INY":
            self.Y = (self.Y + 1) & 0xFF
            self.set_zn_flags(self.Y)

        elif mnemonic == "DEX":
            self.X = (self.X - 1) & 0xFF
            self.set_zn_flags(self.X)

        elif mnemonic == "DEY":
            self.Y = (self.Y - 1) & 0xFF
            self.set_zn_flags(self.Y)

        # -- NOP / BRK --
        elif mnemonic == "NOP":
            pass  # Literally do nothing

        elif mnemonic == "BRK":
            self.B = 1  # Signal that we hit a break
            return {**self.get_state(), "halted": True}

        return {**self.get_state(), "halted": False}
    

if __name__ == "__main__":
    
    cpu = CPU()

    program = [0xA9, 0x05, 0xAA, 0xE8, 0x8D, 0x00, 0x02, 0x00]

    cpu.memory.load(0x0600, program)

    print("Initial state:")
    print(cpu.get_state())
    print()

    halted = False
    while not halted:
        state = cpu.step()
        halted = state["halted"]
        print(f"PC:{state['PC']:#06x}  A:{state['A']:#04x}  X:{state['X']:#04x}  Y:{state['Y']:#04x}  cycles:{state['cycles']}")
        