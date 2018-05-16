from pysnmp.hlapi import *
import pprint

community_name = 'public'
ipaddr = '10.31.70.107'
port = 161
snmp_object_1 = ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)
snmp_object_2 = '1.3.6.1.2.1.2.2.1.2'


result1 = getCmd(SnmpEngine(),
                CommunityData(community_name, mpModel=0),
                UdpTransportTarget((ipaddr, port)),
                ContextData(),
                ObjectType(ObjectIdentity(snmp_object_1)))


result2 = nextCmd(SnmpEngine(),
                  CommunityData(community_name, mpModel=0),
                  UdpTransportTarget((ipaddr, port)),
                  ContextData(),
                  ObjectType(ObjectIdentity(snmp_object_2)),
                  lexicographicMode=False)


for val in result1:
    print(val[3][-1])

print()

for val in result2:
    print(str(val[3][-1]).split(' = ')[1])
