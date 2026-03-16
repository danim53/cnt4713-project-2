import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 mydns.py domain-name root-dns-ip")
        return

    domain_name = sys.argv[1]
    root_dns_ip = sys.argv[2]

    print("Domain Name: ", domain_name)
    print("Root DNS IP: ", root_dns_ip)

if __name__ == "__main__":
    main()
