import fileinput
# hlt={"hlt":"01010"}


reg={"000":"R0","001":"R1","010":"R2","011":"R3","100":"R4","101":"R5","110":"R6"}
# reg={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110"}

# opcode_A={"add":"10000","sub":"10001","mul":"10110","xor":"11010","or":"11011","and":"11100",}
# opcode_B={"mov":"10010","ls":"11001",'rs':'11000'}
# opcode_C={"mov":"10011","div":"10111","not":"11101","cmp":"11110",}
# opcode_D={"ld":"10100","st":"10101"}
# opcode_E={"jmp":"11111","jlt":"01100","jgt":"01101","je":"01111"}
R0=R1=R2=R3=R4=R5=R6=0

V=0   # overflow & underflag same flag 
G=0
L=0
E=0
halt = 0
PC = 0

var ={}

def updatereg(a,regname):
    global R0,R1,R2,R3,R4,R5,R6
    globals()[(regname)]=a



def findReg(a):
    global R0,R1,R2,R3,R4,R5,R6
    if(reg[a]=="R0"):
        return "R0"
    elif(reg[a]=="R1"):
        return "R1"
    elif(reg[a]=="R2"):
        return "R2"
    elif(reg[a]=="R3"):
        return "R3"
    elif(reg[a]=="R4"):
        return "R4"
    elif(reg[a]=="R5"):
        return "R5"
    elif(reg[a]=="R6"):
        return "R6"    
    


# op code  r1 r2 r3 
def Add(n):
    global PC
    global V,L,G,E
    b = globals()[findReg(n[10:13])]
    c = globals()[findReg(n[13:16])]
    # print(type(b))
    temp=b+c
    if(temp>65536):
        V=1
        temp=str(bin(temp).replace("0b",""))
        #"11 1010101010101010"
        lenstr=len(temp)
        temp = temp[(lenstr -16):(lenstr)]
        temp = int(temp,2)
    updatereg(temp , findReg(n[7:10])) 
    G=0
    L=0
    E=0
    PC+=1

def Sub(n):
    global PC
    global V,L,G,E
    b = globals()[findReg(n[10:13])]
    c = globals()[findReg(n[13:16])]
    temp=b-c
    
    if (temp<0):
        V=1
        updatereg(0 , findReg(n[7:10]))
        return 0
    if(temp>65536):
        V=1
        temp=str(bin(temp).replace("0b",""))
        #"11 1010101010101010"
        lenstr=len(temp)
        temp = temp[(lenstr -16):(lenstr)]
        temp=int(temp,2)
        updatereg(temp , findReg(n[7:10]))
        return 0
    updatereg(temp , findReg(n[7:10]))
    G=0
    L=0
    E=0
    PC+=1
   

def Mul(n):
    global PC
    global V,L,G,E
    b = globals()[findReg(n[10:13])]
    c = globals()[findReg(n[13:16])]
    temp=b*c
    if(temp>65536):
        V=1
        temp=str(bin(temp).replace("0b",""))
        #"11 1010101010101010"
        lenstr=len(temp)
        temp = temp[(lenstr -16):(lenstr)]
        temp= int(temp,2)
    updatereg(temp , findReg(n[7:10]))
    G=0
    L=0
    E=0
    PC+=1

def Mov(n):  # need to check how many bits to copy
    global PC
    global V,L,G,E
    updatereg(int(n[8:16],2),findReg(n[5:8]))
    G=0
    L=0
    E=0
    PC+=1

def movreg(n):
    global PC
    global V,L,G,E
    updatereg(globals()[findReg(n[13:16])],globals()[findReg(n[10:13])])
    G,L,E=0,0,0
    PC+=1

def Div(n):
    global PC
    global V,L,G,E
    global R0,R1
    b = globals()[findReg(n[10:13])]
    c = globals()[findReg(n[13:16])]
    R0=b//c
    R1=b%c
    G,L,E=0,0,0
    PC+=1

def ls(n):
    global PC
    global V,L,G,E
    regname=findReg(n[5:8])
    b=int(n[8:16],2)
    globals()[regname] = globals()[regname] << b
    G,L,E=0,0,0
    PC+=1
    

def rs(n):
    global PC
    global V,L,G,E
    regname=findReg(n[5:8])
    b=int(n[8:16],2)
    globals()[regname] = globals()[regname] >> b
    G,L,E=0,0,0
    PC+=1

def And(n):
    global PC
    global V,L,G,E
    a = globals()[findReg(n[7:10])]
    b = globals()[findReg(n[10:13])]
    temp = a & b
    globals()[findReg(n[13:16])]=temp
    G,L,E=0,0,0
    PC+=1
    

def Or(n):
    global PC
    global V,L,G,E
    a = globals()[findReg(n[7:10])]
    b = globals()[findReg(n[10:13])]
    temp = a | b
    globals()[findReg(n[13:16])]=temp
    G,L,E=0,0,0
    PC+=1

def Not(n):
    global PC
    global V,L,G,E
    a = globals()[findReg(n[10:13])]
    temp = ~a
    globals()[findReg(n[13:16])]=temp
    G,L,E=0,0,0
    PC+=1

