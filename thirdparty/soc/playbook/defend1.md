# Modular SOC Playbook Design

## Is Modular Design Possible? **YES**

---

## High-Level Modular Architecture

```
Alert → D3FEND Technique → Playbook (Assembly of Modules)
```

### Core Concept
Build **reusable modules** that can be mixed/matched based on alert type

---

## Module Structure

| Module Type | Purpose | Reusability |
|-------------|---------|-------------|
| **Triage Module** | Determine if alert is real | High - same logic across many alerts |
| **Investigation Module** | Collect evidence for specific artifact | Medium - per artifact type |
| **Response Module** | Take action to stop threat | High - common actions |
| **Containment Module** | Isolate/block threat | High - by asset type |

---

## Example Modular Design

### Alert Structure
```
Alert:
  - D3FEND: LocalAccountMonitoring
  - ATT&CK: T1078.003
  - Artifact: Local User Account
  - Asset: Windows Server
```

### Playbook Assembly
```
Playbook = Triage_Module + Investigation_Module + Response_Module

Where:
  Triage_Module = "Generic_Alert_Validation"
  Investigation_Module = "User_Account_Analysis" 
  Response_Module = "Account_Containment" + "Windows_Isolation"
```

---

## Modular Components

### 1. Triage Modules (Reusable)

| Module Name | When to Use | Checks |
|-------------|-------------|--------|
| **Generic_Validation** | All alerts | False positive check, asset exists, severity scoring |
| **User_Activity_Triage** | User behavior alerts | Business hours, expected location, known user |
| **Network_Activity_Triage** | Network alerts | Known IP, expected protocol, volume check |
| **Process_Activity_Triage** | Endpoint alerts | Known binary, signed, expected path |

### 2. Investigation Modules (By Artifact)

| Module Name | Artifact Type | Actions |
|-------------|--------------|---------|
| **User_Account_Analysis** | User accounts | Check auth logs, privilege changes, failed logins |
| **Process_Analysis** | Processes | Check parent/child, command line, network connections |
| **File_Analysis** | Files | Check hash, path, signature, creation time |
| **Network_Connection_Analysis** | Network flows | Check destination, protocol, volume, duration |

### 3. Response Modules (Reusable)

| Module Name | Action Type | Steps |
|-------------|-------------|-------|
| **Account_Containment** | Disable account | Force logoff, disable AD account, revoke tokens |
| **Network_Isolation** | Block network | Firewall rule, EDR isolation, VLAN change |
| **Process_Termination** | Kill process | EDR kill, parent process check, persistence check |
| **Evidence_Collection** | Preserve data | Memory dump, disk image, log export |

### 4. Containment Modules (By Asset Type)

| Module Name | Asset Type | Actions |
|-------------|-----------|---------|
| **Windows_Isolation** | Windows endpoint | EDR isolate, disable network adapter, block at firewall |
| **Linux_Isolation** | Linux server | iptables drop, disconnect interface, kill sessions |
| **Cloud_Isolation** | Cloud resource | Security group update, disable service, snapshot |

---

## Modular Mapping Table

### D3FEND → Module Assignment

| D3FEND Technique | Triage | Investigation | Response |
|------------------|--------|---------------|----------|
| LocalAccountMonitoring | User_Activity_Triage | User_Account_Analysis | Account_Containment |
| ProcessAnalysis | Process_Activity_Triage | Process_Analysis | Process_Termination |
| NetworkTrafficAnalysis | Network_Activity_Triage | Network_Connection_Analysis | Network_Isolation |

---

## Implementation Pattern

### Option 1: SOAR-Based (Automated)
```
Alert → 
  SOAR reads D3FEND + Artifact → 
  Calls Triage_Module → 
  If confirmed → Calls Investigation_Module → 
  If malicious → Calls Response_Module
```

### Option 2: Document-Based (Manual)
```
Playbook Document:
  1. Run: Generic_Validation
  2. Run: User_Account_Analysis  
  3. If confirmed malicious:
     - Execute: Account_Containment
     - Execute: Windows_Isolation
```

---

## Benefits of Modular Design

| Benefit | Description |
|---------|-------------|
| **Reusability** | Write once, use in multiple playbooks |
| **Consistency** | Same investigation steps every time |
| **Maintainability** | Update module = update all playbooks using it |
| **Scalability** | Mix/match modules for new detection types |
| **Training** | Analysts learn modules, not entire playbooks |

---

## Simple Example

### Alert: Suspicious Local Account Login
```
Assembly:
  1. Generic_Validation (Is alert real?)
  2. User_Activity_Triage (Expected user behavior?)
  3. User_Account_Analysis (What did account do?)
  4. IF malicious:
     a. Account_Containment (Disable account)
     b. Windows_Isolation (Isolate system)
     c. Evidence_Collection (Preserve logs)
```

Each component is a **separate, reusable module**.

---
