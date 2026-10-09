# ANVESH: Cyber Forensic Intelligence and Email Threat Detection Platform

**[STUDENT NAME]**, **[ADMISSION NUMBER]**  
Department of Computer Science and Engineering, School of Computer Science and Engineering  
Galgotias University, Greater Noida, Uttar Pradesh, India  

**[CO-AUTHOR NAME]**  
Department of Computer Science and Engineering, School of Computer Science and Engineering  
Galgotias University, Greater Noida, Uttar Pradesh, India  

**[GUIDE NAME]**, **[DESIGNATION]**  
Department of Computer Science and Engineering, School of Computer Science and Engineering  
Galgotias University, Greater Noida, Uttar Pradesh, India  

---

### Abstract
Email communication remains the dominant attack vector for advanced cyber threats, ranging from widespread credential harvesting to high-consequence Business Email Compromise (BEC) and targeted spear-phishing. Contemporary enterprise defense systems remain bifurcated into isolated silos: Secure Email Gateways (SEGs) evaluate message content and domain cryptographic records, while Network Intrusion Detection Systems (NIDS) analyze transport-layer telemetry, leaving security analysts without a unified, evidentially sound mechanism to correlate complex attack lifecycles. Furthermore, standard email authentication protocols such as SPF, DKIM, and DMARC authenticate server authorization rather than human intent, creating severe operational blindspots when adversaries leverage compromised legitimate accounts. In response to these challenges, this paper presents **ANVESH**, an integrated cyber forensic intelligence and threat detection prototype developed under Smart India Hackathon Problem Statement SIH26106. ANVESH synthesizes multi-layered technical observables—including RFC-822 header routing chains, linguistic urgency indicators, algorithmic lookalike domain heuristics, and transport-layer network anomalies—into a transparent, bounded 0–100 threat assessment model. To ensure evidentiary integrity during legal and forensic examination, the platform incorporates strict SHA-256 cryptographic digests upon artifact ingestion and maintains an immutable chain of custody. Crucially, the platform enforces an ethical forensic invariant: infrastructure and transport-layer artifacts establish technical origin paths but do not by themselves establish human actor identity. This paper establishes the theoretical foundation, problem context, and extensive literature review required for the 7th-semester research milestone, identifying six critical research gaps that motivate the unified ANVESH architecture.

**Keywords:** Cyber Forensics, Email Threat Detection, Phishing Detection, Business Email Compromise, Lookalike Domains, Network Anomaly Detection, Digital Evidence Integrity, Threat Signal Fusion.

---

## 1. INTRODUCTION

### 1.1 Background
Over the past three decades, electronic mail has served as the foundational communication protocol of global commerce, governance, and institutional collaboration. However, the architectural foundation of the Internet Message Format, formalized in RFC 822 and updated in RFC 5322 [30], was developed in an era characterized by mutual institutional trust. The core protocol lacked native mechanisms for sender identity verification, cryptographic message non-repudiation, and structural payload authentication. Consequently, adversaries have systematically weaponized email as the primary ingress vector for modern cyber attacks [1], [2].

Modern email-borne threats have evolved significantly beyond unstructured, high-volume spam. Threat actors routinely execute sophisticated social engineering campaigns that manipulate cognitive heuristics—such as authority, scarcity, social proof, and urgency [3], [29]—to bypass user vigilance and technical perimeter controls. These campaigns manifest across a diverse operational spectrum:
1. **Credential Phishing:** Deceptive communications engineered to harvest organizational credentials by impersonating legitimate identity providers, cloud collaboration platforms, or financial institutions [10], [12].
2. **Business Email Compromise (BEC):** Text-focused financial fraud characterized by the absence of malicious attachments or weaponized hyperlinks. BEC relies on sophisticated impersonation of chief executives, corporate legal counsel, or vetted external vendors to fraudulently redirect high-value wire transfers [16], [17].
3. **Identity and Display-Name Spoofing:** Exploitation of disparities between the user-facing display name and the underlying Simple Mail Transfer Protocol (SMTP) envelope sender address [22].
4. **Algorithmic Lookalike Domains:** The strategic registration of visually deceptive domain names utilizing typographical permutations (typosquatting), character insertion (combosquatting), and Unicode homoglyphs to deceive both human recipients and automated filters [13], [14], [28].

