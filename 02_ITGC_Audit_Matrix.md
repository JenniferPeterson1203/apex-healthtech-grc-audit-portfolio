# 02. Apex HealthTech: IT General Controls (ITGC) Audit & Framework Mapping Matrix

## 1. Audit Scope & Framework Objectives
This audit workpaper evaluates the design and operating effectiveness of IT General Controls (ITGC) supporting the **Apex HealthTech Analytics Platform**. Controls are evaluated against criteria established by:
* **AICPA SOC 2 Type II:** Trust Services Criteria (Security, Availability, Confidentiality)
* **ISO/IEC 27001:2022:** Annex A Controls (Access Control, Operations Security, Change Management)
* **HIPAA Security Rule:** 45 CFR Part 164 Subpart C (§ 164.308, § 164.312)

---

## 2. ITGC Control Evaluation Matrix

| Control ID | Domain | Control Description | Tested Technology / System | Framework Reference | Audit Test Procedure | Test Result | Finding / Deficiency Summary |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AC-01** | Logical Access | Multi-Factor Authentication (MFA) is enforced for all corporate and administrative cloud access. | Microsoft Entra ID (Azure AD) / AWS IAM | SOC 2: CC6.1<br>ISO: A.9.4.2<br>HIPAA: § 164.312(d) | Sampled 25 active user accounts and verified MFA enrollment policy configuration in Azure AD Conditional Access. | **Effective** | All sampled accounts require FIDO2/Authenticator app prompt upon authentication. |
| **AC-02** | Logical Access | Terminated personnel access rights are revoked within 24 hours of separation. | Active Directory / HR BambooHR Feed | SOC 2: CC6.2<br>ISO: A.9.2.6<br>HIPAA: § 164.308(a)(3) | Inspected 10 employee terminations from Q2; compared HR separation timestamps against AD account deactivation logs. | **Deficiency (Low)** | 1 contractor account remained active for 72 hours post-contract end date. Remediated via automated HR webhook sync. |
| **AC-03** | Logical Access | Database administrative privileges are restricted to designated database administrators (DBAs) with annual recertification. | PostgreSQL / AWS IAM DB Auth | SOC 2: CC6.3<br>ISO: A.9.2.3<br>HIPAA: § 164.312(a)(1) | Queried `pg_roles` for accounts with `SUPERUSER` privileges; cross-referenced with approved access request tickets. | **Effective** | Only 2 named DBA accounts hold superuser access. Workstations access DB via least-privilege IAM roles. |
| **CM-01** | Change Management | Production code deployments require peer review, automated security testing, and management approval. | GitHub Enterprise / GitHub Actions CI/CD | SOC 2: CC8.1<br>ISO: A.12.1.2<br>HIPAA: § 164.312(b) | Sampled 15 pull requests deployed to production. Inspected branch protection rules and mandatory reviewer approvals. | **Effective** | Direct commits to `main` branch are blocked. 2 peer approvals and static analysis passes required before merge. |
| **CM-02** | Change Management | Developers are restricted from having direct write access to production database environments (Separation of Duties). | AWS IAM / PostgreSQL Production Cluster | SOC 2: CC6.3<br>ISO: A.12.1.4<br>HIPAA: § 164.308(a)(4) | Reviewed AWS IAM policy attachments for engineering staff and inspected PostgreSQL connection grants. | **Effective** | Developers hold read-only staging access; production deployments are executed solely by automated CI/CD runners. |
| **OP-01** | Operations & Backup | PostgreSQL databases are backed up automatically on a daily schedule, encrypted, and tested for restoration. | AWS RDS PostgreSQL / AWS Backup (KMS) | SOC 2: A1.2<br>ISO: A.12.3.1<br>HIPAA: § 164.308(7)(ii)(A) | Inspected AWS Backup daily snapshots for 30 consecutive days and verified KMS AES-256 encryption keys. | **Effective** | Point-in-time recovery (PITR) enabled with 35-day retention. Annual tabletop disaster recovery restore completed successfully. |
| **OP-02** | Logging & Monitoring | Operating system and database access logs are centralized, write-protected, and monitored for unauthorized access. | CloudWatch / Linux Syslog / AWS CloudTrail | SOC 2: CC7.2<br>ISO: A.12.4.1<br>HIPAA: § 164.312(b) | Verified log forwarding agent on Linux app servers; inspected CloudTrail bucket access control and alert triggers. | **Effective** | Logs forwarded to an isolated S3 audit bucket with Object Lock (WORM compliance) and MFA delete enabled. |

---

## 3. Auditor Summary & Recommendations
* **Control Environment Health:** 6 out of 7 sampled ITGC controls operated with complete effectiveness throughout the evaluation period.
* **Remediation Priority (AC-02):** The 72-hour deprovisioning gap was an isolated manual workflow failure for third-party contractors. Apex HealthTech integrated automated API webhooks between the HR management system and Active Directory to enforce automatic, immediate account disabling upon termination ticket closure.
