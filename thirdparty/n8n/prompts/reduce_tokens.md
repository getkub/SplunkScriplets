# 🧩 Reusable SIEM Investigation Prompt (Cache-Optimized)

Use this as your **System Prompt** (keep it 100% identical every run):

```text
You are a senior SOC analyst performing structured SIEM alert investigations.

Your task is to analyze alert data and produce a consistent, high-confidence investigation.

Follow this exact process:

1. Alert Classification
- Identify alert type (phishing, malware, lateral movement, brute force, etc.)

2. Indicator Validation
- Extract and evaluate IOCs (IPs, domains, hashes, users)
- Note suspicious vs benign indicators

3. Contextual Analysis
- Review activity patterns (time, frequency, geolocation, user behavior)
- Identify anomalies

4. False Positive Assessment
- List possible benign explanations
- State if evidence supports dismissal

5. Risk Assessment
- Assign severity: Low / Medium / High / Critical
- Justify clearly

6. Recommended Actions
- Provide specific, actionable next steps

Strict Rules:
- Do not invent data
- Base conclusions only on provided evidence
- Be concise and structured
- No unnecessary narrative

Output format (STRICT JSON):
{
  "classification": "",
  "summary": "",
  "indicators": {
    "malicious": [],
    "suspicious": [],
    "benign": []
  },
  "analysis": "",
  "false_positive": "",
  "severity": "",
  "recommended_actions": []
}
```

---

## 🔁 User Prompt (Dynamic Data Only)

This goes in your **user message / input node**:

```text
=== ALERT DATA START ===
{{SIEM_ALERT_JSON}}
=== ALERT DATA END ===
```

In n8n or Tines, this would be your variable payload.

👉 Do NOT add instructions here.
👉 Do NOT change wording.
👉 Only inject data.

---

# 🔑 Key Caching Strategies (What Actually Matters)

## 1. Freeze the “thinking brain”

Everything about:

* methodology
* rules
* output format
* investigation steps

→ must live in the **system prompt only**

If it moves or changes → cache breaks.

---

## 2. Treat user input as a data pipe

Your user prompt should behave like:

* a raw log feed
* not a conversation

Bad:

```text
Investigate this alert carefully...
```

Good:

```text
=== ALERT DATA START ===
<data>
=== ALERT DATA END ===
```

---

## 3. Zero variation means zero cost (almost)

Even tiny changes break caching:

* spacing
* wording
* ordering

Lock it down like code.

---

## 4. Don’t mix instructions with data

This is the biggest mistake in agent workflows.

If you combine:

* instructions + data

→ every run becomes “new” → no cache

---

## 5. Maximize prefix size

The bigger your static prompt:

* playbooks
* MITRE logic
* examples

…the more you save per run.

This is where tools like ChatGPT and Claude caching really pays off.

---

## 6. Keep structure identical across workflows

If you have multiple alert types:

* don’t create different prompts
* use one universal investigation template

Variation = cache loss

---

## ⚙️ Optional (High-Performance Setup)

If you want to push it further:

* Preload:

  * detection logic
  * known false positives
  * enrichment rules

* Then only pass:

  * alert-specific fields

This turns your LLM into a **semi-compiled SOC engine**

---

# 🧠 Mental Model

You’re not “sending prompts” each time.

You’re:

> Reusing a precompiled analyst brain, and just swapping the evidence.

