import sys
import socket

DNS_PORT = 53

#convert domain name into DNS label format
def encode_domain(domain):

    name = b""
    parts = domain.split(".")

    for part in parts:
        name += bytes([len(part)])
        name += part.encode()

    name += b"\x00"

    return name

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 mydns.py domain-name root-dns-ip")
        return

    domain_name = sys.argv[1]
    root_dns_ip = sys.argv[2]

    print("Domain Name: ", domain_name)
    print("Root DNS IP: ", root_dns_ip)
    print("DNS Port: ", DNS_PORT)

    # create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("Socket created successfully")

    # Later steps:
    # 1. Build DNS query packet
    # 2. Send query to root DNS server
    # 3. Receive response
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(query, (root_dns_ip, DNS_PORT))
    data, addr = sock.recvfrom(1024)
    print("Received message from DNS server: ", data.decode())
    sock.close()
    # 4. Parse response
    # 5. Continue iteratively until A record is found

    sock.close()

if __name__ == "__main__":
    main()
