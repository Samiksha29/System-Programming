#sys_dict= [sysmbol_no,Line,Variable,Size,Total_ele,Define,Type,Address,Val]

from error_table import *   

sym_dict={}

jmp_statement=["jmp","loop","jnz","jz"]

#update_sym update the symbol table which store in the form of dictionary
def update_sym(cnt,lineno,var,size,tot_ele,define,type,add,val,lit):
    dict1={"sym#"+str(cnt):{'lineno':lineno,'variable':var,'size':size,'total_ele':tot_ele,'define':define,'type':type,'address':add,'value':val,'literal_no':lit}}
   
    sym_dict.update(dict1)

#use to check wheather symbol define in data or bss section or not if yes then return flag=1 else return error (flag=0)
def search_sym(sym_dict,var):
    flag=0
    for i in range(len(sym_dict)):
        if sym_dict["sym#"+str(i)]['variable']==var:
           flag=1
    return flag

def create_sym_table(fname):
     data_init=0
     bss_init=0
     fp=open(fname,"r")
     list1=fp.readline()  #read single line at a time
     cnt=0 #symbol no
     i=0 #line
     lit=0
     while list1.find("main:")<=-1:  #.data , .bss , .text section cover in this loop 
         if list1 in ['\n','\t\n']:  #if empty line come this handle it
            i=i+1
            print(list1,end="")
         else:
             end=list1.find("\n")     
             list2=list1.split(" ") 
             if list1.find("dd")>-1: 
                left=list2[0].strip("\t")  #strip removes the character if occur at start or end,here \t
                start=list1.find("dd")
                right=list1[start+3:end] 
                rr=right.split(',')
                
                if data_init==0:   #first time address is 0 so this variable is used 
                    add=0
                    data_init=1
                else:
                    add=add+(size*tot_ele)

                tot_ele=len(rr)
                size=4
                define='D'
                type1='S'
                update_sym(cnt,i,left,tot_ele,size,define,type1,add,right,"lit#"+str(lit))
                lit=lit+1  #literal no
                cnt=cnt+1

             
             elif list1.find("db")>-1:
                left=list2[0].strip("\t")
                start=list1.find('"')   #we want value present within " " like "sum of n="  we want sum of n=
                right=list1[start+1:]
                end=right.find('"')
                right=right[:end]
                if data_init==0:
                    add=0
                    data_init=1
                else:
                    add=add+(size*tot_ele)
                tot_ele=len(right)
                size=1
                define='D'
                type1='S'
                update_sym(cnt,i,left,tot_ele,size,define,type1,add,right,"lit#"+str(lit))
                lit=lit+1
                cnt=cnt+1

             elif list1.find("dq")>-1:
                left=list2[0].strip("\t")
                start=list1.find("dq")
                right=list1[start+3:end]
                rr=right.split(',')
                
                if data_init==0:
                    add=0
                    data_init=1
                else:
                    add=add+(size*tot_ele)
                    
                tot_ele=len(rr)
                size=8
                define='D'
                type1='S'
                update_sym(cnt,i,left,tot_ele,size,define,type1,add,right,"lit#"+str(lit))
                lit=lit+1
                cnt=cnt+1

             elif list1.find("resb")>-1 or list1.find("resd")>-1 or list1.find("resq")>-1:
                iresb=list1.find("resb")
                iresd=list1.find("resd")
                iresq=list1.find("resq")
                if iresb>-1:
                        mm=iresb
                        size=1
                elif iresd>-1:
                        mm=iresd
                        size=4
                elif iresq>-1:
                        mm=iresq
                        size=8
                left=list2[0].strip("\t")
                right=list1[mm+5:end]
                if bss_init==0:
                        add=0
                        bss_init=1
                else:
                        add=add+(size*tot_ele)
                
                tot_ele=int(right)
                define='D'
                type1='S'
                right='-'
                update_sym(cnt,i,left,tot_ele,size,define,type1,add,right,"lit#"+str(lit))
                cnt=cnt+1

             elif list1.find("extern")>-1:
                 for i in range(1,len(list2)):
                     list2[i]=list2[i].strip('\n').strip(',')
                     
                     
                 
                 
         list1=fp.readline()
         i=i+1

     while list1:
        list2=list1.split(" ")
        if list1.find(":")>-1:
            end=list1.find(":")
            left=list2[0][:end]
            tot_ele='-'
            size='-'
            define='U'
            type1='L'
            add=i
            right='-'
            update_sym(cnt,i,left,tot_ele,size,define,type1,add,right,'-')
            cnt=cnt+1

        if list2[0].find(":")>-1:
            start=list2[0].find(":")
            list2[0]=list2[0][start+1:]
            list3=list2[0].strip("\t")
          
        if list2[0].strip("\t") in jmp_statement:
            list2[1]=list2[1].strip("\n")
            flag=search_sym(sym_dict,list2[1])
            if flag==0:
                print("%s :ln %d : error:symbol '%s' %s"%(fname,i,list2[1],error_dict['undefined']))
                return -1
            
    
        list1=fp.readline()
        i=i+1

def disp_symbol_table(sym_dict):
    print("Symbol\tLine\tVariable\tTotal_ele\tSize\tDefine \tType\t\tAddress\t\tVal\t\t\tLiteral_no\n")
    print("-----------------------------------------------------------------------------------------------------------------------------------------")
    for i in range(len(sym_dict)):
        
         print("%s\t%d\t%s\t\t%s\t\t%s\t\t%c\t%c\t\t%d\t\t%s\t\t\t%s"%("sym#"+str(i),sym_dict["sym#"+str(i)]['lineno'],sym_dict["sym#"+str(i)]['variable'],sym_dict["sym#"+str(i)]['size'],sym_dict["sym#"+str(i)]['total_ele'],sym_dict["sym#"+str(i)]['define'],sym_dict["sym#"+str(i)]['type'],sym_dict["sym#"+str(i)]['address'],sym_dict["sym#"+str(i)]['value'],sym_dict["sym#"+str(i)]['literal_no']))


def  write_to_file(fname,sym_dict):
    start=fname.find(".")
    fname=fname[:start]+".s"
    fp=open(fname,"w+")
    fp.write("symbol"+"\t"+"Line"+"\t"+"Variable"+"\t"+"size"+"\t"+"Total_ele"+"\t"+"Define"+"\t"+"Type"+"\t"+"Address"+"\t\t"+"Val"+"\t\t"+"lit_no"+"\n")
    if(fp):
        for i in range (len(sym_dict)):
            fp.write("sym#"+str(i)+"\t"+str(sym_dict["sym#"+str(i)]['lineno'])+"\t"+str(sym_dict["sym#"+str(i)]['variable'])+"\t\t"+str(sym_dict["sym#"+str(i)]['size'])+"\t"+str(sym_dict["sym#"+str(i)]['total_ele'])+"\t\t"+str(sym_dict["sym#"+str(i)]['define'])+"\t"+str(sym_dict["sym#"+str(i)]['type'])+"\t"+str(sym_dict["sym#"+str(i)]['address'])+"\t\t"+str(sym_dict["sym#"+str(i)]['value'])+"\t\t"+str(sym_dict["sym#"+str(i)]['literal_no'])+"\n")


if __name__=="__main__":
    import sys
    sys_list=[]
    fname=sys.argv[1]
    ff=create_sym_table(fname)
    if ff!=-1:
        disp_symbol_table(sym_dict)
    write_to_file(fname,sym_dict)



