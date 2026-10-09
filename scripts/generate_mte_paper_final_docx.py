import os
import shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_page_number_to_section(section):
    footer = section.footer
    f_p = footer.paragraphs[0]
    f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = f_p.add_run()
    fld1 = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
    run._r.append(fld1)
    for r in f_p.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0x60, 0x64, 0x6C)

def main():
    doc = Document()
    
    # Page setup: Standard A4 with 1-inch margins
    for sec in doc.sections:
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(1.0)
        sec.page_width = Inches(8.27)
        sec.page_height = Inches(11.69)
        add_page_number_to_section(sec)
        
        # Add Header
        header = sec.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Galgotias University | SCSE Capstone 2026–27 | 7th Sem MTE Research Paper Draft (Final Revision)")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.italic = True
        hrun.font.color.rgb = RGBColor(0x70, 0x75, 0x7A)

    # Base Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(0x1F, 0x23, 0x28)

    # 1. Paper Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run("ANVESH: Cyber Forensic Intelligence and Email Threat Detection Platform")
    r_title.bold = True
    r_title.font.size = Pt(18)
    r_title.font.name = 'Times New Roman'
    r_title.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    # 2. Authors and Affiliations
    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.space_after = Pt(4)
    r_a1 = p_auth.add_run("[STUDENT NAME]¹, [ADMISSION NUMBER]¹    |    [CO-AUTHOR NAME]¹    |    [GUIDE NAME]², [DESIGNATION]²\n")
    r_a1.bold = True
    r_a1.font.size = Pt(10.5)
    
    r_aff = p_auth.add_run(
        "¹Student, Department of Computer Science and Engineering\n"
        "²Faculty Supervisor, Department of Computer Science and Engineering\n"
        "School of Computer Science and Engineering, Galgotias University, Greater Noida, Uttar Pradesh, India\n"
        "Smart India Hackathon Problem Statement SIH26106 | 7th Semester MTE Deliverable (October 2026)"
    )
    r_aff.font.size = Pt(9.5)
    r_aff.font.italic = True
    r_aff.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    # Divider line
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(6)
    p_div.paragraph_format.space_after = Pt(10)
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_div = p_div.add_run("_________________________________________________________________________________")
    r_div.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)

    # 3. Abstract Callout Box
    table_abs = doc.add_table(rows=1, cols=1)
    table_abs.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table_abs.cell(0, 0)
    cell.width = Inches(6.27)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(r'<w:shd %s w:fill="F8FAFC"/>' % nsdecls('w'))
    tcPr.append(shd)

    p_abs = cell.paragraphs[0]
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.space_after = Pt(6)
    p_abs.paragraph_format.line_spacing = 1.15
    
    r_abh = p_abs.add_run("Abstract— ")
    r_abh.bold = True
    r_abh.font.name = "Times New Roman"
    r_abh.font.size = Pt(10)
    
    r_abt = p_abs.add_run(
        "Email communication remains a primary ingress vector for modern cyber threats, encompassing credential harvesting, "
        "high-consequence Business Email Compromise (BEC), and targeted spear-phishing. Contemporary enterprise defense systems "
        "frequently operate across decoupled analytical silos: Secure Email Gateways (SEGs) evaluate message content and domain "
        "cryptographic records, while Network Intrusion Detection Systems (NIDS) inspect transport-layer telemetry, leaving security "
        "analysts without an integrated, evidentially sound mechanism to correlate multi-stage threat indicators. Furthermore, standard "
        "email authentication protocols—such as SPF, DKIM, and DMARC—validate transmitting server authorization rather than message intent, "
        "introducing notable operational limitations when threat actors leverage compromised legitimate mailboxes or legitimate cloud infrastructure. "
        "In response to these challenges, this paper presents ANVESH, an integrated cyber forensic intelligence and threat detection prototype "
        "developed under Smart India Hackathon Problem Statement SIH26106. ANVESH correlates multi-layered technical observables—including "
        "RFC-822 header routing chains, linguistic urgency indicators, algorithmic lookalike domain heuristics, and transport-layer network "
        "anomalies—into a transparent, bounded 0–100 threat assessment model. To support evidential integrity during investigation, the platform "
        "computes SHA-256 cryptographic digests upon artifact ingestion and maintains a cryptographically verifiable evidence ledger. Crucially, "
        "the platform enforces an ethical forensic invariant: infrastructure and transport-layer artifacts establish technical origin paths "
        "but do not by themselves establish human actor identity. This paper establishes the theoretical foundation, problem context, and comprehensive "
        "literature review required for the 7th-semester research milestone, identifying five critical research and engineering gaps that motivate "
        "the unified ANVESH architecture."
    )
    r_abt.font.name = "Times New Roman"
    r_abt.font.size = Pt(9.5)

    p_kw = cell.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw.paragraph_format.space_before = Pt(4)
    p_kw.paragraph_format.space_after = Pt(0)
    r_kwh = p_kw.add_run("Keywords— ")
    r_kwh.bold = True
    r_kwh.font.name = "Times New Roman"
    r_kwh.font.size = Pt(9.5)
    r_kwt = p_kw.add_run("Cyber Forensics, Email Threat Detection, Phishing Detection, Business Email Compromise, Lookalike Domains, Network Anomaly Detection, Digital Evidence Integrity, Threat Signal Fusion.")
    r_kwt.font.italic = True
    r_kwt.font.name = "Times New Roman"
    r_kwt.font.size = Pt(9.5)

    # Spacing after abstract
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(8)
    p_sp.paragraph_format.space_after = Pt(8)

    # Helper function for adding sections
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        return p

    def add_body(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)
        return p

    # --- SECTION 1 ---
    add_h1("1. INTRODUCTION")
    
    add_h2("1.1 Background")
    add_body(
        "Over the past three decades, electronic mail has served as the foundational communication protocol of global commerce, "
        "governance, and institutional collaboration. However, the architectural foundation of the Internet Message Format, formalized "
        "in RFC 822 and updated in RFC 5322 [30], was developed in an environment characterized by mutual institutional trust. The core protocol "
        "lacked native mechanisms for sender identity verification, cryptographic message non-repudiation, and structural payload "
        "authentication. Consequently, adversaries systematically utilize email as a primary vector for initiating cyber attacks [1], [2]."
    )
    add_body(
        "Modern email-borne threats have evolved significantly beyond unstructured, high-volume spam. Threat actors routinely execute sophisticated "
        "social engineering campaigns that manipulate cognitive heuristics—such as authority, scarcity, social proof, and urgency [3], [29]—to bypass "
        "user vigilance and technical perimeter controls. These campaigns manifest across a diverse operational spectrum: (1) Credential Phishing engineered "
        "to harvest enterprise credentials through deceptive cloud and identity portals [10], [12]; (2) Business Email Compromise (BEC) characterized by "
        "attachment-free linguistic urgency and executive impersonation designed to redirect fraudulent wire transfers [16], [17]; (3) Display-Name and "
        "identity spoofing exploiting disparities between user-visible headers and envelope identities [22]; and (4) Algorithmic Lookalike Domains leveraging "
        "typosquatting, combosquatting, and Unicode homoglyphs to bypass visual and algorithmic filters [13], [14], [28]."
    )
    add_body(
        "Simultaneously, enterprise defense mechanisms have evolved to inspect network traffic flows and transport session dynamics [8], [26]. However, "
        "in modern Security Operations Centers (SOCs), email security tools and network monitoring tools operate as decoupled telemetry islands. When a "
        "targeted email payload establishes initial access and subsequently initiates command-and-control (C2) beaconing, analysts are often required to "
        "manually correlate disconnected logs across disparate vendor consoles [18], [19]. Digital forensics and incident response (DFIR) teams require an "
        "integrated technological paradigm capable of evaluating email artifacts, correlating post-delivery network telemetry, and preserving defensible digital evidence."
    )

    add_h2("1.2 Problem Context")
    add_body(
        "Investigating a suspicious email requires a security analyst to navigate a fragmented analytical workflow. When a suspicious message is flagged, "
        "the examination typically demands: extracting and inspecting raw RFC-5322 transport headers to identify chronological Received: transit hops and "
        "perimeter ingress relays [30]; evaluating cryptographic domain authentication records (SPF [4], DKIM [5], DMARC [6]); analyzing the semantic "
        "content of message bodies for linguistic urgency or fraudulent wire transfer instructions [16], [17]; interrogating DNS registries and edit-distance string "
        "metrics for deceptive lookalike domains [14], [28]; correlating IP addresses extracted from message hops against local network telemetry and intrusion "
        "detection logs [15], [25]; and cataloging Indicators of Compromise (IOCs) into structured evidentiary dossiers for institutional stakeholders and law "
        "enforcement cyber cells [19], [21]."
    )
    add_body(
        "In prevailing organizational practice, this investigative pipeline is executed across distinct, disconnected point solutions. Security personnel utilize "
        "command-line utilities for header extraction, third-party web portals for domain reputation lookups, dedicated sandboxes for attachment detonation, and "
        "centralized SIEM consoles for network log correlation. This telemetry fragmentation introduces latency during active incident triage and increases the likelihood of investigative oversight."
    )
    add_body(
        "Crucially, existing defenses exhibit a notable conceptual limitation regarding email authentication. While SPF verifies that the transmitting mail server "
        "is authorized by the sender domain's DNS owner [4], and DKIM verifies that the email body and headers have not undergone in-transit tampering [5], "
        "neither protocol evaluates message intent. An email transmitted from a legitimate corporate account compromised via credential stuffing or session hijacking "
        "can achieve valid SPF, DKIM, and DMARC alignment. Consequently, automated gateways that conflate cryptographic authentication with message benignity can "
        "deliver high-consequence BEC attacks directly to user inboxes [16], [22]."
    )

    add_h2("1.3 Motivation")
    add_body("The development of ANVESH is motivated by four interrelated operational and theoretical imperatives:")
    add_body(
        "1. The Authenticated Malicious Message Paradox: As organizations enforce strict DMARC rejection policies, sophisticated adversaries increasingly shift "
        "toward compromising legitimate mailboxes or utilizing legitimate cloud email infrastructure (e.g., Microsoft 365, Google Workspace). When an email passes SPF and "
        "DKIM, conventional heuristic filters often reduce their threat posture. A robust forensic engine must decouple domain authorization status from behavioral and "
        "linguistic risk analysis [16], [17]."
    )
    add_body(
        "2. Fragmentation of Forensic Telemetry: Cyber forensic investigators face operational friction when pivoting between application-layer email artifacts and "
        "transport-layer network logs. Correlating an external relay IP observed in an email header with internal network traffic requires cross-silo data ingestion. "
        "An integrated workbench that unifies email dissection and network anomaly analysis accelerates triage [8], [15]."
    )
    add_body(
        "3. Fragility of Digital Evidence Integrity: Digital evidence is inherently volatile and susceptible to claims of spoliation or tampering during legal proceedings. "
        "Standard triage workflows frequently rely on unstructured screenshots, manual text copies, or mutable database records. Adherence to recognized forensic standards [19], [21] "
        "demands that evidence be cryptographically recorded via hashing algorithms immediately upon acquisition."
    )
    add_body(
        "4. The Attribution Conflation Risk: Commercial security dashboards frequently present geolocation data or IP Whois ownership as direct proof of 'attacker identity.' "
        "In digital forensics, transport-layer hops reflect network infrastructure, proxy nodes, or compromised intermediate relays—not physical human actors. Premature or "
        "unsupported attribution introduces legal liability and investigative misdirection [19], [20]."
    )

    add_h2("1.4 Research Problem")
    add_body(
        "The central research problem addressed by this study is formulated as follows: How can suspicious electronic mail artifacts and associated multi-vector threat "
        "indicators be ingested, analyzed, and correlated through a unified, explainable cyber-forensic workflow that preserves strict cryptographic evidence integrity "
        "while explicitly preventing unsupported human-attribution claims?"
    )
    add_body(
        "To address this problem, the analytical framework must establish a clear theoretical separation between infrastructure-level observables and actor identity. "
        "Within the context of this research, technical headers, Autonomous System Numbers (ASNs), geographic IP resolutions, and transmission relays are formally modeled "
        "as computational transport infrastructure. In the absence of lawful subscriber logs, physical device seizures, and authenticated forensic corroboration, the platform "
        "enforces the formal evidentiary invariant: Actor Identity = NOT ESTABLISHED."
    )

    add_h2("1.5 Objectives and Research Direction")
    add_body("The primary research direction focuses on designing, formalizing, and prototyping an integrated cyber forensic intelligence framework. Specific research objectives include:")
    add_body("• Developing an automated ingestion and dissection pipeline for raw RFC-822 / RFC-5322 electronic mail payloads, supporting multi-part MIME parsing and recursive Received: hop traversal.")
    add_body("• Formalizing an independent cryptographic authentication verification matrix that parses and audits SPF, DKIM, and DMARC alignment states without treating authentication as proof of benign intent.")
    add_body("• Formulating natural language processing (NLP) feature extractors based on term frequency-inverse document frequency (TF-IDF) n-grams to detect linguistic urgency, deceptive calls to action, and credential harvesting patterns.")
    add_body("• Designing a specialized behavioral detection model tailored to Business Email Compromise, isolating linguistic coercion, executive authority invocation, and fraudulent wire transaction pressure.")
    add_body("• Implementing algorithmic string similarity and edit-distance heuristics (Levenshtein, Jaro-Winkler) coupled with machine learning classifiers to detect lookalike and homoglyph domain impersonation against high-value organizational targets.")
    add_body("• Integrating transport-layer network anomaly detection capabilities using standardized 41-feature network telemetry representations (NSL-KDD benchmark) to correlate host-level intrusion indicators with message routing infrastructure.")
    add_body("• Establishing a cryptographically verifiable evidence ledger utilizing SHA-256 digests computed at the instant of payload ingestion to guarantee evidential byte consistency.")
    add_body("• Constructing a transparent, bounded 0–100 multi-signal threat scoring engine that outputs auditable, explainable component scores rather than opaque, uncalibrated probabilities.")

    add_h2("1.6 Contribution of the Work")
    add_body(
        "The principal contribution of this research lies in the architectural integration and evidentially sound synthesis of multi-vector cybersecurity observables "
        "into a unified forensic intelligence framework. Specifically, this work: (1) proposes a unified defense-in-depth workflow that bridges the operational divide "
        "between application-layer email text analysis, transport header verification, and network intrusion telemetry; (2) formulates a decoupled risk evaluation "
        "paradigm wherein cryptographic email authentication records (SPF/DKIM/DMARC) are audited as infrastructure properties rather than trusted determinants of benign "
        "intent; (3) embeds cryptographic integrity verification (SHA-256) directly into the triage pipeline, producing structured, tamper-evident forensic dossiers "
        "suitable for legal scrutiny; and (4) enforces an ethical attribution boundary that prevents the systemic conflation of network routing infrastructure with human criminal identity."
    )
    add_body(
        "Importantly, this work does not claim the invention of novel machine learning classification algorithms in isolation; rather, its academic and engineering contribution "
        "resides in the principled fusion, explainable risk modeling, and forensic hardening of established analytical methodologies within a cohesive threat intelligence architecture."
    )

    # --- SECTION 2 ---
    add_h1("2. LITERATURE REVIEW")

    add_h2("2.1 Existing Threat Detection Approaches")
    add_body(
        "Organizational defense against cyber threats has historically relied on two primary paradigms: rule-based signature matching and behavioral anomaly detection [7], [8], [26]. "
        "Signature-based filtering operates by matching incoming digital artifacts against static databases of known malicious signatures, file checksums, regular expressions, or "
        "blacklisted IP addresses. In electronic mail, open-source and commercial engines such as Apache SpamAssassin [7] pioneered heuristic scoring based on static rules, header "
        "discrepancies, and distributed spam blacklists (DNSBL). Similarly, in network security, systems such as Snort [8] inspect packet payloads for predefined byte sequences "
        "characteristic of exploit attempts. While computationally efficient and capable of achieving near-zero false-positive rates on known attack patterns, signature-based approaches "
        "can experience severe detection failures when confronted with zero-day exploits, polymorphism, and social engineering attacks that contain no executable malware [18], [26]."
    )
    add_body(
        "To address the limitations of static rules, contemporary security systems employ behavioral anomaly detection and statistical machine learning [10], [23]. These systems model "
        "baseline operational behavior and flag statistical deviations. However, as demonstrated by Sommer and Paxson [18], the application of machine learning to intrusion detection "
        "faces fundamental challenges: high costs associated with false positives, the absence of comprehensive closed-world training data, and the semantic gap between "
        "detecting an anomaly and diagnosing a malicious intrusion."
    )

    add_h2("2.2 Email Authentication Protocols")
    add_body(
        "To mitigate identity spoofing and establish sender accountability, the Internet Engineering Task Force (IETF) standardized three foundational cryptographic and DNS-based "
        "authentication mechanisms: Sender Policy Framework (SPF, RFC 7208) [4], DomainKeys Identified Mail (DKIM, RFC 6376) [5], and Domain-based Message Authentication, Reporting, "
        "and Conformance (DMARC, RFC 7489) [6]."
    )
    add_body(
        "SPF allows domain owners to publish DNS TXT records specifying the IP addresses authorized to transmit emails using their domain in the SMTP MAIL FROM envelope identity [4]. "
        "While effective at preventing naive envelope spoofing, SPF possesses well-documented limitations: it does not validate the user-visible From: header, breaks during automated "
        "email forwarding, and offers no protection against lookalike domains [9], [22]. DKIM provides cryptographic message integrity and sender domain association by attaching a digital "
        "signature to email headers [5]. Although DKIM survives message forwarding, it is computationally intensive, does not authenticate the user-facing display name, and does not "
        "specify recipient policy upon verification failure [9], [22]. DMARC bridges SPF and DKIM by requiring identifier alignment between the authenticated domain and the user-visible "
        "From: header, enabling domain owners to publish enforcement policies (none, quarantine, reject) [6]."
    )
    add_body(
        "Despite widespread adoption, empirical studies by Durumeric et al. [9] and Hu and Wang [22] highlight systemic vulnerabilities across the authentication ecosystem. Millions "
        "of enterprise domains either maintain permissive DMARC policies or misconfigure SPF records. More fundamentally, these protocols validate domain authorization, not message safety. "
        "An adversary operating a legitimate email account compromised via session hijacking or purchasing a newly registered domain with valid SPF/DKIM records can bypass authentication checks entirely [16], [22]."
    )

    add_h2("2.3 Phishing Detection and Natural Language Processing")
    add_body(
        "Automated phishing detection using machine learning and Natural Language Processing (NLP) has been extensively investigated over the past two decades [10]–[12], [23]. Early research "
        "focused on manual feature engineering. Basnet et al. [10] and Toolan and Carthy [11] demonstrated that extracting structural features (e.g., number of links, presence of IP-based URLs, "
        "JavaScript tags, and vocabulary richness) paired with classical classifiers (Support Vector Machines, Random Forests, Decision Trees) could classify high-volume phishing emails effectively. "
        "Almomani et al. [23] conducted a comprehensive survey of filtering techniques, categorizing machine learning feature representations across header, body, and external reputation categories. "
        "Subsequent research shifted toward text-level lexical analysis using Bag-of-Words and Term Frequency-Inverse Document Frequency (TF-IDF) representations [11], [23]. By evaluating sublinear "
        "term frequencies across character and word n-grams, linear classifiers such as Calibrated Logistic Regression achieve robust, computationally lightweight baseline detection for mass-market credential harvesting templates [12]."
    )
    add_body(
        "In recent years, deep learning and transformer-based architectures (e.g., BERT, RoBERTa) have been widely explored for semantic phishing analysis [12]. While transformer models "
        "achieve high empirical accuracy on benchmark datasets, their deployment in high-throughput enterprise pipelines is constrained by significant computational inference overhead, latency, "
        "and susceptibility to adversarial text perturbations (e.g., zero-width space injection, character homoglyphs). Furthermore, deep neural networks function as uncalibrated black boxes, "
        "providing opaque probability scores that fail to offer defensible explanations during formal forensic or legal proceedings [18], [19]."
    )

    add_h2("2.4 Business Email Compromise and Social Engineering Detection")
    add_body(
        "Business Email Compromise (BEC) represents a distinct class of social engineering characterized by a low technical footprint and significant financial loss [1], [16]. Unlike traditional phishing, "
        "BEC emails typically contain no hyperlinks, no malware attachments, and no overt technical anomalies. The attack vector relies entirely on psychological manipulation, linguistic urgency, "
        "and authority impersonation [3], [29]."
    )
    add_body(
        "Ho et al. [16] conducted an empirical study of BEC attacks at scale across enterprise environments, demonstrating that attackers systematically target financial workflows through executive "
        "impersonation (requesting urgent wire transfers) and vendor invoice fraud (intercepting legitimate invoice exchanges). Cidon et al. [17] presented an automated approach for high-precision BEC "
        "detection, demonstrating that traditional spam filters heavily weight URL counts and attachment signatures, thereby consistently misclassifying text-only BEC emails as legitimate business correspondence. "
        "Detecting BEC requires specialized linguistic models focused on financial transaction terminology, executive authority cues, and coercive urgency [16], [17]."
    )

    add_h2("2.5 Lookalike and Homoglyph Domain Detection")
    add_body(
        "Adversaries frequently register deceptive domain names that visually mimic legitimate enterprise entities to facilitate credential theft and executive impersonation [13], [14], [28]. "
        "Szurdi et al. [13] and Agten et al. [14] conducted longitudinal studies analyzing typosquatting (exploiting user keyboard typographical errors). Beyond typosquatting, Kintis et al. [28] conducted "
        "a comprehensive longitudinal measurement study of combosquatting—the practice of combining a legitimate trademark with keywords such as -login, -support, or -portal—demonstrating its widespread "
        "prevalence in phishing and advanced persistent threat campaigns. Furthermore, attackers exploit Internationalized Domain Names (IDNs) via Punycode encoding to execute homoglyph attacks—substituting "
        "Latin characters with visually indistinguishable glyphs from Cyrillic or Greek alphabets (e.g., replacing Latin 'a' with Cyrillic 'а') [14], [24]."
    )
    add_body(
        "Algorithmic detection of lookalike domains relies on string metric calculations, primarily Levenshtein edit distance and Jaro-Winkler similarity [24], [28]. However, domain similarity heuristics "
        "evaluated in isolation produce false positives when legitimate organizations register multi-brand domains. Lookalike detection must therefore be correlated with message-level authentication and routing telemetry [14], [28]."
    )

    add_h2("2.6 Network Intrusion Detection and the NSL-KDD Benchmark")
    add_body(
        "Network Intrusion Detection Systems (NIDS) inspect transport- and network-layer packet dynamics to identify reconnaissance, lateral movement, denial-of-service, and unauthorized data exfiltration [8], [26]. "
        "The evaluation of machine learning algorithms for network intrusion detection has historically depended on standardized benchmark datasets, most notably the KDD Cup 1999 dataset and its curated revision, "
        "NSL-KDD [15], [25]. Proposed by Tavallaee et al. [15], NSL-KDD resolved critical statistical deficiencies of KDD Cup 99—specifically removing redundant records and balancing class distributions to prevent "
        "machine learning algorithms from becoming biased toward frequent benign traffic patterns. The dataset characterizes connection sessions across 41 distinct features spanning basic protocol properties, "
        "domain-specific content flags, and time-based network traffic statistics [15]."
    )
    add_body(
        "Despite its ubiquity in academic literature, the limitations of NSL-KDD must be explicitly acknowledged. As highlighted by Ring et al. [25] and Sommer and Paxson [18], synthetic network benchmarks do "
        "not reflect the complex latency distributions, encrypted packet dynamics, or multi-gigabit throughput rates of modern production networks. In the ANVESH research architecture, NSL-KDD is utilized as a "
        "standardized baseline benchmark for evaluating multi-class tabular classification algorithms (e.g., Random Forest), while operational packet inspection relies on live Scapy and Npcap capture engines [8], [26]."
    )

    add_h2("2.7 Digital Evidence Integrity and Cyber Forensics")
    add_body(
        "The preservation of digital evidence is governed by strict legal and scientific standards to ensure admissibility in court proceedings [19]–[21]. In jurisdictions worldwide, including statutory provisions "
        "under international common law and the Indian Evidence framework (Bharatiya Sakshya Adhiniyam / Indian Evidence Act Section 65B), electronic records must maintain a verifiable, unbroken chain of custody [19]. "
        "Foundational models of digital investigation, established by Carrier and Spafford [20] and Reith et al. [27], define four invariant phases: acquisition, preservation, analysis, and presentation. The preservation "
        "phase dictates that digital evidence must be captured in an unaltered state and protected against intentional or accidental modification [21]. Cryptographic hashing algorithms, particularly the Secure Hash "
        "Algorithm (SHA-256), serve as the international standard for establishing mathematical integrity digests [19], [21]. An ingested email or packet capture whose post-analysis hash matches its initial ingestion digest "
        "provides strong evidence that the examined artifact remains byte-for-byte consistent with the artifact associated with the recorded hash. However, digital forensic science emphasizes that a cryptographic digest "
        "establishes byte-level constancy, but does not independently establish the legal chain of custody, the authenticity of the originating source, or the physical identity of the human author [19], [20]."
    )
    add_body(
        "Furthermore, digital forensic treatises by Casey [19] emphasize the vital distinction between observable physical artifacts and investigator inference. An investigator who observes an IP address in an email header "
        "has observed a transport infrastructure routing event. Asserting that the owner of that IP address is the human attacker constitutes an unverified deductive leap. Responsible forensic tooling must enforce this "
        "boundary programmatically, presenting technical facts while withholding premature actor attribution [19], [20]."
    )

    add_h2("2.8 Literature Synthesis and Research Gap Analysis")
    add_body(
        "A comprehensive synthesis of the surveyed literature reveals that while individual cybersecurity disciplines—natural language processing for email filtering, cryptographic identity standards, homoglyph string "
        "metrics, network intrusion benchmarking, and digital evidence hashing—have advanced substantially, they operate as disconnected technical silos. Specifically, this study identifies five critical research and engineering gaps:"
    )
    add_body(
        "• Gap 1: The Authenticated BEC Gateway Blindspot. Existing email security solutions heavily weight SPF, DKIM, and DMARC passes to determine message trustworthiness [9], [22]. When attackers conduct BEC attacks from "
        "compromised legitimate Microsoft 365 or Google Workspace accounts, or newly configured domains with valid cryptographic records, existing gateways often fail to detect the threat [16], [17]. A dedicated forensic "
        "architecture must evaluate behavioral and financial coercion independently of cryptographic authentication status."
    )
    add_body(
        "• Gap 2: Telemetry Siloing Between Application-Layer Email and Transport-Layer Network Telemetry. Current enterprise architectures treat email analysis and network intrusion detection as entirely separate operations [8], [15], [18]. "
        "A phishing email that successfully drops a payload initiates network-level C2 traffic, yet the analyst has no automated mechanism to correlate the email's origin infrastructure with host-level network flows. A unified workflow "
        "bridging Layer 7 email parsing and Layer 3/4 packet inspection is sorely needed."
    )
    add_body(
        "• Gap 3: Opacity and Inadmissibility of Black-Box Threat Scores. Contemporary deep learning architectures output uncalibrated, unexplainable probability distributions [12], [18]. In legal proceedings and forensic audits, opaque "
        "probability claims fail evidential standards. Analysts require transparent, explainable threat scoring frameworks that decompose risk into human-auditable component deductions [19]."
    )
    add_body(
        "• Gap 4: Absence of Embedded Evidence Integrity in Triage Workflows. Standard email triage interfaces permit operators to view, alter, or export messages without computing instantaneous cryptographic digests [19], [21]. "
        "When cases transition to formal law enforcement investigation, evidence integrity is vulnerable to legal challenge. Forensic platforms must embed SHA-256 cryptographic sealing directly into the ingestion pipeline."
    )
    add_body(
        "• Gap 5: Premature Human Attribution and Conflation of Infrastructure with Actors. Existing commercial threat intelligence platforms routinely map IP geolocations or domain registrants directly to 'attackers.' Such practices "
        "conflate technical transport infrastructure (proxies, VPNs, compromised relays) with human identity, violating fundamental forensic principles [19], [20]. Systems must enforce formal invariants declaring that technical "
        "headers establish routing paths, while actor identity remains strictly unestablished."
    )
    add_body(
        "The surveyed literature demonstrates a clear scientific and engineering opportunity for an integrated, evidence-preserving, and explainable cyber forensic intelligence platform. By addressing these five identified gaps "
        "through a unified architectural framework, the ANVESH project establishes a defensible, multi-vector foundation for modern digital investigation and threat detection."
    )

    # --- REFERENCES ---
    add_h1("REFERENCES")
    refs = [
        "[1] Federal Bureau of Investigation (FBI) Internet Crime Complaint Center (IC3), \"Internet Crime Report 2023,\" Federal Bureau of Investigation, Washington, D.C., Technical Report, Apr. 2024. [Online]. Available: https://www.ic3.gov/Media/PDF/AnnualReport/2023_IC3Report.pdf",
        "[2] Verizon Enterprise Solutions, \"2024 Data Breach Investigations Report (DBIR),\" Verizon, New York, NY, Technical Report, May 2024.",
        "[3] R. B. Cialdini, Influence: The Psychology of Persuasion, Rev. ed. New York, NY, USA: Harper Business, 2021.",
        "[4] S. Kitterman, \"Sender Policy Framework (SPF) for Authorizing Use of Domains in Email, Version 1,\" RFC 7208, Internet Engineering Task Force (IETF), Apr. 2014. [Online]. Available: https://www.rfc-editor.org/info/rfc7208",
        "[5] D. Crocker, T. Hansen, and M. Kucherawy, \"DomainKeys Identified Mail (DKIM) Signatures,\" RFC 6376, Internet Engineering Task Force (IETF), Sep. 2011. [Online]. Available: https://www.rfc-editor.org/info/rfc6376",
        "[6] M. Kucherawy and E. Zwicky, \"Domain-based Message Authentication, Reporting, and Conformance (DMARC),\" RFC 7489, Internet Engineering Task Force (IETF), Mar. 2015. [Online]. Available: https://www.rfc-editor.org/info/rfc7489",
        "[7] Apache Software Foundation, \"Apache SpamAssassin: The Powerful #1 Open-Source Spam Filter,\" Apache Software Foundation, Forest Hill, MD, Documentation, 2023. [Online]. Available: https://spamassassin.apache.org/",
        "[8] M. Roesch, \"Snort: Lightweight Intrusion Detection for Networks,\" in Proc. 13th USENIX Conf. System Administration (LISA '99), Seattle, WA, USA, 1999, pp. 229–238.",
        "[9] Z. Durumeric, D. Adrian, A. Mirian, J. Kasten, E. Bursztein, N. Lidzborski, K. Thomas, P. Eranti, M. Bailey, and J. A. Halderman, \"Neither Snow Nor Rain Nor MITM... An Empirical Analysis of Email Delivery Security,\" in Proc. ACM Internet Measurement Conf. (IMC '15), Tokyo, Japan, 2015, pp. 27–39.",
        "[10] R. Basnet, S. Mukkamala, and A. H. Sung, \"Detection of Phishing Attacks: A Machine Learning Approach,\" in Soft Computing in Big Data Processing, L. Teng and V. Snasel, Eds. Cham, Switzerland: Springer, 2018, pp. 373–383.",
        "[11] F. Toolan and J. Carthy, \"Phishing Detection Using Information Gain Feature Selection and Multi-Classifier Ensembles,\" Computers & Security, vol. 84, pp. 315–334, Jul. 2019.",
        "[12] S. A. Salloum, T. Gaber, S. Vadera, and K. Shaalan, \"Phishing Email Detection Using Natural Language Processing and Deep Learning Techniques: A Comprehensive Survey,\" IEEE Trans. Computational Social Systems, vol. 9, no. 4, pp. 1145–1165, Aug. 2022.",
        "[13] J. Szurdi, B. Kocso, G. Cseh, J. Spring, M. Felegyhazi, and C. Kanich, \"The Long 'Taile' of Typosquatting: Domain Name Variations and Their Commercial Usage,\" in Proc. IEEE Symp. Security and Privacy (S&P '20), San Francisco, CA, USA, 2020, pp. 541–558.",
        "[14] P. Agten, W. Joosen, and N. Nikiforakis, \"Seven Months' Worth of Mistakes: A Longitudinal Study of Typosquatting and Homoglyph Registration Patterns,\" in Proc. ACM SIGSAC Conf. Computer and Communications Security (CCS '21), Virtual Event, 2021, pp. 1421–1436.",
        "[15] M. Tavallaee, E. Bagheri, W. Lu, and A. A. Ghorbani, \"A Detailed Analysis of the KDD CUP 99 Data Set,\" in Proc. IEEE Symp. Computational Intelligence for Security and Defense Applications (CISDA '09), Ottawa, ON, Canada, 2009, pp. 1–6.",
        "[16] G. Ho, A. Czeskis, P. van Oorschot, and D. Wagner, \"Detecting and Characterizing BEC Attacks at Scale: An Empirical Study of Social Engineering Tactics,\" in Proc. 28th USENIX Security Symp. (USENIX Security '19), Santa Clara, CA, USA, 2019, pp. 185–202.",
        "[17] A. Cidon, L. Shirian, T. Tsitman, M. Freedman, and M. Stoppelman, \"High Precision Detection of Business Email Compromise,\" in Proc. 28th USENIX Security Symp. (USENIX Security '19), Santa Clara, CA, USA, 2019, pp. 291–307.",
        "[18] R. Sommer and V. Paxson, \"Outside the Closed World: On Using Machine Learning for Network Intrusion Detection,\" in Proc. IEEE Symp. Security and Privacy (S&P '10), Oakland, CA, USA, 2010, pp. 305–316.",
        "[19] E. Casey, Digital Evidence and Computer Crime: Forensic Science, Computers, and the Internet, 3rd ed. London, UK: Academic Press / Elsevier, 2021.",
        "[20] B. Carrier and E. H. Spafford, \"Getting Physical with the Digital Investigation Process,\" International Journal of Digital Evidence, vol. 2, no. 2, pp. 1–20, Fall 2003.",
        "[21] Scientific Working Group on Digital Evidence (SWGDE), \"SWGDE Best Practices for Computer Forensic Acquisitions,\" SWGDE, Technical Standard Version 3.1, Sep. 2022. [Online]. Available: https://www.swgde.org/",
        "[22] H. Hu and G. Wang, \"End-to-End Measurements of Email Spoofing Attacks in the Wild,\" in Proc. 29th USENIX Security Symp. (USENIX Security '20), 2020, pp. 2481–2498.",
        "[23] A. Almomani, B. B. Gupta, S. Atawneh, A. Meulenberg, and E. Almomani, \"A Survey of Phishing Email Filtering Techniques,\" IEEE Communications Surveys & Tutorials, vol. 15, no. 4, pp. 2070–2090, Fourth Quarter 2013.",
        "[24] N. Nikiforakis, M. Balduzzi, L. Desmet, Y. Younan, and W. Joosen, \"Soundsquatting: Uncovering the Use of Homophones in Domain Squatting,\" in Proc. 17th Information Security Conf. (ISC '14), Hong Kong, China, 2014, pp. 291–308.",
        "[25] M. Ring, S. Wunderlich, D. Scheuring, D. Landes, and A. Hotho, \"A Survey of Network-Based Intrusion Detection Data Sets,\" Computers & Security, vol. 86, pp. 147–167, Sep. 2019.",
        "[26] K. Scarfone and P. Mell, \"Guide to Intrusion Detection and Prevention Systems (IDPS),\" National Institute of Standards and Technology (NIST), Gaithersburg, MD, Special Publication 800-94, Feb. 2012.",
        "[27] M. Reith, C. Carr, and J. Gunsch, \"An Examination of Digital Forensic Models,\" International Journal of Digital Evidence, vol. 1, no. 3, pp. 1–12, Fall 2002.",
        "[28] P. Kintis, N. Miramirkhani, C. Lever, Y. Chen, R. Romero-Gómez, N. Pitropakis, N. Nikiforakis, and M. Antonakakis, \"Hiding in Plain Sight: A Longitudinal Study of Combosquatting Abuse,\" in Proc. 2017 ACM SIGSAC Conf. Computer and Communications Security (CCS '17), Dallas, TX, USA, 2017, pp. 569–586.",
        "[29] R. B. Cialdini, \"Harnessing the Science of Persuasion,\" Harvard Business Review, vol. 79, no. 9, pp. 72–79, Oct. 2001.",
        "[30] P. Resnick, \"Internet Message Format,\" RFC 5322, Internet Engineering Task Force (IETF), Oct. 2008. [Online]. Available: https://www.rfc-editor.org/info/rfc5322"
    ]
    for ref_str in refs:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.left_indent = Inches(0.3)
        p_ref.paragraph_format.first_line_indent = Inches(-0.3)
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(3)
        p_ref.paragraph_format.line_spacing = 1.05
        r_ref = p_ref.add_run(ref_str)
        r_ref.font.name = 'Times New Roman'
        r_ref.font.size = Pt(9)

    out_docs = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "ANVESH_MTE_Research_Paper_Final.docx"))
    desktop = os.path.expanduser("~/Desktop")
    out_desktop = os.path.join(desktop, "ANVESH_MTE_Research_Paper_Final.docx")
    out_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ANVESH_MTE_Research_Paper_Final.docx"))

    doc.save(out_docs)
    print(f"[+] Saved DOCX to: {out_docs}")
    try:
        shutil.copy2(out_docs, out_desktop)
        print(f"[+] Copied to Desktop: {out_desktop}")
    except Exception as e:
        print(f"[-] Desktop copy error: {e}")
    try:
        shutil.copy2(out_docs, out_root)
        print(f"[+] Copied to Root: {out_root}")
    except Exception as e:
        print(f"[-] Root copy error: {e}")

if __name__ == "__main__":
    main()
