# emulator/opcodes.py

# Each entry: opcode value -> (mnemonic, addressing_mode, cycles)
OPCODES = {

    # --- LDA (Load Accumulator) ---
    0xA9: ("LDA", "IMM",  2),
    0xA5: ("LDA", "ZP",   3),
    0xB5: ("LDA", "ZP_X", 4),
    0xAD: ("LDA", "ABS",  4),
    0xBD: ("LDA", "ABS_X",4),
    0xB9: ("LDA", "ABS_Y",4),

    # --- LDX (Load X Register) ---
    0xA2: ("LDX", "IMM",  2),
    0xA6: ("LDX", "ZP",   3),
    0xB6: ("LDX", "ZP_Y", 4),
    0xAE: ("LDX", "ABS",  4),
    0xBE: ("LDX", "ABS_Y",4),

    # --- LDY (Load Y Register) ---
    0xA0: ("LDY", "IMM",  2),
    0xA4: ("LDY", "ZP",   3),
    0xB4: ("LDY", "ZP_X", 4),
    0xAC: ("LDY", "ABS",  4),
    0xBC: ("LDY", "ABS_X",4),

    # --- STA (Store Accumulator) ---
    0x85: ("STA", "ZP",   3),
    0x95: ("STA", "ZP_X", 4),
    0x8D: ("STA", "ABS",  4),
    0x9D: ("STA", "ABS_X",5),
    0x99: ("STA", "ABS_Y",5),

    # --- STX (Store X Register) ---
    0x86: ("STX", "ZP",   3),
    0x96: ("STX", "ZP_Y", 4),
    0x8E: ("STX", "ABS",  4),

    # --- STY (Store Y Register) ---
    0x84: ("STY", "ZP",   3),
    0x94: ("STY", "ZP_X", 4),
    0x8C: ("STY", "ABS",  4),

    # --- Register transfers ---
    0xAA: ("TAX", "IMP", 2),  # A -> X
    0xA8: ("TAY", "IMP", 2),  # A -> Y
    0x8A: ("TXA", "IMP", 2),  # X -> A
    0x98: ("TYA", "IMP", 2),  # Y -> A

    # --- Increment / Decrement ---
    0xE8: ("INX", "IMP", 2),  # X + 1
    0xC8: ("INY", "IMP", 2),  # Y + 1
    0xCA: ("DEX", "IMP", 2),  # X - 1
    0x88: ("DEY", "IMP", 2),  # Y - 1

    # --- No operation / Break ---
    0xEA: ("NOP", "IMP", 2),
    0x00: ("BRK", "IMP", 7),
}