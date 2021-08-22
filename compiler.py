class Compiler:

    class UnknownInstructionException(Exception):
        pass
    
    class CompilerError(Exception):
        class FileNotExist(Exception):
            pass
        class ModeNotExist(Exception):
            pass
        class Empty(Exception):
            pass
    
    class Instruction:
        class NotMemoryLocation(Exception):
            pass
        class WrongRegister(Exception):
            pass
        class NotEnoughValue(Exception):
            pass
        class WrongValue(Exception):
            pass
    
    stdout = 1
    binary = 0
    __mnemonic = [
        "nop", "cls", "ret", "jp",   "call", "se",  "ld",  "add", "or",  "and",
        "xor", "sub", "shr", "subn", "shl",  "sne", "rnd", "drw", "skp", "sknp"
    ]
    __hex = "0123456789abcdef"
    
    def __init__(self):
        self.__instStorage = []
        self.instValue = [0, 0]
        self.currentLine = 1
    
    def __parse(self, string: str):
        inst = string.split(" ")
        if inst[0] in self.__mnemonic:
        
            if inst[0] == "nop":
                self.instValue = [0, 0]
            
            elif inst[0] == "cls":
                self.instValue = [0, 0xe0]
            
            elif inst[0] == "ret":
                self.instValue = [0, 0xee]
            
            elif inst[0] == "jp":
                if len(inst) <= 1:
                    raise self.Instruction.NotEnoughValue("Requires a memory location, or V0 + memory location.")
                elif len(inst) == 2:
                    if inst[1][0] in self.__hex:
                        self.instValue = [int(f"1{inst[1][0]}", 16), int(inst[1][1:], 16)]
                    else:
                        raise self.Instruction.NotMemoryLocation(f"{inst[1]} is not a memory location.")
                elif len(inst) == 3:
                    if inst[1][0:2] != "V0":
                        raise self.Instruction.WrongRegister("Can't use the V{inst[1][1]} register.")
                    elif inst[2][0] in self.__hex:
                        self.instValue = [int(f"b{inst[2][0]}", 16), int(inst[2][1:], 16)]
                    else:
                        raise self.Instruction.NotMemoryLocation(f"{inst[2]} is not a memory location.")
            
            elif inst[0] == "call":
                if len(inst) <= 1:
                    raise self.Instruction.NotEnoughValue("Requires a memory location.")
                elif inst[1][0] in self.__hex:
                    self.instValue = [int(f"2{inst[1][0]}", 16), int(inst[1][1:], 16)]
                else:
                    raise self.Instruction.NotMemoryLocation(f"{inst[1]} is not a memory location.")
            
            elif inst[0] == "se":
                if len(inst) <= 2:
                    raise self.Instruction.NotEnoughValue("Requires a register or a number.")
                elif inst[2][0] != "V" and inst[2][0] not in self.__hex:
                    raise self.Instruction.WrongValue("Requires a register or a number.")
                elif inst[2][0] != "V":
                    self.instValue = [int(f"3{inst[1][1]}", 16), int(inst[2], 16)]
                else:
                    self.instValue = [int(f"5{inst[1][1]}", 16), int(f"{inst[2][1]}0", 16)]
            
            elif inst[0] == "ld":
                if len(inst) <= 2:
                    raise self.Instruction.NotEnoughValue("Requires 2 more values.")
                elif inst[1][0] == "V":
                    if inst[2][0] == "V":
                        self.instValue = [int(f"8{inst[1][1]}", 16), int(f"{inst[2][1]}0", 16)]
                    elif inst[2] == "DT":
                        self.instValue = [int(f"f{inst[1][1]}", 16), 0x07]
                    elif inst[2] == "K":
                        self.instValue = [int(f"f{inst[1][1]}", 16), 0x0a]
                    elif inst[2] == "[I]":
                        self.instValue = [int(f"f{inst[1][1]}", 16), 0x65]
                    elif inst[2][0] in self.__hex:
                        self.instValue = [int(f"6{inst[1][1]}", 16), int(inst[2], 16)]
                    else:
                        raise self.Instruction.WrongValue("Requires a register, DT, K, [I] or a number.")
                elif inst[1][:-1] == "I":
                    self.instValue = [int(f"a{inst[2][0]}", 16), int(inst[2][1:], 16)]
                elif inst[1][:-1] == "DT":
                    self.instValue = [int(f"f{inst[2][1]}", 16), 0x15]
                elif inst[1][:-1] == "ST":
                    self.instValue = [int(f"f{inst[2][1]}", 16), 0x18]
                elif inst[1][:-1] == "F":
                    self.instValue = [int(f"f{inst[2][1]}", 16), 0x29]
                elif inst[1][:-1] == "B":
                    self.instValue = [int(f"f{inst[2][1]}", 16), 0x33]
                elif inst[1][:-1] == "[I]":
                    self.instValue = [int(f"f{inst[2][1]}", 16), 0x55]
                else:
                    raise self.Instruction.WrongValue("Wrong value, expected V, I, DT, ST, F, B or [I].")
            
            elif inst[0] == "add":
                if len(inst) <= 2:
                    raise self.Instruction.NotEnoughValue("Requires a register and a number/register.")
                elif inst[1][0] == "V":
                    if inst[2][0] != "V":
                        self.instValue = [int(f"7{inst[1][1]}", 16), int(inst[2], 16)]
                    elif inst[2][0] in self.__hex:
                        self.instValue = [int(f"8{inst[1][1]}", 16), int(f"{inst[2][1]}4", 16)]
                    else:
                        raise self.Instruction.WrongValue("Requires a register or a number.")
                elif inst[1][0] == "I":
                    self.instValue = [int(f"f{inst[2][1]}", 16), 0x1e]
                else:
                    raise self.Instruction.WrongValue("Wrong value, expected V or I.")
            
            elif inst[0] == "or":
                if len(inst) <= 2:
                    raise self.Instruction.NotEnoughValue("Requires two registers.")
                elif inst[1][0] != "V" or inst[2][0] != "V":
                    raise self.Instruction.WrongValue("Requires two registers.")
                else:
                    self.instValue = [int(f"8{inst[1][1]}", 16), int(f"{inst[2][1]}1", 16)]
            
            elif inst[0] == "and":
                if len(inst) <= 2:
                    raise self.Instruction.NotEnoughValue("Requires two registers.")
                elif inst[1][0] != "V" or inst[2][0] != "V":
                    raise self.Instruction.WrongValue("Requires two registers.")
                else:
                    self.instValue = [int(f"8{inst[1][1]}", 16), int(f"{inst[2][1]}2", 16)]
            
            elif inst[0] == "xor":
                if len(inst) <= 2:
                    raise self.Instruction.NotEnoughValue("Requires two registers.")
                elif inst[1][0] != "V" or inst[2][0] != "V":
                    raise self.Instruction.WrongValue("Requires two registers.")
                else:
                    self.instValue = [int(f"8{inst[1][1]}", 16), int(f"{inst[2][1]}3", 16)]
            
            elif inst[0] == "sub":
                if len(inst) <= 2:
                    raise self.Instruction.NotEnoughValue("Requires two registers.")
                elif inst[1][0] != "V" or inst[2][0] != "V":
                    raise self.Instruction.WrongValue("Requires two registers.")
                else:
                    self.instValue = [int(f"8{inst[1][1]}", 16), int(f"{inst[2][1]}5", 16)]
            
            elif inst[0] == "subn":
                if len(inst) <= 2:
                    raise self.Instruction.NotEnoughValue("Requires two registers.")
                elif inst[1][0] != "V" or inst[2][0] != "V":
                    raise self.Instruction.WrongValue("Requires two registers.")
                else:
                    self.instValue = [int(f"8{inst[1][1]}", 16), int(f"{inst[2][1]}7", 16)]
            
            elif inst[0] == "shr":
                if len(inst) <= 2:
                    raise self.Instruction.NotEnoughValue("Requires two registers.")
                elif inst[1][0] != "V" or inst[2][0] != "V":
                    raise self.Instruction.WrongValue("Requires two registers.")
                else:
                    self.instValue = [int(f"8{inst[1][1]}", 16), int(f"{inst[2][1]}6", 16)]
            
            elif inst[0] == "shl":
                if len(inst) <= 2:
                    raise self.Instruction.NotEnoughValue("Requires two registers.")
                elif inst[1][0] != "V" or inst[2][0] != "V":
                    raise self.Instruction.WrongValue("Requires two registers.")
                else:
                    self.instValue = [int(f"8{inst[1][1]}", 16), int(f"{inst[2][1]}e", 16)]
            
            elif inst[0] == "sne":
                if len(inst) <= 2:
                    raise self.Instruction.NotEnoughValue("Requires two registers.")
                elif inst[1][0] != "V" or inst[2][0] != "V":
                    raise self.Instruction.WrongValue("Requires two registers.")
                else:
                    self.instValue = [int(f"9{inst[1][1]}", 16), int(f"{inst[2][1]}0", 16)]
            
            elif inst[0] == "rnd":
                if len(inst) <= 2:
                    raise self.Instruction.NotEnoughValue("Requires a register and a number.")
                elif inst[1][0] != "V":
                    raise self.Instruction.WrongValue("Requires a register.")
                else:
                    self.instValue = [int(f"c{inst[1][1]}", 16), int(inst[2], 16)]
            
            elif inst[0] == "drw":
                if len(inst) <= 3:
                    raise self.Instruction.NotEnoughValue("Requires two registers and a nibble.")
                elif inst[1][0] != "V" or inst[2][0] != "V":
                    raise self.Instruction.WrongValue("Requires two registers.")
                else:
                    self.instValue = [int(f"d{inst[1][1]}", 16), int(f"{inst[2][1]}{inst[3]}", 16)]
            
            elif inst[0] == "skp":
                if len(inst) <= 1:
                    raise self.Instruction.NotEnoughValue("Requires a register.")
                else:
                    self.instValue = [int(f"e{inst[1][1]}", 16), 0x9e]
            
            elif inst[0] == "sknp":
                if len(inst) <= 1:
                    raise self.Instruction.NotEnoughValue("Requires a register.")
                else:
                    self.instValue = [int(f"e{inst[1][1]}", 16), 0xa1]
            
        else:
            raise self.UnknownInstructionException("Unknown instruction.")
    
    def build(self, instList: list):
        if len(instList) < 1:
            raise self.CompilerError.Empty("No instructions.")
        for inst in instList:
            self.__parse(inst)
            self.__instStorage.extend(self.instValue)
            self.currentLine += 1
    
    def buildFromSource(self):
        for inst in self.__source.split("\n")[:-1]:
            self.__parse(inst)
            self.__instStorage.extend(self.instValue)
            self.currentLine += 1
    
    def writeTo(self, mode: int, name=None):
        if mode == self.stdout:
            print(self.__instStorage)
        elif mode == self.binary:
            with open(f"{name}.c8x", "wb") as f:
                f.write(bytes(self.__instStorage))
        else:
            raise self.CompilerError.ModeNotExist(f"Mode {mode} is not defined, expected stdout or binary.")
    
    def loadSource(self, path: str):
        if __import__("os").path.isfile(path):
            with open(path, "r") as f:
                self.__source = f.read()
        else:
            raise self.CompilerError.FileNotExist(f"Cannot find {path}. Either it is deleted or does not exist.")
