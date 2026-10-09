# PROJECT_NAME Design System — Screen Map & Information Architecture

> **Navigation & Information Flow Across Web Workstation**

---

## 1. Web Workstation Screen Map

```
[Overview Dashboard]
    │
    ├── [Email Analyzer] ─────── Ingest .eml ───► Run Parser ───► Generate Case
    │
    ├── [Investigations / Cases]
    │       └── [Case Details (CASE-xxxx)]
    │               ├── Header Analysis & Auth Grid (SPF/DKIM/DMARC)
    │               ├── Delivery Relay Path & Probable Origin
    │               ├── Approximate GeoLocation & ASN / ISP Infrastructure
    │               ├── Observed IOCs (IPs, Domains, URLs)
    │               ├── Correlated Campaigns
    │               ├── SHA-256 Off-Chain Evidence Chain
    │               └── AI Forensic Explainer & Report Generator
    │
    ├── [Alerts Triage] ──────── Multi-criteria filter (Critical, BEC, Phishing)
    │
    ├── [Threat Campaigns] ───── Clustered attack campaigns & common infrastructure
    │
    ├── [Intelligence Hub] ───── On-demand lookup for IP, Domain, and URL
    │
    ├── [Evidence Ledger] ────── Cryptographic hash chain & audit custody records
    │
    ├── [Reports] ────────────── Formal forensic incident export (PDF/JSON)
    │
    ├── [AI Copilot] ─────────── Interactive evidence question-and-answering
    │
    └── [Settings] ───────────── API credentials, SOC thresholds, theme settings
```
