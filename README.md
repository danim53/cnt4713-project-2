# DNS Iterative Lookup Client

A simple DNS lookup client that performs **iterative DNS resolution** using **UDP socket programming in Python**.

---

## 📋 Project Overview

This project implements a command-line DNS client written in **Python 3**. The program starts with a **root DNS server** and follows referrals to intermediate DNS servers until it finds the **IPv4 address (A record)** for the requested domain.

The DNS query messages are built manually and sent using **UDP sockets**, without using any existing DNS libraries.

---

## ⭐ Key Features

- UDP socket communication
- Iterative DNS resolution
- Manual DNS query packet creation
- DNS response parsing
- Supports **A records** and **NS records**
- Displays intermediate DNS server replies
- Stops once the final IP address is found

---

## 🛠️ Technical Requirements

### Language

Python 3

### Restrictions

- Must use **socket programming**
- No external DNS libraries allowed
- Program name must be exactly **mydns**

---

## 🏗️ Program Architecture

The DNS client follows the **iterative DNS lookup process**:

1. Send a DNS query to a **root DNS server**
2. The root server returns **NS records** in the Authority section
3. The **Additional Information section** contains IP addresses of those servers
4. The program chooses one of those IPs
5. A new query is sent to that DNS server
6. The process continues until the final **A record** is returned

### Lookup Flow

Client → Root DNS Server  
↳ returns NS records and additional IP addresses  
Client → Intermediate DNS Server  
↳ returns more referrals or final answer  
Client → Authoritative DNS Server  
↳ returns final A record  
Client prints final IP address

---

## 🚀 Usage

### Starting the Program

Run the program from the command line:

`python3 mydns.py domain-name root-dns-ip`

### Example

`python3 mydns.py cs.fiu.edu 202.12.27.33`

Where:

- **domain-name** = the domain you want to resolve
- **root-dns-ip** = the IPv4 address of a root DNS server

A list of root DNS servers can be found here:

https://www.iana.org/domains/root/servers

---

## 📝 DNS Records Used

### A Record

Contains the IPv4 address for the domain being queried.

### NS Record

Contains the hostname of an intermediate name server.

### Sections Parsed

The program reads the following sections in the DNS reply:

- **Answers Section** → final IP address
- **Authority Section** → intermediate name servers
- **Additional Section** → IP addresses of those servers

---

## 🧪 Testing

### Example Test

`python3 mydns.py cs.fiu.edu 202.12.27.33`

### Verify with nslookup

`nslookup cs.fiu.edu 8.8.8.8`

The IP address returned by `nslookup` should match the result from the program.

---

## 📊 Grading Breakdown

| Component | Weight |
|---|---:|
| Send query to root DNS server | 15% |
| Receive reply from root DNS server | 15% |
| Display server reply content | 10% |
| Extract intermediate DNS server IP | 15% |
| Send query to intermediate servers | 15% |
| Receive reply from intermediate servers | 15% |
| Display IPs for queried domain name | 15% |

**Total: 100%**

---

## 📦 Files Included

- `mydns.py` – DNS lookup client implementation
- `README.md` – Member names and IDs,
Language used (Python3),
Compiling instructions (command-line only, not IDE-specific)

---

## 🔗 Resources

- RFC 1035 – DNS Message Format  
  https://www.ietf.org/rfc/rfc1035.txt

- Root DNS Servers  
  https://www.iana.org/domains/root/servers

---

## 👤 Authors

Danielle Martin
Khalil Peguero Goris
Migdony Romero
Xavier Wlliams

---

## 🎓 Course Information

**Course:** CNT 4713  
**Project:** DNS Iterative Lookup Client
