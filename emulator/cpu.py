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
        if mode == "IMM":
            addr = self.PC
            self.PC = (self.PC + 1) & 0xFFFF
            self.cycles += 1
            return addr

        elif mode == "ZP":
            return self.fetch_byte()

        elif mode == "ZP_X":
            base = self.fetch_byte()
            self.cycles += 1
            return (base + self.X) & 0xFF

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

        elif mode == "IND_X":
            # Fetch a zero page address, add X, read the 16-bit address stored there
            base = (self.fetch_byte() + self.X) & 0xFF
            low  = self.memory.read(base)
            high = self.memory.read((base + 1) & 0xFF)
            self.cycles += 2
            return (high << 8) | low

        elif mode == "IND_Y":
            # Fetch zero page address, read 16-bit address there, then add Y
            base = self.fetch_byte()
            low  = self.memory.read(base)
            high = self.memory.read((base + 1) & 0xFF)
            self.cycles += 1
            return ((high << 8) | low) + self.Y

        elif mode == "IND":
            # Only used by JMP — fetch address, read the actual target from there
            ptr  = self.fetch_word()
            low  = self.memory.read(ptr)
            high = self.memory.read((ptr & 0xFF00) | ((ptr + 1) & 0xFF))
            return (high << 8) | low

        elif mode == "REL":
            # Signed 1-byte offset from current PC — used by all branches
            offset = self.fetch_byte()
            if offset & 0x80:          # If bit 7 is set, it's a negative offset
                offset -= 0x100        # Convert to Python negative int
            return (self.PC + offset) & 0xFFFF

        else:
            raise ValueError(f"Unknown addressing mode: {mode}")
        

    def step(self) -> dict:
        from emulator.opcodes import OPCODES

        # --- FETCH ---
        opcode_byte = self.fetch_byte()

        # --- DECODE ---
        if opcode_byte not in OPCODES:
            raise ValueError(f"Unknown opcode: {opcode_byte:#04x} at PC {self.PC - 1:#06x}")

        mnemonic, mode, base_cycles = OPCODES[opcode_byte]
        self.cycles += base_cycles - 1

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

        # -- Arithmetic --
        elif mnemonic == "ADC":
            addr = self.resolve_address(mode)
            value = self.memory.read(addr)
            result = self.A + value + self.C
            # Overflow: if two positives produce a negative (or vice versa)
            self.V = 1 if (~(self.A ^ value) & (self.A ^ result) & 0x80) else 0
            self.C = 1 if result > 0xFF else 0
            self.A = result & 0xFF
            self.set_zn_flags(self.A)

        elif mnemonic == "SBC":
            addr = self.resolve_address(mode)
            value = self.memory.read(addr) ^ 0xFF  # Invert for subtraction
            result = self.A + value + self.C
            self.V = 1 if (~(self.A ^ value) & (self.A ^ result) & 0x80) else 0
            self.C = 1 if result > 0xFF else 0
            self.A = result & 0xFF
            self.set_zn_flags(self.A)

        # -- Logic --
        elif mnemonic == "AND":
            addr = self.resolve_address(mode)
            self.A &= self.memory.read(addr)
            self.set_zn_flags(self.A)

        elif mnemonic == "ORA":
            addr = self.resolve_address(mode)
            self.A |= self.memory.read(addr)
            self.set_zn_flags(self.A)

        elif mnemonic == "EOR":
            addr = self.resolve_address(mode)
            self.A ^= self.memory.read(addr)
            self.set_zn_flags(self.A)

        # -- Shifts --
        elif mnemonic == "ASL":
            if mode == "ACC":
                self.C = (self.A >> 7) & 1
                self.A = (self.A << 1) & 0xFF
                self.set_zn_flags(self.A)
            else:
                addr  = self.resolve_address(mode)
                value = self.memory.read(addr)
                self.C = (value >> 7) & 1
                result = (value << 1) & 0xFF
                self.memory.write(addr, result)
                self.set_zn_flags(result)

        elif mnemonic == "LSR":
            if mode == "ACC":
                self.C = self.A & 1
                self.A = (self.A >> 1) & 0xFF
                self.set_zn_flags(self.A)
            else:
                addr  = self.resolve_address(mode)
                value = self.memory.read(addr)
                self.C = value & 1
                result = (value >> 1) & 0xFF
                self.memory.write(addr, result)
                self.set_zn_flags(result)

        elif mnemonic == "ROL":
            if mode == "ACC":
                new_c  = (self.A >> 7) & 1
                self.A = ((self.A << 1) | self.C) & 0xFF
                self.C = new_c
                self.set_zn_flags(self.A)
            else:
                addr   = self.resolve_address(mode)
                value  = self.memory.read(addr)
                new_c  = (value >> 7) & 1
                result = ((value << 1) | self.C) & 0xFF
                self.memory.write(addr, result)
                self.C = new_c
                self.set_zn_flags(result)

        elif mnemonic == "ROR":
            if mode == "ACC":
                new_c  = self.A & 1
                self.A = ((self.A >> 1) | (self.C << 7)) & 0xFF
                self.C = new_c
                self.set_zn_flags(self.A)
            else:
                addr   = self.resolve_address(mode)
                value  = self.memory.read(addr)
                new_c  = value & 1
                result = ((value >> 1) | (self.C << 7)) & 0xFF
                self.memory.write(addr, result)
                self.C = new_c
                self.set_zn_flags(result)

        # -- Compare --
        elif mnemonic in ("CMP", "CPX", "CPY"):
            addr  = self.resolve_address(mode)
            value = self.memory.read(addr)
            reg   = self.A if mnemonic == "CMP" else (self.X if mnemonic == "CPX" else self.Y)
            result = (reg - value) & 0xFF
            self.C = 1 if reg >= value else 0
            self.set_zn_flags(result)

        elif mnemonic == "BIT":
            addr  = self.resolve_address(mode)
            value = self.memory.read(addr)
            self.Z = 1 if (self.A & value) == 0 else 0
            self.N = (value >> 7) & 1
            self.V = (value >> 6) & 1

        # -- Branches --
        elif mnemonic in ("BCC","BCS","BEQ","BNE","BMI","BPL","BVC","BVS"):
            target = self.resolve_address("REL")
            branch_map = {
                "BCC": self.C == 0, "BCS": self.C == 1,
                "BEQ": self.Z == 1, "BNE": self.Z == 0,
                "BMI": self.N == 1, "BPL": self.N == 0,
                "BVC": self.V == 0, "BVS": self.V == 1,
            }
            if branch_map[mnemonic]:
                self.cycles += 1
                self.PC = target

        # -- Jumps --
        elif mnemonic == "JMP":
            self.PC = self.resolve_address(mode)

        elif mnemonic == "JSR":
            target = self.fetch_word()
            ret    = (self.PC - 1) & 0xFFFF
            self.stack_push((ret >> 8) & 0xFF)  # Push high byte
            self.stack_push(ret & 0xFF)          # Push low byte
            self.PC = target

        elif mnemonic == "RTS":
            low    = self.stack_pop()
            high   = self.stack_pop()
            self.PC = (((high << 8) | low) + 1) & 0xFFFF

        # -- Stack --
        elif mnemonic == "PHA":
            self.stack_push(self.A)

        elif mnemonic == "PLA":
            self.A = self.stack_pop()
            self.set_zn_flags(self.A)

        elif mnemonic == "PHP":
            self.stack_push(self.get_status_byte())

        elif mnemonic == "PLP":
            self.set_status_byte(self.stack_pop())

        # -- Register transfers --
        elif mnemonic == "TAX":
            self.X = self.A;  self.set_zn_flags(self.X)

        elif mnemonic == "TAY":
            self.Y = self.A;  self.set_zn_flags(self.Y)

        elif mnemonic == "TXA":
            self.A = self.X;  self.set_zn_flags(self.A)

        elif mnemonic == "TYA":
            self.A = self.Y;  self.set_zn_flags(self.A)

        elif mnemonic == "TSX":
            self.X = self.SP; self.set_zn_flags(self.X)

        elif mnemonic == "TXS":
            self.SP = self.X  # No flags set for TXS

        # -- INC / DEC memory --
        elif mnemonic == "INC":
            addr   = self.resolve_address(mode)
            result = (self.memory.read(addr) + 1) & 0xFF
            self.memory.write(addr, result)
            self.set_zn_flags(result)

        elif mnemonic == "DEC":
            addr   = self.resolve_address(mode)
            result = (self.memory.read(addr) - 1) & 0xFF
            self.memory.write(addr, result)
            self.set_zn_flags(result)

        # -- INX, INY, DEX, DEY --
        elif mnemonic == "INX":
            self.X = (self.X + 1) & 0xFF; self.set_zn_flags(self.X)

        elif mnemonic == "INY":
            self.Y = (self.Y + 1) & 0xFF; self.set_zn_flags(self.Y)

        elif mnemonic == "DEX":
            self.X = (self.X - 1) & 0xFF; self.set_zn_flags(self.X)

        elif mnemonic == "DEY":
            self.Y = (self.Y - 1) & 0xFF; self.set_zn_flags(self.Y)

        # -- Flag instructions --
        elif mnemonic == "CLC": self.C = 0
        elif mnemonic == "SEC": self.C = 1
        elif mnemonic == "CLI": self.I = 0
        elif mnemonic == "SEI": self.I = 1
        elif mnemonic == "CLV": self.V = 0
        elif mnemonic == "CLD": self.D = 0
        elif mnemonic == "SED": self.D = 1

        elif mnemonic == "NOP":
            pass

        elif mnemonic == "BRK":
            self.B = 1
            return {**self.get_state(), "halted": True}

        return {**self.get_state(), "halted": False}
    

if __name__ == "__main__":
    
    cpu = CPU()

    program = [0xA9, 0x00, 0xAA, 0xE8, 0xE0, 0x03, 0xD0, 0xFB, 0x00]

    cpu.memory.load(0x0600, program)

    halted = False
    while not halted:
        state = cpu.step()
        halted = state["halted"]
        print(f"PC:{state['PC']:#06x}  A:{state['A']:#04x}  X:{state['X']:#04x}  Y:{state['Y']:#04x}  cycles:{state['cycles']}")
        