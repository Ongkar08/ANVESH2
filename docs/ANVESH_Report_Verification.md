# ANVESH — Interim Project Report-I (MTE 2026) Technical Verification & Fact Sheet

**Institution:** Galgotias University, School of Computer Science & Engineering  
**Degree:** Bachelor of Technology in Computer Science & Engineering  
**Academic Session:** 2026–27  
**Evaluation Milestone:** 7th Semester Mid-Term Examination (MTE) — Interim Project Report-I (IPR-I)  
**Project Title:** ANVESH: Cyber Forensic Intelligence & Email Threat Detection Platform  
**Problem Statement Alignment:** Smart India Hackathon 2026 (Problem Statement SIH26106)  
**Audit Date:** October 2026  

---

## 1. Verified Repository Inventory & Implementation Status

Every technical claim in the Interim Project Report-I has been audited directly against the actual codebase (`c:\Users\Ongkar\Desktop\Avnesh\Anvesha-main\Anvesha-main`). No unverified or fabricated claims are permitted.

### Category A: Verified Implemented Functionality
1. **RFC-822 / MIME Email Ingestion:**
   - *Source File:* `backend/app/api/v1/endpoints/emails.py`, `backend/app/services/forensic_fusion_service.py`
   - *Implementation:* Standard Python `email.parser` ingesting raw `.eml` and multipart MIME payloads. Extracts headers (`From`, `To`, `Subject`, `Message-ID`, `Date`, `Return-Path`, `Reply-To`).
   - *Evidence Ledger:* Computes cryptographic SHA-256 fingerprint immediately upon message receipt to preserve evidence baseline.
2. **Reverse Received-Hop Traversal:**
   - *Source File:* `backend/app/services/forensic_fusion_service.py`, `backend/app/services/attribution_service.py`
   - *Implementation:* Traverses chronological `Received:` headers backwards from perimeter recipient gateway to candidate origin IP.
3. **Cryptographic Authentication Matrix (SPF / DKIM / DMARC):**
   - *Source File:* `backend/app/services/forensic_fusion_service.py`
   - *Implementation:* Evaluates `Authentication-Results` and `Received-SPF` headers, classifying results into PASS, FAIL, SOFTFAIL, NEUTRAL, and PERMERROR. Distinguishes administrative configuration issues from active domain spoofing.
4. **Model 1 — Phishing NLP Vector Classifier:**
   - *Source Files:* `ml/training/train_baseline.py`, `ml/models/phishing_baseline_v1/model.joblib`
   - *Implementation:* Scikit-learn Pipeline using TF-IDF vectorizer (1–2 n-grams, 10,000 max features, sublinear term frequency) paired with Calibrated Logistic Regression (`C=1.0`, balanced class weighting). Classifies `BENIGN` vs `THREAT_PHISHING`.
5. **Model 2 — Business Email Compromise (BEC) & Financial Coercion Detector:**
   - *Source Files:* `ml/training/train_bec_baseline.py`, `ml/models/bec_baseline_v1/model.joblib`
   - *Implementation:* TF-IDF vectorizer (1–2 n-grams, 5,000 max features, English stop words) with balanced Logistic Regression. Trained on specialized BEC datasets to detect wire transfer pressure, invoice fraud, and executive coercion.
6. **Model 3A — Identity Impersonation & Display-Name Discrepancy Engine:**
   - *Source File:* `backend/app/services/identity_impersonation_service.py`
   - *Implementation:* Heuristic discrepancy matching comparing display names against mailbox local-parts, flagging high-risk executive impersonation and `Reply-To` offsets.
7. **Model 3B — Lookalike Domain & Homoglyph Engine:**
   - *Source Files:* `ml/inference/lookalike_predictor.py`, `backend/app/services/lookalike_service.py`, `ml/models/lookalike_domain_v1/model.joblib`
   - *Implementation:* Computes 6 structural and distance metrics (Levenshtein distance, Jaro-Winkler similarity, normalized edit distance, length delta, TLD match, digit substitution index) evaluated against a curated registry of high-value corporate targets (`microsoft.com`, `paypal.com`, `apple.com`, etc.).
