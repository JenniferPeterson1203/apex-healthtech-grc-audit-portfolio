# 03. Apex HealthTech: Enterprise Cybersecurity Risk Register & Threat Assessment

## 1. Risk Assessment Methodology
This Risk Register assesses organizational, operational, and technical threats to the **Apex HealthTech** environment using a standard qualitative/semi-quantitative scoring matrix.

* **Inherent Risk Score** = Likelihood (1–5) × Impact (1–5)
* **Residual Risk Score** = Likelihood after Controls (1–5) × Impact after Controls (1–5)
* **Risk Tiers:** Critical (20–25) | High (15–19) | Medium (8–14) | Low (1–7)

---

## 2. Enterprise Risk Register

| Risk ID | Threat Scenario / Vulnerability | Inherent Likelihood (1-5) | Inherent Impact (1-5) | Inherent Score | Existing Mitigating Security Controls | Residual Likelihood (1-5) | Residual Impact (1-5) | Residual Score | Risk Treatment | Risk Owner |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RSK-01** | **Ransomware / Local Data Loss:** Workstation compromised via phishing targeting corporate active directory. | 4 | 4 | **16 (High)** | • EDR deployed on all endpoints<br>• MFA on all AD logons<br>• Immutable S3 backups with Object Lock | 2 | 2 | **4 (Low)** | Mitigate | SecOps Lead |
| **RSK-02** | **Direct Database Exposure (ePHI Breach):** PostgreSQL port 5432 exposed to the public internet via misconfigured AWS Security Group. | 3 | 5 | **15 (High)** | • Private subnet isolation (no public IP)<br>• AWS Config automated drift detection rule<br>• Security group ingress locked to App Tier | 1 | 4 | **4 (Low)** | Mitigate | Cloud Architect |
| **RSK-03** | **Third-Party Vendor SaaS Breach:** Downstream telehealth API partner suffers credential leak, exposing shared analytics data. | 3 | 4 | **12 (Med)** | • Vendor risk management (VRM) reviews<br>• Least-privilege API tokens with 90-day rotation<br>• Payload field-level tokenization | 2 | 2 | **4 (Low)** | Mitigate / Transfer | GRC Lead |
| **RSK-04** | **Privilege Creep & Orphaned Accounts:** Terminated contractors retain active access to GitHub repository or AWS console. | 4 | 3 | **12 (Med)** | • Automated HR webhook for deprovisioning<br>• Quarterly user access reviews (UAR)<br>• Session timeout after 1 hour inactivity | 1 | 3 | **3 (Low)** | Mitigate | IT Admin |
| **RSK-05** | **Insider Threat / Unauthorized DB Modification:** Rogue engineer accesses production PostgreSQL to manipulate clinical records. | 2 | 5 | **10 (Med)** | • Developers restricted to read-only staging<br>• Production changes routed via CI/CD runners<br>• Detailed SQL audit logging forwarded to S3 | 1 | 4 | **4 (Low)** | Mitigate | Lead DBA |

---

## 3. Risk Treatment Strategy Summary
* **Mitigate:** Applied technical controls (MFA, network isolation, automated CI/CD) reduced all High and Medium inherent risks to acceptable Low residual levels.
* **Continuous Monitoring:** High-impact residual areas (ePHI protection in RSK-02 and RSK-05) maintain automated alerting and strict quarterly audit cycles.
