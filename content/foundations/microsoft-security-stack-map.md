+++
slug = "microsoft-security-stack-map"
title = "The Microsoft security stack: which product does what, and where"
summary = "Every product named in SC-200 — Defender XDR and its family, Microsoft Sentinel, Defender for Cloud, Purview, Entra ID and ID Protection, Security Copilot — what each one protects, which portal it lives in, and how alerts flow between them."
order = 2
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/defender-xdr/microsoft-365-defender",
  "https://learn.microsoft.com/en-us/azure/sentinel/overview",
  "https://learn.microsoft.com/en-us/azure/sentinel/microsoft-sentinel-defender-portal",
  "https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-overview",
  "https://learn.microsoft.com/en-us/azure/sentinel/microsoft-365-defender-sentinel-integration",
  "https://learn.microsoft.com/en-us/security/zero-trust/siem-xdr-overview",
  "https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-cloud-introduction",
  "https://learn.microsoft.com/en-us/purview/purview",
  "https://learn.microsoft.com/en-us/purview/data-governance-purview-portal-faq",
  "https://learn.microsoft.com/en-us/entra/fundamentals/whatis",
  "https://learn.microsoft.com/en-us/entra/id-protection/overview-identity-protection",
  "https://learn.microsoft.com/en-us/copilot/security/microsoft-security-copilot",
]
captured = 2026-11-12
+++

## In one sentence

Microsoft sells one product per thing you need to protect — devices, email, identities, cloud apps, cloud servers, data — plus one SIEM (Microsoft Sentinel) that collects everything, and today almost all of it is worked from one website: the **Microsoft Defender portal** at `https://security.microsoft.com`.

## Why it exists

Picture a shopping centre. Each shop has its own alarm: the jeweller, the bank, the car park. Each alarm knows its own shop well. But a thief who cases the car park, then the bank, then the jeweller looks harmless to each alarm alone. You need a **central control room** that sees all the alarms on one wall, plus the shopping centre's own cameras.

Microsoft's stack is built the same way:

- each **Defender** product is a shop alarm for one kind of thing;
- **Defender XDR** is the wall that joins the Microsoft alarms into one story;
- **Microsoft Sentinel** is the control room that also takes in feeds from *non-Microsoft* systems (firewalls, AWS, Linux servers).

SC-200 tests whether you know **which product sees which attack step** and **which portal you open to act on it**. Beginners lose marks there first.

## Mental model

