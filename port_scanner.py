import socket as s
import sys
import tqdm as tq
import threading as th
s.setdefaulttimeout(7)
l=[]
def scan(ip, port,Version):
    sock=s.socket(Version, s.SOCK_STREAM)
    conn=sock.connect_ex((ip, port))
    if conn==0:
        l.append(port)
__file__
if(len(sys.argv)<4):
    print("\npython %s ip starting_port ending_port"%__file__.split('\\')[-1])
    sys.exit(1)
starting_port=int(sys.argv[2])
ending_port=int(sys.argv[3])
ip=sys.argv[1]
version=s.AF_INET6
if(len(ip.split(":"))==6):
    version=s.AF_INET6
if((starting_port>=0 and starting_port<65536)*
   (ending_port>=0 and ending_port<65536) and 
   starting_port<=ending_port):
    for i in tq.tqdm(range(starting_port, ending_port+1),desc="Scanning",unit=' port'):
        #scan(sys.argv[1], i,version)
        a=th.Thread(target=scan,args=(sys.argv[1], i,version))
        a.daemon=True
        a.start()
    print(l)
else:
    print("Port Number Should be in [0,65535]")
#Port 80,443,2000,2922==ssh,5060 is open dsmnrup.in