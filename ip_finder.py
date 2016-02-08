import socket #  Added For Finding Host IP
import subprocess as sub # Added For Run Command By CMD
import string
import datetime
import sys # For Exit
def ip_filter(i_list): # This Function Get A List Of IPs and Split IP
    '''((list)->list'''
    temp_list=[]
    for i in range(len(i_list)):
        for j in range(len(i_list[i])):
            if i_list[i][j] not in dic:
                temp_list.append(i_list[i][:j])
                break
    return temp_list
def search_ip(output): # This Function Get A String As Input ( ARP Command Output) and Find For Local IPs
    '''(str)->list'''
    index=0
    ip_list=[]
    while(True):
        index=output.find("192",index)
        ip_list.append(output[index:index+16])
        if (index==-1):
            break
        else:
            index=index+16
    return ip_list
def find(mask="192.168.166.",mode="manual",iplist=[],range_min=1,range_max=255): # This Function Ping And SSH IPs to find SSH Server
    log_file=open("log_file.txt","a")
    if mode=="manual":
        try:
            for i in range(range_min,range_max):
                output=str(list(sub.Popen("ping "+mask+str(i),stdout=sub.PIPE,stderr=sub.PIPE,shell=True).communicate())[0])
                if output.find("timed out")==-1 and output.find("unreachable")==-1:
                    ssh_response=sub.call("ssh "+mask+str(i),stdout=sub.PIPE,stderr=sub.PIPE,timeout=30,shell=True)
                    print("IP : ",mask+str(i),"Is available but it is not ssh server")
                else:
                    print("IP : ",mask+str(i),"Is not available")
            input("Press Any Key To Exit")
        except sub.TimeoutExpired:
            print("IP : ",mask+str(i),"Is SSH Server")
            log_file.write("IP : "+mask+str(i)+"Is SSH Server  "+str(datetime.datetime.today())+"\n")
            log_file.close()
            input("Press Any Key To Exit")
    else:
        try:
            for i in iplist:
                ssh_response=sub.call("ssh "+str(i),stdout=sub.PIPE,stderr=sub.PIPE,timeout=30,shell=True)
                print("IP : ",str(i),"Is available but it is not ssh server")
            input("Press Any Key To Exit")
        except sub.TimeoutExpired:
            print("IP : ",str(i),"Is SSH Server")
            log_file.write("IP : "+str(i)+"Is SSH Server  "+str(datetime.datetime.today())+"\n")
            log_file.close()
            input("Press Any Key To Exit")
            
        
if __name__=="__main__":
    dic=list(string.digits+".")
    my_ip=socket.gethostbyname(socket.gethostname())
    if my_ip=="127.0.0.1":
        print("Problem In Netwrok Connection")
        sys.exit()
    inp=int(input("Please Choose ARP[1] or Linear Search[2]"))
    if inp==1:
        sub.Popen("ping "+my_ip,stdout=sub.PIPE ,stderr=sub.PIPE,shell=True)
        response=sub.Popen("arp -a",stdout=sub.PIPE ,stderr=sub.PIPE,shell=True)
        output=str(list(response.communicate())[0])
        ip_list=search_ip(output)
        ip_list=ip_filter(ip_list)
        find(mode="ARP",iplist=ip_list)
    else:
        get_mask=input("Please Enter Mask :")
        range_max_input=int(input("Please Enter Range Max : "))
        range_min_input=int(input("Please Enter Range Min : "))
        if get_mask.find("192.")!=-1 and get_mask.find("168.")!=-1:
            if get_mask[-1]!=".":
                get_mask=get_mask+"."
            if range_max_input>range_min_input and range_max_input<256:
                find(mask=get_mask,mode="manual",range_max=range_max_input,range_min=range_min_input)
            else:
                find(mask=get_mask,mode="manual")
        else:
            if range_max_input>range_min_input and range_max_input<256:
                find(range_max=range_max_input,mode="manual",range_min=range_min_input)
            else:
                find()
        
        
        
