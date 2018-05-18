import glob

list_addr = []
for file in glob.glob('*.txt'):
    with open(file) as openfile:
        for line in openfile:
            if (line.lstrip().find('ip address') == 0 and not 'dhcp' in line):
                if line in list_addr: continue
                list_addr.append(line.replace('ip address', '').strip())

for line in list_addr:
    print(line)
