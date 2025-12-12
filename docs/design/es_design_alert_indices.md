# Immutable Alert Storage Design

## Two-Index Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Detection Triggers                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
┌───────────────────────────┐  ┌──────────────────────────────────┐
│   index=my_alert_basic    │  │   index=my_alert_details         │
│   (Core Alert Data)       │  │   (Context & Drilldowns)         │
│                           │  │                                  │
│   • alert_id              │  │   • alert_id (FK)                │
│   • detection_id          │  │   • drilldown_searches (array)   │
│   • alert_name            │  │   • original_search              │
│   • creation_time_epoch   │  │   • search_timerange             │
│   • severity              │  │   • event_count                  │
│   • category              │  │   • raw_results                  │
│   • result_summary        │  │   • metadata (extended)          │
│   • triggered_by          │  │   • artifacts                    │
└───────────────────────────┘  └──────────────────────────────────┘
         (Lightweight)                  (Verbose)
```

## Index 1: my_alert_basic (Core)

**Purpose**: Lightweight, fast queries, essential alert information only

### Sample Event Structure

```json
{
  "_time": "2025-12-12T10:30:15.000Z",
  "sourcetype": "alert:basic",
  "source": "detection_engine",
  "index": "my_alert_basic",
  
  "alert_id": "alert_20251212103015_det001_chatbot",
  "detection_id": "105e4a69-ec55-49fc-be1f-902467435ea8",
  "detection_name": "Cisco AI Defense - Prompt Injection Detected",
  "creation_time_epoch": 1702380615,
  
  "severity": "critical",
  "category": "AI Security",
  "subcategory": "Prompt Injection",
  
  "result_summary": {
    "application_name": "ChatBot-Production",
    "model_name": "gpt-4",
    "user_id": "user_12345",
    "event_action": "blocked",
    "event_count": 1,
    "risk_score": 100
  },
  
  "triggered_by": {
    "policy_name": "AI Runtime Latency Testing - Prompt Injection",
    "guardrail_type": "prompt_injection",
    "threshold_exceeded": true
  },
  
  "classification": {
    "mitre_attack": ["T1059.001"],
    "kill_chain_phase": "execution",
    "data_source": "Cisco AI Defense Alerts"
  },
  
  "priority": {
    "score": 95,
    "urgency": "high",
    "impact": "high"
  }
}
```

### Example 2: Network-based Alert

```json
{
  "_time": "2025-12-12T11:15:00.000Z",
  "sourcetype": "alert:basic",
  "index": "my_alert_basic",
  
  "alert_id": "alert_20251212111500_det042_192168",
  "detection_id": "det-042-network-exfil",
  "detection_name": "Suspicious Data Exfiltration",
  "creation_time_epoch": 1702383300,
  
  "severity": "high",
  "category": "Network Security",
  "subcategory": "Data Exfiltration",
  
  "result_summary": {
    "src_ip": "192.168.1.100",
    "dest_ip": "203.0.113.50",
    "user": "jdoe",
    "bytes_transferred": 5242880,
    "event_count": 47,
    "protocol": "https"
  },
  
  "triggered_by": {
    "rule_name": "Large Upload to External IP",
    "threshold_bytes": 1048576,
    "threshold_exceeded": true
  },
  
  "classification": {
    "mitre_attack": ["T1041"],
    "kill_chain_phase": "exfiltration",
    "data_source": "Network Traffic"
  },
  
  "priority": {
    "score": 85,
    "urgency": "high",
    "impact": "medium"
  }
}
```

---

## Index 2: my_alert_details (Context)

**Purpose**: Rich context, investigation data, drilldowns, verbose information

### Sample Event Structure

```json
{
  "_time": "2025-12-12T10:30:15.000Z",
  "sourcetype": "alert:details",
  "source": "detection_engine",
  "index": "my_alert_details",
  
  "alert_id": "alert_20251212103015_det001_chatbot",
  
  "original_search": {
    "query": "index=cisco_ai_defense | rename genai_application.application_name as application_name | stats count values(user_id) as user_id by model.model_name application_name",
    "earliest_time": "2025-12-12T10:15:00Z",
    "latest_time": "2025-12-12T10:30:00Z",
    "earliest_time_epoch": 1702379700,
    "latest_time_epoch": 1702380600,
    "duration_seconds": 900,
    "search_id": "scheduler__admin__search__RMD5f2d..."
  },
  
  "drilldown_searches": [
    {
      "name": "View Application Details",
      "description": "All events for this application in last 24 hours",
      "search": "index=cisco_ai_defense application_name=\"ChatBot-Production\"",
      "url": "https://splunk.company.com/app/search/search?q=index%3Dcisco_ai_defense%20application_name%3D%22ChatBot-Production%22&earliest=-24h&latest=now",
      "earliest": "-24h",
      "latest": "now",
      "type": "investigation"
    },
    {
      "name": "User Activity Timeline",
      "description": "All activity for this user across systems",
      "search": "index=* user_id=\"user_12345\" | timechart span=1h count by sourcetype",
      "url": "https://splunk.company.com/app/search/search?q=index%3D*%20user_id%3D%22user_12345%22%20%7C%20timechart%20span%3D1h%20count%20by%20sourcetype&earliest=-7d&latest=now",
      "earliest": "-7d",
      "latest": "now",
      "type": "timeline"
    },
    {
      "name": "Risk Analysis",
      "description": "Risk events for this application",
      "search": "| from datamodel Risk.All_Risk | search normalized_risk_object=\"ChatBot-Production\" starthoursago=168",
      "url": "https://splunk.company.com/app/search/search?q=%7C%20from%20datamodel%20Risk.All_Risk%20%7C%20search%20normalized_risk_object%3D%22ChatBot-Production%22%20starthoursago%3D168",
      "earliest": "-7d",
      "latest": "now",
      "type": "risk_correlation"
    },
    {
      "name": "Similar Alerts",
      "description": "Other alerts for this model",
      "search": "index=my_alert_basic result_summary.model_name=\"gpt-4\" severity IN (critical, high)",
      "url": "https://splunk.company.com/app/search/search?q=index%3Dmy_alert_basic%20result_summary.model_name%3D%22gpt-4%22%20severity%20IN%20(critical%2C%20high)&earliest=-30d&latest=now",
      "earliest": "-30d",
      "latest": "now",
      "type": "correlation"
    }
  ],
  
  "raw_results": {
    "event_count": 1,
    "result_rows": [
      {
        "model.model_name": "gpt-4",
        "application_name": "ChatBot-Production",
        "user_id": "user_12345",
        "event_message_type": "security_alert",
        "event_action": "blocked",
        "policy_name": "AI Runtime Latency Testing - Prompt Injection",
        "guardrail_entity_name": "Prompt Injection Detector",
        "guardrail_ruleset_type": "prompt_injection",
        "connection_name": "production_api"
      }
    ]
  },
  
  "metadata": {
    "analytic_story": ["Critical Alerts", "AI/ML Security"],
    "cis_controls": ["CIS 10"],
    "nist_controls": ["DE.AE", "DE.CM"],
    "confidence": "high",
    "data_models_used": [],
    "tags": ["ai_security", "llm", "prompt_injection", "auto_blocked"],
    "detection_version": "3",
    "last_modified": "2025-05-02"
  },
  
  "artifacts": {
    "indicators": [
      {
        "type": "application",
        "value": "ChatBot-Production",
        "context": "AI application under attack"
      },
      {
        "type": "user",
        "value": "user_12345",
        "context": "User attempting prompt injection"
      },
      {
        "type": "model",
        "value": "gpt-4",
        "context": "Target AI model"
      }
    ],
    "observables": [
      {
        "type": "policy_violation",
        "name": "AI Runtime Latency Testing - Prompt Injection",
        "action": "blocked"
      }
    ]
  },
  
  "enrichment": {
    "threat_intelligence": {
      "user_risk_score": 25,
      "application_risk_score": 10,
      "is_known_attacker": false
    },
    "asset_context": {
      "application_criticality": "high",
      "data_classification": "confidential",
      "business_unit": "Customer Support"
    }
  }
}
```

### Example 2: Network Alert Details

```json
{
  "_time": "2025-12-12T11:15:00.000Z",
  "sourcetype": "alert:details",
  "index": "my_alert_details",
  
  "alert_id": "alert_20251212111500_det042_192168",
  
  "original_search": {
    "query": "index=netflow src_ip=192.168.0.0/16 dest_ip!=192.168.0.0/16 | stats sum(bytes) as bytes by src_ip, dest_ip, user | where bytes > 1048576",
    "earliest_time": "2025-12-12T11:00:00Z",
    "latest_time": "2025-12-12T11:15:00Z",
    "earliest_time_epoch": 1702382400,
    "latest_time_epoch": 1702383300,
    "duration_seconds": 900,
    "search_id": "scheduler__admin__search__ABC123..."
  },
  
  "drilldown_searches": [
    {
      "name": "Source IP All Activity",
      "description": "Complete activity for source IP",
      "search": "index=netflow src_ip=\"192.168.1.100\"",
      "url": "https://splunk.company.com/app/search/search?q=index%3Dnetflow%20src_ip%3D%22192.168.1.100%22&earliest=-24h&latest=now",
      "earliest": "-24h",
      "latest": "now",
      "type": "investigation"
    },
    {
      "name": "Destination IP Reputation",
      "description": "Check external IP reputation and history",
      "search": "index=netflow dest_ip=\"203.0.113.50\" | stats count by src_ip | sort -count",
      "url": "https://splunk.company.com/app/search/search?q=index%3Dnetflow%20dest_ip%3D%22203.0.113.50%22%20%7C%20stats%20count%20by%20src_ip%20%7C%20sort%20-count&earliest=-30d&latest=now",
      "earliest": "-30d",
      "latest": "now",
      "type": "threat_intel"
    },
    {
      "name": "User Behavior Analysis",
      "description": "User's network activity patterns",
      "search": "index=netflow user=\"jdoe\" | timechart span=1h sum(bytes) by dest_ip",
      "url": "https://splunk.company.com/app/search/search?q=index%3Dnetflow%20user%3D%22jdoe%22%20%7C%20timechart%20span%3D1h%20sum(bytes)%20by%20dest_ip&earliest=-7d&latest=now",
      "earliest": "-7d",
      "latest": "now",
      "type": "behavioral"
    }
  ],
  
  "raw_results": {
    "event_count": 47,
    "result_rows": [
      {
        "src_ip": "192.168.1.100",
        "dest_ip": "203.0.113.50",
        "user": "jdoe",
        "bytes_transferred": 5242880,
        "protocol": "https",
        "dest_port": 443,
        "session_count": 47
      }
    ]
  },
  
  "metadata": {
    "analytic_story": ["Data Exfiltration"],
    "cis_controls": ["CIS 13"],
    "nist_controls": ["DE.CM"],
    "mitre_attack": ["T1041"],
    "confidence": "medium",
    "tags": ["exfiltration", "network", "large_upload"]
  },
  
  "artifacts": {
    "indicators": [
      {
        "type": "ipv4",
        "value": "192.168.1.100",
        "context": "Source of suspicious upload"
      },
      {
        "type": "ipv4",
        "value": "203.0.113.50",
        "context": "External destination"
      },
      {
        "type": "user",
        "value": "jdoe",
        "context": "User account performing upload"
      }
    ]
  },
  
  "enrichment": {
    "geo_ip": {
      "dest_country": "Unknown",
      "dest_asn": "AS64496",
      "dest_org": "Example Hosting"
    },
    "threat_intelligence": {
      "dest_ip_reputation": "unknown",
      "threat_feeds_matched": []
    }
  }
}
```

---

## Field Breakdown by Index

### my_alert_basic (Core)
| Field Category | Fields | Purpose |
|----------------|--------|---------|
| **Identity** | alert_id, detection_id, detection_name | Unique identifiers |
| **Timing** | _time, creation_time_epoch | When alert was created |
| **Severity** | severity, category, subcategory, priority | Risk classification |
| **Summary** | result_summary.* | Key findings (5-10 fields max) |
| **Trigger** | triggered_by.* | What caused the alert |
| **Classification** | mitre_attack, kill_chain_phase | Threat taxonomy |

**Size**: ~1-2 KB per event  
**Query Performance**: Fast (indexed fields only)  
**Use Cases**: Dashboards, counts, filtering, initial triage

### my_alert_details (Context)
| Field Category | Fields | Purpose |
|----------------|--------|---------|
| **Link** | alert_id | Foreign key to basic index |
| **Search Context** | original_search.* | Provenance and reproducibility |
| **Drilldowns** | drilldown_searches[] | Investigation paths with URLs |
| **Raw Data** | raw_results.* | Complete detection output |
| **Metadata** | metadata.* | Extended classification |
| **Artifacts** | artifacts.* | IOCs and observables |
| **Enrichment** | enrichment.* | Contextual data |

**Size**: ~10-50 KB per event  
**Query Performance**: Slower (verbose JSON)  
**Use Cases**: Deep investigation, case building, correlation

---

## Stitching Pattern (Join Query)

```spl
# Get basic alert info
index=my_alert_basic severity IN (critical, high) earliest=-24h
| table alert_id, detection_name, severity, result_summary.*

