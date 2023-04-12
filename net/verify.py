"""
@Project : CJLU-Net-Verifier
@File    : verify.py
@Author  : Charles Stark
@Date    : 2023/4/12 10:20
"""
import os
import socket

import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
}


def get_host_ip():
    """
    Get host IP address
    :return: IP address
    :rtype: str
    """

    # noinspection PyBroadException
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        return None

    s.close()
    ip = ip.replace('\n', '')
    return ip


def net_verify():
    """
    Verify network
    :return: Is verified
    :rtype: bool
    """

    # username password
    account = ''
    password = None
    ip = get_host_ip()

    url = 'https://portal2.cjlu.edu.cn:802/eportal/portal/login'
    params = {
        'callback': 'dr1003',
        'user_account': ',0,__' + account,
        'user_password': password,
        'wlan_user_ip': ip,
        'wlan_user_ipv6': '',
        'wlan_user_mac': '000000000000',
        'wlan_ac_ip': '',
        'wlan_ac_name': '',
        'jsVersion': '4.2.1',
        'terminal_type': '1',
        'v': '7420',
        'lang': 'en'
    }

    try:
        resp = requests.post(url=url, headers=headers, params=params)
        return True
    except requests.exceptions.ConnectionError:
        return False


def vpn_verify():
    """
    Verify L2TP vpn
    :return: Is verified
    :rtype: bool
    """

    name = None
    username = None
    password = None

    os.system('rasdial {} {} {}'.format(name, username, password))

    return ping()


def ping(url='http://baidu.com'):
    """
    Ping an url
    :param url: Target url
    :type url: str
    :return: Is connected
    :rtype: bool
    """

    # noinspection PyBroadException
    try:
        resp = requests.get(url=url, headers=headers, timeout=5)
        return resp.status_code == 200
    except Exception:
        return False


if __name__ == '__main__':
    print(get_host_ip())
    print(ping())
