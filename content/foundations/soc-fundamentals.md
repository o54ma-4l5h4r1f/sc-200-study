+++
slug = "soc-fundamentals"
title = "SOC fundamentals: alerts, incidents, triage and ATT&CK"
summary = "What a security operations centre does all day, and the words SC-200 assumes you already know: event, alert, incident, triage, true/false/benign positive, severity, SIEM, SOAR, XDR, EDR, IoC, TTP, MITRE ATT&CK, hunting and automation levels."
order = 1
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/training/modules/describe-security-capabilities-of-azure-sentinel/2-define-concepts-of-siem-soar",
  "https://learn.microsoft.com/en-us/defender-xdr/microsoft-365-defender",
  "https://learn.microsoft.com/en-us/defender-endpoint/overview-endpoint-detection-response",
  "https://learn.microsoft.com/en-us/azure/sentinel/incident-navigate-triage",
  "https://learn.microsoft.com/en-us/azure/sentinel/microsoft-365-defender-sentinel-integration",
  "https://learn.microsoft.com/en-us/azure/sentinel/understand-threat-intelligence",
  "https://learn.microsoft.com/en-us/azure/sentinel/mitre-coverage",
  "https://learn.microsoft.com/en-us/security/zero-trust/siem-xdr-implement",
  "https://learn.microsoft.com/en-us/defender-xdr/playbook-detecting-ransomware-m365-defender",
  "https://learn.microsoft.com/en-us/defender-endpoint/automation-levels",
  "https://learn.microsoft.com/cli/azure/sentinel/incident?view=azure-cli-latest",
]
captured = 2026-11-12
+++

## In one sentence

A **security operations centre (SOC)** is the team that watches an organisation's computers, accounts and email for signs of attack, decides which warnings are real, and stops the real ones.

## Why it exists

Think of a large office building. It has hundreds of cameras, door sensors and smoke detectors. Nobody can watch every camera. So the building has a **guard desk**: one room where every sensor reports, where a guard decides "that's the cleaner" or "that's a burglar", and where someone phones the police.

A SOC is that guard desk for IT. Thousands of systems produce activity records every minute. Attackers hide inside that noise. Without one place to collect, sort and act on it, a break-in can go unnoticed for days or weeks. Microsoft's own training puts it plainly: with a central system, detection can happen within minutes instead.

SC-200 is the exam for the person sitting at that desk — the **security operations analyst**. Every tool in the exam (Microsoft Sentinel, Microsoft Defender XDR, Defender for Cloud) exists to feed, sort or act on that desk's work.

## Mental model

Everything in a SOC is a funnel. Lots of raw activity goes in the top. A few real cases come out the bottom.

