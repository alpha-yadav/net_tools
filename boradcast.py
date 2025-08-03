import socket,sys
import tqdm as tq
def broadcast_message(pkts,data,ip,port): # Broadcast address   
    # Port for broadcasting

    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    for i in tq.tqdm(range(pkts*1_000_000),desc='Sending',unit=' pkt'):
        # Send the message to the broadcast address
        server_socket.sendto(data.encode(), (ip, port))

if __name__ == "__main__":
    ag=zip(sys.argv[1:len(sys.argv):2],sys.argv[2:len(sys.argv):2])
    arg={"-b":"255.255.255.255","-p":22340,"-pkt":1,"-d":"Hello, this is a broadcast message!"}
    f=False
    for i in ag:
        if(arg.get(i[0])==None):
            f=True
            print(f"Wraning: Argument {i[0]} not recognized.")
        else:
            arg[i[0]]=i[1]
        if(f):
            print("Usage: python broadcast_send.py -b <broadcast_ip> -p <port> -pkt <number_of_packets> -d <data>")
    broadcast_message(pkts=int(arg["-pkt"]), data=arg["-d"], ip=arg["-b"], port=int(arg["-p"]))