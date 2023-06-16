from asyncio.windows_events import NULL


opcode={'add':'10000','sub':'10001','mov':'10010','ld':'10100','st':'10101','mul':'10110','div':'10111','rs':'11000','ls':'11001','xor':'11010','or':'11011','and':'11100','not':'11101','cmp':'11110','jmp':'11111','jlt':'01100','jgt':'01101','je':'01111','hlt':'01010'}

reg={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}

counter="00000000"

convert1=""
var={}
label={}
def var_form(name):
    global var
    global counter
    sum = str(bin(1 + int(counter, 2)).replace("0b",""))
    while(len(sum)<8):
        sum="0"+sum
    var[str(name)]=str(sum)
    counter=str(sum)


def label_form(name):
    global label
    global counter
    sum = str(bin(1 + int(counter, 2)).replace("0b",""))
    while(len(sum)<8):
        sum="0"+sum
    label[str(name)]=str(sum)
    counter=str(sum)



type_A=[opcode,reg,reg,reg]
type_B=[opcode,reg]
type_C=[opcode,reg,reg]
type_D=[opcode,reg]
type_E=[opcode]
type_F=[opcode]


def checkA(data):
    global convert1
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
        converted=""
        for i in data:
            if i in opcode:
                converted+=opcode[i]+"00"
            elif i in reg:
                converted+=reg[i]
        
        convert1=converted
        return True
    else:
        return False 

        

def checkB(data):
    global convert1
    if(len(data)!=3):
        return False
    truestr="ORI"
    checkstr=""
    for i in range(0,len(data)):
        if data[i] in type_B[0]:
            checkstr+="O"
        elif data[i] in type_B[1]:
            checkstr+="R"  
        elif (data[i][0] =="$"):
            checkstr+="I" 
    if(checkstr==truestr):
        converted=""
        for i in data:
            if i in opcode:
                converted+=opcode[i]
            elif i in reg:
                converted+=reg[i]
            elif (i[0]=="$"):
                # check for immediate >=0 and <=255
                imm=str(bin(int(i[1:len(i)+1])).replace("0b",""))   # len(i)+1  might be incorrect
                if (len(imm)>8):
                    print("Immediate out of range")
                    break # return FALSE not break
                while(len(imm)<8):
                    imm="0"+imm
                converted+=imm
        convert1=converted
        return True
    else:
        return False 
    

def checkC(data):
    global convert1
    if(len(data)!=3):
        return False
    truestr="ORR"
    checkstr=""
    for i in range(0,len(data)):
        if data[i] in type_C[0]:
            checkstr+="O"
        elif data[i] in type_C[1]:
            checkstr+="R"  
        
    if(checkstr==truestr):
        converted=""
        for i in data:
            if i in opcode:
                converted+=str(int(opcode[i])+1)+"00000"
            elif i in reg:
                converted+=reg[i]
        convert1=converted
        return True
    else:
        return False 
    

def checkD(data):
    global var
    global convert1
    arglen=len(data)
    if arglen!=3:
        return False
    
    truestr="ORM"         # no need to check for memory adrre
    checkstr=""
    for i in range(0,len(data)):
        if data[i] in type_D[0]:
            checkstr+="O"
        elif data[i] in type_D[1]:
            checkstr+="R"  
        else:
            checkstr+="M"   # else might not be required
    if(checkstr==truestr):
        converted=""
        valid_var=NULL
        for i in data:
            if i in opcode:
                converted+=opcode[i]
            elif i in reg:
                converted+=reg[i]
            else:
                valid_var=var[i]      # chcking is done here for valid memmory adrres
                if(valid_var==NULL):
                    return False
                converted+=var[i]    
        convert1=converted
        return True
    else:
        return False
    
    
   
        

def checkE(data):
    global convert1
    global label
    arglen=len(data)
    if arglen!=2:
        return False
    truestr="O"
    checkstr=""
    
    for i in range(0,len(data)):
        if data[i] in type_E[0]:
            checkstr+="O"
        
    
    if(checkstr==truestr):
        converted=""
        valid_addr=NULL
        for i in data:
            if i in opcode:
                converted+=opcode[i]+"000"
            else:
                valid_addr=label[i]
                if(valid_addr==NULL):
                    return False
                converted+=label[i]
        convert1=converted
        return True
    else:
        return False



def checkF(data):
    global convert1
    arglen=len(data)
    if arglen!=1:
        return False
    truestr="O"
    checkstr=""
    converted=""
    for i in range(0,len(data)):
        if data[i] in type_F[0]:
            checkstr+="O"
          
    if(checkstr==truestr):
        for i in data:
            if i in opcode:
                converted+=opcode[i]+"00000000000"    
        convert1=converted
        return True
    else:
        return False 
                       

for i in range(5):
    inp=input()
    data=inp.split()

    if(checkA(data)==True): 
        print(convert1)
    elif(checkB(data)==True):
        print(convert1)
    elif(checkC(data)==True):
        print(convert1)

    elif(checkD(data)==True):
        print(convert1)

    elif(checkE(data)==True):
        print(convert1)

    elif(checkF(data)==True):
        print(convert1)
    elif(data[0]=="Var"):
        var_form(data[1])
    elif(data[0][-1]==":"):
        label_form(data[0][0:len(data[0])-1])

     
    
