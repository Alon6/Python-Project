import http.client

from flask import Flask, request
import logging
import ipaddress
import socket, struct


def ip_to_long(ip):
    """
    Convert an IP string to long
    """
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]

def long_to_ip(num):
    """
        Convert a long number to ip string
    """
    return socket.inet_ntoa(struct.pack('!L', num))

app = Flask(__name__)
@app.route('/get_ip', methods=['GET'])
def get_ip():
    global curr_host
    if net_addr & curr_host != 0:
        return "All of the addresses are assigned", http.client.BAD_REQUEST
    if curr_host == ip_addr - net_addr:
        curr_host += 1
    res_addr = net_addr + curr_host
    curr_host += 1
    return long_to_ip(res_addr), http.client.OK

hostname = socket.gethostname()
ip_addr = ip_to_long(socket.gethostbyname(hostname))
subnet_mask = ip_to_long("255.255.255.0")
net_addr = ip_addr & subnet_mask
curr_host = 0

if __name__ == "__main__":

    # Create and configure logger
    logging.basicConfig(filename="log.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')

    # Creating an object
    logger = logging.getLogger()
    logger.setLevel(0)
    app.run()