# Enrich with details
| join type=left alert_id 
    [search index=my_alert_details 
    | table alert_id, drilldown_searches{}, original_search.*, artifacts.*]

# Now you have combined view
| table alert_id, detection_name, severity, drilldown_searches{}.name, drilldown_searches{}.url
```

---

## Benefits of Two-Index Design

| Benefit | Description |
|---------|-------------|
| **Performance** | Fast queries on lightweight basic index |
| **Cost** | Can apply different retention policies |
| **Clarity** | Separation of concerns (what vs how) |
| **Flexibility** | Query basic without loading verbose details |
| **Scalability** | Basic index stays small and fast |
| **Use Case Optimization** | Dashboards use basic, investigations use details |

---

## Retention Strategy

```
my_alert_basic:   90 days (or longer) - small, frequently accessed
my_alert_details: 30 days - large, rarely accessed after initial investigation
```

---

## Key Design Principles

✅ **my_alert_basic**: Think "alert ticket" - what you'd see in a case management dashboard  
✅ **my_alert_details**: Think "investigation pack" - everything needed to dig deep  
✅ **Both immutable**: Never update, only create new alerts  
✅ **Linked by alert_id**: One-to-one relationship  
✅ **Created simultaneously**: Both written when detection triggers  
✅ **Self-contained**: Details index has everything, basic has summary  

This design allows fast triage on `my_alert_basic` while keeping complete context available in `my_alert_details` for deep investigation.
