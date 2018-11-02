#literal_dict-[literal_no,line ,literl_symbol, literal hex,size]

import sys

lit_dict={}

#update_lit update the literal table which store in the form of dictionary
def update_lit(cnt,lineno,var,hex_val,size):
    dict1={"lit#"+str(cnt):{'lineno':lineno,'variable':var,'hex_val':hex_val,'size':size}}
    lit_dict.update(dict1)

#it use to convert number to its hex val
def no_to_hex(right,rarr):
    if len(right)>=1:
        right=right.split(",");
        for i in range(len(right)):
            hexval=hex(int(right[i]))
            hexval=hexval[2:]
            rarr.append(hexval)
            
            
        
#it use to convert string to its hex val                      
def str_to_hex(right,rarr):
    for i in range(len(right)):
        k=ord(right[i])  #gives ascii values of character
        k=hex(k)
        k=k[2:]
        rarr.append(k)
   
   


def create_literal_table(fname):
   arr=[]
   i=0  #store line no
   fp=open(fname,"r")
   list1=fp.readline()  #read single line at a time
   cnt=0 #store the literal no entry
  
   while list1.find("main:")<=-1:
       rarr=[]
       if list1 in ['\n','\t\n']:
           print("")
       else:
           ddindex=list1.find("dd")
           if ddindex>-1:
               right=list1[ddindex+3:].strip("\n")
               no_to_hex(right,rarr)
               if len(rarr)>1:
                   rarr=','.join(rarr)
               else:
                   rarr=''.join(rarr)
               size='4'
               update_lit(cnt,i,right,rarr,size)
               cnt=cnt+1
          
          
           
           else:
               dbindex=list1.find("db")
               if dbindex>-1:
                   rt=list1.find('"')
                   right=list1[rt+1:].strip("\n")
                   rt=right.find('"')
                   right=right[:rt]
                   str_to_hex(right,rarr)
                   rarr=''.join(rarr)
                   size='1'
                   update_lit(cnt,i,right,rarr,size)
                   cnt=cnt+1
              
               elif list1.find("resb")>-1  or list1.find("resd")>-1  or list1.find("resq")>-1:
                   regb=list1.find("resb")
                   regd=list1.find("resd")
                   regq=list1.find("resq")
                   if regb>-1:
                       reg=regb
                       size='1'
                   elif regd>-1:
                       reg=regd
                       size='4'
                   elif regq>-1:
                       reg=regq
                       size='8'
                   right=list1[reg+5:].strip("\n")
                   no_to_hex(right,rarr)
                   if len(rarr)>1:
                       rarr=','.join(rarr)
                   else:
                       rarr=''.join(rarr)
                   update_lit(cnt,i,right,rarr,size)
                   cnt=cnt+1

               
       list1=fp.readline()
       i=i+1
   

   while list1:
       if list1 in ['\n','\t\n']:
           print("")
       else:
           list1=list1.split(' ')
           if len(list1)>1:
               list1=list1[1].split(',')
               if len(list1)>1:
                   list1=list1[1].split()
                   list2=list(list1[0])
                   kk=ord(list2[0])
                   if kk>=48 and kk<=57:
                       no_to_hex(list1[0],rarr)
                       if len(rarr)>1:
                            rarr=','.join(rarr)
                       else:
                            rarr=''.join(rarr)
                       update_lit(cnt,i,list1[0],rarr,'-')
                       cnt=cnt+1
                       rarr=[]
                   
                 
       list1=fp.readline()
       i=i+1
   
       
def disp_literal_table(lit_dict):
    print("Literal\t\tLine no\t\t\tLiteral_symbol\t\tLiteral_Hex\t\t\tSize")
    print("-------------------------------------------------------------------------------------------------")
    for i in range(len(lit_dict)):
        print("%s\t\t%d\t\t\t%s\t\t\t%s\t\t\t\t%s"%("lit#"+str(i),lit_dict["lit#"+str(i)]['lineno'],lit_dict["lit#"+str(i)]['variable'],lit_dict["lit#"+str(i)]['hex_val'],lit_dict["lit#"+str(i)]['size']))


def  write_to_file(fname,lit_dict):
    start=fname.find(".")
    fname=fname[:start]+".l"
    fp=open(fname,"w+")
    fp.write("Literal"+"\t\t"+"Line no"+"\t\t"+"Literal_symbol"+"\t\t"+"Literal_Hex"+"\t\t\t"+"Size"+"\n")
    if(fp):
        for i in range (len(lit_dict)):
            fp.write("lit#"+str(i)+"\t\t"+str(lit_dict["lit#"+str(i)]['lineno'])+"\t\t"+str(lit_dict["lit#"+str(i)]['variable'])+"\t\t\tt"+str(lit_dict["lit#"+str(i)]['hex_val'])+"\t\t\t\t"+str(lit_dict["lit#"+str(i)]['size'])+"\n")
            
if __name__=="__main__":
    fname=sys.argv[1]
    create_literal_table(fname)
    disp_literal_table(lit_dict)
    write_to_file(fname,lit_dict)
