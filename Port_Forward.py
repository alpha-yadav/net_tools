#PORT FORWARDING
import socket as s
import sys
def forward(src, dst):
    s.setdefaulttimeout(10)
    l=[s.socket(s.AF_INET, s.SOCK_STREAM), s.socket(s.AF_INET, s.SOCK_STREAM)]
    l[0].bind(src)
    l[0].listen(1)
    print(f'Listening on port {l[0].getsockname()}...')
    while True:
        try:
            conn, addr = l[0].accept()
        #print(f'Connection from {addr}')
            l[1]= s.socket(s.AF_INET, s.SOCK_STREAM)
            conn.settimeout(10)
            l[1].connect(dst)
            l[1].settimeout(10)
        except s.timeout:
            print(f'\033[91mTimeout occurred while connecting to {dst}\033[0m')
            return 6
        try:
            i=0
            while True:
                data = conn.recv(4096)
                if(i==0):
                    dt=data.decode()
                    #print(dt)
                    print(f'[{addr[0]}:{addr[1]}] ',end='')
                    for j in dt:
                        if j=="\n":
                            break
                        print(j,end='')
                    print("")
                l[1].send(data)
                if len(data)!= 4096:
                    break
                i+=1
            while True:
                data = l[1].recv(1024)
                if not data:
                    break
                conn.send(data)
            conn.close()
            l[1].close()
        except s.timeout:
            print(f'\033[91mTimeout occurred for [{addr[0]}:{addr[1]}]\033[0m')
            conn.close()
            l[1].close()
        except ConnectionAbortedError as e:
            print(f'\033[91mConnection aborted for [{addr[0]}:{addr[1]}]\033[0m')
            conn.close()
            l[1].close()
        except Exception as e:
            print(f'{e}')
            return e
def args():
    z=zip(sys.argv[1::2], sys.argv[2::2])
    if len(sys.argv) < 3:
        print("Usage: python Port_Forward.py -s <src_ip:src_port> -d <dst_ip:dst_port>/<dst_port>")
        sys.exit(2)
    dict_args = dict(z)
    for key in dict_args:
        a=dict_args[key].split(':')
        if(len(a)==2):
            if(a[1].isnumeric() == False):
                print(f'\033[91mInvalid port number: {a[1]}\033[0m')
                sys.exit(1)
        ip_chunk=[int(i) for i in a[0].split('.') if i.isnumeric()]
        if len(ip_chunk) != 4:
            if key=='-s'  and len(a) == 1:
                dict_args[key] = ("", int(a[0]))
                continue
            print(f'\033[91mInvalid IP address: {a[0]}\033[0m')
            sys.exit(1)
        for i in ip_chunk:
            if i < 0 or i > 255:
                print(f'\033[91mInvalid IP address: {a[0]}\033[0m')
                sys.exit(1)
        if len(a) == 2:
            dict_args[key] = (a[0], abs(int(a[1])))
        else:
            dict_args[key] = (a[0],0)
        if dict_args[key][1] < 0 or dict_args[key][1] > 65535:
            print(f'\033[91mInvalid port number: {a[1]}\033[0m')
            sys.exit(1)
    if dict_args.get('-d') is None or len(dict_args['-d']) < 2 or dict_args['-d'][1] == 0:
        print('\033[91mDestination port is required\033[0m')
        sys.exit(1)
    dict_args['-s']= ("",0) if dict_args.get('-s')==None else dict_args['-s']
    return dict_args
if __name__ == '__main__':
    dict_args = args()
    forward(dict_args['-s'], dict_args['-d'])
