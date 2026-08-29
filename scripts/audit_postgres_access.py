"""
Apex HealthTech - ITGC Control Testing Automation Script (Control AC-03)
Simulates automated verification of database role privileges against the Principle of Least Privilege (PoLP).
Author: Jennifer Peterson
"""

# 'sys' allows us to interact with the system runtime and pass exit status codes (0 for pass, 1 for fail).
import sys

# 'datetime' allows us to timestamp our audit logs so evidence is verifiable for SOC 2 compliance.
from datetime import datetime


# ==============================================================================
# 1. AUDIT DATA SOURCE (Simulated PostgreSQL 'pg_roles' System Catalog)
# In a live environment, this list of dictionaries represents the rows returned
# by running: "SELECT rolname, rolsuper, rolcanlogin FROM pg_roles;"
# ==============================================================================
DB_ROLES_INVENTORY = [
    # AWS default admin account required for RDS engine management
    {"role_name": "postgres", "is_superuser": True, "can_login": True, "owner": "AWS Managed"},
    
    # Authorized Lead DBA account (explicitly approved in access management tickets)
    {"role_name": "dba_jennifer", "is_superuser": True, "can_login": True, "owner": "Lead DBA"},
    
    # Service account used by the backend application to query clinical data (Least Privilege)
    {"role_name": "app_backend_service", "is_superuser": False, "can_login": True, "owner": "App Cluster IAM"},
    
    # Read-only analyst account for reporting dashboards
    {"role_name": "analytics_readonly", "is_superuser": False, "can_login": True, "owner": "BI Team"},
    
    # Temporary account assigned to an external contractor (Auditor Flag: Privilege Creep)
    {"role_name": "dev_intern_temp", "is_superuser": True, "can_login": True, "owner": "Contractor"},
]


# ==============================================================================
# 2. AUTHORIZED BASELINE (The "Ground Truth" approved by Security & Management)
# We use a Python 'set' ({...}) because set lookups ("if item in set") run in O(1) time.
# ==============================================================================
APPROVED_SUPERUSERS = {"postgres", "dba_jennifer"}


# ==============================================================================
# 3. CORE AUDIT FUNCTION
# Iterates through active database accounts, compares permissions against policy,
# logs compliant vs. deficient findings, and generates a remediation command.
# ==============================================================================
def audit_database_superusers(roles_data):
    # Print standard corporate header with audit scope and UTC timestamp
    print("=" * 70)
    print("APEX HEALTHTECH: AUTOMATED ITGC AUDIT LOG (Control AC-03)")
    print(f"Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("Target: PostgreSQL Cluster (Private Subnet Zone)")
    print("=" * 70)
    
    # Empty list to collect any non-compliant accounts discovered during the scan
    findings = []
    
    # Loop through each database role dictionary in our inventory
    for role in roles_data:
        role_name = role["role_name"]
        is_su = role["is_superuser"]
        owner = role["owner"]
        
        # Test 1: Check if the account has SUPERUSER (unrestricted admin rights)
        if is_su:
            # Test 2: Check if this superuser account is explicitly on the authorized whitelist
            if role_name not in APPROVED_SUPERUSERS:
                # Discovered an unapproved admin account: Record finding and log a deficiency
                findings.append({
                    "role": role_name,
                    "owner": owner,
                    "severity": "HIGH",
                    "issue": f"Unapproved SUPERUSER privilege detected on account '{role_name}'."
                })
                print(f"[!] DEFICIENCY DETECTED: Role '{role_name}' ({owner}) holds unapproved SUPERUSER privileges.")
            else:
                # Account is a superuser, but is approved on the formal DBA roster
                print(f"[+] APPROVED: Superuser '{role_name}' matches approved DBA roster.")
        else:
            # Account is not a superuser; adheres to Least Privilege
            print(f"[+] COMPLIANT: Role '{role_name}' adheres to Least Privilege (Non-Superuser).")
            
    # Print summary statistics
    print("-" * 70)
    print(f"Audit Summary: {len(roles_data)} roles audited | {len(findings)} deficiency found.")
    
    # ==========================================================================
    # 4. REMEDIATION & EXIT CODE HANDLING
    # If deficiencies are found, print direct SQL commands for engineers to fix.
    # In CI/CD pipelines, returning 1 triggers an alert or fails a compliance build.
    # ==========================================================================
    if findings:
        print("\n--- ACTION REQUIRED ---")
        for f in findings:
            # Output the exact PostgreSQL DDL command to revoke superuser rights
            print(f"• Remediation: Revoke SUPERUSER from '{f['role']}' -> Execute: ALTER ROLE {f['role']} NOSUPERUSER;")
        print("-" * 70)
        return 1  # Exit Code 1: Audit Failed (Deficiency Detected)
        
    return 0  # Exit Code 0: Audit Passed (100% Compliant)


# Standard Python boilerplate: ensures function only executes when run directly
if __name__ == "__main__":
    # Passes the exit code (0 or 1) back to the terminal or CI/CD runner
    sys.exit(audit_database_superusers(DB_ROLES_INVENTORY))
