+++
slug = "purview-basics"
title = "Microsoft Purview basics for a SOC analyst"
summary = "You will know what Microsoft Purview is, how to find your way around the Purview portal (purview.microsoft.com), what DLP, Insider Risk Management, Audit, eDiscovery, sensitivity labels and Communication Compliance each do in a line or two, how Purview roles and role groups work, the licensing shape at a high level, and how Purview alerts reach the Defender portal incident queue."
order = 20
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/purview/purview",
  "https://learn.microsoft.com/en-us/purview/purview-portal",
  "https://learn.microsoft.com/en-us/purview/purview-permissions",
  "https://learn.microsoft.com/en-us/purview/purview-security",
  "https://learn.microsoft.com/en-us/purview/purview-compliance",
  "https://learn.microsoft.com/en-us/purview/purview-trial",
  "https://learn.microsoft.com/en-us/office365/servicedescriptions/microsoft-365-service-descriptions/microsoft-365-tenantlevel-services-licensing-guidance/microsoft-purview-service-description",
  "https://learn.microsoft.com/en-us/purview/dlp-alerts-dashboard-get-started",
  "https://learn.microsoft.com/en-us/purview/dlp-alert-investigation-learn",
  "https://learn.microsoft.com/en-us/defender-xdr/dlp-investigate-alerts-defender",
  "https://learn.microsoft.com/en-us/defender-xdr/irm-investigate-alerts-defender",
]
captured = 2026-11-12
related_objectives = ["D2.1.2", "D2.3.1", "D2.3.2"]
+++

## In one sentence

**Microsoft Purview** is Microsoft's family of *data* protection and compliance tools for Microsoft 365 and beyond. It watches what happens to sensitive information, keeps records of who did what, and finds content for investigations.

## Why it exists

Defender and Sentinel ask "is an attacker in my network?" Purview asks a different question: "is my *data* safe, and can I prove what happened to it?"

Think of a bank. The guards and cameras watch for robbers — that is Defender. But the bank also has rules about which documents may leave the building, a log of every vault opening, staff who watch for employees stealing, and a records room lawyers can search. That second set of jobs is Purview.

A SOC (security operations centre) analyst meets Purview in three places:

- Its **alerts** — data loss prevention and insider risk — land in the same **Defender portal** incident queue as malware alerts (D2.1.2).
- **Audit** is the "who did what, when" log you search after a compromise (D2.3.1).
- **eDiscovery** finds every copy of a phishing email or a leaked file across mailboxes and sites (D2.3.2).

## Mental model

Purview is a **toolbox with three drawers**: data security, data compliance, data governance. A SOC analyst mostly opens the first two. Everything sits behind one front door, the Purview portal, and access is handed out by **role groups**.

