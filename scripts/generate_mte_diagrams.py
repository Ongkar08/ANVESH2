"""
Generates academic diagram figures for the ANVESH MTE Interim Project Report-I.
Outputs clean, professional figures formatted for academic publication.
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

SCREENSHOTS_DIR = r"C:\Users\Ongkar\Desktop\Avnesh\Anvesha-main\Anvesha-main\docs\screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def draw_box(ax, x, y, w, h, title, subtitle="", bg="#FFFFFF", border="#1E293B", text_color="#0F172A", round_size=0.1):
    rect = patches.FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0.04,rounding_size={round_size}",
        facecolor=bg, edgecolor=border, linewidth=1.2
    )
    ax.add_patch(rect)
    if subtitle:
        ax.text(x + w/2, y + h*0.62, title, ha="center", va="center",
                fontsize=8.5, fontweight="bold", color=text_color)
        ax.text(x + w/2, y + h*0.28, subtitle, ha="center", va="center",
                fontsize=7.0, color="#475569")
    else:
        ax.text(x + w/2, y + h*0.5, title, ha="center", va="center",
                fontsize=8.0, fontweight="bold", color=text_color)

def draw_arrow(ax, x1, y1, x2, y2, color="#0284C7", label=""):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5, mutation_scale=12)
    )
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.1, label, ha="center", va="bottom",
                fontsize=6.5, color="#0F172A", fontweight="bold")

def generate_figure_1_1():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_facecolor("#F8FAFC")
    fig.patch.set_facecolor("#F8FAFC")
    ax.axis("off")

    ax.text(5, 4.6, "Figure 1.1: Multi-Vector Cyber Attack Landscape Targeted by ANVESH",
            ha="center", va="center", fontsize=11, fontweight="bold", color="#0F172A")

    # Inbound Payload Box
    draw_box(ax, 0.4, 1.8, 2.2, 1.4, "Inbound Malicious Payload", "RFC-822 Raw Email or Wire Stream", "#EFF6FF", "#0284C7")

    # Attack Vectors
    vectors = [
        ("Vector 1: Phishing & Credential Harvesting", "Urgent deceptive links & login replicas", 3.8, 3.2),
        ("Vector 2: Business Email Compromise (BEC)", "Executive pressure, swift wire fraud lures", 3.8, 2.3),
        ("Vector 3: Display-Name & Header Spoofing", "Visible name mismatch vs mailbox envelope", 3.8, 1.4),
        ("Vector 4: Lookalike & Homoglyph Domains", "Typosquatting & Unicode character substitutes", 3.8, 0.5),
        ("Vector 5: Multi-Hop Obfuscation", "Tor exit nodes & bulletproof transit relays", 7.0, 2.3),
        ("Vector 6: Post-Delivery Network Anomaly", "C2 beaconing, port scans, SYN floods", 7.0, 1.4),
    ]

    for title, sub, x, y in vectors:
        draw_box(ax, x, y, 2.8, 0.75, title, sub, "#FFFFFF", "#64748B")

    draw_arrow(ax, 2.6, 2.5, 3.8, 3.57)
    draw_arrow(ax, 2.6, 2.5, 3.8, 2.67)
    draw_arrow(ax, 2.6, 2.5, 3.8, 1.77)
    draw_arrow(ax, 2.6, 2.5, 3.8, 0.87)

    draw_arrow(ax, 6.6, 2.67, 7.0, 2.67)
    draw_arrow(ax, 6.6, 1.77, 7.0, 1.77)

    ax.set_xlim(0, 10.2)
    ax.set_ylim(0.2, 5.0)
    plt.tight_layout()
    out = os.path.join(SCREENSHOTS_DIR, "figure_1_1_attack_landscape.png")
    plt.savefig(out, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[+] Figure 1.1 saved: {out}")

def generate_figure_1_2():
    fig, ax = plt.subplots(figsize=(10.5, 5.5), dpi=300)
    ax.set_facecolor("#F8FAFC")
    fig.patch.set_facecolor("#F8FAFC")
    ax.axis("off")

    ax.text(5.25, 5.1, "Figure 1.2: High-Level ANVESH Conceptual Forensic Architecture",
            ha="center", va="center", fontsize=11, fontweight="bold", color="#0F172A")

    # Column 1: Ingestion
    draw_box(ax, 0.3, 3.4, 2.1, 1.1, "RFC-822 Email File", "SHA-256 Evidence Ledger", "#EFF6FF", "#0284C7")
    draw_box(ax, 0.3, 1.2, 2.1, 1.1, "Live Physical Wire", "Passive Npcap Packet Hook", "#ECFDF5", "#059669")

    # Column 2: Parsers
    draw_box(ax, 2.8, 3.4, 2.2, 1.1, "MIME & Hop Traversal", "SPF/DKIM Matrix & Tor Check", "#F1F5F9", "#475569")
    draw_box(ax, 2.8, 1.2, 2.2, 1.1, "Scapy Dissector", "5-Tuple Flow Aggregator", "#F1F5F9", "#475569")

    # Column 3: Multi-Tier ML
    draw_box(ax, 5.4, 3.8, 2.4, 0.8, "Model 1: Phishing NLP", "10k Features + Logistic Reg", "#FFF1F2", "#E11D48")
    draw_box(ax, 5.4, 2.8, 2.4, 0.8, "Model 2: BEC Detector", "5k Features + Balanced LR", "#FFFBEB", "#D97706")
    draw_box(ax, 5.4, 1.8, 2.4, 0.8, "Model 3A/3B: Identity & Lookalike", "Levenshtein + Brand Registry", "#F5F3FF", "#7C3AED")
    draw_box(ax, 5.4, 0.8, 2.4, 0.8, "Model 4/5: Network NDR", "41 NSL-KDD Feats (Random Forest)", "#ECFDF5", "#059669")

    # Column 4: Fusion & Output
    draw_box(ax, 8.2, 2.7, 2.0, 1.5, "Signal Fusion Engine", "Normalized 0-100 Score\nActor Identity: NOT ESTABLISHED", "#EDE9FE", "#6D28D9")
    draw_box(ax, 8.2, 0.8, 2.0, 1.5, "Forensic Deliverables", "Court-Ready PDF Dossier\nWireshark .pcap Evidence", "#EFF6FF", "#0284C7")

    # Arrows
    draw_arrow(ax, 2.4, 3.95, 2.8, 3.95)
    draw_arrow(ax, 2.4, 1.75, 2.8, 1.75)

    draw_arrow(ax, 5.0, 3.95, 5.4, 4.2)
    draw_arrow(ax, 5.0, 3.95, 5.4, 3.2)
    draw_arrow(ax, 5.0, 3.95, 5.4, 2.2)
    draw_arrow(ax, 5.0, 1.75, 5.4, 1.2)

    draw_arrow(ax, 7.8, 4.2, 8.2, 3.7)
    draw_arrow(ax, 7.8, 3.2, 8.2, 3.5)
    draw_arrow(ax, 7.8, 2.2, 8.2, 3.2)
    draw_arrow(ax, 7.8, 1.2, 8.2, 2.9)

    draw_arrow(ax, 9.2, 2.7, 9.2, 2.3)

    ax.set_xlim(0, 10.5)
    ax.set_ylim(0.4, 5.5)
    plt.tight_layout()
    out = os.path.join(SCREENSHOTS_DIR, "figure_1_2_conceptual_architecture.png")
    plt.savefig(out, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[+] Figure 1.2 saved: {out}")

def generate_figure_2_1():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_facecolor("#F8FAFC")
    fig.patch.set_facecolor("#F8FAFC")
    ax.axis("off")

    ax.text(5, 4.6, "Figure 2.1: Taxonomy of Existing Threat Detection Paradigms",
            ha="center", va="center", fontsize=11, fontweight="bold", color="#0F172A")

    draw_box(ax, 0.4, 2.0, 2.2, 1.2, "Threat Detection Paradigms", "Surveyed Literature (2018-2026)", "#EFF6FF", "#0284C7")

    p_list = [
        ("Deterministic / Rule-Based", "SpamAssassin, Snort, Static Domain Blacklists", 3.2, 3.4),
        ("Cryptographic Authentication", "SPF (RFC 7208), DKIM (RFC 6376), DMARC (RFC 7489)", 3.2, 2.4),
        ("Machine Learning & NLP", "TF-IDF, BERT, Random Forests, Logistic Regression", 3.2, 1.4),
        ("Network Intrusion Systems (NIDS)", "41-Feature NSL-KDD Benchmark, Flow Analysis", 3.2, 0.4),
    ]

    for title, sub, x, y in p_list:
        draw_box(ax, x, y, 3.2, 0.8, title, sub, "#FFFFFF", "#64748B")

    draw_box(ax, 6.9, 1.5, 2.8, 1.8, "Proposed ANVESH Paradigm", "Multi-Signal Forensic Fusion\n+ Cryptographic Evidence Hashing\n+ Layer 3, 4 & 7 Telemetry Correlation\n+ Attribution Invariant Enforcement", "#EDE9FE", "#7C3AED")

    draw_arrow(ax, 2.6, 2.6, 3.2, 3.8)
    draw_arrow(ax, 2.6, 2.6, 3.2, 2.8)
    draw_arrow(ax, 2.6, 2.6, 3.2, 1.8)
    draw_arrow(ax, 2.6, 2.6, 3.2, 0.8)

    draw_arrow(ax, 6.4, 2.4, 6.9, 2.4)

    ax.set_xlim(0, 10.0)
    ax.set_ylim(0.1, 5.0)
    plt.tight_layout()
    out = os.path.join(SCREENSHOTS_DIR, "figure_2_1_taxonomy_paradigms.png")
    plt.savefig(out, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[+] Figure 2.1 saved: {out}")

def generate_figure_2_2():
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=300)
    ax.set_facecolor("#F8FAFC")
    fig.patch.set_facecolor("#F8FAFC")
    ax.axis("off")

    ax.text(5, 4.8, "Figure 2.2: Identified Research Gaps vs ANVESH Architectural Responses",
            ha="center", va="center", fontsize=11, fontweight="bold", color="#0F172A")

    gaps = [
        ("GAP 1: Authenticated BEC Blindspot", "Legitimate hijacked mail passes SPF/DKIM", 0.5, 3.5),
        ("GAP 2: Telemetry Siloing (Email vs Net)", "Layer 7 text detached from Layer 3/4 flows", 0.5, 2.4),
        ("GAP 3: Opaque Black-Box Model Scoring", "Uncalibrated probabilities fail court scrutiny", 0.5, 1.3),
        ("GAP 4: Fragile Digital Chain of Custody", "Manual screenshots break evidentiary validity", 0.5, 0.2),
    ]

    responses = [
        ("Response 1: Auth-Decoupled Behavioral Modeling", "Model 2 scans financial urgency independently", 5.5, 3.5),
        ("Response 2: Integrated Engine 5 (41-Feat NDR)", "Live Npcap packet capture alongside email", 5.5, 2.4),
        ("Response 3: Explainable 0-100 Bayesian Fusion", "Transparent point deductions with audit trace", 5.5, 1.3),
        ("Response 4: Immutable SHA-256 Forensic Ledger", "Tamper-evident court-ready PDF dossiers", 5.5, 0.2),
    ]

    for title, sub, x, y in gaps:
        draw_box(ax, x, y, 4.0, 0.85, title, sub, "#FEF2F2", "#EF4444")

    for title, sub, x, y in responses:
        draw_box(ax, x, y, 4.0, 0.85, title, sub, "#F0FDF4", "#22C55E")

    draw_arrow(ax, 4.5, 3.92, 5.5, 3.92, "#10B981")
    draw_arrow(ax, 4.5, 2.82, 5.5, 2.82, "#10B981")
    draw_arrow(ax, 4.5, 1.72, 5.5, 1.72, "#10B981")
    draw_arrow(ax, 4.5, 0.62, 5.5, 0.62, "#10B981")

    ax.set_xlim(0, 10.0)
    ax.set_ylim(0.0, 5.2)
    plt.tight_layout()
    out = os.path.join(SCREENSHOTS_DIR, "figure_2_2_research_gaps.png")
    plt.savefig(out, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[+] Figure 2.2 saved: {out}")

if __name__ == "__main__":
    generate_figure_1_1()
    generate_figure_1_2()
    generate_figure_2_1()
    generate_figure_2_2()