8. **Model 4 / 5 — Network Intrusion Anomaly Classifier (NSL-KDD Benchmark):**
   - *Source Files:* `ml/training/train_42_feature_model.py`, `backend/app/services/network_intrusion_service.py`, `ml/models/network_intrusion_v1/model.joblib`
   - *Implementation:* Random Forest classifier trained using Scikit-learn `ColumnTransformer` (One-Hot Encoding on 7 categorical features + StandardScaler on 34 continuous numerical features = 41 input telemetry features + 1 target class) on the standard NSL-KDD benchmark (`KDDTest+.arff`, 22,544 rows; tested on adversarial `KDDTest-21.arff`, 11,850 hard rows).
9. **Live Wire Packet Sniffing & PCAP Inspection (Engine 5):**
   - *Source File:* `backend/app/services/scapy_network_service.py`
   - *Implementation:* Passive packet sniffing using Windows **Npcap driver** kernel hooking, Scapy 2.7 frame decoding (Ethernet, IPv4, TCP, UDP, ICMP), 5-tuple flow aggregation, synthetic safe simulation, and Wireshark `.pcap` export.
10. **Forensic Signal Fusion & Normalized Threat Scoring:**
    - *Source File:* `backend/app/services/forensic_fusion_service.py`
    - *Implementation:* Multi-signal weighted Bayesian point synthesis normalizing contributions across Content, Identity, Infrastructure, Cryptographic Auth, and Threat Intel into a transparent 0–100 Threat Score.
11. **Attribution Boundary Safeguard (Ethical Invariant):**
    - *Source File:* `backend/app/services/attribution_service.py`
    - *Implementation:* Explicitly enforces `Actor Identity: NOT ESTABLISHED`. Technical transport headers identify network infrastructure and transit gateways only; physical human identity cannot be established without formal ISP subscriber log subpoenas.
12. **Automated Forensic Dossier PDF Generator:**
    - *Source File:* `backend/app/services/pdf_report_generator.py`
    - *Implementation:* ReportLab engine producing multi-page court-admissible dossiers complete with SHA-256 evidence digests, technical breakdown tables, and audit chains.
13. **Analyst Workstation Web UI:**
    - *Source Directory:* `web/src/`
    - *Implementation:* React 18, Vite, Tailwind CSS, Lucide icons. Responsive dark-mode SOC workstation with RFC-822 parser, live telemetry tester, cases ledger, and campaign correlation views.

---

### Category B: Partially Implemented / Fallback Components
1. **Threat Intelligence Enrichment:**
   - *Source File:* `backend/app/services/intelligence_service.py`
   - *Status:* Implemented with graceful fallback. When external API keys (VirusTotal v3, AbuseIPDB v2) are not provided in environment variables, the platform falls back to deterministic local IP range and BGP heuristics without raising runtime errors.
2. **Persistence Layer (Dual-Engine Database):**
   - *Source File:* `backend/app/database/supabase_client.py`, `backend/app/database/session.py`
   - *Status:* Configured for cloud PostgreSQL / Supabase, with automatic seamless fallback to local zero-configuration SQLite for offline or air-gapped lab testing.

---

### Category C: Planned / Future Milestone Functionality (Post-MTE)
1. **Multi-Gigabit Hardware-Accelerated Packet Capture:**
   - Transitioning from Python Scapy to kernel-bypass C++ / DPDK for 10Gbps+ enterprise trunk inspection.
2. **Automated SOAR Firewall Containment:**
   - Direct execution of host firewall isolation (`netsh advfirewall` or Linux iptables) upon critical alert confirmation.
3. **QR Code ("Quishing") Static Dissector:**
   - Optical extraction of embedded QR codes in image attachments using computer vision (`pyzbar`/`opencv`) and sandboxed redirect following.
4. **Indian Evidence Act Section 65B Certificate Generation:**
   - Dedicated legal affidavit template engine auto-populating system MAC, software checksums, and examiner declarations under the Bharatiya Sakshya Adhiniyam.
5. **Interactive 3D WebGL Multi-Hop Map:**
   - Visualizing global relay transit on a 3D globe rather than a 2D chronological table.

---

