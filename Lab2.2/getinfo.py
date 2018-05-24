import re, ipaddress, glob, sys
from flask import Flask
sys.path.append('../Homework')


def classifier(line):
    ip_addr_search = re.search(r'ip address ((?:\d{1,3}\.){3}\d{1,3}) ((?:\d{1,3}\.){3}\d{1,3})', line)
    if ip_addr_search:
        return {'ip': ipaddress.IPv4Interface(ip_addr_search.group(1) + '/' + ip_addr_search.group(2))}
    ip_dhcp_search = re.search(r'ip address dhcp', line)
    if ip_dhcp_search:
        return {'ip': 'dhcp'}
    interface_search = re.search(r'^interface ([^ \n]+)', line.lstrip())
    if interface_search:
        return {'int': interface_search.group(1)}
    hostname_search = re.search(r'hostname ([^ \n\']+)', line.lstrip())
    if hostname_search:
        return {'host': hostname_search.group(1)}
    return {}


def struct_func(file):
    """
    Создание структуры данных с информацией об устройствах
    """
    with open(file) as openfile:
        if_list = []
        ifname = ''
        for line in openfile:
            class_dict = classifier(line)
            if 'host' in class_dict:
                hostname = class_dict['host']
            elif 'int' in class_dict:
                if ifname:
                    if_list.append(if_dict)
                ifname = class_dict['int']
                if_dict = {'ifname': ifname, 'ifaddr': None}
            elif 'ip' in class_dict:
                if_dict['ifaddr'] = class_dict['ip']

                if class_dict['ip'] == 'dhcp': continue

        if ifname:
            if_list.append(if_dict)

        dev_dict = {'hostname': hostname,
                    'interfaces': if_list}
        structure.append(dev_dict)


def generate_host_list():
    host_list = []
    for device in structure:
        host_list.append(device['hostname'])
    return '<br>'.join(host_list)


def generate_addr_list(hostname):
    addr_list = []
    for i in range(len(structure)):
        if structure[i]['hostname'] == hostname:
            host_index = i
            break
    for interface in structure[host_index]['interfaces']:
        if type(interface['ifaddr']) is ipaddress.IPv4Interface:
            ifaddr = str(interface['ifaddr'].ip)
            ifmask = str(interface['ifaddr'].netmask)
        elif interface['ifaddr'] is None:
            ifaddr = 'None'
            ifmask = 'None'
        elif interface['ifaddr'] == 'dhcp':
            ifaddr = 'dhcp'
            ifmask = 'dhcp'

        addr_list.append('{:20s}{:16s}{:16s}'.format(interface['ifname'],
                                                     ifaddr, ifmask))

    return '<br>'.join(addr_list)

app = Flask(__name__)


@app.route('/')
def index():
    return 'Preved!'


@app.route('/configs')
def configs():
    S = generate_host_list()
    return S


@app.route('/configs/<hostname>')
def print_hostname(hostname):
    S = generate_addr_list(hostname)
    return S

structure = []
for file in glob.glob('../configs/*.txt'):
    struct_func(file)

if __name__ == '__main__':
    app.run(debug=True)
