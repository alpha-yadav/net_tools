import requests as req
from scapy.all import IP, ICMP, sr1
import sys
if(len(sys.argv)<2):
        print("ip address Require :\n python %s ip"%__file__.split('\\')[-1])
        sys.exit(1)
l=[]
TOKEN='YOUR_IPINFO_TOKEN'  # Replace with your actual token
target =sys.argv[1]
def trace(target,ttl):
    pkt = IP(dst=target, ttl=ttl) / ICMP()
    reply = sr1(pkt, timeout=1, verbose=0)
    if reply is None:
        print(f"{ttl} * * * Unknown IP")
        l.append('* * *')
    else:
        if(reply.src in l):
             return 2
        ipinfo=req.get(f'https://ipinfo.io/{reply.src}?token={TOKEN}').json()
        if(ipinfo.get('country')!=None):
            print(f'{ttl}> {reply.src} - {ipinfo["city"]}, {ipinfo["region"]}, {ipinfo["country"]}') 
        else:
            print(f'{ttl}> {reply.src} - Private IP/No Information Available')
        if reply.src == pkt.dst:
                return 1
        l.append(reply.src)
    if(len(l)>2 and l[-5:-1]+[l[-1]]==['* * *']*5):
         return 3
    return 0
for ttl in range(1, 30):
    a=trace(target,ttl)
    if(a):
         sys.exit(a)