```svg
<svg viewBox="0 0 900 600" role="img" aria-label="Microsoft security stack map: protected things on the left, the products that watch them in the middle, and the portals where analysts work on the right, with Sentinel and Defender XDR feeding one incident queue in the Defender portal">
  <defs>
    <marker id="msarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="currentColor"/>
    </marker>
  </defs>
  <text x="90" y="24" text-anchor="middle" class="label-accent">What is protected</text>
  <text x="400" y="24" text-anchor="middle" class="label-accent">Product that watches it</text>
  <text x="770" y="24" text-anchor="middle" class="label-accent">Where you work</text>
  <rect class="box" x="10" y="40" width="160" height="40" rx="6"/><text x="90" y="65" text-anchor="middle">Laptops, servers</text>
  <rect class="box" x="10" y="90" width="160" height="40" rx="6"/><text x="90" y="115" text-anchor="middle">Email, Teams</text>
  <rect class="box" x="10" y="140" width="160" height="40" rx="6"/><text x="90" y="165" text-anchor="middle">On-prem AD accounts</text>
  <rect class="box" x="10" y="190" width="160" height="40" rx="6"/><text x="90" y="215" text-anchor="middle">SaaS / cloud apps</text>
  <rect class="box" x="10" y="250" width="160" height="40" rx="6"/><text x="90" y="275" text-anchor="middle">Cloud sign-ins</text>
  <rect class="box" x="10" y="320" width="160" height="40" rx="6"/><text x="90" y="345" text-anchor="middle">Azure, AWS, GCP</text>
  <rect class="box" x="10" y="400" width="160" height="40" rx="6"/><text x="90" y="425" text-anchor="middle">Firewalls, 3rd party</text>
  <rect class="box" x="10" y="480" width="160" height="40" rx="6"/><text x="90" y="505" text-anchor="middle">Files, mail content</text>
  <rect class="box-accent" x="230" y="36" width="340" height="200" rx="10"/>
  <text x="400" y="56" text-anchor="middle" class="label-accent">Microsoft Defender XDR</text>
  <rect class="box" x="245" y="64" width="310" height="34" rx="5"/><text x="400" y="86" text-anchor="middle">Defender for Endpoint (EDR)</text>
  <rect class="box" x="245" y="104" width="310" height="34" rx="5"/><text x="400" y="126" text-anchor="middle">Defender for Office 365</text>
  <rect class="box" x="245" y="144" width="310" height="34" rx="5"/><text x="400" y="166" text-anchor="middle">Defender for Identity</text>
  <rect class="box" x="245" y="184" width="310" height="34" rx="5"/><text x="400" y="206" text-anchor="middle">Defender for Cloud Apps</text>
  <rect class="box" x="230" y="250" width="340" height="40" rx="6"/><text x="400" y="275" text-anchor="middle">Entra ID + Entra ID Protection</text>
  <rect class="box" x="230" y="320" width="340" height="40" rx="6"/><text x="400" y="345" text-anchor="middle">Defender for Cloud (CSPM + CWPP)</text>
  <rect class="box-ok" x="230" y="385" width="340" height="70" rx="8"/>
  <text x="400" y="410" text-anchor="middle" class="label-accent">Microsoft Sentinel (SIEM + SOAR)</text>
  <text x="400" y="432" text-anchor="middle">+ Sentinel data lake</text>
  <text x="400" y="448" text-anchor="middle" class="muted">collects everything, any vendor</text>
  <rect class="box" x="230" y="480" width="340" height="40" rx="6"/><text x="400" y="505" text-anchor="middle">Microsoft Purview (DLP, IRM, Audit, eDiscovery)</text>
  <line class="line" x1="170" y1="60" x2="241" y2="81" marker-end="url(#msarrow)"/>
  <line class="line" x1="170" y1="110" x2="241" y2="121" marker-end="url(#msarrow)"/>
  <line class="line" x1="170" y1="160" x2="241" y2="161" marker-end="url(#msarrow)"/>
  <line class="line" x1="170" y1="210" x2="241" y2="201" marker-end="url(#msarrow)"/>
  <line class="line" x1="170" y1="270" x2="226" y2="270" marker-end="url(#msarrow)"/>
  <line class="line" x1="170" y1="340" x2="226" y2="340" marker-end="url(#msarrow)"/>
  <line class="line" x1="170" y1="420" x2="226" y2="420" marker-end="url(#msarrow)"/>
  <line class="line" x1="170" y1="500" x2="226" y2="500" marker-end="url(#msarrow)"/>
  <rect class="box-accent" x="650" y="60" width="240" height="190" rx="10"/>
  <text x="770" y="88" text-anchor="middle" class="label-accent">Microsoft Defender portal</text>
  <text x="770" y="110" text-anchor="middle">security.microsoft.com</text>
  <text x="770" y="140" text-anchor="middle">one incident queue</text>
  <text x="770" y="162" text-anchor="middle">advanced hunting</text>
  <text x="770" y="184" text-anchor="middle">Sentinel menus</text>
  <text x="770" y="206" text-anchor="middle">Security Copilot embedded</text>
  <rect class="box" x="650" y="270" width="240" height="60" rx="8"/>
  <text x="770" y="295" text-anchor="middle">Entra admin center</text>
  <text x="770" y="317" text-anchor="middle" class="muted">entra.microsoft.com</text>
  <rect class="box" x="650" y="345" width="240" height="70" rx="8"/>
  <text x="770" y="370" text-anchor="middle">Azure portal</text>
  <text x="770" y="390" text-anchor="middle" class="muted">Defender for Cloud; Sentinel</text>
  <text x="770" y="407" text-anchor="middle" class="label-risk">Sentinel here until 31 Mar 2027</text>
  <rect class="box" x="650" y="475" width="240" height="50" rx="8"/>
  <text x="770" y="497" text-anchor="middle">Microsoft Purview portal</text>
  <text x="770" y="515" text-anchor="middle" class="muted">purview.microsoft.com</text>
  <line class="line-accent" x1="570" y1="136" x2="646" y2="136" marker-end="url(#msarrow)"/>
  <line class="line-accent" x1="570" y1="415" x2="646" y2="190" marker-end="url(#msarrow)"/>
  <line class="line" x1="570" y1="270" x2="646" y2="295" marker-end="url(#msarrow)"/>
  <line class="line" x1="570" y1="340" x2="646" y2="375" marker-end="url(#msarrow)"/>
  <line class="line" x1="570" y1="500" x2="646" y2="500" marker-end="url(#msarrow)"/>
  <rect class="box-risk" x="230" y="545" width="660" height="40" rx="8"/>
  <text x="560" y="570" text-anchor="middle">Security Copilot — an AI assistant layered over all of the above, not a sensor</text>
</svg>
```

