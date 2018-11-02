
import sys
from symbol_table import *
from literal_table import *
from error_table import *
from register import *
reg={'eax':'R1','ecx':'R2','edx':'R3','ebx':'R4','esp':'R5','ebp':'R6','esi':'R7','edi':'R8'}

my_sym=['mov','add','sub','mul','inc','dec','push','pop','call','and','or','xor','jmp','jz','jnz','jnc','je','jng','jge','loop','cmp','puts','printf','scanf','extern','main']

memory=['dword','qword']

jmp_statement=['jmp','jz','jnc','je','jge','loop']


#return symbol no as output if symbol name is input
def search_sym(sym_dict,var):
    for i in range(len(sym_dict)):
        if sym_dict["sym#"+str(i)]['variable']==var:
           return "sym#"+str(i)

#return literal no as output if literal values is input
def search_lit(lit_dict,var,cnt):
    for i in range(len(lit_dict)):
        if lit_dict["lit#"+str(i)]['variable']==var and lit_dict["lit#"+str(i)]['lineno']==cnt:
           return "lit#"+str(i)

#from sym_dict collect symbol name in sym_arr
def collect_sym_in_array(sym_dict,sym_arr):
    for i in range(len(sym_dict)):
        sym_arr.append(sym_dict["sym#"+str(i)]['variable'])

#from lit_dict collect literal values in lit_arr
def collect_lit_in_array(lit_dict,lit_arr):
    for i in range(len(lit_dict)):
        lit_arr.append(lit_dict["lit#"+str(i)]['variable'])

#check that given opcode is correct or or not
def check_correctness(set1,symm):
    if symm not in set1:
        return -1

#input literal no gives it's hex values from lit_dict
def search_lit_hex(lit_dict,var,cnt):
    for i in range(len(lit_dict)):
        if lit_dict["lit#"+str(i)]['variable']==var and lit_dict["lit#"+str(i)]['lineno']==cnt:
           return lit_dict["lit#"+str(i)]['hex_val']

        
def create_intermediate(fp1,fp2):
    flag=0
    list1=fp1.readline()
    cnt=0
    while list1.find("main:")<=-1:
            
        arr=[]
        end=list1.find("\n")
        mylst=list1
       
        if list1.find("extern")>-1 or list1.find("global")>-1 or  list1.find("section")>-1:
            arr.extend([list1.strip("\n")])
            
        else:
            list1=list1.split(' ')
            list1[0]=list1[0].strip("\t")
            if list1[0] in sym_arr:
                list1[0]=search_sym(sym_dict,list1[0])
                add1=sym_dict[list1[0]]['address']
                arr.extend(["\t",list1[0]," "])

            if list1[1].find("dd")>-1:
                start=mylst.find("dd")
                val=mylst[start+3:end].strip("\n")
                val=val.strip("\t")
                val=search_lit_hex(lit_dict,val,cnt)
                arr.extend([val])

            elif list1[1].find("db")>-1:
                start=mylst.find("db")
                val=mylst.find('"')
                val=mylst[val+1:]
                val1=val.find('"')
                val=val[:val1]
                val=search_lit_hex(lit_dict,val,cnt)
                arr.extend([val])

            elif list1[1].find("resb")>-1 or  list1[1].find("resd")>-1 or  list1[1].find("resq")>-1:
                rb=list1[1].find("resb")
                rd=list1[1].find("resd")
                rq=list1[1].find("resq")
                if rb>-1:
                    head="resb"
                elif rd>-1:
                    head="resd"
                elif rq>-1:
                    head="resq"
                                 
                start=mylst.find(head)
                val=mylst[start+5:end].strip("\n")
                val=val.strip("\t")
                val=search_lit_hex(lit_dict,val,cnt)
                arr.extend([val])

                
              
               
            
        arr=''.join(arr)
        fp2.write(arr+"\n")
        #print(arr)

        list1=fp1.readline()
        cnt=cnt+1
    
    while list1:
        arr=[]
        list1=list1.split(' ') #split line by space
        if list1[0].find(':')>-1:  
            index=list1[0].find(':')
            list2=list1[0][:index] #list2 contain label
            list2=search_sym(sym_dict,list2)
            arr.extend([list2,":","\t"])
            list2=list1[0].split('\t')
            status=check_correctness(my_sym,list2[1])
            if status==-1:
                print("%s :ln %d : error: '%s' %s"%(fname,cnt,list2[1],error_dict['opcode']))
                return -1
            list4=list2[1]
            arr.extend([list2[1]," "])
           
        else:
            list1[0]=list1[0].strip("\t")
            status=check_correctness(my_sym,list1[0])
            if status==-1:
                print("%s :ln %d : error: '%s' %s"%(fname,cnt,list1[0],error_dict['opcode']))
                return -1
            list4=list1[0]
            arr.extend(["\t",list1[0]," "])
        
        list2=list1[1].split(',')
            
        for j in range(len(list2)):
            
            list2[j]=list2[j].strip('\n')
            

            #check the symbol comes with jmp statements is define or not
            if list4 in jmp_statement:
                status=check_correctness(sym_arr,list2[j])
                if status==-1:
                    print("%s :ln %d : error: '%s' %s"%(fname,cnt,list2[j],error_dict['undefined']))
                    flag=-1
                    return -1

            #check wheather given values is register or not
            if list2[j] in reg:
                list2[j]=reg[list2[j]]
                arr.extend([list2[j],","])
                
            #check wheather value is symbol or not
            elif list2[j] in sym_arr:
                list2[j]=search_sym(sym_dict,list2[j])
                arr.extend([list2[j],","])
            
            #check wheather values is literal or not
            elif list2[j] in lit_arr:
                list2[j]=search_lit(lit_dict,list2[j],cnt)
                arr.extend([list2[j],","])

                
            elif list2[j].find("dword")>-1:
                start=list2[j].find("[")
                end=list2[j].find("]")
                list3=list2[j][start+1:end]
                if list3 in sym_arr:
                    list2[j]=search_sym(sym_dict,list3)
                elif list3 in reg:
                    list2[j]=reg[list3]
                arr.extend(["dword[",list2[j],"]",","])
                
            else:
                arr.extend([list2[j],","])
          
        if flag==-1:
            return
        arr=''.join(arr)
        arr=arr.strip(',')
        fp2.write(arr+"\n")
        #print(arr)
        list1=fp1.readline()
        cnt=cnt+1
    return

def disp_intermediate(fp2):
    f=fp2.readline()
    while f:
        print(f,end="")
        f=fp2.readline()
        
    

if __name__=="__main__":
    sym_arr=[]
    lit_arr=[]
    fname=sys.argv[1]
    
    create_sym_table(fname)
    collect_sym_in_array(sym_dict,sym_arr)

    create_literal_table(fname)
    collect_lit_in_array(lit_dict,lit_arr)
    
    fp1=open(fname,"r")
    fp2=open("add.i","w+")
    create_intermediate(fp1,fp2)
    fp2=open("add.i","r")
    disp_intermediate(fp2)
    
    
        
    

    
