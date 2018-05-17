import ipaddress
import random


start_addr = int(ipaddress.IPv4Address('11.0.0.0'))
end_addr = int(ipaddress.IPv4Address('223.0.0.0'))
start_pref = 8
end_pref = 24

class IPv4RandomNetwork(ipaddress.IPv4Network):
    def __init__(self):
        int_addr = random.randint(start_addr, end_addr)
        int_pref = random.randint(start_pref, end_pref)
        str_net = str(ipaddress.IPv4Address(int_addr)) + '/' + str(int_pref)
        ipaddress.IPv4Network.__init__(self, str_net, strict=False)
        self.key = IPv4RandomNetwork.key_value(self)

    def regular(self):
        return self.is_global

    def key_value(self):
        pref_shift = self.prefixlen << 32
        return pref_shift + int(self.network_address)


L = []
while len(L) < 50:
    net_addr = IPv4RandomNetwork()
    if net_addr in L: continue
    if not net_addr.regular(): continue
    L.append(net_addr)


def sortfunc(x):
    return x.key


print(len(L))
for addr in sorted(L, key=sortfunc):
    print(addr)