Read it left to right: **thing protected → product that watches it → portal you work in.** The thick arrows matter most: Defender XDR and Sentinel both land in the **one incident queue** of the Defender portal.

## What actually matters

**1. The product table.** Learn this one table and most "which product?" questions answer themselves.

| Product | Protects / does | Kind of tool |
|---|---|---|
| **Microsoft Defender XDR** | Joins the four Defender products below into one incident queue, cross-product hunting (30 days of raw data) and automatic attack disruption | XDR |
| Defender for Endpoint | Endpoints (laptops, desktops, servers): prevention, post-breach detection, automated investigation and response | EDR |
| Defender for Office 365 | Email messages, links (URLs) and collaboration tools — phishing, malicious attachments | Email security |
| Defender for Identity | **On-premises Active Directory** accounts — compromised identities, insider actions | Identity threat detection |
| Defender for Cloud Apps | SaaS (software-as-a-service) cloud apps — visibility, data controls, threat protection | Cloud app security |
| **Microsoft Sentinel** | Collects logs from Microsoft *and* non-Microsoft sources; analytics rules, incidents, hunting, playbooks | SIEM + SOAR |
| Sentinel data lake | Cheap long-term store for security data, up to **12 years**, queried with KQL or notebooks | Storage tier of Sentinel |
| **Microsoft Defender for Cloud** | Cloud resources in Azure, AWS, GCP and on-premises: posture (**CSPM**) and workload protection (**CWPP**) | CNAPP |
| **Microsoft Entra ID** | The identity service: users, groups, apps, sign-ins | Identity provider |
| Entra ID Protection | Detects risky sign-ins and risky users; feeds Conditional Access | Identity risk |
| **Microsoft Purview** | Data security and compliance: Data Loss Prevention, Insider Risk Management, Audit, eDiscovery | Data / compliance |
| **Microsoft Security Copilot** | Generative-AI assistant: summarises incidents, writes KQL, analyses scripts | AI assistant |

Terms used above: **CSPM** (cloud security posture management) finds *misconfigurations* before an attack — "this storage account is public". **CWPP** (cloud workload protection platform) detects *attacks* on running workloads — servers, containers, storage, databases. **CNAPP** (cloud-native application protection platform) is Microsoft's name for both together. **DLP** (data loss prevention) stops sensitive data leaving. **Insider Risk Management** spots risky behaviour by your own staff. **Audit** records who did what in Microsoft 365. **eDiscovery** finds and holds content for legal cases.

**2. Defender XDR is a layer, not a fifth product.** It is the cross-product layer over Defender for Endpoint, Office 365, Identity and Cloud Apps. It can also pull in signals from Defender for Cloud, Entra ID Protection, Purview DLP and Insider Risk Management. It correlates only the products you have **licensed and turned on**.

**3. Sentinel has moved into the Defender portal.** Sentinel is generally available in the Defender portal, even for customers without Defender XDR or an E5 licence. ==!After 31 March 2027, Sentinel is no longer supported in the Azure portal== — it will be available only in the Defender portal. Since **July 2025**, a brand-new tenant's first Sentinel workspace is automatically onboarded to the Defender portal when the person onboarding is a subscription **Owner** or **User Access Administrator** (and is not using Azure Lighthouse, a cross-tenant delegation feature). Microsoft calls the combined experience **unified security operations (SecOps)**.

**4. How data flows.**

