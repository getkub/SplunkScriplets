# Agentic AI Use Cases with ElasticSearch

A set of practical, real-world examples for leveraging agentic AI capabilities on top of ElasticSearch data, designed to automate threat hunting, orchestrate response, and enrich alerts dynamically.

---

## ✅ Use Case 1: Intelligent Threat Alert Enrichment and Triage

- **Trigger**: Alert for user accessing a known malware host.
- **Agentic AI Flow**:
  1. Ingest alert (via webhook or API).
  2. Correlate IP/domain with multiple external threat intel sources (e.g. MISP, VirusTotal, AbuseIPDB) at runtime.
  3. Score severity based on malware family, behavior, and prevalence.
  4. Query Elastic for:
     - AD activity (logins, devices used)
     - Recent process execution (Sysmon)
     - Network flows (firewall logs)
  5. Ask user via email/portal:
     - “Were you aware of accessing this domain?”
     - Button: [Yes], [No]
  6. If unaware:
     - Trigger AV/EDR scan via API (e.g., CrowdStrike).
- **Outcome**: Dynamic triage and enrichment. Human interaction only when necessary.

---

## ✅ Use Case 2: Automated Lateral Movement Detection (Multi-Domain)

- **Trigger**: Suspicious login or remote execution.
- **Agentic AI Flow**:
  1. Identify potentially compromised host.
  2. Query Elastic:
     - User logins across machines
     - Host-to-host traffic (NetFlow, firewall)
     - Process trees with credential dump tools
  3. Build timeline and map user movement across systems.
  4. Score risk and recommend:
     - Host isolation
     - AD account disablement
     - Full forensic investigation
- **Outcome**: Maps out attacker movement using timeline and context.

---

## ✅ Use Case 3: Shadow Admin and Privilege Escalation Detection

- **Trigger**: Periodic or event-based detection.
- **Agentic AI Flow**:
  1. Query AD logs:
     - Group changes (e.g., Domain Admins)
     - Rights assignments (e.g., Logon as a service)
  2. Compare user roles with historical baseline.
  3. Detect execution of suspicious tools (`net user`, `whoami`, etc.)
  4. Score abnormality and escalate with context.
  5. Offer decision buttons:
     - [Auto-remediate], [Escalate to SOC], [Ignore]
- **Outcome**: Detects privilege escalation attempts with full visibility.

---

## ✅ Use Case 4: Coordinated Attack Detection via Entity Correlation

- **Trigger**: Multiple low-severity events across domains.
- **Agentic AI Flow**:
  1. Continuously ingest:
     - Failed logins
     - Rare processes
     - Network anomalies
  2. Link events using LLM:
     - Create attack timeline
     - Correlate across users, hosts, and assets
  3. Detect pattern resembling known APT or MITRE chain.
  4. Alert with consolidated narrative and evidence chain.
- **Outcome**: Proactively catches multi-stage coordinated attacks.

---

## ✅ Use Case 5: Vulnerability Exploitation Prioritization

- **Trigger**: CVE feed update or new vuln scan result.
- **Agentic AI Flow**:
  1. Ingest vulnerability scan data.
  2. Cross-check Elastic:
     - Exposure to internet (firewall/proxy logs)
     - Process activity indicating exploitation
     - Threat intel on weaponization
  3. Rank vulnerabilities by exploitation likelihood.
  4. Recommend patching or segmentation.
- **Outcome**: Focuses effort on the most dangerous and exposed risks.

---

## ✅ Use Case 6: Insider Threat Contextual Investigation

- **Trigger**: High file access volume or login to sensitive system.
- **Agentic AI Flow**:
  1. Detect anomaly (e.g., HR accessing Finance folder).
  2. Enrich user with:
     - Role and org unit
     - Resignation status from HRMS
  3. Trace file access from SMB or cloud logs.
  4. Present risk to manager with action buttons.
- **Outcome**: Investigates insider risk with contextual intelligence.

---

## ✅ Use Case 7: Stealth Data Exfiltration via Rare Protocols

- **Trigger**: High outbound traffic or upload to unknown domain.
- **Agentic AI Flow**:
  1. Enrich destination with ASN, WHOIS, threat score.
  2. Check for:
     - Compressed archive creation
     - Sensitive data access
     - Protocols like DNS tunneling or TOR
  3. Score intent as benign/malicious.
  4. Recommend:
     - Block domain
     - Open case with DPO
- **Outcome**: Detects and responds to stealth exfil attempts in real time.

---
## ✅ Use Case 9: Baseline and Anomaly Detection Using Indexed Data in ElasticSearch

- **Trigger**: Periodic baseline computation or real-time anomaly scoring on new events.

- **Agentic AI Flow**:
  1. **Identify Target Entities**:
     - Select entities to baseline:
       - User accounts
       - Hostnames
       - Applications
       - IP addresses

  2. **Index Baseline Behavior**:
     - Create new indices in ElasticSearch (or rollup indices) that store historical behavior patterns:
       - Login times per user per weekday
       - Average number of processes per hour per host
       - Average data upload volume per application per day
       - USB activity per user/device per week
     - Example:
       ```json
       {
         "user": "jdoe",
         "avg_login_hour": 9,
         "avg_daily_upload_MB": 32,
         "typical_dest_domains": ["corp.sharepoint.com", "api.dropbox.com"]
       }
       ```

  3. **Compare Incoming Events Against Baselines**:
     - When new logs arrive, agent compares them to indexed baselines:
       - Is user logging in at 2AM instead of usual 9AM?
       - Is a host uploading 10x more than its weekly average?
       - Is a new, unapproved domain being accessed?
     - Use statistical thresholds (e.g., z-score > 3) or clustering (e.g., DBSCAN) to define outliers.

  4. **Enrich and Score**:
     - Apply severity scoring based on:
       - Deviation from baseline
       - Sensitivity of asset involved
       - Presence of multiple anomalies in short span
     - Enrich event with context from baseline index (e.g., "First time accessing this domain in 90 days").

  5. **Store Detected Anomalies**:
     - Write anomalies into a dedicated index:
       - `anomaly_events-*`
       - Includes raw event, baseline reference, anomaly score, risk level
     - Optionally, visualize using Kibana lens or dashboards.

  6. **Trigger Next Action**:
     - If anomaly is high risk:
       - Open a case in SOAR platform
       - Notify analyst via Slack/Teams
       - Auto-isolate device or block outbound traffic (optional)

- **Outcome**:
  - Dynamically creates and maintains entity-level behavior profiles.
  - Enables low-latency detection of subtle and complex anomalies.
  - Reduces false positives by anchoring on real historical context.

- **Data Sources**:
  - Elastic indexes: `winlogbeat-*`, `auditbeat-*`, `sysmon-*`, `network-*`, `proxy-*`, `cloudtrail-*`
  - Baseline index: `baselines-*`
  - Anomaly index: `anomaly-events-*`

---

## 🔍 Data Sources Typically Used

- **Identity**: Active Directory, LDAP, Okta
- **Endpoint**: Sysmon, EDR (CrowdStrike, Defender ATP)
- **Network**: NetFlow, Firewall logs, Proxy
- **Application**: Web logs, CloudTrail, Auditd
- **Threat Intel**: MISP, VirusTotal, AbuseIPDB
- **Vulnerability**: Nessus, Qualys, OpenVAS
- **HR/Org**: Employee data, separation status

---

## 📌 Notes

- All use cases are **agentic** in nature — they involve the AI **deciding, querying, summarizing, and initiating** action dynamically, **without hard-coded rules or pipelines**.
- These can be integrated with **ElasticSearch, SOAR platforms, and external APIs** via custom orchestration.
