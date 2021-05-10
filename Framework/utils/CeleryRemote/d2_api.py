def get_dut_info_from_hq(hq_ip, username, password):
        import requests
        import urllib, base64
        import re
        import json

        LOGIN_URL = 'http://'+hq_ip+':5478/director/login'
        LIST_SWITCH_URL = 'http://'+hq_ip+':5478/director/switches/list'
        LIST_PPHONES_URL = 'http://'+hq_ip+':5478/director/ip_phones/list'
        print(LOGIN_URL)
        print(LIST_SWITCH_URL)
        print(LIST_PPHONES_URL)
        devices2 = []
        try:
            client = requests.session()

            # Retrieve the CSRF token first
            client.get(LOGIN_URL)  # sets cookie
            #print(client.cookies.items())
            d2_cookie = client.cookies['_director2_session']
            # print(d2_cookie)
            csrftoken = re.match('(.+)--',d2_cookie).group(1)
            # print(csrftoken)
            csrftoken = urllib.unquote(d2_cookie)
            # print(csrftoken)
            csrftoken = base64.b64decode(csrftoken)
            # csrftoken = r'{I"session_id:EFI"%8cb0cc7d1645b236e217e3e35826b9dd; TI"abc; F{:	hostI"localhost; FI"_csrf_token; FI"1lC0TGuAk9D6C0f68Fy9T8UsQ0RaQg9uXiTRnPra+iLE=; F'
            # print(csrftoken)
            csrftoken = re.match('.*_csrf_token.*1(.*=).*', csrftoken).group(1)
            # print(csrftoken)

            client.post(LOGIN_URL,data={"user_session[login_name]": username, "user_session[login_password]": password, "authenticity_token": csrftoken})
            r = client.get(LIST_SWITCH_URL)
            # print(r.text)
            devices = []
            keys = ['name', 'type', 'ip']
            d = json.loads(r.text)
            for device in d['rows']:
                 d = dict((key, device['cell'][i]) for key, i in zip(keys,[0,6,7]))
                 devices.append(d)

            r = client.get(LIST_PPHONES_URL)
            # print(r.text)

            d = json.loads(r.text)
            # print(d['rows'][0]['cell'])
            keys = ['name','ip']
            for device in d['rows']:
                 d = dict((key, device['cell'][i]) for key, i in zip(keys,[0,4]))
                 d['type'] = 'PPhone'
                 devices.append(d)

            d_type = {
                    'SW' : 'HQ',
                    'SG-LinuxDVS' : 'LDVS',
                    'SG-vPhone' : 'Switch',
                    'vPhoneSwitch' : 'Switch',
                    'SG-vTrunk' : 'Trunk',
                    'SA-vCollab' : 'UCB',
                    'PPhone': 'PPhone',
                    'CC': 'CC'
            }
            d_os = {
                    'SW' : 'Windows',
                    'SG-LinuxDVS' : 'Linux',
                    'SG-vPhone' : 'Linux',
                    'SG-vTrunk' : 'Linux',
                    'SA-vCollab' : 'Linux',
                    'PPhone': 'Linux'
            }
            d_user = {
                    'SW' : 'administrator',
                    'SG-LinuxDVS' : 'admin',
                    'SG-vPhone' : 'admin',
                    'SG-vTrunk' : 'admin',
                    'SA-vCollab' : 'admin',
                    'PPhone': 'admin'
            }
            d_password = {
                    'SW' : 'Shoreadmin1',
                    'SG-LinuxDVS' : 'ShoreTel',
                    'SG-vPhone' : 'ShoreTel',
                    'SG-vTrunk' : 'ShoreTel',
                    'SA-vCollab' : 'ShoreTel',
                    'PPhone': ''
            }
            d_pkey = {
                    'PPhone': r'c:\NextGenArc\etc\hq_rsa\hq_rsa'
            }
            for d in devices:
                d['os'] = d_os[d['type']]
                d['password'] = d_password[d['type']]
                d['username'] = d_user[d['type']]
                if d['type'] == 'PPhone':
                    d['pkey'] = d_pkey[d['type']]
                if d['type'] == 'SW' and d['ip'] != hq_ip:
                    d['type'] = 'CC'
                d['type'] = d_type[d['type']]
                if d['type'] in ('HQ','PPhone','Switch', 'CC'):
                    devices2.append(d)
            return devices2
        except Exception as e:
            print("Could not fetch dut info from director..", e)
            return devices2

def copy_rsa_from_hq(ip,user,password):
    from util import netcopy
    try:
        netcopy.netcopy(ip,r'C:\Shoreline Data\keystore\ssh\hq_rsa', r'C:\NextGenArc\etc\hq_rsa',user,password)
    except Exception:
        print("failed to copy hq_rsa key")
        pass

if __name__ == '__main__':
    dut_info = get_dut_info_from_hq('10.198.128.69','admin',r'changeme')
    print(dut_info)
