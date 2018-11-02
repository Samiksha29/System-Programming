import sys

#fp1=macro.asm
#fp3=new_macro.txt
mdt_dict={}
mnt_dict={}

def update_mdt_dict(mname,arr):
    dict1={mname:arr}
    mdt_dict.update(dict1)

def update_mnt_dict(cnt,mname,para,start,end):
    dict1={"macro#"+str(cnt):{'mname':mname,'parameter':para,'start':start,'end':end}}
    mnt_dict.update(dict1)

def disp_mnt(mnt_dict):
    print("\n\t\t\tMNT TABLE\t\t\t")
    print("\nMacro_no\tMname\t    Parameter\tStart\tEnd")
    print("-------------------------------------------------------")
    for i in range(1,len(mnt_dict)+1):
        print("%s\t\t%s\t%d\t  %d\t %d"%("macro#"+str(i),mnt_dict["macro#"+str(i)]['mname'],int(mnt_dict["macro#"+str(i)]['parameter']),mnt_dict["macro#"+str(i)]['start'],mnt_dict["macro#"+str(i)]['end']))

def disp_mdt(mdt_dict):
    print("\n\n\n\t\t\tMDT TABLE\t\t\t")
    for key in mdt_dict:
        print("Mname:%s"%key)
        print("Defination:\n%s"%mdt_dict[key])
               
def disp_newasm(fp3):
    print("\n\n\n\t\t\tnew_macro.asm\t\t\t")
    line3=fp3.readline()
    while line3:
        print(line3,end=' ')
        line3=fp3.readline()

def disp_asm(fname,fp1):
    print("\n\n\n\t\t\t%s\t\t\t"%fname)
    line1=fp1.readline()
    while line1:
        print(line1,end=' ')
        line1=fp1.readline()
        
def create_table(fname,fp1,fp3):
    lineno=0 #line count
    cnt=0 #cnt no of macro
    line1=fp1.readline()
    lineno=lineno+1
    arr=[] #to store mdt lines
    mname_arr=[] #store macroname
    present_bit=0 
    
    while line1.find(".data")==-1:
        if line1.find("%macro")>-1:
            cnt=cnt+1
            list1=line1.split(' ')
            mname=list1[1].strip("\n").strip("\t")
           
                
            para=list1[2].strip("\n").strip("\t")
            start=lineno
            line1=fp1.readline()
            lineno=lineno+1
            #if macro name already exists in mnt then previous is replace by latest
            #present bit is set to 1 if it is present
            #by using index i can update mnt at that index so that same name not exists
            if mname in mname_arr :
                index=mname_arr.index(mname)
                present_bit=1
            mname_arr.append(mname)
            while line1.find("%endmacro")==-1:
                arr.append(line1)
                line1=fp1.readline()
                lineno=lineno+1

            end=lineno
            if present_bit==1:
                update_mnt_dict(index+1,mname,para,start,end)
                present_bit==0
            else:
                update_mnt_dict(cnt,mname,para,start,end)

        
            arr=''.join(arr)
            update_mdt_dict(mname,arr)
            arr=[]

        line1=fp1.readline()
        lineno=lineno+1
     
    while line1:
        #print(line1,end="")
        list1=line1.split(' ')
        list1[0]=list1[0].strip("\n").strip("\t")
        
        #if we get macro name after any label
        if list1[0].find(":")>-1:
            colon=list1[0].find(":")
            label=list1[0][:colon+1]
            list1[0]=list1[0][colon+1:].strip("\t")
            flag=1
        if list1[0] in mname_arr:
            index=mname_arr.index(list1[0])
            if flag==1:
                fp3.write(label)
            flag=0
            ll=line1.split(' ')
            value=ll[1].split(',')

            #val1 val2 store the parameter values
            length=len(value)
            argu=int(mnt_dict["macro#"+str(index+1)]['parameter'])
            if argu==length:
                if length==1:
                    val1=value[0].strip("\n").strip("\t")
                    v1=mdt_dict[list1[0]].find("%")
                    end=mdt_dict[list1[0]].find("\n")
                    my_mdt=mdt_dict[list1[0]][:v1]+str(val1)+mdt_dict[list1[0]][end:]
                    fp3.write(my_mdt)

                if length==2:
                    val1=value[0].strip("\n").strip("\t") 
                    val2=value[1].strip("\n").strip("\t")

                    if mdt_dict[list1[0]].find("%"):
                        v1=mdt_dict[list1[0]].find("%")
                        end=mdt_dict[list1[0]].find("\n")
                        my_mdt=mdt_dict[list1[0]][:v1]+str(val1)+mdt_dict[list1[0]][end:]
                        v1=my_mdt.find("%")
                        my_mdt=my_mdt[:v1]+str(val2)+my_mdt[v1+2:]
        
                        fp3.write(my_mdt)
        
            else:
                if length < argu:
                    diff=argu-length
                    print("%s:%d: warning: macro '%s' exists, but not taking %d parameters [-w+macro-params]"%(fname,lineno,list1[0],diff))
                    print("%s:%d: error: parser: instruction expected"%(fname,lineno))
                
                
                if length > argu:
                    print("%s:%d: warning: macro '%s' exists, but not taking %d parameters [-w+macro-params]"%(fname,lineno,list1[0],length))
                    print("%s:%d: error: parser: instruction expected"%(fname,lineno))
                return -1
            

        else:
            fp3.write(line1)
        line1=fp1.readline()
        lineno=lineno+1
    fp1.close
    fp3.close
       
if __name__=="__main__":
    fname=sys.argv[1]
    fp1=open(fname,"r")
    fp3=open("new_macro.asm","w+")
   
    flag=create_table(fname,fp1,fp3)
    if flag!=-1:
        disp_mnt(mnt_dict)
        disp_mdt(mdt_dict)

        fp1=open(fname,"r")
        disp_asm(fname,fp1)

        fp3=open("new_macro.asm","r")
        disp_newasm(fp3)
