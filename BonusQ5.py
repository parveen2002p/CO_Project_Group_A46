# from atexit import register
from cmath import log


import math
from secrets import choice
from textwrap import fill
from typing import final


def initialFunction():
    memmory=input("Enter the spaace in memmory ")
    typeofmemmory=input("Enter how memmory is adressed ")

    instructionlength=int(input("Enter the length of instrution "))
    registerlength=int(input("Enter the length of register "))
    if(typeofmemmory=="Bit"):
        pins = 1
    elif (typeofmemmory=="Nibble"):
        pins = 2
    elif (typeofmemmory=="Byte"):
        pins = 3
    
    
    if(memmory[-1]=="B"):
        if(memmory[-2:-1]=="E"):
            memmory=int(memmory[0:len(memmory)-3])*1024*1024*1024*1024*1024*1024*8
            bits=int(math.log(memmory,2))-pins
            print(bits)
        elif(memmory[-2:-1]=="P"):
            memmory=int(memmory[0:len(memmory)-3])*1024*1024*1024*1024*1024*8
            bits=int(math.log(memmory,2))-pins
            print(bits)
        elif(memmory[-2:-1]=="T"):
            memmory=int(memmory[0:len(memmory)-3])*1024*1024*1024*1024*8
            bits=int(math.log(memmory,2))-pins
            print(bits)
        elif(memmory[-2:-1]=="G"):
            memmory=int(memmory[0:len(memmory)-3])*1024*1024*1024*8
            bits=int(math.log(memmory,2))-pins
            print(bits)
        elif(memmory[-2:-1]=="M"):
            memmory=int(memmory[0:len(memmory)-3])*1024*1024*8
            bits=int(math.log(memmory,2))-pins
            print(bits)
        elif(memmory[-2:-1]=="K"):
            memmory=int(memmory[0:len(memmory)-3])*1024*8
            bits=int(math.log(memmory,2))-pins
            print(bits)
        elif(memmory[-2:-1]==" "):
            memmory=int(memmory[0:len(memmory)-2])*8
            bits=int(math.log(memmory,2))-pins
            print(bits)
    
    elif(memmory[-1]=="b"):
        if(memmory[-2:-1]=="E"):
            memmory=int(memmory[0:len(memmory)-3])*1024*1024*1024*1024*1024*1024
            bits=int(math.log(memmory,2))-pins
            print(bits)
        elif(memmory[-2:-1]=="P"):
            memmory=int(memmory[0:len(memmory)-3])*1024*1024*1024*1024*1024
            bits=int(math.log(memmory,2))-pins
            print(bits)
        elif(memmory[-2:-1]=="T"):
            memmory=int(memmory[0:len(memmory)-3])*1024*1024*1024*1024
            bits=int(math.log(memmory,2))-pins
            print(bits)
        elif(memmory[-2:-1]=="G"):
            memmory=int(memmory[0:len(memmory)-3])*1024*1024*1024
            bits=int(math.log(memmory,2))-pins
            print(bits)
        elif(memmory[-2:-1]=="M"):
            memmory=int(memmory[0:len(memmory)-3])*1024*1024
            bits=int(math.log(memmory,2))-pins
            print(bits)
        elif(memmory[-2:-1]=="K"):
            memmory=int(memmory[0:len(memmory)-3])*1024
            bits=int(math.log(memmory,2))-pins
            print(bits)
        elif(memmory[-2:-1]==" "):
            memmory=int(memmory[0:len(memmory)-2])
            bits=int(math.log(memmory,2))-pins
            print(bits)

    oplen = instructionlength - ( registerlength + bits)
    filler = instructionlength - ((2*registerlength) + oplen)
    maxinst=2**oplen
    maxreg=2**registerlength
    print("OP ",oplen)
    print("filler ",filler)
    print("Max instructin are ",maxinst)
    print("Max reg ",maxreg)

# Type 1
def Type1():
    memmory=input("Enter the spaace in memmory ")
    typeofmemmory = input("Enter the adressable mem ")
    cpubit=int(input("Enter the bit of CPU "))
    typeofmemmory2 = input("Enter the adressable mem enchanced ")
    if(typeofmemmory=="Bit"):
        pins = 1
    elif (typeofmemmory=="Nibble"):
        pins = 2
    elif (typeofmemmory=="Byte"):
        pins = 3
    elif (typeofmemmory=="Word"):
        pins = int(math.log(cpubit,2))
    
    if(typeofmemmory2=="Bit"):
        pins1 = 1
    elif (typeofmemmory2=="Nibble"):
        pins1 = 2
    elif (typeofmemmory2=="Byte"):
        pins1 = 3
    elif (typeofmemmory2=="Word"):
        pins1 = int(math.log(cpubit,2))
    
    finalpin=pins-pins1
    print("Finalpins: ",finalpin)



# Type 2
def Type2():
    cpubit=int(input("Enter the bit of CPU "))
    adresspins=int(input("Enter the address pins "))
    typeofmemmory = input("Enter the adressable mem ")

    if(typeofmemmory=="Bit"):
        finalmem = (2**adresspins) * (2**1)
    elif (typeofmemmory=="Nibble"):
        finalmem = (2**adresspins) * (2**4)
    elif (typeofmemmory=="Byte"):
        finalmem = (2**adresspins) * (2**8)
    elif (typeofmemmory=="Word"):
        finalmem = (2**adresspins) * cpubit
    finalmem=finalmem//(2**3)
    print("Main Memory Size (in bytes): ",finalmem)



exit = 1
while exit:
    print("1.Initial Type(ISA Related)")
    print("2. Type 1")
    print("3. Type 2")
    print("4. Exit")
    choice=int(input("Enter your choice: "))
    if choice==1 :
        initialFunction()
    elif choice==2 :
        Type1()
    elif choice==3:
        Type2()
    elif choice==4:
        break
        
