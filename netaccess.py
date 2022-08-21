import requests
from dotenv import load_dotenv
import os

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

def main():
    LDAP_USERNAME = os.getenv('LDAP_USR', None)
    LDAP_PASSWORD = os.getenv('LDAP_PWD', None)

    assert LDAP_USERNAME is not None, "Invalid username"
    assert LDAP_PASSWORD is not None, "Invalid password"

    print("LDAP Username: ", LDAP_USERNAME)
    with requests.Session() as session:
        resp = session.post('https://netaccess.iitm.ac.in/account/login', data = {
            'userLogin': LDAP_USERNAME,
            'userPassword': LDAP_PASSWORD,
            'submit': '',
            }, verify=False)

        assert resp.ok

        assert resp.url == 'https://netaccess.iitm.ac.in/account/index', 'Login failed'
        print("Logged In")

        resp = session.post('https://netaccess.iitm.ac.in/account/approve', data = {
            'duration': '2',
            'approveBtn': '',
            }, verify=False)

        assert resp.ok, "Error sending request to approve machine"

        print("Request sent to approve machine")

if __name__ == '__main__':
    load_dotenv()
    main()