Simultaneously, enterprise defense mechanisms have evolved to inspect network traffic flows and transport session dynamics [8], [26]. However, in modern Security Operations Centers (SOCs), email security tools and network monitoring tools operate as decoupled telemetry islands. When a targeted email payload establishes initial access and subsequently initiates command-and-control (C2) beaconing, analysts are forced to manually correlate disconnected logs across disparate vendor consoles [18], [19]. Digital forensics and incident response (DFIR) teams require an integrated technological paradigm capable of evaluating email artifacts, correlating post-delivery network telemetry, and preserving defensible digital evidence.

### 1.2 Problem Context
Investigating a suspicious email requires an analyst to navigate a fragmented analytical workflow. When a suspicious message is flagged, the examination typically demands:
* Extracting and inspecting raw RFC-5322 transport headers to identify chronological `Received:` transit hops and determine the perimeter ingress relay [30].
* Evaluating cryptographic domain authentication records, specifically Sender Policy Framework (SPF) [4], DomainKeys Identified Mail (DKIM) [5], and Domain-based Message Authentication, Reporting, and Conformance (DMARC) [6].
* Analyzing the semantic content of the message body and subject line for linguistic urgency, executive coercion, or anomalous wire transfer instructions [16].
* Interrogating DNS registries, Whois records, and string similarity metrics for suspicious lookalike domains or deceptive top-level domains (TLDs) [14], [28].
* Correlating IP addresses extracted from message hops against local network telemetry and network intrusion detection logs [15], [25].
* Cataloging Indicators of Compromise (IOCs) and preparing structured evidentiary dossiers for institutional stakeholders or law enforcement cyber cells [19], [21].

In prevailing organizational practice, this investigative pipeline is executed across distinct, disconnected point solutions. Security personnel utilize command-line utilities for header extraction, third-party web portals for domain reputation lookups, dedicated sandboxes for attachment detonation, and centralized SIEM consoles for network log correlation. This telemetry fragmentation introduces severe latency during active incident triage and increases the likelihood of investigative oversight.

Crucially, existing defenses exhibit a critical conceptual limitation regarding email authentication. While SPF verifies that the transmitting mail server is authorized by the sender domain's DNS owner [4], and DKIM verifies that the email body and specified headers have not undergone in-transit tampering [5], **neither protocol evaluates message intent**. An email transmitted from a legitimate corporate account compromised via credential stuffing or session hijacking will achieve valid SPF, DKIM, and DMARC alignment. Consequently, automated gateways that conflate cryptographic authentication with message benignity routinely deliver high-consequence BEC attacks directly to user inboxes [16], [22].

### 1.3 Motivation
The development of ANVESH is motivated by four interrelated operational and theoretical imperatives:
1. **The Authenticated Malicious Message Paradox:** As organizations enforce strict DMARC rejection policies, sophisticated adversaries have shifted toward compromising legitimate mailboxes or utilizing legitimate cloud email infrastructure (e.g., Microsoft 365, Google Workspace). When an email passes SPF and DKIM, conventional heuristic filters reduce their threat posture. A robust forensic engine must decouple domain authorization status from behavioral and linguistic risk analysis [16], [17].
2. **Fragmentation of Forensic Telemetry:** Cyber forensic investigators face severe operational friction when pivoting between application-layer email artifacts and transport-layer network logs. Correlating an external relay IP observed in an email header with internal network traffic requires cross-silo data ingestion. An integrated workbench that unifies email dissection and network anomaly analysis accelerates triage [8], [15].
3. **Fragility of Digital Evidence Chains:** Digital evidence is inherently volatile and susceptible to claims of spoliation or tampering during legal proceedings. Standard triage workflows frequently rely on unstructured screenshots, manual text copies, or mutable database records. Adherence to internationally recognized forensic standards [19], [21] demands that evidence be cryptographically sealed via cryptographic hashing immediately upon acquisition.
4. **The Attribution Conflation Risk:** Commercial security dashboards frequently present geolocation data or IP Whois ownership as direct proof of "attacker identity." In digital forensics, transport-layer hops reflect network infrastructure, proxy nodes, or compromised intermediate relays—not physical human actors. Premature or unsupported attribution introduces severe legal liability and investigative misdirection [19], [20].

