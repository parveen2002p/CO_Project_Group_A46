opcode={'add':'10000','sub':'10001','mov':'10010','ld':'10100',
'st':'10101','mul':'10110','div':'10111','rs':'11000','ls':'11001','xor':'11010',
'or':'11011','and':'11100','not':'11101','cmp':'11110','jmp':'11111','jlt':'01100',
'jgt':'01101','je':'01111','hlt':'01010'}

# Unwanted checking of opcode
# prepare new list for opcode check then calling type check function
# upgrading type check for preparing return machine code
# check prpoer imm and mem add
# flag operation prohibited only mov inst possible

OP_A=["add","sub"]
OP_B=["rs","ls"]
sum = 00000001
x = 00000001
sum++
y =

var{x:1000},



reg={"R0":"000","R1":"001","R2":"002","R3":"003","R4":"004","R5":"005","R6":"006","FLAGS":"111"}

type_A=[opcode,"00",reg,reg,reg]
type_B=[opcode,reg,"$"]
type_C=[opcode,"00000",reg,reg]
type_D=[opcode,reg,"MEMADD"]
type_E=[opcode,"000","MEMADD"]
type_F=[opcode,"00000000000"]

for i in f.readlines():
    data=i.split()

def validmem():
    return True

def validimm():
    return True

    

def checkA():
    arglen=len(data)
    if arglen!=4:
        return False
    checkstr=""
    truestr="ORRR"
    for i in range(0,len(data)):
            if data[i] in type_A[0]:
                checkstr+="O"
            elif data[i] in type_A[2]:
                checkstr+="R"
    if checkstr==truestr:
        return True

        

    def checkB():
        arglen=len(data)
        if arglen!=3:
            return False
        truestr="ORIV"
        for i in range(0,len(data)):
            if data[i] in type_B[0]:
                checkstr+="O"
            elif data[i] in type_B[1]:
                checkstr+="R"  
            elif (data[i][0] =="$"):
                checkstr+="I" 
        if validimm(data[3]):
            checkstr+="V"
        if(checkstr==truestr):
            return True

    

    def checkC():
        arglen=len(data)
        if arglen!=3:
            return False
        truestr="ORR"
        for i in range(0,len(data)):
            if data[i] in type_B[0]:
                checkstr+="O"
            elif data[i] in type_B[1]:
                checkstr+="R"  
            
        if(checkstr==truestr):
            return True


    def checkD():
        arglen=len(data)
        if arglen!=3:
            return False
        truestr="ORM"
        if data[1] in type_B[0]:
                checkstr+="O"
        if data[2] in type_B[1]:
                checkstr+="R"
        if validmem(data[3]):
                checkstr+="M"  
        if(checkstr==truestr):
                return True


    def checkE():
        arglen=len(data)
        if arglen!=2:
            return False
        truestr="OM"
        if data[1] in type_B[0]:
                checkstr+="O"
        if validmem(data[2]):
                checkstr+="M"
             
        if(checkstr==truestr):
                return True

    def checkF():
        arglen=len(data)
        if arglen!=1:
            return False
        truestr="O"
        for i in range(0,len(data)):
            if data[i] in type_B[0]:
                checkstr+="O"
              
        if(checkstr==truestr):
                return True                        

import fileinput
list1=[]
for line in fileinput.input():
    print(line.rstrip())
    list1.append(line.rstrip())

# for one go
import sys
list1=sys.stdin.readlines()
#for removing /n
list1=[line.rstrip() for line in list1]   # do we need to remove blank line from list as it would change i value for reporting error

import sys
print("Hello, World!")
list1=sys.stdin.readlines()
print(list1)
#for removing /n
list1=[line.rstrip() for line in list1]  
print(list1)

import fileinput
list1=[]
for line in fileinput.input():
    list1.append(line)
print(list1)
list1=[line.rstrip() for line in list1]
print(list1)


# 0.0 -ve char check and function is alpha
            
                                
