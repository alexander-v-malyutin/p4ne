import glob

list_addr = []
for file in glob.glob('*.txt'):
    with open(file) as openfile:
        for line in openfile:
            if ('ip address' in line and not 'ip address dhcp' in line
                    and not 'no ip address' in line and not 'match' in line):
                if line in list_addr: continue
                list_addr.append(line.replace('ip address', '').strip())

for line in list_addr:
    print(line)
