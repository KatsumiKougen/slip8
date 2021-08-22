import sys, os
from compiler import Compiler

if len(sys.argv) <= 1:
    print("\x1b[1mSLIP-8 the CHIP-8 Compiler: \x1b[31mError: \x1b[0mNo input files.\nCompilation terminated.")
elif not os.path.isfile(sys.argv[1]):
    print(f"\x1b[1mSLIP-8 the CHIP-8 Compiler: \x1b[31mError: \x1b[0mFile \x1b[1;7m{sys.argv[1]}\x1b[0m does not exist.\nCompilation terminated.")
elif sys.argv[1].split(".")[-1] != "c8asm":
    print(f"\x1b[1mSLIP-8 the CHIP-8 Compiler: \x1b[31mError: \x1b[0mFile \x1b[1;7m{sys.argv[1]}\x1b[0m is of wrong format, expecting .c8asm file.\nCompilation terminated.")
else:
    compiler = Compiler()
    compiler.loadSource(sys.argv[1])
    try:
        compiler.buildFromSource()
        if sys.argv[2] == "--stdout":
            compiler.writeTo(compiler.stdout)
        elif sys.argv[2] == "--out":
            compiler.writeTo(compiler.binary, name=sys.argv[3])
    except compiler.UnknownInstructionException:
        print(f"\x1b[1mSLIP-8 the CHIP-8 Compiler: \x1b[31mError: \x1b[0mUnknown instruction at \x1b[93;1m{compiler.currentLine}\x1b[0m\nCompilation terminated.")
    except compiler.Instruction.NotMemoryLocation:
        print(f"\x1b[1mSLIP-8 the CHIP-8 Compiler: \x1b[31mError: \x1b[0mDetected discrepancy at \x1b[93;1m{compiler.currentLine} \x1b[0;1;42m(Not a memory location)\x1b[0m\nCompilation terminated.")
    except compiler.Instruction.WrongRegister:
        print(f"\x1b[1mSLIP-8 the CHIP-8 Compiler: \x1b[31mError: \x1b[0mDetected discrepancy at \x1b[93;1m{compiler.currentLine} \x1b[0;1;36m(Wrong register)\x1b[0m\nCompilation terminated.")
    except compiler.Instruction.NotEnoughValue:
        print(f"\x1b[1mSLIP-8 the CHIP-8 Compiler: \x1b[31mError: \x1b[0mDetected discrepancy at \x1b[93;1m{compiler.currentLine} \x1b[0;1;34m(Not enough values)\x1b[0m\nCompilation terminated.")
    except compiler.Instruction.WrongValue:
        print(f"\x1b[1mSLIP-8 the CHIP-8 Compiler: \x1b[31mError: \x1b[0mDetected discrepancy at \x1b[93;1m{compiler.currentLine} \x1b[0;1;41m(Wrong value)\x1b[0m\nCompilation terminated.")