def Xor(n):
    global PC
    global V,L,G,E
    a = globals()[findReg(n[7:10])]
    b = globals()[findReg(n[10:13])]
    temp = a ^ b
    globals()[findReg(n[13:16])]=temp
    G,L,E=0,0,0
    PC+=1
    
    

def Compare(n):   # need to reset flag zero after execution of every normal instruction
    global PC
    global V,L,G,E
    a = globals()[findReg(n[10:13])]
    b = globals()[findReg(n[13:16])]
    global G,L,E
    if a> b:
        G = 1
    elif a< b:
        L = 1
    elif a == b:
        E = 1
    PC+=1

def Load(n):
    global PC
    global V,L,G,E
    regname=findReg(n[5:8])
    b = n[8:16]
    globals()[regname] = int(var[b],2)   # var value is in binary
    G,L,E=0,0,0
    PC+=1

def Store(n):
    global PC
    global V,L,G,E
    regname=findReg(n[5:8])
    b = n[8:16]
    temp = globals()[regname]
    var[b]= str(bin(temp).replace("0b",""))
    G,L,E=0,0,0
    PC+=1

def Jmp(n):   # LABEL MAY BE STR VALUE OF bin TYPE
    global PC
    global V,L,G,E
    global PC
    label = n[8:16]
    PC = int(label,2)
    G,L,E=0,0,0

def Jlt(n):
    global PC
    global V,L,G,E
    global PC,L
    label = n[8:16]
    if(L==1):
        PC = int(label,2)
    G,L,E=0,0,0

def Jgt(n):
    global PC
    global V,L,G,E
    global PC,G
    label = n[8:16]
    if(G==1):
        PC = int(label,2)
    G,L,E=0,0,0

def Je(n):
    global PC
    global V,L,G,E
    global PC,E
    label = n[8:16]
    if(E==1):
        PC = int(label,2)
    G,L,E=0,0,0

# Floating point functions  #2.5
def flo(n):
    n=str(n)
    floatlist=n.split(".")
    bin1=str(bin(int(floatlist[0])).replace("0b",""))
    dec="."+floatlist[1]
    dec=float(dec)
    convert=""
    count= 5 - (len(bin1)-1)
    exponent=count-2
    if(count<0 or exponent>3):
        print("overflow")
    while(dec!=0):
        # print("Count=",count)
        dec=float(dec*2)
        print(dec)
        flist=str(dec).split(".")
        integer=flist[0]
        dec=float("."+(flist[1]))
        convert+=integer
        count-=1
        if(count==0):
            break
        


op={"10000":Add,"10001":Sub,"10010":Mov,"10011":movreg,"10100":Load,"10101":Store,"10110":Mul,
"10111":Div,"11000":rs,"11001":ls,"11010":Xor,
"11011":Or,"11100":And,"11101":Not,"11110":Compare,"11111":Jmp,"01100":Jlt,"01101":Jgt,"01111":Je}



datalist=[]
def engine(pc):
    global PC,halt,datalist
    
    n = datalist[pc]
    if(n[0:5]=="01010"):
        halt=1
        return halt
    op[n[0:5]](n)
    printall(pc)
    return halt
    

def printall(pc):
    global R0,R1,R2,R3,R4,R5,R6
    global V,L,G,E
    print("NEW")
    pc=str(bin(pc).replace("0b",""))
    while(len(pc)<8):
        pc="0"+pc
    print(pc," ")

    r0=str(bin(R0).replace("0b",""))
    while(len(r0)<16):
        r0="0"+r0
    print("R0=",R0)
    print(r0," ")
    

    r1=str(bin(R1).replace("0b",""))
    while(len(r1)<16):
        r1="0"+r1
    print("R1=",R1)
    print(r1," ")

    r2=str(bin(R2).replace("0b",""))
    while(len(r2)<16):
        r2="0"+r2
    print("R2=",R2)
    print(r2," ")
    
    r3=str(bin(R3).replace("0b",""))
    while(len(r3)<16):
        r3="0"+r3
    print("R3=",R3)
    print(r3," ")

    r4=str(bin(R4).replace("0b",""))
    while(len(r4)<16):
        r4="0"+r4
    print("R4=",R4)
    print(r4," ")

    r5=str(bin(R5).replace("0b",""))
    while(len(r5)<16):
        r5="0"+r5
    print("R5=",R5)
    print(r5," ")

    r6=str(bin(R6).replace("0b",""))
    while(len(r6)<16):
        r6="0"+r6
    print("R6=",R6)
    print(r6," ")
    
    flgstr="0"*12
    flgstr=flgstr+ str(V) +str(L) +str(G) +str(E)
    print(flgstr)
    
# also need to print whole memory at end comprising 256 lines 

# run code

for line in fileinput.input():
    datalist.append(line)

for i in datalist:
    if(i[0:5]=="10100" or i[0:5]=="10101"):
        varname = i[8:16]
        var[varname]="0" 

while(not halt):
    halt = engine(PC)





"""
instead 

function = op[n[0:5]]
globals()[function()]   No return No arguments  make global scope ins then slice it inside function (all may take complete ins )

op[n[0:5]](inst)


"""


    
    


    