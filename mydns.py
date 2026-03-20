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
    sock.sendto(query, (server_ip, DNS_PORT))

# Receive response from DNS server
def receive_response(sock):
    data, server = sock.recvfrom(1024)
    return data, server

def parse_header(response):
    #Extract count (first 12 bytes) from DNS header

    #bytes 6-7 (num of answers)
    anscount = int.from_bytes(response[6:8], "big")

    #bytes 8-9 (num of NS authority records)
    nscount = int.from_bytes(response[8:10], "big")

    #bytes 10-11 (num of additional records)
    addcount = int.from_bytes(response[10:12], "big")

    print("Reply received. Content overview: ")
    print(str(anscount) + " Answers.")
    print(str(nscount) + " Intermediate Name Servers.")
    print(str(addcount) + " Additional Information Records.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 mydns.py domain-name root-dns-ip")
        return

    domain_name = sys.argv[1]
    root_dns_ip = sys.argv[2]

    # create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    print("Socket created successfully")

    query = build_query(domain_name)

    print("----------------------------------------------------------------")
    print("DNS server to query: ", root_dns_ip)

    try:
        send_query(sock, query, root_dns_ip)
        response, server = receive_response(sock)

        parse_header(response)
        print("Query packet was built and sent successfully.")
    # Later steps:
    # read Authority section (NS records)
    # read Additional section (A records)
    # match NS → IP
    # Pick next server
    # Repeat until A record is found

    except socket.timeout:
        print("ERROR: DNS query timed out")
    print("----------------------------------------------------------------")
    sock.close()

if __name__ == "__main__":
    main()
