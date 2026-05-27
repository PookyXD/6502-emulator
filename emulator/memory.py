#emulator's memory

class Memory:
    SIZE = 65536

    def __init__(self):
        self.data = [0x00] * self.SIZE
    
    def read(self, address: int) -> int:
        """Read one byte from the given address."""
        if not (0 <= address < self.SIZE):
            raise ValueError(f"Memory read out of range: {address:#06x}")
        return self.data[address]

    def write(self, address: int, value: int) -> None:
        """Write one byte to the given address."""
        if not (0 <= address < self.SIZE):
            raise ValueError(f"Memory write out of range: {address:#06x}")
        if not (0 <= value <= 0xFF):
            raise ValueError(f"Value out of byte range: {value}")
        self.data[address] = value

    def load(self, start_address: int, program: list[int]) -> None:
        """Load a list of bytes into memory starting at a given address."""
        for offset, byte in enumerate(program):
            self.write(start_address + offset, byte)

    def reset(self) -> None:
        """Wipe all memory back to zero."""
        self.data = [0x00] * self.SIZE