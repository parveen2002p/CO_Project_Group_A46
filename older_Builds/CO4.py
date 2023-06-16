
from distutils.log import error


opcode={'add':'10000','sub':'10001','mov':'10010','ld':'10100','st':'10101','mul':'10110','div':'10111','rs':'11000','ls':'11001','xor':'11010','or':'11011','and':'11100','not':'11101','cmp':'11110','jmp':'11111','jlt':'01100','jgt':'01101','je':'01111','hlt':'01010'}

reg={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110"}

Flags={"FLAGS":"111"}

counter="00000000"

convert1=""
var={}
label={}
errorflag=0
# hlt last mein ur ek hi and not missing
# empty line
# whitespace in start
# varible only at start
# error typo of name in reg op
# error with line number (print any one)
# error for use of flag in other operations
# interchanged misuse of var & lab
# do we need to print all erors or single error or save text file for error
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


def checkA(data,line_num):
    global errorflag
    global convert1
    # print("IN A")
    arglen=len(data)
    if (arglen!=4):
        # print("Here")
        return False
    checkstr=""
    truestr="ORRR"
    for i in range(0,len(data)):
            if data[i] in type_A[0]:
                checkstr+="O"
            elif data[i] in type_A[2]:
                checkstr+="R"
            elif data[i]=="FLAGS":       # flag error udated
                print(f"Line {line_num}:Misuse of FLAGS Error")
                errorflag=1
                return False
                
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

        

def checkB(data,line_num):
    global errorflag
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
        elif data[i]=="FLAGS":       # flag error udated
            print(f"Line {line_num}:Misuse of FLAGS Error")
            errorflag=1
            return False

    if(checkstr==truestr):
        converted=""
        for i in data:
            if i in opcode:
                converted+=opcode[i]
            elif i in reg:
                converted+=reg[i]
            elif (i[0]=="$"):
                # check for immediate >=0 and <=255
                imm=str(bin(int(i[1:len(i)])).replace("0b",""))  
                if (len(imm)>8):
                    print(f"Line {line_num}:Immediate out of range")
                    errorflag=1
                    return False 
                while(len(imm)<8):
                    imm="0"+imm
                converted+=imm
        convert1=converted
        return True
    else:
        return False 
    

def checkC(data,line_num):
    global errorflag
    global convert1
    truestr=""
    if(len(data)!=3):          
        return False
    if(data[-1][0]=="R"):
        truestr="ORR"
    elif(data[-1]=="FLAGS"):
        truestr="ORF"
    checkstr=""
    for i in range(0,len(data)):
        if data[i] in type_C[0]:
            checkstr+="O"
        elif data[i] in type_C[1]:
            checkstr+="R" 
        elif data[i] in Flags:
            checkstr+="F"                            # what if flag is in between we have to report that as misuse of FLAG not as syntax error
        elif data[i]=="FLAGS" and i<(len(data)-1):       # flag error udated
            print(f"Line {line_num}:Misuse of FLAGS Error")
            errorflag=1
            return False
        
    if(checkstr==truestr):
        converted=""
        for i in data:
            if i in opcode:
                converted+=str(int(opcode[i])+1)+"00000"
            elif i in reg:
                converted+=reg[i]
            elif i in Flags:
                converted+=Flags[i]
        convert1=converted
        return True
    else:
        return False 
    

def checkD(data,line_num):
    global errorflag
    global var
    global convert1
    arglen=len(data)
    if arglen!=3:
        return False
    
    truestr="ORM"         
    checkstr=""
    for i in range(0,len(data)):
        if data[i] in type_D[0]:
            checkstr+="O"
        elif data[i] in type_D[1]:
            checkstr+="R"
        elif data[i]=="FLAGS":       # flag error udated
            print(f"Line{line_num}:Misuse of FLAGS Error")
            errorflag=1
            return False
        else:
            checkstr+="M"
    if(checkstr==truestr):
        converted=""
        valid_var=None
        for i in data:
            if i in opcode:
                converted+=opcode[i]
            elif i in reg:
                converted+=reg[i]
            else:
                try:
                    valid_var=var[i]
                except KeyError:
                    pass
                if(valid_var==None and i in label):
                    print(f"Line {line_num}:Label used in place of variable")
                    errorflag=1
                    return False
                    
                elif(valid_var==None):
                    print(f"Line {line_num}:Undeclared variable used")
                    errorflag=1
                    return False
                converted+=var[i]    
        convert1=converted
        return True
    else:
        return False
    
    
   
        


def checkE(data,line_num):
    global errorflag
    global convert1
    global label
    arglen=len(data)
    if arglen!=2:
        return False
    truestr="OM"
    checkstr=""
    
    for i in range(0,len(data)):    # does order doesnt matter here for adrress and opcode
        if data[i] in type_E[0]:
            checkstr+="O"
        else:
            checkstr+="M"
        
    
    if(checkstr==truestr):
        converted=""
        valid_addr=None
        for i in data:
            if i in opcode:
                converted+=opcode[i]+"000"
            else:
                try:
                    valid_addr=label[i]
                except KeyError:
                    pass

                if(valid_addr==None and i in var):
                    print(f"Line {line_num}:Variable used in place of label")
                    errorflag=1
                    return False
                elif(valid_addr==None):
                    print(f"Line {line_num}:Undeclared label used")
                    errorflag=1
                    return False
                converted+=label[i]
        convert1=converted
        return True
    else:
        return False



def checkF(data,line_num):
    global errorflag
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
                       

flagvar=0
f = open("test.txt","r")
list1 = f.readlines()
for i in list1:            
    data=i.split()               
    try:
        if(data[0][-1]==":" and len(data)==1):
            label_form(data[0][0:len(data[0])-1])
    except:
        pass
    


data=list1[-1].split()  
if data[0]!="hlt" and len(data)>1:        
    print("NO hlt present at end or hlt syntax is not appropriate")

print(list1)
# print((list1[4].split())[2])
for i in range(len(list1)):

    data=list1[i].split()
    if(list1[i]=='\n'):     #change this condition for list[i]=="" after putting stdin command
        pass
    
    elif(checkA(data,i+1)==True): 
        print(convert1)
        flagvar=1

    elif(checkB(data,i+1)==True):
        print(convert1)
        flagvar=1
    elif(checkC(data,i+1)==True):
        print(convert1)
        flagvar=1

    elif(checkD(data,i+1)==True):
        print(convert1)
        flagvar=1

    elif(checkE(data,i+1)==True):
        print(convert1)
        flagvar=1

    elif(checkF(data,i+1)==True and not(i<len(list1)-1)):
        print(convert1)
        flagvar=1

    elif(data[0]=="Var" and len(data)==2):
        # can it handle redeclaration of variable & non ususal variable names
        var_form(data[1])

    elif(data[0][-1]==":" and len(data)==1):
        pass
    
    elif(data[0][-1]==":" and len(data)>1):
        flagvar=1
        print(f"Line {i+1}:General Syntax Error")
                                                    #Need to handle error here if syntax is wrong also labels are formed in starting (make it just to report error)   Also can it handle redeclaration
                                                  #had to ask TA is var declaration after label is correct
    elif(data[0]=="Var" and flagvar==1):         
        print(f"Line {i+1}:Cannot declare variable")

    elif(data[0]=="hlt" and i<(len(list1)-1)):
        if len(data)>1:
            print(f"Line {i+1}:General Syntax Error")
        else:
            print("Hlt detected in between ")
    elif(errorflag!=1):
        print(f"Line {i+1}:General Syntax Error")
        errorflag=0
f.close()
# ask ta for label declaration semantics