# ES Alternative Architecture Design Summary

## Overview
Build a detection-as-code platform that loads security detections from GitHub YAML files, indexes alerts in Splunk with contextual drilldowns, and integrates with third-party case management systems - all without requiring Splunk Enterprise Security.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    GitHub Repository                             │
│              (security_content detections)                       │
│                                                                   │
│  detection.yml:                                                  │
│    - name, description                                           │
│    - search (SPL query)                                         │
│    - drilldown_searches (array)                                 │
│    - metadata (severity, MITRE ATT&CK, etc.)                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ 1. Fetch & Parse YAML
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Detection Loader Script                       │
│                                                                   │
│  Tasks:                                                          │
│  • Fetch YAML from GitHub                                       │
│  • Parse detection + drilldown_searches                         │
│  • Generate SPL for drilldown URL creation                      │
│  • Append | collect index=alerts logic                          │
│  • Create/update saved search via Splunk REST API               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ 2. Create Scheduled Searches
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Splunk Enterprise                             │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Saved Search (auto-generated)                         │    │
│  │                                                         │    │
│  │  <core detection SPL>                                  │    │
│  │  | eval alert_id=...                                   │    │
│  │  | eval drilldowns=json_array(...)                     │    │
│  │  | collect index=my_custom_alerts                      │    │
│  │  | outputlookup alerts_status_kvstore                  │    │
│  └────────────────────────────────────────────────────────┘    │
│                             │                                    │
│                             ▼                                    │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  index=my_custom_alerts (immutable)                    │    │
│  │  • alert_id (unique key)                               │    │
│  │  • alert_name, detection_id                            │    │
│  │  • severity, category                                  │    │
│  │  • result_data (detection findings)                    │    │
│  │  • drilldowns (with substituted tokens & URLs)        │    │
│  │  • metadata (MITRE, confidence, etc.)                 │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  alerts_status_kvstore (mutable)                       │    │
│  │  • _key: alert_id                                      │    │
│  │  • status: new/processing/closed                       │    │
│  │  • case_id, assigned_to                                │    │
│  │  • tags, notes                                         │    │
│  │  • updated_time, processing_attempts                   │    │
│  └────────────────────────────────────────────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ 3. Poll & Process
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│           Case Management Integration Script                     │
│                                                                   │
│  Query: index=my_custom_alerts                                   │
│         | lookup alerts_status_kvstore status                    │
│         | search status=new                                      │
│                                                                   │
│  For each alert:                                                 │
│    • Create case with drilldown links                           │
│    • Update KV store status via REST API                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ 4. Create Cases
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│         Case Management System (ServiceNow/Jira/TheHive)        │
│                                                                   │
│  Case Created With:                                              │
│    • Alert details & severity                                    │
│    • Clickable drilldown links to Splunk                        │
│    • Metadata (MITRE ATT&CK, confidence)                        │
│    • Bidirectional sync (case_id back to KV store)             │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. GitHub YAML Detection Format
```yaml
name: Detection Rule Name
description: What this detects
search: |
  index=main suspicious_activity
  | stats count by src_ip, user

drilldown_searches:
  - name: View Source Details
    search: index=main src_ip="$src_ip$"
    earliest: -24h
    latest: now
  - name: User Activity
    search: index=main user="$user$"
    earliest: -7d
    latest: now

tags:
  severity: high
  category: Network Security
  mitre_attack: [T1059]
  confidence: 85
```

### 2. Alert Event Structure (in index=my_custom_alerts)
```json
{
  "_time": "2025-12-12T10:30:15Z",
  "alert_id": "alert_20251212103015_det001_192.168.1.100",
  "alert_name": "Suspicious Network Activity",
  "detection_id": "det-001",
  "severity": "high",
  "category": "Network Security",
  
  "result_data": {
    "src_ip": "192.168.1.100",
    "user": "jdoe",
    "count": 150
  },
  
  "drilldowns": [
    {
      "name": "View Source Details",
      "url": "https://splunk.company.com/app/search/search?q=index%3Dmain%20src_ip%3D%22192.168.1.100%22&earliest=-24h&latest=now",
      "search": "index=main src_ip=\"192.168.1.100\"",
      "earliest": "-24h",
      "latest": "now"
    }
  ],
  
  "metadata": {
    "mitre_attack": ["T1059"],
    "confidence": 85
  }
}
```

### 3. KV Store Status Entry
```json
{
  "_key": "alert_20251212103015_det001_192.168.1.100",
  "status": "processing",
  "case_id": "INC0012345",
  "assigned_to": "analyst@company.com",
  "created_time": "2025-12-12T10:30:15Z",
  "updated_time": "2025-12-12T10:45:00Z",
  "tags": ["network_security", "investigated"],
  "notes": "Benign scan from vulnerability scanner",
  "processing_attempts": 1
}
```

## Data Flow

