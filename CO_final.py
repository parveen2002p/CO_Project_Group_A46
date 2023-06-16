
import fileinput

# opcode={'add':'10000','sub':'10001','mov':'10010','ld':'10100','st':'10101','mul':'10110',
# 'div':'10111','rs':'11000','ls':'11001','xor':'11010','or':'11011','and':'11100','not':'11101',
# 'cmp':'11110','jmp':'11111','jlt':'01100','jgt':'01101','je':'01111'}

hlt={"hlt":"01010"}
reg={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110"}

opcode_A={"add":"10000","sub":"10001","mul":"10110","xor":"11010","or":"11011","and":"11100",}
opcode_B={"mov":"10010","ls":"11001",'rs':'11000'}
opcode_C={"mov":"10010","div":"10111","not":"11101","cmp":"11110",}
opcode_D={"ld":"10100","st":"10101"}
opcode_E={"jmp":"11111","jlt":"01100","jgt":"01101","je":"01111"}





Flags={"FLAGS":"111"}

counter="00000000"
# mov r1 256
# check b or d
# check_a={mov,mov,ls,}
# check_d={ld,st}

convert1=""
var={}
label={}
errorflag=0
finalflag=0
immediateflag=0
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




type_A=[opcode_A,reg,reg,reg]
type_B=[opcode_B,reg]
type_C=[opcode_C,reg,reg]
type_D=[opcode_D,reg]
type_E=[opcode_E]
type_F=[hlt]


def checkA(data,line_num):
    global finalflag
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
                finalflag=1
                errorflag=1
                return False
                
    if checkstr==truestr:
        converted=""
        for i in data:
            if i in opcode_A:
                converted+=opcode_A[i]+"00"
            elif i in reg:
                converted+=reg[i]
        
        convert1=converted
        return True
    else:
        return False 

        

def checkB(data,line_num):
    global finalflag
    global errorflag
    global immediateflag
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
        elif (data[i][0] =="$" and data[i][1:len(data[i])].isdigit()):
            checkstr+="I"
        elif data[i]=="FLAGS":       # flag error udated
            print(f"Line {line_num}:Misuse of FLAGS Error")
            finalflag=1
            errorflag=1
            return False

    if(checkstr==truestr):
        converted=""
        for i in data:
            if i in opcode_B:
                converted+=opcode_B[i]
            elif i in reg:
                converted+=reg[i]
            elif (i[0]=="$"):
                # check for immediate >=0 and <=255
                imm=str(bin(int(i[1:len(i)])).replace("0b",""))  
                if (len(imm)>8):
                    print(f"Line {line_num}:Immediate out of range")
                    finalflag=1
                    immediateflag=1
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
    global finalflag
    global errorflag
    global convert1
    truestr="1"                             #truestr=1 so that checkstr!=truestr if truestr not updated in if elif statement
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
            finalflag=1
            errorflag=1
            return False
        
    if(checkstr==truestr):
        converted=""
        for i in data:
            if i in opcode_C:
                converted+=str(int(opcode_C[i])+1)+"00000"
            elif i in reg:
                converted+=reg[i]
            elif i in Flags:
                converted+=Flags[i]
        convert1=converted
        return True
    else:
        return False 
    

def checkD(data,line_num):
    global finalflag
    global errorflag
    global immediateflag
    global var
    global convert1
    arglen=len(data)
    if (arglen!=3 or immediateflag==1):
        
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
            finalflag=1
            errorflag=1
            return False
        else:
            checkstr+="M"
    if(checkstr==truestr):
        converted=""
        valid_var=None
        for i in data:
            if i in opcode_D:
                converted+=opcode_D[i]
            elif i in reg:
                converted+=reg[i]
            else:
                try:
                    valid_var=var[i]
                except KeyError:
                    pass
                if(valid_var==None and i in label):
                    print(f"Line {line_num}:Label used in place of variable")
                    finalflag=1
                    errorflag=1
                    return False
                    
                elif(valid_var==None):
                    print(f"Line {line_num}:Undeclared variable used")
                    finalflag=1
                    errorflag=1
                    return False
                converted+=var[i]    
        convert1=converted
        return True
    else:
        return False
    
    
   
        


def checkE(data,line_num):
    
    global finalflag
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
            if i in opcode_E:
                converted+=opcode_E[i]+"000"
            else:
                try:
                    valid_addr=label[i]
                except KeyError:
                    pass

                if(valid_addr==None and i in var):
                    print(f"Line {line_num}:Variable used in place of label")
                    finalflag=1
                    errorflag=1
                    return False
                elif(valid_addr==None):
                    print(f"Line {line_num}:Undeclared label used")
                    finalflag=1
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
    if (arglen!=1):
        return False
    truestr="O"
    checkstr=""
    converted=""
    for i in range(0,len(data)):
        if data[i] in type_F[0]:
            checkstr+="O"
          
    if(checkstr==truestr):
        for i in data:
            if i in hlt:
                converted+=hlt[i]+"00000000000"    
        convert1=converted
        return True
    else:
        return False 
                       

flagvar=0
finallist=[]
# f = open("stdin.txt","r")
# list1 = f.readlines()
# list1=[line.rstrip() for line in list1]
# if(len(list1)>256):
#     print("line limit exceeded")
#     finalflag=1
list1=[]
for line in fileinput.input():
    list1.append(line)
list1=[line.rstrip() for line in list1]
# print(list1)
if(len(list1)>256):
    print("line limit exceeded")
    finalflag=1
for i in list1:            
    doublelabelflag=0
    data=i.split()               
    try: 
        if(data[0][-1]==":"):
            data2=[]
            for k in range(1,len(data)):
                data2.append(data[k])
            # print(data2)
            for j in data2:
                if (":" in j):
                    # print(": in data")
                    doublelabelflag=1
                    break
            # print(doublelabelflag)    
            if(doublelabelflag!=1 and len(data)>1):    
                # print("Form label")
                label_form(data[0][0:len(data[0])-1])
    except:
        # print("pass")
        pass
    

data=list1[-1].split()  
if data[0]=="hlt" and len(data)>1:        
    print("NO hlt present at end or hlt syntax is not appropriate")
    finalflag=1
elif data[0]!="hlt":
    print("NO hlt present at end or hlt syntax is not appropriate")
    finalflag=1


# print(list1)

# print((list1[4].split())[2])
data=[]
for i in range(len(list1)):
    data=list1[i].split()
    
    # print(i)
    
    
    if(list1[i]==''):     #change this condition for list[i]=="" after putting stdin command
        pass
    
    elif(data[0][-1]==":"):
        doublelabelflag=0             
        try: 
            if(data[0][-1]==":"):
                data2=[]
                for j in range(1,len(data)):
                    data2.append(data[j])
                # print(data2)
                for k in data2:
                    if (":" in k):
                        doublelabelflag=1
                        break
                    
                if(doublelabelflag==1):    
                    print(f"Line {i+1}:General Syntax Error")
                    finalflag=1
                    # print(379)
            if(len(data)>1):
                data=data[1:len(data)]
        
        except:
            # print("pass")
            pass

    
    
    if(checkA(data,i+1)==True and errorflag!=1): 
        
        finallist.append(convert1)
        flagvar=1

    elif(checkB(data,i+1)==True and errorflag!=1):
        
        finallist.append(convert1)
        flagvar=1
    elif(checkC(data,i+1)==True and errorflag!=1):
        
        finallist.append(convert1)
        flagvar=1

    elif(checkD(data,i+1)==True and errorflag!=1):
        
        finallist.append(convert1)
        flagvar=1

    elif(checkE(data,i+1)==True and errorflag!=1):
        
        finallist.append(convert1)
        flagvar=1

    elif(checkF(data,i+1)==True and not(i<len(list1)-1)):
        
        finallist.append(convert1)
        flagvar=1
    
    
    elif(data[0]=="var" and flagvar==1):         
        print(f"Line {i+1}:Cannot declare variable")
        finalflag=1
    
    elif(data[0]=="var" and len(data)==2):
        
        # can it handle redeclaration of variable & non ususal variable names
        var_form(data[1])
        
    # elif(data[0]=="Var" and len(data)!=2):                          #condiition added to check valid var statement
        
    #     print(f"Line {i+1}:General Syntax Error")
    
    
    elif(data[0][-1]==":" and len(data)>1):
        flagvar=1
        print(f"Line {i+1}:General Syntax Error")
        finalflag=1
        
                                                    #Need to handle error here if syntax is wrong also labels are formed in starting (make it just to report error)   Also can it handle redeclaration
                                                  #had to ask TA is var declaration after label is correct
    

    elif(data[0]=="hlt" and i<(len(list1)-1)):
        if len(data)>1:
            print(f"Line {i+1}:General Syntax Error")
            finalflag=1
            
        else:
            print(f"Line {i+1}:Hlt detected in between ")
            finalflag=1
    elif(errorflag!=1):
        print(f"Line {i+1}:General Syntax Error")
        finalflag=1
        
    errorflag=0
    immediateflag=0
    

f1=open("stdout.txt","w")
f1.close()
if(finalflag!=1):
    f1=open("stdout.txt","w")
    for i in finallist:
        f1.write(i+"\n")
    f1.close() 

import sys
 
 
def print_to_stdout(*a):
    print(*a, file = sys.stdout)
 

if(finalflag!=1):
    
    for i in finallist:
        print_to_stdout(i)



