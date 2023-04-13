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
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 '
                  'Safari/537.36',
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
        ip = s.getsockname()[0].replace('\n', '')
    except Exception:
        return None

    s.close()
    return ip


def net_verify(account, password):
    """
    Verify network
    :param account: Account
    :type account: str
    :param password: Password
    :type password: str
    :return: Is verified
    :rtype: bool
    """

    ip = get_host_ip()

    url = 'https://portal2.cjlu.edu.cn:802/eportal/portal/login'
    params = {
        'callback': 'dr1003',
        'login_method': '1',
        'user_account': ',0,__' + account,
        'user_password': password,
        'wlan_user_ip': ip,
        'wlan_user_ipv6': None,
        'wlan_user_mac': '000000000000',
        'wlan_ac_ip': None,
        'wlan_ac_name': None,
        'jsVersion': '4.2.1',
        'terminal_type': '1',
        'lang': 'zh-cn',
        'v': '9780',
    }

    try:
        resp = requests.get(url=url, headers=headers, params=params)
        return resp.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


def net_disconnect():
    pass


def vpn_verify(name, username, password):
    """
    Verify L2TP vpn connection
    :param name: VPN name
    :type name: str
    :param username: Username
    :type username: str
    :param password: Password
    :type password: str
    :return: Is verified
    :rtype: bool
    """

    os.system('rasdial {} {} {}'.format(name, username, password))

    return ping()


def vpn_disconnect(name):
    """
    Disconnect L2TP vpn
    :param name: VPN name
    :type name: str
    """
    os.system('rasdial {} /DISCONNECT'.format(name))


def ping(url='https://baidu.com'):
    """
    Ping an url
    :param url: Target url
    :type url: str
    :return: Is connected
    :rtype: bool
    """

    # noinspection PyBroadException
    try:
        resp = requests.get(url=url, headers=headers, timeout=3)
        return resp.status_code == 200
    except Exception:
        return False


if __name__ == '__main__':
    print(get_host_ip())
    print(ping())
