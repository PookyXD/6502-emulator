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

if __name__ == "__main__":
    cpu = CPU()
    print(cpu.get_state())
