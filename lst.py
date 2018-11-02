import sys
from sys import argv
from subprocess import call
from symbol_table import *
from literal_table import *
from intermediate import *
from register import *

list_temp_add={}

#update symbol with there temporary address
def update_temp_add(st_sym,temp_add):
    tmp1={st_sym:{'temp_add':temp_add}}
    list_temp_add.update(tmp1)

#give line no of given symbol from sym_dict
def get_line_no(val):
        return sym_dict[val]['lineno']
    
    
#gives address for each value by adding with previous value
def add_to_hex(prev,adder):
    k1=int(prev,16)
    op=hex(k1+adder)[2:]
    op=str(op)
    if len(op)==1:
        op="0000000"+op
    if len(op)==2:
        op="000000"+op               
    return op.upper()
                    
#on basis of line no in bss section it gives size on basis of resd,resb or resq
def get_size_in_bss(cnt):
    for i in range(len(lit_dict)):
        if lit_dict["lit#"+str(i)]['lineno']==cnt:
            return lit_dict["lit#"+str(i)]['size']

        
#it gives length of opcode so that this values add in next address to get new address
def cal_length(op):
    n=len(op)//2
    if op.find("(")>-1 or op.find("[")>-1:
        n=n-1
    return n

'''
reg,reg=11+r2+r3
mov eax,ecx
eax=000
ecx=001
rm byte=11
input=11001000
output=c8
'''
def give_modrm1(n):
    k=int(n,2)
    k=hex(k)[2:].upper()
    return k


'''
mov ecx,50
op=B8
val1-001
val2-32(hex of 50)

rm=B8+001=B9
rm=10111000+001

'''
def give_modrm2(op,reg_val):
    op=bin(int(op,16))[2:]
    k1=int(op,2)
    k2=int(reg2[reg_val],2)
    k=hex(k1+k2)[2:]
    k=k.upper()
    return k
    
        
        


def give_rmbyte(op,val1,val2,v1,v2):
    if v1=="R32" and v2=="R32":
        rm=str(11)+reg2[val2]+reg2[val1]
        rm=give_modrm1(rm)
        rm=str(op)+rm+"\t"
     
    
    elif v1=="R32" and v2=="I32" :
        l_val2=lit_dict[val2]['hex_val'].upper()
        rm=give_modrm2(op,val1)
        if len(l_val2)==1 and op=="B8":   #mov for register,immediarte if length=1
            rm=rm+"0"+l_val2+"000000"
        elif len(l_val2)==2 and op=="B8":   #mov for register,immediarte if length=2
            rm=rm+l_val2+"000000"
        elif len(l_val2)==1 and op=="83C0": #add for register,immediarte if length=1
            rm=rm+"0"+l_val2+"\t" 
        elif len(l_val2)==2 and op=="83C0":   #add for register,immediarte if length=2
            rm=rm+l_val2+"\t"
    
    
    elif v1=="M32" and v2=="S32":
        #line=get_line_no(val2)
        my_add=list_temp_add[val2]['temp_add']
        c1=0
        for z in range(len(my_add)):
            if my_add[z]=='0':
                c1=c1+1
            else:
                break
        my_add=my_add[c1:len(my_add)]
        if len(my_add)==1:
            rm=op+"["+"0"+my_add+"000000"+"]"
        elif len(my_add)==2:
            rm=op+"["+my_add+"000000"+"]"
            
                
        
        
    
    elif v1=="M32" and v2=="R32":
         rm=give_modrm2(op,val1)
         
        
    elif v1=="R32" and v2=="N32":
        rm=give_modrm2(op,val1)+"\t"

    elif v1=="L32" and v2=="N32":
        rm="11111111"

    elif v1=="M32" and v2=="N32":
        rm="11111111"

    elif (v1=="pr32" and v2=="N32") or (v1=="sc32" and v2=="N32") or(v1=="pu32" and v2=="N32") :
        rm=op
        
    return rm
            
#fp1=add.asm
#fp2=inter.txt->intermediate code
#fp3=add.lst
#fp4=opcode.txt


def give_opcode(opc,val1,val2,fp4):
   if val1[0]=='R':
       v1="R32"
   elif val1[0]=='l':
       v1="I32"
   elif val1[0]=='d' and val2[0]=='s':
       v1="M32"
       v2="S32"
   elif val1[0]=='d' and val2[0]=='R':
       v1="M32"
       v2="R32"
   if val2[0]=='R':
       v2="R32"
   elif val2[0]=='l':
       v2="I32"
   
   elif val2[0]=='N':
       v2="N32"

   if opc=="call" and val1=="printf":
       v1="pr32"
       v2="N32"

   elif opc=="call" and val1=="scanf":
       v1="sc32"
       v2="N32"

       
   elif opc=="call" and val1=="scanf":
       v1="pu32"
       v2="N32"

   f4=fp4.readline()
   while f4:
       if f4.find(opc)>-1:
           f4=fp4.readline()
           while f4:
               list4=f4.split(" ")
               list4[1]=list4[1].strip("\n")
               list4[2]=list4[2].strip("\n")
               if list4[1]==v1 and list4[2]==v2:
                   op=list4[0]
                   '''
                   val1,val2=original val
                   v1,v2=converted val
                   '''
               
                   op=give_rmbyte(op,val1,val2,v1,v2)
                   fp4.seek(0,0)
                   return op
               
               f4=fp4.readline()
          
       f4=fp4.readline()
       

       