### Phase 1: Detection Loading (One-time or Scheduled)
1. Detection Loader fetches YAML from GitHub
2. Parses detection query and drilldown_searches
3. Generates SPL to:
   - Create unique alert_id
   - Substitute tokens in drilldowns ($field$ → actual values)
   - Generate Splunk URLs for each drilldown
   - Index to `my_custom_alerts`
   - Initialize status in KV store
4. Creates/updates saved search via REST API

### Phase 2: Detection Execution (Continuous)
1. Saved search runs on schedule (e.g., every 15 minutes)
2. Results written to index with:
   - Fully resolved drilldown URLs
   - All metadata and context
   - Unique alert_id
3. Initial status entry created in KV store (`status=new`)

### Phase 3: Case Management Integration (Continuous)
1. Integration script polls Splunk every 1-5 minutes:
   ```spl
   index=my_custom_alerts 
   | lookup alerts_status_kvstore alert_id OUTPUT status
   | search status=new
   ```
2. For each new alert:
   - Create case in external system with drilldown links
   - Update KV store: `status=processing`, add `case_id`
3. Bidirectional sync:
   - Case updates flow back to KV store
   - Splunk dashboard shows current case status

## Key Design Decisions

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| **Detection Source** | GitHub YAML (unchanged) | No code modifications, version controlled |
| **Alert Storage** | Splunk Index (immutable) | Audit trail, searchable, retainable |
| **Status Tracking** | KV Store (mutable) | Fast updates, no license impact |
| **Drilldowns** | Pre-generated URLs in SPL | No custom alert actions needed |
| **Integration** | Pull model (polling) | Decoupled, reliable, retry-friendly |
| **No ES Required** | Core Splunk + REST API | Cost-effective, flexible |

## Required Scripts

### 1. Detection Loader Script
- **Language**: Python (or any)
- **Frequency**: Daily or on-demand
- **Complexity**: Medium
- **Purpose**: GitHub YAML → Splunk saved searches

### 2. Case Management Integration Script
- **Language**: Python (or any)
- **Frequency**: Every 1-5 minutes
- **Complexity**: Low
- **Purpose**: Poll alerts → Create cases → Update status

## Benefits

✅ **No ES license required** - Uses core Splunk features  
✅ **Detection-as-Code** - YAML files in version control  
✅ **No custom Splunk apps** - Standard collect/outputlookup  
✅ **Immutable audit trail** - Original alerts never modified  
✅ **Flexible integrations** - Works with any case management system  
✅ **Drilldown context** - One-click investigation from cases  
✅ **Scalable** - Load hundreds of detections automatically  
✅ **Cost-effective** - Minimal license impact (KV store for status)  
✅ **Decoupled** - Systems can fail independently  
✅ **Retry-friendly** - Alerts persist until processed  

## REST API Touchpoints

1. **Detection Loader** → Splunk REST API
   - Create/update saved searches: `/servicesNS/.../saved/searches`

2. **Case Integration** → Splunk REST API
   - Query alerts: `/services/search/jobs`
   - Update KV store: `/servicesNS/.../storage/collections/data/alerts_status_kvstore`

3. **Case Integration** → Case Management API
   - Create cases: System-specific endpoint
   - Update cases: System-specific endpoint

## Example SPL Generated by Loader

```spl
`cisco_ai_defense`
| stats count by application_name, user_id
| eval severity="critical"

# Generate unique alert_id
| eval alert_id=_time."_det001_".application_name

# Generate drilldown 1
| eval d1_search="index=cisco_ai_defense application_name=\"".application_name."\""
| eval d1_url="https://splunk.company.com/app/search/search?q=".urlencode(d1_search)."&earliest=-24h&latest=now"

# Generate drilldown 2
| eval d2_search="| from datamodel Risk | search normalized_risk_object=\"".application_name."\""
| eval d2_url="https://splunk.company.com/app/search/search?q=".urlencode(d2_search)."&earliest=-7d&latest=now"

# Combine drilldowns
| eval drilldowns=json_array(
    json_object("name","View Details","url",d1_url,"search",d1_search),
    json_object("name","Risk Events","url",d2_url,"search",d2_search)
  )

# Add metadata
| eval alert_name="Cisco AI Defense Alert"
| eval detection_id="105e4a69-ec55-49fc-be1f-902467435ea8"

# Index alert (immutable)
| collect index=my_custom_alerts

# Initialize status (mutable)
| eval status="new", created_time=now(), processing_attempts=0
| outputlookup append=true alerts_status_kvstore key_field=alert_id
```

## This Design Provides

- ✅ ES-like detection management without ES
- ✅ Automated detection deployment from GitHub
- ✅ Rich context with drilldowns in every alert
- ✅ Integration with any case management platform
- ✅ Clean separation of immutable data vs workflow state
- ✅ Scalable architecture for thousands of detections
