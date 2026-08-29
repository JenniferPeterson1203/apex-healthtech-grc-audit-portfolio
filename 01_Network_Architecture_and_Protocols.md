# 01. Apex HealthTech: Network Architecture & Protocol Communication Baseline

## 1. Executive Environment Overview
Apex HealthTech hosts a multi-tier, cloud-native healthcare analytics application within an Amazon Web Services (AWS) Virtual Private Cloud (VPC). The environment enforces strict network segmentation to ensure patient data in the database tier is isolated from direct public Internet exposure.

---

## 2. Network Topology & Segmentation

**Data Flow & Access Paths:**
* **Hospital Clients (Public Internet):** Connect over port 443 (HTTPS) to the AWS Application Load Balancer in the Public DMZ.
* **AWS Application Load Balancer:** Terminates TLS and routes internal traffic over port 8080 to the Application Cluster in the Private Subnet.
* **Linux Application Cluster:** Processes healthcare data and communicates directly with the Managed PostgreSQL Database over port 5432.
* **IT Administrators & SecOps:** Connect via Azure AD SSO and MFA to a dedicated Bastion Jump Host, then manage Linux nodes via port 22 (SSH).
* **Corporate Workstations:** Authenticate against the on-premises/cloud Windows Active Directory Domain Controller using Kerberos (port 88) and access internal file shares via SMB (port 445).

### Segmentation Zones:
* **Public Zone (DMZ):** AWS Application Load Balancer terminating external TLS.
* **Application Zone (Private Subnet):** Hardened Ubuntu Linux nodes processing application logic without public IPs.
* **Database Zone (Isolated Subnet):** Managed PostgreSQL cluster accepting ingress exclusively from the Application Zone security group.
* **Corporate Management Zone:** Windows Active Directory domain controlling internal workstation access, file shares, and role-based administrative access.

---

## 3. Baseline Protocol & OSI Mapping Matrix

The following matrix documents authorized and restricted protocol communication channels across the enterprise environment, their respective OSI model layer, functional role, and security audit baseline:

| Protocol | Standard Port | OSI Layer | Transport Layer | Direction / Path | Security Function & Audit Baseline |
| :--- | :--- | :--- | :--- | :--- | :--- |
| DNS | 53 | Layer 7 (App) | UDP / TCP | All Subnets -> Internal DNS | Resolves domain names to IP addresses. Audited for DNS tunneling and restricted to authorized internal resolvers. |
| HTTP | 80 | Layer 7 (App) | TCP | Inbound to Load Balancer | Plaintext web traffic. Blocked for direct data transport; restricted solely to automatic 301 redirection to HTTPS. |
| HTTPS (TLS) | 443 | Layer 7 (App) | TCP | Hospital Clients -> AWS ALB | Encrypted web application traffic (TLS 1.3). Protects Electronic Protected Health Information (ePHI) in transit. |
| SSH | 22 | Layer 7 (App) | TCP | Admin Bastion -> Linux Nodes | Encrypted command-line administration. Password authentication disabled; requires SSH key pairs, MFA jump box, and source IP filtering. |
| PostgreSQL | 5432 | Layer 7 (App) | TCP | Linux App -> PostgreSQL DB | Relational database connection. Blocked at perimeter; inbound access restricted strictly to App Node Security Group with TLS enforced. |
| SMB | 445 | Layer 7 (App) | TCP | Workstations -> File Server | Server Message Block for file sharing in Windows AD. Prohibited over public internet due to remote code execution risks (e.g., EternalBlue). |
| Active Directory / Kerberos | 88 / 636 | Layer 7 (App) | TCP / UDP | Workstations -> Domain Controller | Authentication and directory services. LDAPS (Port 636) enforced over plaintext LDAP (Port 389). |

---

## 4. Technical Audit & Compliance Implications
* **Data in Transit Security:** SOC 2 CC6.6 requires boundary protection and encryption across public networks. Plaintext protocols (HTTP:80, Telnet:23, FTP:21, LDAP:389) are systematically disabled or forced to encrypted equivalents.
* **Separation of Duties (SoD):** Database port 5432 is not reachable by corporate workstations or public users. Only service accounts tied to the application cluster hold database connection rights.
* **Lateral Movement Prevention:** Internal firewalls (AWS Security Groups and Network ACLs) drop all east-west traffic between non-essential services.
