path_server_Asterisk="/root/pcap_download/"
ip_addr_server_Asterisk='10.112.123.89'
server_username_Asterisk="root"
server_pwd_Asterisk="Jafe@20_20"
testbed="C:/Users/abhishek.khanchi/Desktop/14042020/5.1_Robo_SVN/Desktop_Automation/"

path_server_mxone="/local/home/mxone_admin/pcap_download/"
ip_addr_server_mxone='10.112.110.111'
server_username_mxone="mxone_admin"
server_pwd_mxone="Mxone@456"
root_passwd_mxone='Mx0n3@!2#'

# coreserverIPAddress='10.112.91.70'
# coreserverUsername="dev"
# coreserverpass='root@123'
# path_server_core='/home/dev/pcap_download/'
# core_server_home='/home/dev/'
coreserverIPAddress='10.112.91.70'
coreserverUsername="dev"
coreserverpass='root@123'
path_server_core='/home/dev/pcap_download/'
core_server_home='/home/dev/'
httpipfiletlslocal='/httpdsslconfig/'
httpdserverIPAddress=coreserverIPAddress
httpdUsername=coreserverUsername
httpdpass=coreserverpass
httpdserverconfpath='/opt/lampp/etc/extra/'
serverhttpdfile=httpdserverconfpath+'httpd-ssl.conf'
httpdpulishxmlLocal=testbed+'/phonexml/'
httpdpulishxmlserver='/opt/lampp/htdocs/'

phoneConfigLocal=testbed+"phoneconfig/"
tftp_server=coreserverIPAddress
tftp_path_root='/srv/tftp/'
ftp_server=coreserverIPAddress
ftp_server_root='/ftp/'
ftp_server_username= 'anonymous'
ftp_server_passwd='ftpuser'
resource=testbed+"resource/"
phonexml=testbed+"phonexml/"
csvFilelocal=resource+'directoryList.csv'
wavFilelocal=resource+"beep.wav"
csvFile='directoryList.csv'
wavFile="beep.wav"





# scp_get(**kwargs)4165142538 5060
# from pcap_to_json import pcap_to_json
#
# if __name__ == '__main__':
#     # Sniff two packets using scapy
#     a = sniff(count=2)
#     # Convert the captured packets to json
#     json_data = pcap_to_json(a,json_indent=2)
#     print(json_data)
