
---

## **1️⃣ Systemd-journald**

* **Type:** Daemon (`systemd-journald.service`)
* **Role:** Collects logs from:

  * Kernel (`dmesg`)
  * Systemd services (stdout/stderr)
  * Syslog messages
* **Elastic Agent collection:**

  * Elastic Agent **reads from journald** via the journal API (not directly from kernel memory).
  * Journald acts as a **buffer**, storing logs on disk (`/var/log/journal`) or in memory.
* **Kernel interaction:**

  * Journald **does get messages from the kernel**, but Elastic Agent does **not pull from kernel directly** — it talks to journald.

---

## **2️⃣ auditd**

* **Type:** Daemon (`auditd.service`)
* **Role:** Collects security/audit events: syscalls, SELinux denials, login attempts, sudo usage, etc.
* **Elastic Agent collection:**

  * There are two options:

    1. **From auditd service / audit netlink socket** (preferred, real-time)
    2. **From `/var/log/audit/audit.log` file** (older, batch reading)
* **Kernel interaction:**

  * Auditd **receives events directly from the Linux kernel via the audit subsystem**.
  * Elastic Agent can listen to the audit netlink socket **or** just read auditd’s logs — it does **not pull directly from the kernel** itself.

---

### **3️⃣ Key difference**

| Daemon   | Elastic Agent talks to       | Kernel interaction                 |
| -------- | ---------------------------- | ---------------------------------- |
| journald | journald API / journal files | journald reads kernel messages     |
| auditd   | auditd service / audit.log   | auditd receives events from kernel |

✅ So in **both cases**, Elastic Agent is **not pulling directly from the kernel**, it talks to the daemon (or the daemon’s files/socket) that is responsible for collecting events from the kernel.

---

## Elastic Agent

```mermaid
flowchart LR
    subgraph Kernel
        K[Linux Kernel]
    end

    subgraph Journald_Daemon
        J[systemd-journald]
    end

    subgraph Auditd_Daemon
        A[auditd]
    end

    subgraph Elastic_Agent
        EA[Elastic Agent]
    end

    subgraph Storage
        ELK[Elasticsearch / Kibana]
    end

    %% Flow for journald
    K -->|kernel messages| J
    ServiceLogs[systemd service stdout/stderr] --> J
    SyslogLogs[syslog messages] --> J
    J -->|journal API / files| EA
    EA --> ELK

    %% Flow for auditd
    K -->|audit events| A
    A -->|audit netlink socket or audit.log| EA
    EA --> ELK

    %% Styling
    style Journald_Daemon fill:#f9f,stroke:#333,stroke-width:2px
    style Auditd_Daemon fill:#9f9,stroke:#333,stroke-width:2px
    style Elastic_Agent fill:#ff9,stroke:#333,stroke-width:2px
```

---

## Splunk UF

```mermaid
flowchart LR
    subgraph Kernel
        K[Linux Kernel]
    end

    subgraph Journald_Daemon
        J[systemd-journald]
    end

    subgraph Auditd_Daemon
        A[auditd]
    end

    subgraph Splunk_UF
        UF[Splunk Universal Forwarder]
    end

    subgraph Storage
        SPLK[Splunk Indexer / Splunk Cloud]
    end

    %% Flow for journald logs (via files)
    J -->|/var/log/messages, /var/log/auth.log| UF
    ServiceLogs[systemd service stdout/stderr] -->|via journald → syslog| /var/log/messages
    SyslogLogs[syslog messages] -->|via journald → syslog| /var/log/messages

    %% Flow for auditd logs (via audit.log)
    A -->|/var/log/audit/audit.log| UF

    %% Forward to Splunk
    UF --> SPLK

    %% Styling
    style Journald_Daemon fill:#f9f,stroke:#333,stroke-width:2px
    style Auditd_Daemon fill:#9f9,stroke:#333,stroke-width:2px
    style Splunk_UF fill:#ff9,stroke:#333,stroke-width:2px

```
