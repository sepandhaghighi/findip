import socket #  Added For Finding Host IP
import subprocess as sub # Added For Run Command By CMD
import string
import datetime
import sys # For Exit
import multiprocessing as mu # for multtiprocessing
import time
import os
mask = "192.168.1."
def logo_handler():
    if "logo.txt" in os.listdir():
        with open("logo.txt","r") as logo:
            for char_line in logo:
                print(char_line.rstrip())
        print(line(70,"*"))
        print("Visit : "+"http://github.com/sepandhaghighi/findip")
        print(line(70, "*"))
def line(number,char="-"):
    response=""
    i=0
    while(i<number):
        response+=char
        i+=1
    return response
def ping(i): # ping function
    output=str(list(sub.Popen("ping "+i,stdout=sub.PIPE,stderr=sub.PIPE,shell=True).communicate())[0])
    return output
def ip_filter(i_list): # This Function Get A List Of IPs and Split IP
    '''((list)->list'''
    dic = list(string.digits + ".")
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
def ARP(my_ip,file):
    try:
        sub.Popen("ping " + my_ip, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
        response = sub.Popen("arp -a", stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
        output = str(list(response.communicate())[0])
        ip_list = search_ip(output)
        ip_list = ip_filter(ip_list)
        for i in ip_list:
            print("IP : ", i, "Is  available")
            file.write("IP : "+ i+ "Is  available\n")
    except Exception as e:
        if file.closed==False:
            file.close()
        print(e)

def Manual(range_min,range_max,file):
    try:
        ip_list = list(map(string_conv, list(range(range_min, range_max + 1))))
        p = mu.Pool(mu.cpu_count() + 100)  # for multiprocessing
        result = p.map(ping, ip_list)  # result of pings
        for output in result:
            if output.find("timed out") == -1 and output.find("unreachable") == -1:
                # ssh_response=sub.call("ssh "+ip_list[result.index(output)],stdout=sub.PIPE,stderr=sub.PIPE,timeout=30,shell=True)
                print("IP : ", ip_list[result.index(output)], "Is available")
                file.write("IP : "+ ip_list[result.index(output)]+ " Is available\n")
            else:
                print("IP : ", ip_list[result.index(output)], "Is not available")
                file.write("IP : "+ ip_list[result.index(output)]+ " Is not available\n")
    except Exception as e:
        if file.closed==False:
            file.close()
        print(e)

def find(mode="manual",my_ip="0.0.0.0",range_min=0,range_max=254): # This Function Ping And SSH IPs to find SSH Server
    log_file=open("log_file.txt","a")
    log_file.write(str(datetime.datetime.now())+"\n")
    log_file.write(line(30,"%")+"\n")
    if mode=="manual":
        Manual(range_max=range_max,range_min=range_min,file=log_file)
    elif mode=="ARP":
        ARP(my_ip,log_file)
    log_file.write(line(30, "*") + "\n")
    log_file.close()
def set_mask():
    get_mask = input("Please Enter Mask :")
    if get_mask.find("192.") != -1 and get_mask.find("168.") != -1:
        if get_mask[-1] != ".":
            get_mask = get_mask + "."
    return get_mask
def set_range():
    try:
        range_max_input = int(input("Please Enter Range Max : "))
        range_min_input = int(input("Please Enter Range Min : "))
    except ValueError:  # If User Ignore Input Step
        range_max_input = 0
        range_min_input = 0
    print("Please Wait : Scan IPs . . . ")
    if range_max_input > range_min_input and range_max_input < 256:
        find(range_max=range_max_input, range_min=range_min_input)
    else:
        find()
def main():
    logo_handler()
    mu.freeze_support()
    global mask
    print("Running On Netmask: " + mask)
    my_ip = socket.gethostbyname(socket.gethostname())
    if my_ip == "127.0.0.1":
        print("Problem In Netwrok Connection ( Please Check )")
        input()
        sys.exit()
    inp = int(input("Please Choose ARP[1] or Linear Search[2]"))
    time_1 = time.perf_counter()
    if inp == 1:
        print("Please Wait : Scan IPs . . . ")
        find(mode="ARP", my_ip=my_ip)
        time_2 = time.perf_counter()
    else:
        mask = set_mask()
        set_range()
        time_2 = time.perf_counter()
    print("Scan Time :", str((time_2 - time_1) / 60), " min")
    input("Press Any Key To Exit")

                
        
        
        
