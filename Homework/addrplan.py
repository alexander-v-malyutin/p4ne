'''
1. Чтение файлов с выводом команды "show tech-support"
2. Формирование структуры (structure) вида:
    [
        {
            'hostname': '...',
            'interfaces':
            {
                'ifname': '...',
                'ifaddr': ipaddress.IPv4Address()
            },
            {
                'ifname': '...',
                'ifaddr': None
            },
            ...
        },
        {
        },
        ...
    ]
3. Составление списка сетей (net_list) с сортировкой по маске/сети
4. Запись в файл 'AddrPlan.xlsx' в 2 стобца в worksheeet 'AddrPlan'
5. Вывод на экран списка сетей/масок в 2 столбца
'''

import glob, ipaddress, re, pprint
from openpyxl import Workbook, load_workbook


addr_plan_file = 'AddrPlan.xlsx'

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
    return {}


def struct_func(file):
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

                netaddr = ipaddress.IPv4Network(class_dict['ip'], strict=False)
                if netaddr not in net_list:
                    net_list.append(netaddr)
        if ifname:
            if_list.append(if_dict)

        dev_dict = {'hostname': hostname,
                    'interfaces': if_list}
        structure.append(dev_dict)


def sortfunc(net):
    return (net.prefixlen << 32) + int(net.network_address)


structure = []
net_list = []
for file in glob.glob('../configs/*.txt'):
    struct_func(file)

net_list.sort(key=sortfunc)


def write_addrplan_to_file(file):
    if glob.glob(file):
        wb = load_workbook(file)
        try:
            wb.remove(wb['AddrPlan'])
        except ValueError as e:
            print(e)
    else:
        wb = Workbook()

    ws = wb.create_sheet('AddrPlan')
    ws['A1'] = 'Сеть'
    ws['B1'] = 'Маска'

    for net in net_list:
        ws.append({'A': str(net.network_address), 'B': str(net.netmask)})

    wb.save(file)
    wb.close()

write_addrplan_to_file(addr_plan_file)

print('{:16s}{:16s}'.format('Сеть', 'Маска'))
for net in net_list:
    print('{:16s}{:16s}'.format(str(net.network_address), str(net.netmask)))

