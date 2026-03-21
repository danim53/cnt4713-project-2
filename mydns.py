import sys
import socket
import random

DNS_PORT = 53

# Convert domain name into DNS label format
def encode_domain(domain):
    name = b""
    parts = domain.split(".")
    for part in parts:
        name += bytes([len(part)])
        name += part.encode()
    name += b"\x00"
    return name

# Build DNS query packet
def build_query(domain):
    query = b""
    # header
    # Transaction ID
    query += random.randint(0, 65535).to_bytes(2, "big")
    # flags
    query += (0).to_bytes(2, "big")
    # question count
    query += (1).to_bytes(2, "big")
    # answer count
    query += (0).to_bytes(2, "big")
    # ns count
    query += (0).to_bytes(2, "big")
    # ar count
    query += (0).to_bytes(2, "big")

    # question section
    query += encode_domain(domain)
    # question type is A (1)
    query += (1).to_bytes(2, "big")
    # question class = IN (1)
    query += (1).to_bytes(2, "big")

    return query

# Send query to root DNS server
def send_query(sock, query, server_ip):
    sock.sendto(query, (server_ip, DNS_PORT))

# Receive response from DNS server
def receive_response(sock):
    data, server = sock.recvfrom(1024)
    return data, server

# Parse DNS domain names (handling 0xC0 pointer compression)
def parse_name(response, offset):
    labels = []
    jumped = False
    original_offset = offset

    while True:
        length = response[offset]
        
        # End of name
        if length == 0:
            offset += 1
            break
        
        # Pointer
        elif (length & 0xC0) == 0xC0:
            if not jumped:
                original_offset = offset + 2
            jumped = True
            pointer_offset = int.from_bytes(response[offset:offset+2], "big") & 0x3FFF
            offset = pointer_offset
        
        # Regular label
        else:
            offset += 1
            labels.append(response[offset:offset+length].decode('utf-8'))
            offset += length
            
    if not jumped:
        original_offset = offset

    return ".".join(labels), original_offset

# Parse a single DNS resource record
def parse_record(response, offset):
    name, offset = parse_name(response, offset)
    
    rtype = int.from_bytes(response[offset:offset+2], "big")
    rclass = int.from_bytes(response[offset+2:offset+4], "big")
    ttl = int.from_bytes(response[offset+4:offset+8], "big")
    rdlength = int.from_bytes(response[offset+8:offset+10], "big")
    offset += 10
    
    rdata_offset = offset
    rdata = response[offset:offset+rdlength]
    offset += rdlength
    
    parsed_data = None
    
    # Type A record (IPv4)
    if rtype == 1: 
        parsed_data = socket.inet_ntoa(rdata)
    # Type NS record (Name Server)
    elif rtype == 2: 
        parsed_data, _ = parse_name(response, rdata_offset)
        
    return name, rtype, parsed_data, offset

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 mydns.py domain-name root-dns-ip")
        return

    domain_name = sys.argv[1]
    current_dns_ip = sys.argv[2]

    # create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    # Iterative lookup loop
    while True:
        print("----------------------------------------------------------------")
        print(f"DNS server to query: {current_dns_ip}")
        query = build_query(domain_name)
        
        try:
            send_query(sock, query, current_dns_ip)
            response, server = receive_response(sock)
        except socket.timeout:
            print("ERROR: DNS query timed out")
            break

        # Extract counts from header
        anscount = int.from_bytes(response[6:8], "big")
        nscount = int.from_bytes(response[8:10], "big")
        addcount = int.from_bytes(response[10:12], "big")

        print("Reply received. Content overview: ")
        print(f"  {anscount} Answers.")
        print(f"  {nscount} Intermediate Name Servers.")
        print(f"  {addcount} Additional Information Records.")

        # Skip the Question Section
        offset = 12
        _, offset = parse_name(response, offset)
        offset += 4 # Skip QTYPE (2) and QCLASS (2)

        # Parse Answers Section
        print("Answers section:")
        found_ip = False
        for _ in range(anscount):
            name, rtype, rdata, offset = parse_record(response, offset)
            if rtype == 1: # A record
                print(f"  Name: {name}")
                print(f"  IP: {rdata}")
                found_ip = True

        # If we found an answer, stop the client
        if found_ip:
            break

        # Parse Authority Section
        print("Authority Section:")
        for _ in range(nscount):
            name, rtype, rdata, offset = parse_record(response, offset)
            if rtype == 2: # NS record
                print(f"  Name: {name}")
                print(f"  Name Server: {rdata}")

        # Parse Additional Information Section
        print("Additional Information Section:")
        next_ips = []
        for _ in range(addcount):
            name, rtype, rdata, offset = parse_record(response, offset)
            if rtype == 1: # A record
                print(f"  Name: {name}")
                print(f"  IP: {rdata}")
                next_ips.append(rdata)
            # Ignoring IPv6 (Type 28 / AAAA) as per requirements

        # Pick the next server to query
        if next_ips:
            current_dns_ip = next_ips[0] # Pick the first available intermediate IP
        else:
            print("No intermediate IPs found in Additional section. Resolution failed.")
            break

    sock.close()

if __name__ == "__main__":
    main()