```svg
<svg viewBox="0 0 760 330" role="img" aria-label="SOC funnel: events become alerts, alerts are grouped into incidents, incidents are triaged, investigated, responded to and closed with a classification">
  <defs>
    <marker id="sfarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="currentColor"/>
    </marker>
  </defs>
  <rect class="box" x="20" y="20" width="200" height="80" rx="8"/>
  <text x="120" y="48" text-anchor="middle" class="label-accent">Events</text>
  <text x="120" y="70" text-anchor="middle">millions per day</text>
  <text x="120" y="90" text-anchor="middle" class="muted">"user signed in", "file opened"</text>
  <rect class="box-accent" x="280" y="20" width="200" height="80" rx="8"/>
  <text x="380" y="48" text-anchor="middle" class="label-accent">Alerts</text>
  <text x="380" y="70" text-anchor="middle">a rule or sensor says</text>
  <text x="380" y="90" text-anchor="middle">"this looks suspicious"</text>
  <rect class="box-risk" x="540" y="20" width="200" height="80" rx="8"/>
  <text x="640" y="48" text-anchor="middle" class="label-risk">Incident</text>
  <text x="640" y="70" text-anchor="middle">related alerts grouped</text>
  <text x="640" y="90" text-anchor="middle">into one case file</text>
  <line class="line" x1="220" y1="60" x2="276" y2="60" marker-end="url(#sfarrow)"/>
  <line class="line" x1="480" y1="60" x2="536" y2="60" marker-end="url(#sfarrow)"/>
  <text x="248" y="50" text-anchor="middle" class="muted">detect</text>
  <text x="508" y="50" text-anchor="middle" class="muted">correlate</text>
  <rect class="box" x="20" y="170" width="160" height="70" rx="8"/>
  <text x="100" y="198" text-anchor="middle" class="label-accent">Triage</text>
  <text x="100" y="220" text-anchor="middle">real? how bad?</text>
  <rect class="box" x="210" y="170" width="160" height="70" rx="8"/>
  <text x="290" y="198" text-anchor="middle" class="label-accent">Investigate</text>
  <text x="290" y="220" text-anchor="middle">scope, root cause</text>
  <rect class="box" x="400" y="170" width="160" height="70" rx="8"/>
  <text x="480" y="198" text-anchor="middle" class="label-accent">Respond</text>
  <text x="480" y="220" text-anchor="middle">isolate, disable, block</text>
  <rect class="box-ok" x="590" y="170" width="150" height="70" rx="8"/>
  <text x="665" y="198" text-anchor="middle" class="label-accent">Close</text>
  <text x="665" y="220" text-anchor="middle">with a classification</text>
  <path class="line" d="M640,100 L640,135 L100,135 L100,166" marker-end="url(#sfarrow)"/>
  <line class="line" x1="180" y1="205" x2="206" y2="205" marker-end="url(#sfarrow)"/>
  <line class="line" x1="370" y1="205" x2="396" y2="205" marker-end="url(#sfarrow)"/>
  <line class="line" x1="560" y1="205" x2="586" y2="205" marker-end="url(#sfarrow)"/>
  <text x="380" y="285" text-anchor="middle" class="muted">True positive · Benign positive · False positive · Undetermined</text>
  <text x="380" y="310" text-anchor="middle" class="muted">Severity at every stage: High · Medium · Low · Informational</text>
</svg>
```

- An **event** is one recorded thing that happened: a sign-in, a file download, a process starting. Most events are harmless.
- An **alert** is an event (or pattern of events) that a rule or sensor flagged as suspicious.
- An **incident** is a case file: several related alerts grouped together because they look like one attack. Analysts work incidents, not single alerts.

## What actually matters

**1. Triage, then classify.** **Triage** means the first quick look at a new incident: is it real, how bad is it, who owns it? In Microsoft Sentinel you filter the incident queue by status, severity or product, assign an owner, and change status. Incident **status** is `New`, `Active` or `Closed`. When you close one, choosing a classification is mandatory.

| Verdict | Plain meaning | Example |
|---|---|---|
| ==@True positive== | Real malicious activity | Attacker signed in with a stolen password |
| ==@Benign positive== | The rule worked, the activity was real, but it was allowed | The IT team's own vulnerability scanner |
| ==@False positive== | The rule fired on something that was not what it claimed | A bad rule or bad data |
| ==@Undetermined== | You could not tell | Logs missing |

Sentinel splits false positives into "incorrect alert logic" and "incorrect data". The Defender portal calls a benign positive **"Informational, expected activity"**. When the two are connected, Microsoft maps one to the other automatically.

**2. Severity** is how bad it would be if true: **High, Medium, Low, Informational**. It drives what you look at first. ==!Severity is not confidence== — a High alert can still be a false positive.

**3. SIEM, SOAR, XDR, EDR** — four acronyms, four jobs.

| Term | Stands for | Job | Microsoft product |
|---|---|---|---|
| **SIEM** | Security information and event management | Collects logs from *everything*, correlates them, raises alerts and incidents | Microsoft Sentinel |
| **SOAR** | Security orchestration, automation and response | Runs automatic response workflows (**playbooks**) when an alert or incident fires | Sentinel automation rules + playbooks |
| **XDR** | Extended detection and response | Detection and response across several Microsoft-protected areas at once — devices, identities, email, cloud apps — with one shared incident queue | Microsoft Defender XDR |
| **EDR** | Endpoint detection and response | Detection and response on **endpoints** (laptops, servers) only | Microsoft Defender for Endpoint |