- **Defender portal route (current):** onboard the Sentinel workspace to the Defender portal. Defender data is integrated by default. SIEM and XDR incidents share one queue.
- **Azure portal route (legacy until 31 March 2027):** turn on the **Microsoft Defender XDR data connector** in Sentinel. Incidents then **sync both ways**. Title, severity and tags copy across; status and classification are translated.
- Defender for Cloud and Defender XDR feed Sentinel. Entra ID Protection risk data can go to Sentinel and to a **Log Analytics workspace** (the database Sentinel reads).

**5. Security Copilot sees, it does not sense.** It has a standalone experience and is also embedded inside Defender XDR, Sentinel, Intune and Entra. It reads your data through **plugins**. It never detects anything on its own.

## Where it lives

| Portal | Address | What SC-200 does there |
|---|---|---|
| **Microsoft Defender portal** | `https://security.microsoft.com` | Incidents and alerts, advanced hunting, Defender XDR settings, **Microsoft Sentinel** menus, Copilot |
| **Azure portal** | `https://portal.azure.com` | Defender for Cloud; Sentinel (legacy, until 31 March 2027); the Log Analytics workspace itself |
| **Microsoft Entra admin center** | `https://entra.microsoft.com` | Users, groups, sign-in logs, ID Protection, Conditional Access |
| **Microsoft Purview portal** | `https://purview.microsoft.com` | DLP, Insider Risk Management, Audit, eDiscovery |

Defender for Cloud is also moving into the Defender portal. Some features are there already; more are added over time.

Sentinel menu names change between portals. Three you will meet first:

| Azure portal (Sentinel) | Defender portal |
|---|---|
| Incidents | **Investigation & response > Incidents & alerts > Incidents** |
| Logs | **Investigation & response > Hunting > Advanced hunting** |
| Data connectors | **Microsoft Sentinel > Configuration > Data connectors** |