def lst_create(fp1,fp2,fp3,fp4):
    line=[]
    cnt=0
    f1=fp1.readline()
    f2=fp2.readline()
    addr="00000000"
    while f2.find(":")<=-1:
        if f2.find("data")>-1:
            line.extend(["     ",str(cnt),"\t\t\t\t\t",f1])
            line="".join(line)
            fp3.write(line)
            print(line,end="")
            line=[]       
            f1=fp1.readline()
            f2=fp2.readline()
            cnt=cnt+1
            while (f2.find("bss")<=-1) and (f2.find("text")<=-1):
                list2=f2.split(" ")
                op=list2[1].strip("\n")
                if len(op)==2:
                    op=op+"000000"
                elif len(op)==1:
                    op="0"+op+"000000"
                    
                
                    
                if f1.find("db")>-1:
                    
                    line.extend(["     ",str(cnt)," ",addr," ",op.upper(),"\t",f1])
                else:
                    line.extend(["     ",str(cnt)," ",addr," ",op.upper(),"\t\t",f1])
                    
                prev_byte=cal_length(op)
                ad1=addr
                addr=add_to_hex(addr,int(prev_byte)) 
                line="".join(line)
                fp3.write(line)
                print(line,end="")
                if f2.find("sym#")>-1:
                    st_sym=list2[0].strip("\t")
                    update_temp_add(st_sym,ad1)
                    
                    
                
                line=[]

                f1=fp1.readline()
                f2=fp2.readline()
                cnt=cnt+1
                
            if f2.find("bss")>=-1:
                line.extend(["     ",str(cnt)," ", "\t\t\t\t\t",f1])
                line="".join(line)
                ad1=addr
                fp3.write(line)
                
                print(line,end="")
                if f2.find("sym#")>-1:
                    st_sym=list2[0].strip("\t")
                    update_temp_add(st_sym,ad1)
                    
                line=[]       

                addr="00000000"
                f1=fp1.readline()
                f2=fp2.readline()
                cnt=cnt+1
                
                while (f2.find("text")<=-1):
                    list2=f2.split(" ")
                    op=list2[1].strip("\n") 
                    si=get_size_in_bss(cnt)
                    op=int(op)*int(si)
                    op=add_to_hex("00000000",op)
                    op="<res "+op+">"
                    if len(op)==2:
                        op=op="<res "+op+">"
                        

                    line.extend(["     ",str(cnt)," ",addr," ",op,"\t\t",f1])
                    prev_byte=cal_length(op)
                    ad1=addr
                    addr=add_to_hex(addr,int(prev_byte)) 
                    line="".join(line)
                    fp3.write(line)
                    print(line,end="")
                    if f2.find("sym#")>-1:
                        st_sym=list2[0].strip("\t")
                        update_temp_add(st_sym,ad1)
                
                    line=[]
                    
                    f1=fp1.readline()
                    f2=fp2.readline()
                    cnt=cnt+1

        line.extend(["     ",str(cnt)," ","\t\t\t\t\t",f1])
        line="".join(line)
        fp3.write(line)
        print(line,end="")
        line=[]       
            
                    
        f1=fp1.readline()
        f2=fp2.readline()
        cnt=cnt+1

    addr="00000000"
    while f2:
        
        list1=f2.split(" ")
        if f2.find(":")>-1:
            start=list1[0].find(":")
            opc=list1[0][start+1:].strip("\t")
        else:
            
            opc=list1[0].strip("\t")
            
        list2=list1[1].split(",")
        
        if len(list2)>1:
            val1=list2[0]
            val2=list2[1].strip("\n")
        else:
            val1=list2[0].strip("\n")
            if val1.find("dword")>-1:
                 start=f2.find("[")
                 end=f2.find("]")
                 val2=f2[start+1:end]
                 
            else:
                val2="NULL"
                
            
        
        op=give_opcode(opc,val1,val2,fp4)
     
        line.extend(["     ",str(cnt)," ",addr," ",op,"\t\t",f1])
        prev_byte=cal_length(op)
        addr=add_to_hex(addr,int(prev_byte)) 
        line="".join(line)
        fp3.write(line)
        print(line,end="")
        line=[]       
            
            
            
            
        f1=fp1.readline()
        f2=fp2.readline()
        cnt=cnt+1
        

        
if __name__=="__main__":
   fname1=sys.argv[1]
   call(["python3","intermediate.py",fname1])
   create_sym_table(fname1) #gives me symbol table(sym_dict)
   create_literal_table(fname1) #gives me literal table (lit_dict)
   
   fp1=open(fname1,"r")  #open asm file
   fp2=open("add.i","r") #open intermedate code file

   
   #make add.asm->add.lst
   dot=fname1.find(".") 
   fname2=fname1[:dot+1]+"lst"
   fp3=open(fname2,"w+")
   fp4=open("opcode.txt","r") #opcode

   lst_create(fp1,fp2,fp3,fp4)
   
   