Rule of thumb: EDR is one sensor type. XDR joins several Microsoft sensor types. SIEM takes in anything, Microsoft or not. SOAR is the "do something automatically" layer on top.

```svg
<svg viewBox="0 0 760 270" role="img" aria-label="Scope of EDR inside XDR inside SIEM, with SOAR acting on the output">
  <rect class="box" x="20" y="20" width="520" height="230" rx="10"/>
  <text x="40" y="46" class="label-accent">SIEM — Microsoft Sentinel</text>
  <text x="40" y="66" class="muted">any log: firewalls, Azure, AWS, Linux, Microsoft, others</text>
  <rect class="box-accent" x="50" y="85" width="460" height="145" rx="10"/>
  <text x="70" y="110" class="label-accent">XDR — Microsoft Defender XDR</text>
  <text x="70" y="130" class="muted">endpoints + identities + email + cloud apps</text>
  <rect class="box-ok" x="80" y="148" width="190" height="66" rx="8"/>
  <text x="175" y="174" text-anchor="middle" class="label-accent">EDR</text>
  <text x="175" y="196" text-anchor="middle">Defender for Endpoint</text>
  <rect class="box" x="290" y="148" width="200" height="66" rx="8"/>
  <text x="390" y="174" text-anchor="middle">Office 365, Identity,</text>
  <text x="390" y="196" text-anchor="middle">Cloud Apps sensors</text>
  <rect class="box-risk" x="580" y="85" width="160" height="145" rx="10"/>
  <text x="660" y="115" text-anchor="middle" class="label-risk">SOAR</text>
  <text x="660" y="140" text-anchor="middle">acts on incidents</text>
  <text x="660" y="162" text-anchor="middle">disable user,</text>
  <text x="660" y="182" text-anchor="middle">open ticket,</text>
  <text x="660" y="202" text-anchor="middle">post to Teams</text>
  <line class="line" x1="540" y1="157" x2="576" y2="157"/>
</svg>
```

