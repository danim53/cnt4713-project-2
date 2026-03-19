import sys
import socket
import random

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

#Build DNS query packet
def build_query(domain):
    query = b""

    #header
    #Transaction ID
    query += random.randint(0, 65535).to_bytes(2, "big")
    #flags
    query += (0).to_bytes(2, "big")
    #question count
    query += (1).to_bytes(2, "big")
    #answer count
    query += (0).to_bytes(2, "big")
    #ns count
    query += (0).to_bytes(2, "big")
    #ar count
    query += (0).to_bytes(2, "big")

    #question selection
    query += encode_domain(domain)
    #question type is A
    query += (1).to_bytes(2, "big")
    #question class = in
    query += (1).to_bytes(2, "big")

    return query

    # Send query to root DNS server
def send_query(sock, query, server_ip):
    print("Sending query to root DNS server: ", server_ip)
    sock.sendto(query, (server_ip, DNS_PORT))

# Receive response from DNS server
def receive_response(sock):
    data, server = sock.recvfrom(1024)
    print("Received response from root DNS server: ", server[0])
    print("Response size: ", len(data), "bytes")
    return data

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
    sock.settimeout(5)

    print("Socket created successfully")

    query = build_query(domain_name)
    print("DNS query built successfully")

    try:
        send_query(sock, query, root_dns_ip)
        response = receive_response(sock)

    #Later steps
    #1. Parse DNS header
    #2. Print answer/authority/additional counts
    #3. Parse NS and A records
    #4. Pick next DNS server
    #5. Repeat until final A record is found

    except socket.timeout:
        print("ERROR: DNS query timed out")

    sock.close()

if __name__ == "__main__":
    main()
