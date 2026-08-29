# GRC & IT Audit Technical Interview Study Guide
**Portfolio Project Reference:** Apex HealthTech GRC & ITGC Audit Assessment  
**Target Roles:** GRC Analyst | IT Auditor | Security & Compliance Associate  

---

## 1. Network & Protocol Fundamentals

### Q1: What is the OSI Model, and why do auditors care about it?
* **Answer:** The Open Systems Interconnection (OSI) model standardizes network communication into 7 layers (Physical, Data Link, Network, Transport, Session, Presentation, Application). Auditors care because security controls exist at different layers:
  * **Layer 3/4 (Network/Transport):** Security Groups, Subnets, TCP/UDP port restrictions.
  * **Layer 7 (Application):** TLS encryption, HTTP headers, authentication protocols (Kerberos, OAuth, SAML).

### Q2: Why is SMB (Port 445) considered high-risk if exposed to the Internet?
* **Answer:** Server Message Block (SMB) is an internal protocol designed for local network file sharing and printer access in Windows environments. Exposing Port 445 to the public internet enables unauthenticated service enumeration and remote code execution vulnerabilities (such as EternalBlue/WannaCry). In an IT audit, a publicly exposed SMB port is classified as a critical perimeter finding.

### Q3: Why is direct HTTP (Port 80) traffic restricted in healthcare SaaS?
* **Answer:** HTTP transmits data across public networks in cleartext. For healthcare applications processing Electronic Protected Health Information (ePHI), plaintext transmission violates HIPAA Security Rule § 164.312(e)(1) and SOC 2 CC6.6. Port 80 must only exist to issue automatic 301 HTTP redirects to Port 443 (HTTPS/TLS 1.3).

### Q4: Why isolate PostgreSQL (Port 5432) into a private subnet?
* **Answer:** Implementing Defense-in-Depth and Least Privilege. Database instances containing sensitive client records should never possess public IP addresses. Ingress traffic must be restricted at the network firewall (AWS Security Group) to accept connections strictly from the Application Tier security group.

---

## 2. Access Management & Active Directory

### Q5: What is the difference between Authentication (AuthN) and Authorization (AuthZ)?
* **Answer:**
  * **Authentication (AuthN):** Verifying the user's identity (e.g., "Who are you?" proven via passwords, MFA tokens, or SSO certificates).
  * **Authorization (AuthZ):** Determining the user's permissions (e.g., "What are you allowed to do?" enforced via Role-Based Access Control / RBAC).

### Q6: What is the Principle of Least Privilege (PoLP)?
* **Answer:** A security baseline requiring that users, applications, and service accounts are granted only the minimum access rights and permissions necessary to perform their assigned job duties.

### Q7: Why do auditors perform quarterly User Access Reviews (UAR)?
* **Answer:** Over time, employees change roles, get promoted, or leave organizations, leading to "privilege creep" or orphaned active accounts. Regular access reviews ensure terminated employees are promptly deprovisioned and administrative permissions remain strictly necessary.

---

## 3. Compliance Frameworks & Audit Concepts

### Q8: What is the difference between SOC 2 Type I and SOC 2 Type II?
* **Answer:**
  * **SOC 2 Type I:** Evaluates the **design** of security controls at a single point in time (e.g., "As of August 31, did the company have an MFA policy configured?").
  * **SOC 2 Type II:** Evaluates the **operating effectiveness** of security controls over a specified period, typically 6 to 12 months (e.g., "Over the last 6 months, did every single new hire have an approved ticket before receiving database access?").

### Q9: What are IT General Controls (ITGC)?
* **Answer:** Foundational controls applied across an organization's IT infrastructure to ensure the reliability, integrity, and security of financial and operational systems. The core ITGC domains are:
  * **Logical Access:** Password policies, MFA, onboarding/offboarding, privileged account management.
  * **Change Management:** Peer review, code testing, separation of duties between developers and production environments.
  * **Computer Operations / Backup:** Automated daily backups, disaster recovery testing, incident response logging.

---

## 4. Key Terminology Cheat Sheet

| Term | Definition |
| :--- | :--- |
| **ePHI** | Electronic Protected Health Information (regulated under HIPAA). |
| **RBAC** | Role-Based Access Control (assigning permissions to roles, not individuals). |
| **Bastion / Jump Host** | A single hardened server used to access and manage isolated private instances. |
| **Inherent Risk** | The level of raw risk before any security controls or mitigations are applied. |
| **Residual Risk** | The remaining risk exposure after existing security controls have been implemented. |
| **Separation of Duties (SoD)** | Ensuring no single individual has end-to-end control over a critical process (e.g., writing code vs. deploying to production). |

---

## 5. ITGC & Audit Testing Mastery

### Q10: Why is Separation of Duties (SoD) between Developers and Production critical (CM-02)?
* **Answer:** If software developers hold direct administrative or write access to production database environments, malicious or accidental unauthorized code/data modifications can occur without oversight. Requiring changes to pass through automated CI/CD pipelines with peer approvals ensures auditability and integrity.

### Q11: What is the difference between a Design Deficiency and an Operating Deficiency?
* **Answer:**
  * **Design Deficiency:** The control policy or rule is missing or poorly planned (e.g., the company has no policy requiring MFA for contractors).
  * **Operating Deficiency:** The control is designed properly, but failed during execution (e.g., the policy requires deprovisioning within 24 hours, but one contractor account stayed active for 72 hours due to a manual ticketing lag).

### Q12: How do auditors test database user privileges in PostgreSQL (AC-03)?
* **Answer:** Auditors query system catalogs like `pg_roles` or `information_schema.table_privileges` to identify accounts with `SUPERUSER` or unrestricted `GRANT` rights, verifying that active privileges align with documented least-privilege business approvals.

---

## 6. Executive Communication & Business Alignment

### Q13: How do you explain a technical vulnerability (like an open database port) to a CFO or Board member?
* **Answer:** Frame the technical risk in terms of business impact, regulatory cost, and operational downtime. Instead of focusing only on "PostgreSQL port 5432 is open," explain: *"An exposed database creates an unmonitored entry point that could lead to an ePHI data breach, resulting in potential HIPAA regulatory fines, reputational loss, and client contract cancellations. We mitigated this by isolating the database in a private network zone, reducing our external exposure to near zero."*

### Q14: What is the difference between a SOC 2 Deficiency, Significant Deficiency, and Material Weakness?
* **Answer:**
  * **Control Deficiency:** A control does not operate as designed, but the risk of significant harm is low (e.g., one isolated contractor account took 72 hours to deprovision).
  * **Significant Deficiency:** A deficiency, or combination of deficiencies, less severe than a material weakness yet important enough to merit attention by management.
  * **Material Weakness:** A severe flaw where there is a reasonable possibility that a material breach or financial misstatement will not be prevented or detected on a timely basis.
