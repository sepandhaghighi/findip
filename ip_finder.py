import socket #  Added For Finding Host IP
import subprocess as sub # Added For Run Command By CMD
import string
import datetime
import sys # For Exit
import multiprocessing as mu # for multtiprocessing
import time
def ping(i): # ping function
    output=str(list(sub.Popen("ping "+i,stdout=sub.PIPE,stderr=sub.PIPE,shell=True).communicate())[0])
    return output
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
def string_conv(i):
    return mask+str(i)    
def find(mode="manual",iplist=[],range_min=0,range_max=254,server_counter=0): # This Function Ping And SSH IPs to find SSH Server
    log_file=open("log_file.txt","a")
    if mode=="manual":
        try:
            ip_list=list(map(string_conv,list(range(range_min,range_max))))
            p=mu.Pool(mu.cpu_count()+60) # for multiprocessing
            result=p.map(ping,ip_list) # result of pings
            for output in result:
                if output.find("timed out")==-1 and output.find("unreachable")==-1:
                    ssh_response=sub.call("ssh "+ip_list[result.index(output)],stdout=sub.PIPE,stderr=sub.PIPE,timeout=30,shell=True)
                    print("IP : ",ip_list[result.index(output)],"Is available but it is not ssh server")
                else:
                    print("IP : ",ip_list[result.index(output)],"Is not available")
            p.close()
            p.terminate()
        except sub.TimeoutExpired:
            ssh_find_index=result.index(output)
            for l in range(15):
                print("IP : ",ip_list[ssh_find_index],"Is SSH Server*****+++++---")
            server_counter=server_counter+1
            rec_flag=int(ip_list[ssh_find_index].split(".")[-1])
            log_file.write("IP : "+ip_list[ssh_find_index]+" Is SSH Server  "+str(datetime.datetime.today())+"\n")
            log_file.close()
            p.close()
            p.terminate()
            if server_counter<=4 and range_min<=253:
                find(mode="manual",iplist=[],range_min=rec_flag+1,range_max=255,server_counter=server_counter+1)
    elif mode=="ARP":
        try:
            for i in iplist:
                sub.CREATE_NEW_CONSOLE
                sub.CREATE_NEW_PROCESS_GROUP
                ssh_response=sub.call("ssh "+str(i),stdout=sub.PIPE,stderr=sub.PIPE,timeout=30,shell=True)
                print("IP : ",str(i)," Is available but it is not ssh server")
        except sub.TimeoutExpired:
            for k in range(15):
                print("IP : ",str(i),"Is SSH Server")
            log_file.write("IP : "+str(i)+"Is SSH Server  "+str(datetime.datetime.today())+"\n")
            log_file.close()
            
    
            
        
if __name__=="__main__":
    server_counter=0
    mask="192.168.166."
    mu.freeze_support()
    dic=list(string.digits+".")
    print("Running On Netmask: " + mask)
    my_ip=socket.gethostbyname(socket.gethostname())
    my_ip_mask=int(my_ip.split(".")[-2])
    if my_ip_mask!=166:
        print("Location : Out Of Lab")
    else:
        print("Location : In Lab")
    if my_ip=="127.0.0.1":
        print("Problem In Netwrok Connection ( Please Check )")
        input()
        sys.exit()
    ssh_test=sub.Popen("ssh",stdout=sub.PIPE,stderr=sub.PIPE,shell=True)
    ssh_result=str(list(ssh_test.communicate())[1])
    #print(ssh_result)
    if ssh_result.find("is not recognized")!=-1:
        print("Please First Install Open SSH (Press Any Key To Exit)")
        input()
        sys.exit()
    time_1=time.perf_counter()
    mask="192.168.166."
    print("Please Wait : Scan IPs . . . ")
    find()
    time_2=time.perf_counter()
    print("Scan Time :",str((time_2-time_1)/60)," min")
    input("Press Any Key To Exit")
        