![Diagram of a Microsoft Sentinel and Microsoft Defender XDR architecture in the unified security operations experience](https://learn.microsoft.com/en-us/azure/sentinel/media/microsoft-365-defender-sentinel-integration/sentinel-xdr-usx.svg){Sentinel (SIEM) and Defender XDR together in the Defender portal — the stack-map page explains every box}

![Diagram of the integration of Microsoft Sentinel and Microsoft Defender XDR](https://learn.microsoft.com/en-us/azure/sentinel/media/microsoft-365-defender-sentinel-integration/sentinel-xdr.svg){The same integration drawn the older way, with Sentinel still in the Azure portal}

**4. IoC versus TTP.** An **indicator of compromise (IoC)** is a concrete artefact linked to known bad activity: an IP address, domain, URL or file hash (a fingerprint of a file). A **TTP** (tactics, techniques and procedures) describes *how* an attacker behaves. IoCs are cheap for attackers to change; behaviour is not. Microsoft calls IoC feeds *tactical threat intelligence*, and stores both in Sentinel in the STIX format.

**5. MITRE ATT&CK.** A free public catalogue of attacker behaviour, built from real attacks. A **tactic** is the attacker's goal at a stage (the column, for example *Credential Access*). A **technique** is how they do it (the cell, for example *Valid Accounts*, ID `T1078`). Laid out as a grid, it is called **the matrix**. Sentinel tags rules and incidents with tactics and techniques and shows your coverage on a MITRE ATT&CK page. It is aligned to ATT&CK **version 18**.

**6. The attack chain you will meet.** SC-200 scenarios reuse one story again and again:

| Stage | What the attacker does | Who usually spots it |
|---|---|---|
| Phishing (initial access) | Sends a fake email; user opens attachment or link | Defender for Office 365 |
| Malware / execution | Attachment installs malware | Defender for Endpoint |
| Credential theft | Steals passwords or tokens | Entra ID Protection (cloud accounts), Defender for Identity (on-premises accounts) |
| Privilege escalation | Gets a more powerful account | Defender for Identity |
| Lateral movement | Hops from machine to machine or app to app | Defender for Cloud Apps (apps), Defender for Endpoint (devices) |
| Persistence | Plants a way back in: a new user account, a role change, a new app | Entra ID Protection, Defender for Cloud Apps |
| Exfiltration | Copies data out by email or cloud app, for example a mass SharePoint download | Defender for Cloud Apps, Defender for Office 365 |

![Diagram of a common attack scenario and defenses provided by Microsoft security products](https://learn.microsoft.com/en-us/security/zero-trust/media/common-attack-defense.svg){Phishing to data theft, with the Microsoft product that sees each step}

![Diagram of performing incident investigation using Microsoft Sentinel and Microsoft Defender XDR](https://learn.microsoft.com/en-us/security/zero-trust/media/investigation-flow.svg){How an analyst works that same incident across Defender XDR and Sentinel}

![The qualitative relationship of the impact of a ransomware attack and your time to respond](https://learn.microsoft.com/en-us/defender-xdr/media/playbook-detecting-ransomware-m365-defender/playbook-detecting-ransomware-m365-defender-qualitative-diagram.png){Why speed matters: the faster you detect and respond, the less damage}

**7. Detection, hunting, response.** **Detection** is automatic: a rule or sensor raises an alert for you. **Hunting** is manual: you write your own queries over raw data to look for threats nothing has alerted on yet. Defender XDR keeps **30 days** of raw data for hunting. **Response** is the action: isolate a device, disable an account, block a file.

**8. Automation levels.** Automation runs from "human does every step" to "machine fixes it alone". In Defender for Endpoint the levels are **Full** (remediate automatically — recommended, default for new tenants), several **Semi** levels (ask for approval first, for all folders or only core or non-temp folders), and **No automated response** (not recommended). Pending approvals time out after **seven days**. Since **1 September 2026**, automated investigation no longer runs as a separate investigation experience; its detection and response now run inside the default antivirus protection. Defender XDR also does **automatic attack disruption**: it contains an attack in progress by itself, for example by disabling an account or isolating a device.

## Where it lives

- **Microsoft Defender portal** (`https://security.microsoft.com`): **Investigation & response > Incidents & alerts > Incidents** is the one incident queue for Defender XDR and, once connected, Sentinel.
- **Microsoft Sentinel's MITRE page:** Defender portal **Microsoft Sentinel > Threat management > MITRE ATT&CK**, or Azure portal **Microsoft Sentinel > Threat management > MITRE ATT&CK (Preview)**.
- **Closing an incident from the command line:** `az sentinel incident update` takes `--classification` (`TruePositive`, `BenignPositive`, `FalsePositive`, `Undetermined`) and `--severity` (`High`, `Medium`, `Low`, `Informational`).

![Screenshot of view of incident severity](https://learn.microsoft.com/en-us/azure/sentinel/media/investigate-incidents/incident-grid.png){The Sentinel incident queue in the Azure portal — counts by severity across the top}

![Screenshot of assigning incident to user](https://learn.microsoft.com/en-us/azure/sentinel/media/investigate-incidents/assign-incident-to-user.png){Triage step one: assign an owner}

![Screenshot of menu of actions that can be performed on an incident from the details pane](https://learn.microsoft.com/en-us/azure/sentinel/media/investigate-incidents/incident-actions.png){Actions available straight from the details pane}

![Screenshot of the incident search box and button to select basic and/or advanced search options](https://learn.microsoft.com/en-us/azure/sentinel/media/investigate-incidents/advanced-search.png){Searching the queue}

![Screenshot that highlights the classifications available in the Select classification list](https://learn.microsoft.com/en-us/azure/sentinel/media/investigate-incidents/closing-reasons-dropdown.png){The five closing classifications — true, benign, two kinds of false, undetermined}

![Screenshot of closing an incident](https://learn.microsoft.com/en-us/azure/sentinel/media/investigate-incidents/closing-reasons-comment-apply.png){Add a comment, then Apply}

![Screenshot of the MITRE ATT&CK page in the Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/media/mitre-coverage/mitre-coverage-defender.png){The ATT&CK matrix in the Defender portal: tactics are columns, techniques are cells}

![Screenshot of the MITRE ATT&CK page filtered by a specific threat scenario](https://learn.microsoft.com/en-us/azure/sentinel/media/mitre-coverage/mitre-by-threat-scenario.png){Filtered to one threat scenario}

![Screenshot of the MITRE ATT&CK coverage matrix in the Azure portal showing technique coverage levels](https://learn.microsoft.com/en-us/azure/sentinel/media/mitre-coverage/mitre-coverage.png){The same matrix in the Azure portal}

The threat-intelligence screens, where IoCs and TTP objects live:

![Diagram that shows the upload API import path](https://learn.microsoft.com/en-us/azure/sentinel/media/understand-threat-intelligence/threat-intel-upload-api.png){Indicators arriving through the upload API}

![Screenshot that shows a threat intelligence import path](https://learn.microsoft.com/en-us/azure/sentinel/media/understand-threat-intelligence/threat-intel-import-path.png){Threat intelligence import path}

![Screenshot that shows a TAXII import path](https://learn.microsoft.com/en-us/azure/sentinel/media/understand-threat-intelligence/threat-intel-taxii-import-path.png){TAXII import path — TAXII is a standard feed protocol for STIX data}

![Screenshot showing intel management page in the Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/media/understand-threat-intelligence/intel-management-defender-portal.png){Intel management in the Defender portal}

![Screenshot of the menu to add new STIX objects along with its options](https://learn.microsoft.com/en-us/azure/sentinel/media/understand-threat-intelligence/new-object.png){Adding a STIX object: indicator, attack pattern (a TTP), threat actor, identity, relationship}

![Screenshot shows four ingestion rules matching the use cases](https://learn.microsoft.com/en-us/azure/sentinel/media/understand-threat-intelligence/ingestion-rules-overview.png){Ingestion rules that filter or adjust incoming intelligence}

![Screenshot showing example relationship being built](https://learn.microsoft.com/en-us/azure/sentinel/media/understand-threat-intelligence/relationship-example.png){Linking an indicator to a threat actor}

![Screenshot that shows an advanced search interface with source and confidence conditions selected](https://learn.microsoft.com/en-us/azure/sentinel/media/understand-threat-intelligence/advanced-search.png){Searching intelligence by source and confidence}

![Screenshot that shows a high-fidelity incident generated by matching analytics](https://learn.microsoft.com/en-us/azure/sentinel/media/understand-threat-intelligence/detect-threats-matching-analytics.png){An incident raised because your logs matched a Microsoft threat-intelligence indicator}

## What the exam assumes you know

- ==!Alert and incident are not synonyms.== Questions say "incident" when they mean the grouped case.
- ==!Benign positive is not a false positive.== The detection was correct; the activity was allowed. The fix is to tune or exclude, not to rewrite the rule.
- ==!XDR is not a SIEM.== Defender XDR covers Microsoft-protected workloads. Bringing in a third-party firewall needs Sentinel.
- ==!EDR is not antivirus.== Antivirus blocks known bad files. EDR records behaviour (Defender for Endpoint keeps **six months** of it) so you can investigate after the fact.
- Hunting finds what detection missed. A good hunt becomes a new detection rule.
- MITRE IDs look like `T1078`. Questions may ask you to map a technique to a rule or incident.

## Skip list

- **Skip** the AI/ML marketing in the SIEM/SOAR training unit (anomaly baselines, "machine speed"). Know only that analytics can group low-confidence alerts into one high-confidence incident.
- **Skip** the full STIX object list, TAXII server IP allowlists and ingestion-rule recipes in the threat-intelligence article. Here you need only "IoC versus TTP"; the threat-intelligence lesson covers the rest.
- **Skip** memorising the whole ATT&CK matrix. Know what a tactic and a technique are, the ID format, and the attack-chain stages above.
- **Skip** the Defender for Endpoint temp-folder path list for the semi-automation levels. Know the level names and that Full is recommended.
- **Skip** the ransomware playbook's tool names (Mimikatz, Cobalt Strike, PsExec) beyond recognising them as attacker tools.