### Category D: Claims Excluded / Removed (Zero-Fabrication Compliance)
- ❌ **No claim of research paper publication, acceptance, or Scopus indexing:** The project is at the 7th Semester MTE milestone; the research paper's Introduction and Literature Review are being finalized from this report.
- ❌ **No claim of blockchain-based evidence ledger:** The ledger is cryptographically secured via local SHA-256 hash chains, not distributed ledger/blockchain networks.
- ❌ **No claim of human attacker identification:** The platform strictly enforces evidentiary neutrality (`Actor Identity: NOT ESTABLISHED`).
- ❌ **No claim of 100% detection or zero false positives:** False-positive/false-negative rates are acknowledged and documented as inherent machine learning limitations.
- ❌ **No claim of enterprise-wide production deployment:** Current operational prototype runs in local/staging workstations.

---

## 2. University Milestone & Format Compliance Verification

| Parameter | University Requirement | ANVESH Implementation Verification | Status |
| :--- | :--- | :--- | :--- |
| **Milestone** | 7th Sem MTE Exam — Interim Project Report-I | Strictly formatted as IPR-I; only Chapters 1, 2, and References included | **COMPLIANT** |
| **Cover Page** | Annexure-A sample format | Galgotias University, SCSE, B.Tech CSE, Session 2026–27, October 2026, Placeholders for Guide & Student | **COMPLIANT** |
| **Approval Form** | Progress Approval Form (Appendix-1) | Official Appendix-1 format reproduced with prominent placeholder for guide signature | **COMPLIANT** |
| **Synopsis** | Maximum 2–3 Pages | 2.5 Pages covering all 10 mandated aspects (Background, Problem, Objectives, Methodology, Status, etc.) | **COMPLIANT** |
| **Chapter 1** | Follow Annexure C Sections 1.1 – 1.7 | 1.1 Background, 1.2 Motivation, 1.3 Problem Statement, 1.4 Objectives, 1.5 Scope, 1.6 Limitations, 1.7 Organization | **COMPLIANT** |
| **Chapter 2** | Follow Annexure C Sections 2.1 – 2.5 | 2.1 Existing Techniques, 2.2 Related Research, 2.3 Comparative Table, 2.4 Research Gaps, 2.5 Summary | **COMPLIANT** |
| **Later Chapters** | Chapters 3–7 MUST NOT be included | Excluded from formal submission; report strictly concludes with References | **COMPLIANT** |
| **Page Layout** | A4, 1-inch (25 mm) margins all sides | Configured exactly to 25.4 mm (1 inch) left, right, top, bottom | **COMPLIANT** |
| **Typography** | 16pt bold main headers, 14pt sub, 12pt sub-sub, 12pt body | Exact point sizes configured in both DOCX and PDF template stylesheets | **COMPLIANT** |
| **Page Numbering** | Roman for preliminary, Arabic for Chapters | Lowercase Roman (i, ii, iii...) on Synopsis/TOC/Lists; Arabic (1, 2, 3...) starting Chapter 1 | **COMPLIANT** |
| **Captions** | Figures below, Tables above | All figures captioned below ("Figure X.Y ..."); all tables captioned above ("Table X.Y ...") | **COMPLIANT** |
| **References** | IEEE Style, genuine publications | 30 authentic peer-reviewed papers from IEEE, ACM, Springer, Elsevier, USENIX | **COMPLIANT** |

---

## 3. Figures and Tables Inventory

### List of Figures:
- **Figure 1.1:** Conceptual Multi-Vector Cyber Attack Landscape (Phishing, BEC, Homoglyphs, and Network Anomalies).
- **Figure 1.2:** High-Level Conceptual Overview of the ANVESH Unified Forensic Intelligence Architecture.
- **Figure 2.1:** Taxonomy of Modern Threat Detection Paradigms (Rule-Based, Behavioral, and Multi-Signal Fusion).
- **Figure 2.2:** Research Gap Landscape: The Disconnect Between Application-Layer Email Threat Detection, Network Telemetry, and Digital Evidence Admissibility.

### List of Tables:
- **Table 1.1:** ANVESH Project Objectives and Implementation Alignment.
- **Table 1.2:** Scope Boundaries and Operational Invariants of the ANVESH Platform.
- **Table 2.1:** Comprehensive Summary of Related Research Works in Phishing, BEC, Network Intrusion, and Forensics.
- **Table 2.2:** Comparative Analysis of Existing Email and Network Security Methodologies vs. ANVESH.
- **Table 2.3:** Identification of Key Research Gaps and ANVESH Architectural Responses.

---

*Verified and Certified for Galgotias University Capstone Project Milestone 7th Semester MTE (October 2026).*