```svg
<svg viewBox="0 0 900 420" role="img" aria-label="Microsoft Purview mental model: the Purview portal is one front door with three drawers; data security holds DLP, Insider Risk Management, Information Protection and sensitivity labels; data compliance holds Audit, eDiscovery and Communication Compliance; data governance holds Data Map and Unified Catalog; DLP and Insider Risk alerts flow into the Defender portal incident queue where SOC analysts triage them">
  <defs>
    <marker id="pvbarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <rect class="box-accent" x="20" y="20" width="560" height="50" rx="8"/>
  <text x="300" y="51" text-anchor="middle" class="label-accent">Purview portal — purview.microsoft.com</text>
  <rect class="box" x="20" y="90" width="175" height="200" rx="8"/>
  <text x="107" y="115" text-anchor="middle" class="label-accent">Data security</text>
  <text x="107" y="145" text-anchor="middle">DLP</text>
  <text x="107" y="170" text-anchor="middle">Insider Risk Mgmt</text>
  <text x="107" y="195" text-anchor="middle">Info Protection</text>
  <text x="107" y="220" text-anchor="middle">sensitivity labels</text>
  <text x="107" y="270" text-anchor="middle" class="muted">"stop data leaving"</text>
  <rect class="box" x="212" y="90" width="175" height="200" rx="8"/>
  <text x="299" y="115" text-anchor="middle" class="label-accent">Data compliance</text>
  <text x="299" y="145" text-anchor="middle">Audit</text>
  <text x="299" y="170" text-anchor="middle">eDiscovery</text>
  <text x="299" y="195" text-anchor="middle">Comm. Compliance</text>
  <text x="299" y="220" text-anchor="middle" class="muted">retention, records</text>
  <text x="299" y="270" text-anchor="middle" class="muted">"prove and find"</text>
  <rect class="box" x="405" y="90" width="175" height="200" rx="8"/>
  <text x="492" y="115" text-anchor="middle">Data governance</text>
  <text x="492" y="145" text-anchor="middle" class="muted">Data Map</text>
  <text x="492" y="170" text-anchor="middle" class="muted">Unified Catalog</text>
  <text x="492" y="270" text-anchor="middle" class="muted">not SOC work</text>
  <rect class="box-risk" x="640" y="110" width="240" height="110" rx="10"/>
  <text x="760" y="140" text-anchor="middle" class="label-risk">Defender portal</text>
  <text x="760" y="165" text-anchor="middle">Incidents &amp; alerts</text>
  <text x="760" y="190" text-anchor="middle" class="muted">DLP + IRM alerts sit</text>
  <text x="760" y="208" text-anchor="middle" class="muted">beside malware alerts</text>
  <line class="line-accent" x1="195" y1="155" x2="638" y2="150" marker-end="url(#pvbarrow)"/>
  <rect class="box-ok" x="20" y="320" width="560" height="80" rx="8"/>
  <text x="300" y="347" text-anchor="middle">Access: role groups (bundles of roles) in Settings &gt; Roles and scopes</text>
  <text x="300" y="372" text-anchor="middle" class="muted">e.g. Insider Risk Management, eDiscovery Manager</text>
  <text x="300" y="390" text-anchor="middle" class="muted">plus Entra roles that map onto Purview role groups</text>
  <text x="760" y="260" text-anchor="middle" class="muted">SOC analysts triage here;</text>
  <text x="760" y="280" text-anchor="middle" class="muted">policies are edited in Purview</text>
</svg>
```

