import socket
import subprocess as sub
import string
dic=list(string.digits+".")
my_ip=socket.gethostbyname(socket.gethostname())
def ip_filter(i_list):
    temp_list=[]
    for i in range(len(i_list)):
        for j in range(len(i_list[i])):
            if i_list[i][j] not in dic:
                temp_list.append(i_list[i][:j])
                break
    return temp_list
sub.Popen("ping "+my_ip)
response=sub.Popen("arp -a",stdout=sub.PIPE ,stderr=sub.PIPE)
output=str(list(response.communicate())[0])
index=0
ip_list=[]

while(True):
    index=output.find("192",index)
    ip_list.append(output[index:index+16])
    if (index==-1):
        break
    else:
        index=index+16

print(ip_filter(ip_list))



    