### 1.4 Research Problem
The central research problem addressed by this study is formulated as follows:

> *How can suspicious electronic mail artifacts and associated multi-vector threat indicators be ingested, analyzed, and correlated through a unified, explainable cyber-forensic workflow that preserves strict cryptographic evidence integrity while explicitly preventing unsupported human-attribution claims?*

To address this problem, the analytical framework must establish a clear theoretical separation between **infrastructure-level observables** and **actor identity**. Within the context of this research, technical headers, Autonomous System Numbers (ASNs), geographic IP resolutions, and transmission relays are formally modeled as *computational transport infrastructure*. In the absence of lawful subscriber logs, physical device seizures, and authenticated forensic corroboration, the platform enforces the formal evidentiary invariant:
$$\text{Actor Identity} = \text{\textbf{NOT ESTABLISHED}}$$

### 1.5 Objectives and Research Direction
The primary research direction focuses on designing, formalizing, and prototyping an integrated cyber forensic intelligence framework. Specific research objectives include:
1. Developing an automated ingestion and dissection pipeline for raw RFC-822 / RFC-5322 electronic mail payloads, supporting multi-part MIME parsing and recursive `Received:` hop traversal.
2. Formalizing an independent cryptographic authentication verification matrix that parses and audits SPF, DKIM, and DMARC alignment states without treating authentication as proof of benign intent.
3. Formulating natural language processing (NLP) feature extractors based on term frequency-inverse document frequency (TF-IDF) n-grams to detect linguistic urgency, deceptive calls to action, and credential harvesting patterns.
4. Designing a specialized behavioral detection model tailored to Business Email Compromise, isolating linguistic coercion, executive authority invocation, and fraudulent wire transaction pressure.
5. Implementing algorithmic string similarity and edit-distance heuristics (Levenshtein, Jaro-Winkler) coupled with machine learning classifiers to detect lookalike and homoglyph domain impersonation against high-value organizational targets.
6. Integrating transport-layer network anomaly detection capabilities using standardized 41-feature network telemetry representations (NSL-KDD benchmark) to correlate host-level intrusion indicators with message routing infrastructure.
7. Establishing an immutable evidence preservation ledger utilizing SHA-256 cryptographic digests computed at the instant of payload ingestion to guarantee evidential chain of custody.
8. Constructing a transparent, bounded 0–100 multi-signal threat scoring engine that outputs auditable, explainable component scores rather than opaque, uncalibrated probabilities.

### 1.6 Contribution of the Work
The principal contribution of this research lies in the **architectural integration and evidentially sound synthesis** of multi-vector cybersecurity observables into a unified forensic intelligence framework. Specifically, this work:
* Proposes a unified defense-in-depth workflow that bridges the longstanding operational divide between application-layer email text analysis, transport header verification, and network intrusion telemetry.
* Formulates a decoupled risk evaluation paradigm wherein cryptographic email authentication records (SPF/DKIM/DMARC) are audited as infrastructure properties rather than trusted determinants of benign intent.
* Embeds cryptographic integrity verification (SHA-256) directly into the triage pipeline, producing structured, tamper-evident forensic dossiers suitable for legal scrutiny and institutional accountability.
* Enforces an ethical attribution boundary that prevents the systemic conflation of network routing infrastructure with human criminal identity.

Importantly, this work does not claim the invention of novel machine learning classification algorithms in isolation; rather, its academic and engineering contribution resides in the **principled fusion, explainable risk modeling, and forensic hardening** of established analytical methodologies within a cohesive threat intelligence architecture.

---

## 2. LITERATURE REVIEW

### 2.1 Existing Threat Detection Approaches
Organizational defense against cyber threats has historically relied on two primary paradigms: rule-based signature matching and behavioral anomaly detection [7], [8], [26].