![Solution areas in Microsoft Purview.](https://learn.microsoft.com/en-us/purview/media/purview-areas.png){Microsoft's map of Purview's solution areas}

## What actually matters

**1. The six solutions a SOC analyst should recognise.**

| Solution | What it does, in one line | SC-200 link |
|---|---|---|
| **Data loss prevention (DLP)** | Rules that spot sensitive data (card numbers, passport numbers, labelled files) in Microsoft 365 services and on Windows/macOS devices, then audit, block, or block with override — and can raise an **alert**. | D2.1.2 |
| **Insider Risk Management (IRM)** | Reads Microsoft 365 and Microsoft Graph activity logs to spot risky *employee* behaviour, such as downloading lots of files before leaving. | D2.1.2 |
| **Audit** | The **unified audit log**: thousands of user and admin actions across dozens of Microsoft 365 services, searchable after the fact. | D2.3.1 |
| **eDiscovery** | Searches mail, OneDrive, SharePoint, Teams, Microsoft 365 Groups and Viva Engage for content, can hold it in place, and exports it. Content search is now part of eDiscovery. | D2.3.2 |
| **Sensitivity labels** | Tags like *Confidential* that users or rules put on files and emails. A label can encrypt, restrict access or add a watermark. Labels are part of **Information Protection**. | context for DLP |
| **Communication Compliance** | Scans email and Teams messages for harassment, threats, profanity or sensitive data being shared. | name only |

DLP and IRM look similar. ==DLP looks at one *item* breaking a rule.== IRM looks at one *person's pattern* over time.

**2. Role groups, not just roles.** A **role** is one permission set, such as *Case Management*. A **role group** is a bundle of roles you add people to, such as *Insider Risk Management* or *eDiscovery Manager*. You manage them in the Purview portal at **Settings > Roles and scopes > Role groups**. Viewing role groups there needs **Global Administrator** or the **Role Management** role (only in the *Organization Management* role group). Some Microsoft Entra roles map onto Purview role groups: **Security Reader**, **Security Operator**, **Security Administrator**, **Compliance Administrator**, **Compliance Data Administrator** and **Global Reader** each map to a Purview role group of the same name. If a user has both an Entra role and a scoped Purview assignment, ==!the Entra role wins and the scoping is ignored==.

**3. Two portals, one alert.** DLP and IRM alerts are created in Purview but Microsoft recommends triaging them in the **Defender portal** under **Incidents & alerts**. There they are grouped into incidents with alerts from Defender for Endpoint, Defender for Office 365, Sentinel and others, and you get about six months of incident history and **advanced hunting**. Filter the queue with **Service source** = *Data Loss Prevention* or *Microsoft Purview Insider Risk Management*. Policies are still created and edited in Purview.

Three gotchas:

- ==!Since early October 2026 a built-in alert tuning rule turns DLP signals into *behaviors*, not alerts==, so by default they don't appear in the incident queue. They stay huntable in the `BehaviorInfo` and `BehaviorEntities` tables. Turn the rule off under **Settings > Microsoft Defender XDR > Alert tuning** to get DLP alerts back.
- IRM alerts appear in Defender only after **Data sharing** is turned on in IRM settings. Status and classification sync between the two portals within **30 minutes**.
- You need *both* sides of permission: a Defender role (Security Reader or Security Operator) **and** an IRM role group (*Insider Risk Management*, *Insider Risk Management Analysts* or *Insider Risk Management Investigators*).

**4. Licensing, high level.** Licences decide which solutions appear. Audit (Standard) and core eDiscovery search come with E3-level plans. The investigation-grade features need **E5-level** licences. Insider Risk Management needs Microsoft 365 E5, the **Microsoft Purview Suite** (formerly *Microsoft 365 E5 Compliance*) or the E5 Insider Risk Management add-on. Investigating DLP incidents in the Defender portal needs Office 365 E5, Microsoft 365 E5, Microsoft 365 E5 Compliance or Microsoft 365 E5 Information Protection and Governance. A 90-day **Purview Suite trial** gives 25 licences to tenants with Microsoft 365 E3 (or Office 365 E3 plus EMS E3). An Azure-only subscription has none of this — treat Purview as screenshots.

## Where it lives

The **Microsoft Purview portal** — `https://purview.microsoft.com`. The old *Microsoft Purview compliance portal* is retired.

| Task | Where |
|---|---|
| Open a solution | Home page **solution cards**, or **Solutions** > the solution |
| Roles and role groups | **Settings > Roles and scopes > Role groups** |
| DLP alerts (Purview view) | **Data Loss Prevention > Alerts** |
| DLP / IRM incidents (recommended view) | Defender portal `security.microsoft.com` > **Incidents & alerts > Incidents** |
| Audit, eDiscovery | **Solutions > Audit**, **Solutions > eDiscovery** |
| Start a trial | Home > **Trials and recommendations** > **View all trials and recommendations** |

You only see the solution cards you have both the licence and the permission for.

![Screenshot of the Microsoft Purview portal welcome dialog showing the main starting point for accessing Purview features.](https://learn.microsoft.com/en-us/purview/media/purview-portal-welcome.png){First visit: the welcome dialog}

![Screenshot of the Microsoft Purview portal home page displaying solution cards, compliance posture, and navigation options.](https://learn.microsoft.com/en-us/purview/media/purview-portal.png){The Purview home page}

![Screenshot of Microsoft Purview portal solution cards showing available solutions on the home page.](https://learn.microsoft.com/en-us/purview/media/purview-portal-solution-cards.png){Solution cards — only the ones you are licensed and permitted for}

![Screenshot of the Microsoft Purview portal solutions page showing core, risk and compliance, data governance, and data security sections.](https://learn.microsoft.com/en-us/purview/media/purview-portal-solutions-page.png){Solutions page: Core, Risk & Compliance, Data Governance, Data Security}

![Screenshot of the Microsoft Purview portal left navigation showing links to Home, Solutions, Learn, Settings, and recent solutions.](https://learn.microsoft.com/en-us/purview/media/purview-portal-left-navigation.png){Left navigation inside a solution}

![Screenshot of Microsoft Purview portal search results grouped by navigation, users, and resources categories.](https://learn.microsoft.com/en-us/purview/media/purview-portal-search-results.png){Global search: Navigation, Users, Resources}

![Screenshot of the Microsoft Purview portal settings pane showing centralized options for themes, language, time zone, password, and contact preferences.](https://learn.microsoft.com/en-us/purview/media/purview-portal-settings.png){Settings pane}

![Screenshot of the Microsoft Purview portal solution settings page showing configuration options for a selected solution.](https://learn.microsoft.com/en-us/purview/media/purview-portal-solution-settings.png){Per-solution settings}

![Screenshot of the Role groups page in the Microsoft Purview portal showing role groups, Microsoft Entra roles, and administrative units.](https://learn.microsoft.com/en-us/purview/media/purview-portal-roles.png){Settings > Roles and scopes > Role groups}

![Diagram showing the relationship of role groups to roles and members, where role groups contain roles and members are assigned to role groups.](https://learn.microsoft.com/en-us/purview/media/2a16d200-968c-4755-98ec-f1862d58cb8b.png){Members join role groups; role groups contain roles}

![Screenshot of the Compliance posture status card in the Microsoft Purview portal showing assessment completion percentages and posture breakdown.](https://learn.microsoft.com/en-us/purview/media/purview-portal-compliance-posture-status.png){Compliance posture card (from Compliance Manager) — not SOC work}

![Screenshot of the Trials and recommendations card in the Microsoft Purview portal showing available trial solutions and recommended actions.](https://learn.microsoft.com/en-us/purview/media/purview-portal-trials-recommendations.png){Trials and recommendations — where the Purview Suite trial starts}

![Screenshot of the Knowledge Center card in the Microsoft Purview portal showing articles, product demos, tutorials, and learning materials.](https://learn.microsoft.com/en-us/purview/media/purview-portal-knowledge-center.png){Knowledge Center card}

![Screenshot of the Microsoft Purview portal help and support pane showing options for guided tours, Knowledge Center, and solution-specific help.](https://learn.microsoft.com/en-us/purview/media/purview-portal-help-support.png){Help and support pane}

How Purview alerts look in the Defender portal:

![Highlighting the setting in the Microsoft Purview portal required for insider risk alerts to show in Defender XDR.](https://learn.microsoft.com/en-us/defender-xdr/media/irm-investigate-alerts-defender/irm-toggle-settings-small.png){IRM Data sharing setting — off means no IRM alerts in Defender}

![Sample of an incident with insider risk alerts from Microsoft Purview Insider Risk Management.](https://learn.microsoft.com/en-us/defender-xdr/media/irm-investigate-alerts-defender/xdr-irm-incident-small.png){An incident in Defender that holds Insider Risk Management alerts}

![Sample of an insider risk alerts from Microsoft Purview Insider Risk Management.](https://learn.microsoft.com/en-us/defender-xdr/media/irm-investigate-alerts-defender/xdr-irm-alert-small.png){One IRM alert in the Defender alert page}

![Advanced hunting page showing a query using the tables related to insider risk behaviors and events.](https://learn.microsoft.com/en-us/defender-xdr/media/irm-investigate-alerts-defender/irm-adv-hunting-small.png){Advanced hunting over the DataSecurityEvents table}

## What the exam assumes you know

- The Purview portal is `purview.microsoft.com`; the Defender portal is `security.microsoft.com`. ==+Triage DLP and IRM alerts in Defender; edit policies in Purview.==
- ==!Global Administrator does not automatically make you an eDiscovery Manager.== Purview access comes from role groups (D2.3.2).
- DLP = an item breaking a rule. IRM = a person's risky pattern. Audit = the record of actions. eDiscovery = finding content.
- Advanced Purview features are **E5-level**. Expect "which licence" distractors.
- Detail on alert triage is in D2.1.2, Audit in D2.3.1, eDiscovery in D2.3.2.

## Skip list

- **Skip** data governance (Data Map, Unified Catalog, scanning, the free versus enterprise data governance versions). Data catalogue work, not SOC work.
- **Skip** Compliance Manager, Data Lifecycle Management, Records Management, Information Barriers and Privileged Access Management. Named in the solution list; never an SC-200 task.
- **Skip** encryption keys (Double Key Encryption, Customer Key) and how to build sensitivity labels. Know a label can encrypt and that DLP can read it.
- **Skip** Data Security Posture Management (DSPM) and Data Security Investigations. Preview or out of scope for the exam's bullets.
- **Skip** the per-solution permission articles and administrative units. Learn the role group names on the objective pages that need them.
- **Skip** the Graph security API permission table for IRM and the portal's theme, Knowledge Center and feedback panels. Not tested.
