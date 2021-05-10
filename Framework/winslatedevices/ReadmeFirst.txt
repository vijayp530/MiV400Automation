Pre-requirements:

	Windows 8.1
	Python-2.7.9
	Get latest pip (C:\Python27\python.exe -m pip install --upgrade pip)
	Install python gevent and requests packages ( C:\Python27\Scripts\pip.exe install gevent, C:\Python27\Scripts\pip.exe install requests, C:\Python27\Scripts\pip.exe install selenium)
	Copy HQ root CA (hq_ca.crt) and fake_shoretel_mfg_ca.crt  from server c$\Shoreline Data\keystore\certs to local PC C:\PhoneTool\keys folder
	
Generate fake certs for dummy phone MAC addresses( pick any CentOS machine to perfrom this step):

	Go thru steps provided in ReadmeFirst.txt file under C:\PhoneTool\PhoneMacCertGen folder
	
Prepare SBC and RP to accept fake certs:

	Copy fake_shoretel_mfg_ca.crt file from HQ c$\Shoreline Data\keystore\certs folder to SBC and RP in 
	On SBC, update /etc/kamailio/ca_list.pem file by running "cat fake_shoretel_mfg_ca.crt >> ca_list.pem"
	on RP, update /etc/nginx/trusted_ca_certs.crt by running "cat fake_shoretel_mfg_ca.crt >> trusted_ca_certs.crt"
	
Configuration Files:

	Fill UserDBFile.txt file with all pphone information in specified format. Make sure Phone MAC addresses matches with fake MAC certs.
	Fill ConfigParam.txt file with all global configuration parameters common to all phones/users

Usage:
	Go to Mediaserver folder in command prompt and run "rtp-bridge -s socket"
	python main.py
	Update main.py file with all configuration params and run all applicable scripts