![Screenshot of the Defender portal left navigation with the Microsoft Sentinel section](https://learn.microsoft.com/en-us/azure/sentinel/media/microsoft-sentinel-defender-portal/navigation-defender-portal.png){The Microsoft Sentinel section inside the Defender portal's left menu}

![Screenshot of a redirect link from the Azure portal to the Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/media/overview/redirect-no-defender.png){What new tenants see in the Azure portal: a link sending them to the Defender portal}

Sentinel's main screens, shown in both portals (Defender first, Azure second):

![Screenshot of the Microsoft Sentinel content hub in the Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/media/overview/content-hub-defender-portal.png){Content hub, Defender portal — packaged connectors, rules and workbooks}

![Screenshot of the Microsoft Sentinel content hub in the Azure portal](https://learn.microsoft.com/en-us/azure/sentinel/media/overview/content-hub-azure-portal.png){Content hub, Azure portal}

![Screenshot of the Microsoft Sentinel data connectors page in the Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/media/overview/data-connector-list-defender.png){Data connectors, Defender portal — how data gets in}

![Screenshot of the data connectors page in Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/media/overview/data-connectors.png){Data connectors, Azure portal}

![Screenshot of the MITRE coverage page in Microsoft Defender](https://learn.microsoft.com/en-us/azure/sentinel/media/overview/mitre-coverage-defender.png){MITRE ATT&CK coverage, Defender portal}

![Screenshot of the MITRE coverage page with both active and simulated indicators selected](https://learn.microsoft.com/en-us/azure/sentinel/media/overview/mitre-coverage.png){MITRE ATT&CK coverage, Azure portal}

![Screenshot of an incident investigation that shows an entity and connected entities in an interactive graph](https://learn.microsoft.com/en-us/azure/sentinel/media/overview/map-timeline.png){Investigating an incident: entities and how they connect}

![Screenshot of example automated workflow in Azure Logic Apps](https://learn.microsoft.com/en-us/azure/sentinel/media/overview/logic-app.png){A playbook — Sentinel's SOAR — is a Logic Apps workflow}

How the pieces connect, as Microsoft draws it:

![Diagram of a Microsoft Sentinel and Microsoft Defender XDR architecture with the SecOps operations platform](https://learn.microsoft.com/en-us/security/zero-trust/media/sentinel-xdr-unified-security-experience.png){Current model: Sentinel and Defender XDR both inside the Defender portal}

![Diagram that shows the integration of Microsoft Sentinel and Microsoft XDR](https://learn.microsoft.com/en-us/security/zero-trust/media/sentinel-xdr.png){Legacy model: Defender XDR sends data to Sentinel through connectors, Sentinel worked in the Azure portal}

![Diagram of the process to evaluate and deploy Microsoft Defender XDR components](https://learn.microsoft.com/en-us/security/zero-trust/media/copilot/defender-xdr-pilot-deploy-flow.svg){Microsoft's suggested order for rolling out the Defender XDR products}

![Diagram of a Microsoft Sentinel and Microsoft Defender XDR architecture in the unified security operations experience](https://learn.microsoft.com/en-us/azure/sentinel/media/microsoft-365-defender-sentinel-integration/sentinel-xdr-usx.svg){The same integration from the Sentinel documentation, Defender portal version}

![Diagram of the integration of Microsoft Sentinel and Microsoft Defender XDR](https://learn.microsoft.com/en-us/azure/sentinel/media/microsoft-365-defender-sentinel-integration/sentinel-xdr.svg){Azure portal version}

The other products:

![Screenshot of the KQL query editor in the Microsoft Sentinel data lake](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/sentinel-lake-overview/data-lake-exploration.png){Sentinel data lake: querying long-term data with KQL}

![Screenshot of a Jupyter notebook showing data analysis and visualization](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/sentinel-lake-overview/notebook.png){Sentinel data lake: Python notebooks over the same data}

![Diagram showing the core functionality of Defender for Cloud](https://learn.microsoft.com/en-us/azure/defender-for-cloud/media/defender-for-cloud-introduction/cloud-security-pillars.png){Defender for Cloud: posture (CSPM), DevSecOps and workload protection (CWPP)}

![Conceptual image of CNAPP and how the Defender for Cloud plans protect all of your resources](https://learn.microsoft.com/en-us/azure/defender-for-cloud/media/defender-for-cloud-introduction/defender-plans.png){Defender for Cloud plans — one per workload type (Servers, Storage, Databases, Containers...)}

![Diagram showing how ID Protection works at a high level](https://learn.microsoft.com/en-us/entra/id-protection/media/overview-identity-protection/identity-protection-overview.png){Entra ID Protection: detect risk, investigate, remediate, export to a SIEM}

![Solution areas in Microsoft Purview](https://learn.microsoft.com/en-us/purview/media/purview-areas.png){Purview's solution areas — SC-200 touches only DLP, Insider Risk, Audit and eDiscovery}

![Image of how Security Copilot works](https://learn.microsoft.com/en-us/copilot/security/media/security-copilot-diagram.png){Security Copilot: your prompt, grounded with plugin data, answered by a language model}

## What the exam assumes you know

- ==!Defender for Identity is not Entra ID Protection.== Defender for Identity watches **on-premises Active Directory**. ==+Entra ID Protection watches cloud sign-ins in Entra ID.==
- ==!Defender for Cloud is not Defender for Cloud Apps.== Defender for Cloud protects **your Azure/AWS/GCP resources**. Defender for Cloud Apps protects **SaaS apps** your users sign in to.
- ==!Defender XDR alone cannot read a third-party firewall.== That needs Sentinel.
- ==!"Sentinel lives in the Azure portal" is outdated.== Expect Defender portal paths. The Azure portal still works until 31 March 2027.
- Entra ID Protection needs **Microsoft Entra ID P2**.
- Purview is a separate portal. A DLP or insider-risk alert *shows up* in the Defender incident queue, but you configure the policy in Purview.

## Skip list

- **Skip** Defender Vulnerability Management, Security Exposure Management, App Governance and Defender for IoT. They appear in the Defender XDR family list but are not named in the SC-200 objectives this page supports.
- **Skip** the Defender for Cloud plan-by-plan feature table (Defender for Key Vault, APIs, DNS bundling, AI threat protection). The Defender for Cloud lessons cover the plans SC-200 tests.
- **Skip** Purview's data governance side (Data Map, Unified Catalog) and Compliance Manager. Not SC-200.
- **Skip** the Entra product family beyond Entra ID and ID Protection (Verified ID, Private Access, Internet Access, Agent ID). Not SC-200.
- **Skip** the Security Copilot use-case list for CISOs and IT admins and the grounding internals. Know: AI assistant, standalone plus embedded, reads data through plugins.
- **Skip** the Sentinel-in-Defender feature-comparison tables row by row. Know the retirement date, the auto-onboarding rule, and the three menu moves above.