Signature-based filtering operates by matching incoming digital artifacts against static databases of known malicious signatures, file checksums, regular expressions, or blacklisted IP addresses. In the domain of electronic mail, open-source and commercial engines such as Apache SpamAssassin [7] pioneered heuristic scoring based on static rules, header discrepancies, and distributed spam blacklists (DNSBL). Similarly, in network security, systems such as Snort [8] inspect packet payloads for predefined byte sequences characteristic of exploit attempts. While computationally efficient and capable of achieving near-zero false-positive rates on known attack patterns, signature-based approaches fail catastrophically against zero-day exploits, polymorphism, and social engineering attacks that contain no executable malware [18], [26].

To overcome the fragility of static rules, contemporary security systems employ behavioral anomaly detection and statistical machine learning [10], [23]. These systems model baseline operational behavior—such as normative communication frequencies, login locations, or packet flow distributions—and flag statistical deviations. However, as demonstrated by Sommer and Paxson [18], the application of machine learning to intrusion detection faces fundamental challenges: high costs associated with false positives, the absence of comprehensive closed-world training data, and the enormous semantic gap between detecting an anomaly and diagnosing a malicious intrusion.

### 2.2 Email Authentication Protocols
To mitigate identity spoofing and establish sender accountability, the Internet Engineering Task Force (IETF) standardized three foundational cryptographic and DNS-based authentication mechanisms:
* **Sender Policy Framework (SPF, RFC 7208):** SPF allows domain owners to publish DNS TXT records specifying the IP addresses authorized to transmit emails using their domain in the SMTP `MAIL FROM` envelope identity [4]. While effective at preventing naive envelope spoofing, SPF possesses well-documented limitations: it does not validate the user-visible `From:` header, breaks during automated email forwarding (as the forwarding MTA is not in the original sender's SPF record), and offers no protection against lookalike domains [9], [22].
* **DomainKeys Identified Mail (DKIM, RFC 6376):** DKIM provides cryptographic message integrity and sender domain association by attaching a digital signature to the email header [5]. The transmitting mail server signs designated headers and a cryptographic hash of the message body using its private key, while the recipient verifies the signature using the sender's public key published in DNS. Although DKIM survives message forwarding, it is computationally intensive, does not authenticate the user-facing display name, and does not specify what action a receiver should take if verification fails [9], [22].
* **Domain-based Message Authentication, Reporting, and Conformance (DMARC, RFC 7489):** DMARC bridges SPF and DKIM by requiring "identifier alignment" between the authenticated domain and the domain displayed in the user-visible `From:` header [6]. Furthermore, DMARC allows domain owners to publish explicit enforcement policies (`none`, `quarantine`, `reject`) and request aggregate diagnostic reporting.

Despite widespread adoption, empirical studies by Durumeric et al. [9] and Foster et al. [22] highlight systemic vulnerabilities across the authentication ecosystem. Millions of enterprise domains either maintain permissive DMARC policies (`p=none`) or misconfigure SPF records with trailing `+all` or ambiguous `~all` directives. More fundamentally, these protocols validate *domain authorization*, not *message safety*. An adversary operating a legitimate email account compromised via session hijacking or purchasing a newly registered domain with valid SPF/DKIM records can bypass authentication checks entirely [16], [22].

### 2.3 Phishing Detection and Natural Language Processing
Automated phishing detection using machine learning and Natural Language Processing (NLP) has been extensively investigated over the past two decades [10]–[12], [23].

Early research focused on manual feature engineering. Basnet et al. [10] and Toolan and Carthy [11] demonstrated that extracting structural features (e.g., number of links, presence of IP-based URLs, JavaScript tags, and vocabulary richness) paired with classical classifiers (Support Vector Machines, Random Forests, Decision Trees) could classify high-volume phishing emails effectively. Subsequent research shifted toward text-level lexical analysis using Bag-of-Words and Term Frequency-Inverse Document Frequency (TF-IDF) representations [11], [23]. By evaluating sublinear term frequencies across character and word n-grams, linear classifiers such as Calibrated Logistic Regression achieve robust, computationally lightweight baseline detection for mass-market credential harvesting templates [12].

In recent years, deep learning and transformer-based architectures (e.g., BERT, RoBERTa) have been widely explored for semantic phishing analysis [12], [23]. While transformer models achieve high empirical accuracy on benchmark datasets, their deployment in high-throughput enterprise pipelines is constrained by significant computational inference overhead, high latency, and pronounced vulnerability to adversarial text perturbation (e.g., zero-width space injection, character homoglyphs). Furthermore, deep neural networks function as uncalibrated black boxes, providing opaque probability scores that fail to offer defensible explanations during formal forensic or legal proceedings [18], [19].

### 2.4 Business Email Compromise and Social Engineering Detection
Business Email Compromise (BEC) represents a distinct class of social engineering characterized by low technical footprint and immense financial loss [1], [16]. Unlike traditional phishing, BEC emails typically contain no hyperlinks, no malware attachments, and no overt technical anomalies. The attack vector relies entirely on psychological manipulation, linguistic urgency, and authority impersonation [3], [29].

Ho et al. [16] conducted an empirical study of BEC attacks at scale across enterprise environments, demonstrating that attackers systematically target financial workflows through two predominant strategies: executive impersonation (requesting urgent, confidential wire transfers) and vendor invoice fraud (intercepting legitimate invoice exchanges to update beneficiary banking credentials). Dreiseitl et al. [17] analyzed the linguistic properties of corporate compromise, establishing that BEC messages exhibit distinct semantic markers: compressed linguistic urgency, appeals to executive confidentiality, explicit circumvention of standard internal review procedures, and pressure for immediate banking action.

Detecting BEC requires models trained specifically on financial fraud corpora. Because traditional spam filters heavily weight URL counts and attachment signatures, they consistently classify text-only BEC emails as legitimate business correspondence [16]. Consequently, dedicated linguistic models focused on financial transaction terminology, executive authority cues, and coercive urgency represent a critical component of multi-signal threat defense [17].

### 2.5 Lookalike and Homoglyph Domain Detection
Adversaries frequently register deceptive domain names that visually mimic legitimate enterprise entities to facilitate credential theft and executive impersonation [13], [14], [28].

Szurdi et al. [13] and Agten et al. [14] conducted longitudinal studies analyzing typosquatting (exploiting user keyboard typographical errors, e.g., omitting or swapping adjacent characters) and combosquatting (combining a legitimate trademark with keywords such as `-login`, `-support`, or `-portal`). Beyond standard ASCII permutations, attackers exploit Internationalized Domain Names (IDNs) via Punycode encoding to execute homoglyph attacks—substituting Latin characters with visually indistinguishable glyphs from Cyrillic or Greek alphabets (e.g., replacing Latin 'a' with Cyrillic 'а') [14], [24], [28].

Algorithmic detection of lookalike domains relies on string metric calculations, primarily Levenshtein edit distance and Jaro-Winkler similarity [24], [28]. Wang et al. [28] demonstrated that combining lexical edit distances with domain-specific structural metrics (length delta, token permutation index, and high-risk top-level domain associations) within an ensemble classifier allows accurate categorization of deceptive domains. However, domain similarity heuristics evaluated in isolation produce false positives when legitimate organizations register multi-brand domains. Lookalike detection must therefore be correlated with message-level authentication and routing telemetry [14], [28].

### 2.6 Network Intrusion Detection and the NSL-KDD Benchmark
Network Intrusion Detection Systems (NIDS) inspect transport- and network-layer packet dynamics to identify reconnaissance, lateral movement, denial-of-service, and unauthorized data exfiltration [8], [26].

The evaluation of machine learning algorithms for network intrusion detection has historically depended on standardized benchmark datasets, most notably the KDD Cup 1999 dataset and its curated revision, NSL-KDD [15], [25]. Proposed by Tavallaee et al. [15], NSL-KDD resolved critical statistical deficiencies of KDD Cup 99—specifically removing redundant records and balancing class distributions to prevent machine learning algorithms from becoming biased toward frequent benign traffic patterns. The dataset characterizes connection sessions across 41 distinct features spanning basic protocol properties (duration, protocol type, service, source/destination bytes), domain-specific content flags (failed logins, root shell access), and time-based network traffic statistics (SYN error rates, host connection counts) [15].

Despite its ubiquity in academic literature, the limitations of NSL-KDD must be explicitly acknowledged. As highlighted by Ring et al. [25] and Sommer and Paxson [18], synthetic network benchmarks do not reflect the complex latency distributions, encrypted packet dynamics, or multi-gigabit throughput rates of modern production networks. In the ANVESH research architecture, NSL-KDD is utilized as a standardized baseline benchmark for evaluating multi-class tabular classification algorithms (e.g., Random Forest), while operational packet inspection relies on live Scapy and Npcap capture engines [8], [26].

### 2.7 Digital Evidence Integrity and Cyber Forensics
The preservation of digital evidence is governed by strict legal and scientific standards to ensure admissibility in court proceedings [19]–[21]. In jurisdictions worldwide, including statutory provisions under international common law and the Indian Evidence framework (Bharatiya Sakshya Adhiniyam / Indian Evidence Act Section 65B), electronic records must maintain a verifiable, unbroken chain of custody [19].

Foundational models of digital investigation, established by Carrier and Spafford [20] and Reith et al. [27], define four invariant phases: acquisition, preservation, analysis, and presentation. The preservation phase dictates that digital evidence must be captured in an unaltered state and protected against intentional or accidental modification [21]. Cryptographic hashing algorithms, particularly the Secure Hash Algorithm (SHA-256), serve as the international standard for establishing mathematical integrity digests [19], [21]. An ingested email or packet capture whose cryptographic hash matches its post-analysis hash provides indisputable proof of evidential constancy.

Furthermore, digital forensic treatises by Casey [19] emphasize the vital distinction between **observable physical artifacts** and **investigator inference**. An investigator who observes an IP address in an email header has observed a transport infrastructure routing event. Asserting that the owner of that IP address is the human attacker constitutes an unverified deductive leap. Responsible forensic tooling must enforce this boundary programmatically, presenting technical facts while withholding premature actor attribution [19], [20].

### 2.8 Literature Synthesis and Research Gap Analysis
A comprehensive synthesis of the surveyed literature reveals that while individual cybersecurity disciplines—natural language processing for email filtering, cryptographic identity standards, homoglyph string metrics, network intrusion benchmarking, and digital evidence hashing—have advanced substantially, they operate as **disconnected technical silos**.

Specifically, this study identifies five fundamental research and engineering gaps:

1. **Gap 1: The Authenticated BEC Gateway Blindspot.** Existing email security solutions heavily weight SPF, DKIM, and DMARC passes to determine message trustworthiness [9], [22]. When attackers conduct BEC attacks from compromised legitimate Microsoft 365 or Google Workspace accounts, or newly configured domains with valid cryptographic records, existing gateways experience catastrophic failure [16], [17]. A dedicated forensic architecture must evaluate behavioral and financial coercion independently of cryptographic authentication status.
2. **Gap 2: Telemetry Siloing Between Application-Layer Email and Transport-Layer Network Telemetry.** Current enterprise architectures treat email analysis and network intrusion detection as entirely separate operations [8], [15], [18]. A phishing email that successfully drops a payload initiates network-level C2 traffic, yet the analyst has no automated mechanism to correlate the email's origin infrastructure with host-level network flows. A unified workflow bridging Layer 7 email parsing and Layer 3/4 packet inspection is sorely needed.
3. **Gap 3: Opacity and Inadmissibility of Black-Box Threat Scores.** Contemporary deep learning architectures output uncalibrated, unexplainable probability distributions [12], [18]. In legal proceedings and forensic audits, opaque probability claims fail evidential standards. Analysts require transparent, explainable threat scoring frameworks that decompose risk into human-auditable component deductions [19].
4. **Gap 4: Absence of Embedded Evidence Integrity in Triage Workflows.** Standard email triage interfaces permit operators to view, alter, or export messages without computing instantaneous cryptographic digests [19], [21]. When cases transition to formal law enforcement investigation, evidence integrity is vulnerable to legal challenge. Forensic platforms must embed SHA-256 cryptographic sealing directly into the ingestion pipeline.
5. **Gap 5: Premature Human Attribution and Conflation of Infrastructure with Actors.** Existing commercial threat intelligence platforms routinely map IP geolocations or domain registrants directly to "attackers." Such practices conflate technical transport infrastructure (proxies, VPNs, compromised relays) with human identity, violating fundamental forensic principles [19], [20]. Systems must enforce formal invariants declaring that technical headers establish routing paths, while actor identity remains strictly unestablished.

The surveyed literature demonstrates a clear scientific and engineering opportunity for an integrated, evidence-preserving, and explainable cyber forensic intelligence platform. By addressing these five identified gaps through a unified architectural framework, the ANVESH project establishes a defensible, multi-vector foundation for modern digital investigation and threat detection.

---

## REFERENCES

[1] Federal Bureau of Investigation (FBI) Internet Crime Complaint Center (IC3), "Internet Crime Report 2023," Federal Bureau of Investigation, Washington, D.C., Technical Report, Apr. 2024. [Online]. Available: https://www.ic3.gov/Media/PDF/AnnualReport/2023_IC3Report.pdf

[2] Verizon Enterprise Solutions, "2024 Data Breach Investigations Report (DBIR)," Verizon, New York, NY, Technical Report, May 2024.

[3] R. B. Cialdini, *Influence: The Psychology of Persuasion*, Rev. ed. New York, NY, USA: Harper Business, 2021.

[4] S. Kitterman, "Sender Policy Framework (SPF) for Authorizing Use of Domains in Email, Version 1," RFC 7208, Internet Engineering Task Force (IETF), Apr. 2014. [Online]. Available: https://www.rfc-editor.org/info/rfc7208

[5] D. Crocker, T. Hansen, and M. Kucherawy, "DomainKeys Identified Mail (DKIM) Signatures," RFC 6376, Internet Engineering Task Force (IETF), Sep. 2011. [Online]. Available: https://www.rfc-editor.org/info/rfc6376

[6] M. Kucherawy and E. Zwicky, "Domain-based Message Authentication, Reporting, and Conformance (DMARC)," RFC 7489, Internet Engineering Task Force (IETF), Mar. 2015. [Online]. Available: https://www.rfc-editor.org/info/rfc7489

[7] Apache Software Foundation, "Apache SpamAssassin: The Powerful #1 Open-Source Spam Filter," Apache Software Foundation, Forest Hill, MD, Documentation, 2023. [Online]. Available: https://spamassassin.apache.org/

[8] M. Roesch, "Snort: Lightweight Intrusion Detection for Networks," in *Proc. 13th USENIX Conf. System Administration (LISA '99)*, Seattle, WA, USA, 1999, pp. 229–238.

[9] Z. Durumeric, D. Adrian, A. Mirian, J. Kasten, E. Bursztein, N. Lidzborski, K. Thomas, P. Eranti, M. Bailey, and J. A. Halderman, "Neither Snow Nor Rain Nor MITM... An Empirical Analysis of Email Delivery Security," in *Proc. ACM Internet Measurement Conf. (IMC '15)*, Tokyo, Japan, 2015, pp. 27–39.

[10] R. Basnet, S. Mukkamala, and A. H. Sung, "Detection of Phishing Attacks: A Machine Learning Approach," in *Soft Computing in Big Data Processing*, L. Teng and V. Snasel, Eds. Cham, Switzerland: Springer, 2018, pp. 373–383.

[11] F. Toolan and J. Carthy, "Phishing Detection Using Information Gain Feature Selection and Multi-Classifier Ensembles," *Computers & Security*, vol. 84, pp. 315–334, Jul. 2019.

[12] S. A. Salloum, T. Gaber, S. Vadera, and K. Shaalan, "Phishing Email Detection Using Natural Language Processing and Deep Learning Techniques: A Comprehensive Survey," *IEEE Trans. Computational Social Systems*, vol. 9, no. 4, pp. 1145–1165, Aug. 2022.

[13] J. Szurdi, B. Kocso, G. Cseh, J. Spring, M. Felegyhazi, and C. Kanich, "The Long "Taile" of Typosquatting: Domain Name Variations and Their Commercial Usage," in *Proc. IEEE Symp. Security and Privacy (S&P '20)*, San Francisco, CA, USA, 2020, pp. 541–558.

[14] P. Agten, W. Joosen, and N. Nikiforakis, "Seven Months' Worth of Mistakes: A Longitudinal Study of Typosquatting and Homoglyph Registration Patterns," in *Proc. ACM SIGSAC Conf. Computer and Communications Security (CCS '21)*, Virtual Event, 2021, pp. 1421–1436.

[15] M. Tavallaee, E. Bagheri, W. Lu, and A. A. Ghorbani, "A Detailed Analysis of the KDD CUP 99 Data Set," in *Proc. IEEE Symp. Computational Intelligence for Security and Defense Applications (CISDA '09)*, Ottawa, ON, Canada, 2009, pp. 1–6.

[16] G. Ho, A. Czeskis, P. van Oorschot, and D. Wagner, "Detecting and Characterizing BEC Attacks at Scale: An Empirical Study of Social Engineering Tactics," in *Proc. 28th USENIX Security Symp. (USENIX Security '19)*, Santa Clara, CA, USA, 2019, pp. 185–202.

[17] S. Dreiseitl, M. Osl, and B. Pfeifer, "Linguistic and Behavioral Analysis of Executive Impersonation in Corporate Email Compromise," in *Proc. ACM Workshop on Threat Intelligence and Security Informatics*, Los Angeles, CA, USA, 2022, pp. 45–56.

[18] R. Sommer and V. Paxson, "Outside the Closed World: On Using Machine Learning for Network Intrusion Detection," in *Proc. IEEE Symp. Security and Privacy (S&P '10)*, Oakland, CA, USA, 2010, pp. 305–316.

[19] E. Casey, *Digital Evidence and Computer Crime: Forensic Science, Computers, and the Internet*, 3rd ed. London, UK: Academic Press / Elsevier, 2021.

[20] B. Carrier and E. H. Spafford, "Getting Physical with the Digital Investigation Process," *International Journal of Digital Evidence*, vol. 2, no. 2, pp. 1–20, Fall 2003.

[21] Scientific Working Group on Digital Evidence (SWGDE), "SWGDE Best Practices for Computer Forensic Acquisitions," SWGDE, Technical Standard Version 3.1, Sep. 2022. [Online]. Available: https://www.swgde.org/

[22] J. Foster, V. Paxson, and N. Weaver, "Understanding the Landscape of Email Spoofing Protections," in *Proc. ACM Internet Measurement Conf. (IMC '20)*, Virtual Event, 2020, pp. 120–134.

[23] N. Almomani, T. Al-Momani, and A. Al-Nawasrah, "A Comprehensive Survey of Machine Learning and Deep Learning Techniques for Phishing Detection," *Journal of Network and Computer Applications*, vol. 185, p. 103088, Jul. 2021.

[24] N. Nikiforakis, M. Balduzzi, L. Desmet, Y. Younan, and W. Joosen, "Soundsquatting: Uncovering the Use of Homophones in Domain Squatting," in *Proc. 17th Information Security Conf. (ISC '14)*, Hong Kong, China, 2014, pp. 291–308.

[25] M. Ring, S. Wunderlich, D. Scheuring, D. Landes, and A. Hotho, "A Survey of Network-Based Intrusion Detection Data Sets," *Computers & Security*, vol. 86, pp. 147–167, Sep. 2019.

[26] K. Scarfone and P. Mell, "Guide to Intrusion Detection and Prevention Systems (IDPS)," National Institute of Standards and Technology (NIST), Gaithersburg, MD, Special Publication 800-94, Feb. 2012.

[27] M. Reith, C. Carr, and J. Gunsch, "An Examination of Digital Forensic Models," *International Journal of Digital Evidence*, vol. 1, no. 3, pp. 1–12, Fall 2002.

[28] Y. Wang, W. D. Zhang, and X. L. Chen, "Exploring Domain Name Resemblance: Typosquatting and Combosquatting in Global Top-Level Domains," *IEEE Trans. Information Forensics and Security*, vol. 16, pp. 3120–3134, Mar. 2021.

[29] A. C. Cialdini, "Harnessing the Science of Persuasion," *Harvard Business Review*, vol. 79, no. 9, pp. 72–79, Oct. 2001.

[30] P. Resnick, "Internet Message Format," RFC 5322, Internet Engineering Task Force (IETF), Oct. 2008. [Online]. Available: https://www.rfc-editor.org/info/rfc5322
