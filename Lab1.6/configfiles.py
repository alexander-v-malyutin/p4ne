import glob
import re
import ipaddress


def classifier(line):
    ip_search = re.search(r'ip address ((?:\d{1,3}\.){3}\d{1,3}) ((?:\d{1,3}\.){3}\d{1,3})', line)
    if ip_search:
        return {'ip': ipaddress.IPv4Interface(ip_search.group(1) + '/' + ip_search.group(2))}

    interface_search = re.search(r'^interface ([^ \n]+)', line.lstrip())
    if interface_search:
        return {'int': interface_search.group(1)}

    hostname_search = re.search(r'hostname ([^ \n\']+)', line.lstrip())
    if hostname_search:
        return {'host': hostname_search.group(1)}

    return {'key': None}

#print(classifier(' ip address 192.168.1.1 255.255.255.0'))
#print(classifier('interface Fa1/0'))
#print(classifier(' interface Fa 1/0'))
#print(classifier('hostname Router'))

list_addr = []
list_int = []
list_host = []

for file in glob.glob('../configs/*.txt'):
    with open(file) as openfile:
        for line in openfile:
            class_dict = classifier(line)
            if 'key' in class_dict:
                continue
            elif 'ip' in class_dict:
                if class_dict not in list_addr:
                    list_addr.append(class_dict)
            elif 'int' in class_dict:
                if class_dict not in list_int:
                    list_int.append(class_dict)
            elif 'host' in class_dict:
                if class_dict not in list_host:
                    list_host.append(class_dict)
            else:
                print('BAD!')

print('Hostnames:')
for line in list_host:
    print(line['host'])

print('Interfaces:')
for line in list_int:
    print(line['int'])

print('Addresses:')
for line in list_addr:
    print(line['ip'])
