# 05. Apex HealthTech: Third-Party Vendor Risk Assessment (TPRM)

**Vendor Evaluated:** TeleCare Connect Inc.  
**Service Type:** Cloud-hosted Telehealth Video Consultation & Scheduling API  
**Data Classification In-Scope:** Confidential / Electronic Protected Health Information (ePHI)  
**Assessment Standard:** SIG Lite (Standardized Information Gathering) & SOC 2 Type II Review  
**Assessor:** Jennifer Peterson, GRC Assessment Team  

---

## 1. Vendor Overview & Inherent Risk Scoping

Apex HealthTech integrates TeleCare Connect's REST APIs to facilitate direct video appointments between healthcare providers and patients. Because this integration processes patient identifiers and consultation metadata, the engagement carries a **High Inherent Risk**.

* **Integration Architecture:** Outbound HTTPS (TLS 1.3) API requests via OAuth 2.0 bearer tokens.
* **Hosting Environment:** Multi-tenant AWS infrastructure (US-East Region).
* **Data Transmitted:** Patient Full Name, Appointment Timestamp, Provider ID, Session Connection Token (No clinical notes stored).

---

## 2. Vendor Security Questionnaire & Evidence Evaluation

The following control areas were evaluated via TeleCare Connect's latest SOC 2 Type II report, independent penetration test executive summary, and security questionnaire:

| Domain | Control Requirement | Vendor Response / Evidence | Audit Finding & Assessment | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Certifications & Audits** | Annual independent SOC 2 Type II report with unqualified opinion covering Security & Confidentiality. | Provided SOC 2 Type II report dated June 2026 (Audit period: July 2025 – June 2026). | **Compliant:** Report issued by an accredited CPA firm with zero exceptions noted on access management controls. | **Pass** |
| **Data Encryption** | Encryption of ePHI in transit (TLS 1.3) and at rest (AES-256) with customer-managed keys (KMS). | Enforces TLS 1.3 for all REST endpoints; data at rest encrypted using AWS KMS AES-256. | **Compliant:** Verified active SSL/TLS cipher configurations and KMS envelope encryption mechanisms. | **Pass** |
| **Identity & Access** | Mandatory Multi-Factor Authentication (MFA) and quarterly access recertification for vendor engineers. | SSO enforced across corporate identity; MFA required for all AWS production access. | **Compliant:** Sampled administrative access policies; no shared or generic service credentials identified. | **Pass** |
| **Incident Notification** | Contractual commitment to notify Apex HealthTech of confirmed security breaches within 24 hours. | Vendor standard contract stated a 72-hour notification window. | **Risk Identified (Moderate):** HIPAA Business Associate Agreement (BAA) requires prompt notification to satisfy breach reporting mandates. | **Conditional** |
| **Business Continuity (BC/DR)** | Multi-Region redundancy with an RPO < 1 hour and RTO < 4 hours. | Documented automated cross-region database replication with annual failover test evidence. | **Compliant:** DR tabletop completed in Q1 2026; actual failover measured at 28 minutes. | **Pass** |

---

## 3. Residual Risk Rating & Vendor Approval Recommendation

* **Inherent Risk Score:** **16 (High)** — Direct ePHI transmission across API boundary.
* **Mitigating Vendor Controls:** Valid SOC 2 Type II report, TLS 1.3 enforcement, AWS KMS encryption, and verified DR failover procedures.
* **Residual Risk Score:** **4 (Low)** — Contained via technical mitigations and contractual safeguards.

### Approval Determination: **Approved with Conditions**
TeleCare Connect is approved for production API integration subject to the following mandatory conditions:
1. **BAA Contract Addendum:** Amend the master service agreement to enforce a **24-hour security incident notification SLA** (down from 72 hours).
2. **Credential Hardening:** Enforce automated 90-day rotation for all API access secrets, with tokens restricted strictly to IP-whitelisted egress gateways.
3. **Annual Recertification:** Re-audit TeleCare Connect annually upon delivery of their updated SOC 2 Type II report and third-party penetration test.
