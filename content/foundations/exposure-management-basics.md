+++
slug = "exposure-management-basics"
title = "Microsoft Security Exposure Management basics"
summary = "What Microsoft Security Exposure Management is (the Defender portal's map of what an attacker could reach before anything happens), how critical assets are classified, how the enterprise exposure graph turns assets into nodes and edges, what attack paths, choke points and blast radius mean, how initiatives and scores work at a high level, the ExposureGraphNodes and ExposureGraphEdges hunting tables, and what licences and Defender workloads it needs."
order = 24
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/security-exposure-management/microsoft-security-exposure-management",
  "https://learn.microsoft.com/en-us/security-exposure-management/get-started-exposure-management",
  "https://learn.microsoft.com/en-us/security-exposure-management/prerequisites",
  "https://learn.microsoft.com/en-us/security-exposure-management/integration-licensing",
  "https://learn.microsoft.com/en-us/security-exposure-management/critical-asset-management",
  "https://learn.microsoft.com/en-us/security-exposure-management/classify-critical-assets",
  "https://learn.microsoft.com/en-us/security-exposure-management/predefined-classification-rules-and-levels",
  "https://learn.microsoft.com/en-us/security-exposure-management/cross-workload-attack-surfaces",
  "https://learn.microsoft.com/en-us/security-exposure-management/enterprise-exposure-map",
  "https://learn.microsoft.com/en-us/security-exposure-management/work-attack-paths-overview",
  "https://learn.microsoft.com/en-us/security-exposure-management/exposure-insights-overview",
  "https://learn.microsoft.com/en-us/security-exposure-management/initiatives",
  "https://learn.microsoft.com/en-us/defender-vulnerability-management/tvm-exposure-score",
  "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-exposuregraphnodes-table",
  "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-exposuregraphedges-table",
  "https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-graph-overview",
]
captured = 2026-11-12
related_objectives = ["D2.1.9", "D3.1.1", "D3.1.5"]
+++

## In one sentence

**Microsoft Security Exposure Management** is the part of the Defender portal that keeps a live **map of your assets and how they connect**, marks the **critical** ones, and shows the **paths an attacker could take** to reach them — *before* any attack happens.

## Why it exists

A SOC (security operations centre) normally works **after** something happens: an alert fires, an incident opens, you investigate. That is **post-breach** work. Exposure Management is **pre-breach**. It asks "if someone got in here, where could they go next?"

Think of a building's **fire-safety plan**. Drawn before any fire, it marks the rooms that matter most, every door between rooms, and the corridors many routes squeeze through. Exposure Management is that plan for your IT estate. The **rooms** are assets: laptops, servers, user accounts, cloud VMs, key vaults. The **doors** are relationships: "this user can sign in to that server", "this VM has permissions on that storage account".

For a SOC analyst this pays off **during** an incident too. When a laptop is compromised, the first question is "how bad could this get?". Exposure Management's map answers it. Its data powers **blast radius** in the incident graph (D2.1.9, D3.1.5), the **hunting graph** in advanced hunting (D3.1.5), and two hunting tables you query with KQL (D3.1.1).

## Mental model

```svg
<svg viewBox="0 0 900 430" role="img" aria-label="Enterprise exposure graph: nodes are assets and edges are relationships. An internet-exposed VM can authenticate as a service identity, which has permissions to a key vault and a storage account; a user account is a member of an admin group that can sign in to a domain controller. The admin group is a choke point that several paths pass through. Critical assets carry a crown. Blast radius starts at a compromised node and shows where it could reach.">
  <defs>
    <marker id="emarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <text x="90" y="28" text-anchor="middle" class="muted">ENTRY POINTS</text>
  <text x="450" y="28" text-anchor="middle" class="muted">IN BETWEEN</text>
  <text x="790" y="28" text-anchor="middle" class="muted">TARGETS</text>
  <rect class="box-risk" x="15" y="60" width="150" height="70" rx="8"/>
  <text x="90" y="88" text-anchor="middle" class="label-risk">Cloud VM</text>
  <text x="90" y="110" text-anchor="middle" class="muted">internet-exposed</text>
  <rect class="box-risk" x="15" y="250" width="150" height="70" rx="8"/>
  <text x="90" y="278" text-anchor="middle" class="label-risk">Laptop</text>
  <text x="90" y="300" text-anchor="middle" class="muted">vulnerable (bug)</text>
  <rect class="box" x="260" y="60" width="170" height="70" rx="8"/>
  <text x="345" y="88" text-anchor="middle">Service identity</text>
  <text x="345" y="110" text-anchor="middle" class="muted">node</text>
  <rect class="box" x="260" y="250" width="170" height="70" rx="8"/>
  <text x="345" y="278" text-anchor="middle">User account</text>
  <text x="345" y="300" text-anchor="middle" class="muted">node</text>
  <rect class="box-accent" x="500" y="160" width="170" height="80" rx="8"/>
  <text x="585" y="190" text-anchor="middle" class="label-accent">Admin group</text>
  <text x="585" y="214" text-anchor="middle">CHOKE POINT</text>
  <text x="585" y="232" text-anchor="middle" class="muted">many paths pass here</text>
  <rect class="box-ok" x="720" y="50" width="165" height="70" rx="8"/>
  <text x="802" y="78" text-anchor="middle" class="label-accent">Key vault (crown)</text>
  <text x="802" y="100" text-anchor="middle" class="muted">critical asset</text>
  <rect class="box-ok" x="720" y="165" width="165" height="70" rx="8"/>
  <text x="802" y="193" text-anchor="middle" class="label-accent">Storage (crown)</text>
  <text x="802" y="215" text-anchor="middle" class="muted">sensitive data</text>
  <rect class="box-ok" x="720" y="280" width="165" height="70" rx="8"/>
  <text x="802" y="308" text-anchor="middle" class="label-accent">Domain controller</text>
  <text x="802" y="330" text-anchor="middle" class="muted">"end game" asset</text>
  <line x1="165" y1="95" x2="256" y2="95" class="line-accent" marker-end="url(#emarrow)"/>
  <text x="210" y="84" text-anchor="middle" class="muted">can auth as</text>
  <line x1="165" y1="285" x2="256" y2="285" class="line-accent" marker-end="url(#emarrow)"/>
  <text x="210" y="274" text-anchor="middle" class="muted">has credentials of</text>
  <line x1="430" y1="85" x2="716" y2="85" class="line-accent" marker-end="url(#emarrow)"/>
  <text x="575" y="74" text-anchor="middle" class="muted">has permissions to</text>
  <line x1="430" y1="110" x2="496" y2="175" class="line-accent" marker-end="url(#emarrow)"/>
  <line x1="430" y1="275" x2="496" y2="225" class="line-accent" marker-end="url(#emarrow)"/>
  <text x="455" y="262" text-anchor="middle" class="muted">member of</text>
  <line x1="670" y1="195" x2="716" y2="198" class="line-accent" marker-end="url(#emarrow)"/>
  <line x1="670" y1="225" x2="716" y2="300" class="line-accent" marker-end="url(#emarrow)"/>
  <rect class="divider" x="10" y="240" width="680" height="120" rx="12" fill="none"/>
  <text x="350" y="380" text-anchor="middle" class="label-risk">blast radius of the laptop = everything reachable from it</text>
  <text x="450" y="415" text-anchor="middle" class="muted">One path (entry → … → crown) is an attack path. Rows live in ExposureGraphNodes (boxes) and ExposureGraphEdges (arrows).</text>
</svg>
```

Boxes are **nodes**. Arrows are **edges**, each with a label such as "can authenticate as" or "member of". Follow arrows from a risky entry point to a crowned target and you have an **attack path**. The box many paths squeeze through is a **choke point**. Fix that one and you cut several paths at once.

## What actually matters

**1. Exposure Management is a posture tool, not an alerting tool.** It **discovers assets** continuously across endpoints, identities, cloud (Azure, AWS and GCP through Defender for Cloud) and the external attack surface. It enriches them with security context such as "exposed to the internet" or "vulnerable to remote code execution". Its job is posture, not detection. Alerts and incidents are handled elsewhere in the portal. ==!An attack path is a possibility, not evidence of an attack.== The incident graph shows what *did* happen. Exposure Management shows what *could*.

**2. Critical assets — the crown jewels.** Exposure Management marks business-critical assets with a **crown**, three ways:

| How | Detail |
|---|---|
| **Automatically** | Microsoft's **predefined classifications**: domain controllers, ADCS, ADFS and Entra Connect servers, databases with sensitive data, roles such as Privileged Role Administrator |
| **Custom classification** | Your own rule in a query builder (for example "every device named `SRV-FIN-*`") |
| **Manually** | From the device inventory, or by approving lower-confidence matches under **Pending Approval** |

Asset types are **device, identity, cloud resource** and **AI agent**. There are four **criticality levels**: ==@Very High==, ==@High==, ==@Medium== and ==@Low==. When several rules match one asset, ==+the highest level wins==. Criticality shows up across the portal: device inventory, advanced hunting, attack paths and the map. ==!Paths are only as good as your classification.== An unmarked crown jewel never shows up as a target.

**3. The enterprise exposure graph.** This is the data underneath everything. **Nodes** are assets and entities. **Edges** are relationships between them. It is fed by Defender for Endpoint, Defender for Identity, Defender for Cloud, Defender Vulnerability Management, Microsoft Entra ID, and third-party connectors (ServiceNow CMDB, Tenable, Qualys, Rapid7). The **attack surface map** draws it. The **crown** marks criticality; a **red bug** marks a vulnerable asset; a **plus** expands connections.

**4. Attack paths, choke points and blast radius.**

| Term | Plain meaning |
|---|---|
| ==@Attack path== | A chain of assets and techniques from an **entry point** to a **critical asset**. Generated automatically and recalculated as the estate changes (a sign-in, a group change, a new VM). |
| ==@Choke point== | A node where **many** attack paths converge. The best place to fix first. |
| ==@Blast radius== | Everything that could be affected if **one** asset is compromised. In Exposure Management you open it from a choke point. In an incident you open it from a node in the incident graph (D2.1.9, D3.1.5). |
| **End game asset** | On-premises paths stop at **Domain Admins, Enterprise Admins, Administrators** or **Domain Controllers** — owning one means owning the domain. |

Cloud attack paths focus on **real, externally reachable** weaknesses. That means ==!an empty attack-path page can be normal==. It is not proof that something is broken.

The incident-graph **blast radius** and the advanced-hunting **hunting graph** are built by **Microsoft Sentinel graph** on top of this data. They also need the **Sentinel data lake** (see the data lake primer).

**5. Initiatives and scores — the "how are we doing" layer.** **Exposure insights** turn posture into projects called **security initiatives**: workload initiatives (endpoints, identity, cloud), threat initiatives (for example ransomware), threat-analytics initiatives, **Zero Trust**, **External attack surface management**, and the **Critical Asset Protection** initiative. Each initiative has a **score** (a percentage), a **target score** you can set, **metrics** (groups of related recommendations), **recommendations**, and **events** (alerts that a score dropped). The Overview dashboard shows **domain initiative scores** for Code, Endpoint, Cloud, Identity and SaaS, plus **Resolve Now** (Patch, Mitigate, Fix).

Three scores look alike. Their directions differ:

| Score | Where | Good direction |
|---|---|---|
| **Initiative score** | Exposure insights > Initiatives | ==+Higher is better== (towards your target) |
| **Exposure score** (Defender Vulnerability Management) | Vulnerability management dashboard | ==!Lower is better== — 0–29 low, 30–69 medium, 70–100 high |
| **Microsoft Secure Score** / Secure Score for Devices | Defender portal | Higher is better. Calculated independently of exposure score. |

**6. The two hunting tables.** The graph is queryable in **advanced hunting**:

| Table | One row = | Key columns |
|---|---|---|
| ==@ExposureGraphNodes== | one asset or entity | `NodeId`, `NodeLabel`, `NodeName`, `Categories`, `NodeProperties` (JSON: internet exposure, RCE vulnerability, criticality…), `EntityIds` |
| ==@ExposureGraphEdges== | one relationship | `EdgeId`, `EdgeLabel` (for example "routes traffic to"), `SourceNodeId`/`Name`/`Label`, `TargetNodeId`/`Name`/`Label`, `EdgeProperties` |

Both are marked **preview**. ==!If no Defender service is deployed, queries against them return nothing.== Joining them into paths uses the KQL graph operators `make-graph` and `graph-match`, which D3.1.5 teaches.

```kql
// What kinds of nodes and relationships does my graph hold?
ExposureGraphNodes
| summarize Assets = count() by NodeLabel
| top 15 by Assets
```

```kql
ExposureGraphEdges
| summarize Links = count() by EdgeLabel
| top 15 by Links
```

**7. Licensing and permissions — why your lab is empty.** There is ==@nothing to install==; it is a section of the Defender portal. Licence alone is not enough: the map is built *from* the Defender workloads you actually run. Without Defender for Endpoint, Identity or Cloud feeding it, the graph is thin, attack paths may not appear and the hunting tables are empty.

| Question | Answer |
|---|---|
| Licences for full access | **Microsoft 365 E5/A5**, **E3 + E5 Security add-on**, **EMS E5**, **Defender for Endpoint**, **Defender for Identity**, **Defender for Office 365 Plan 2**, **Defender for Cloud**, **Business Premium** and others |
| Limited licences | ==!Microsoft 365 E3, A3 and Defender for Office 365 Plan 1 get the Secure Score experience only== |
| Clouds | **Public cloud only** — not US Gov, China or other sovereign clouds |
| Unified RBAC | **Exposure Management (read)**, **Exposure Management (manage)**; **Core security settings (manage)** for vendor connections |
| Entra roles | Global Administrator, Security Administrator: read/write · Security Operator: read + limited write · Global Reader, Security Reader: read |
| Device-group scoping | Users limited to some device groups see only those devices in paths, the map and the hunting tables. **Managing critical asset classifications needs all device groups.** |

## Where it lives

All in the **Microsoft Defender portal** (`security.microsoft.com`), under **Exposure management**.

| Task | Path |
|---|---|
| Dashboard | **Exposure management > Overview** |
| Attack paths, choke points | **Exposure management > Attack surface > Attack path** (tabs include **Choke points**, **Recommendations**) |
| Attack surface map | **Attack surface > Map**, or a device > **View Map** |
| Initiatives, metrics, events | **Exposure management > Exposure insights > Initiatives / Events** |
| Critical asset rules | **Settings > Microsoft Defender XDR > Rules > Critical asset management** (see note) |
| Hunting tables | **Advanced hunting** (see the Defender portal tour primer) |

**Critical asset management: three Microsoft paths.** *Critical asset management overview* says **Exposure management > Critical assets**. *Review and classify critical assets* says **Settings > Microsoft XDR > Rules > Critical asset management**. *Prerequisites* says **System > Settings > Microsoft Defender XDR**. They describe the same page as the menus moved. Trust the portal you see, and remember that the rules live under **Settings**.

### Dashboard and prerequisites

![Screenshot of the Exposure Management Overview dashboard showing Resolve Now and Monitor Exposure sections](https://learn.microsoft.com/en-us/security-exposure-management/media/get-started-exposure-management/exposure-management-overview.png){Exposure management > Overview: Resolve Now (Patch, Mitigate, Fix) and Monitor Exposure (internet-exposed resources, domain initiative scores)}

![Screenshot of the Microsoft Defender security portal Help button in the portal header bar](https://learn.microsoft.com/en-us/security-exposure-management/media/microsoft-defender-portal-header.png){The Defender portal header — Exposure Management has no separate portal}

### Critical assets

![Screenshot of a flowchart showing asset criticality](https://learn.microsoft.com/en-us/security-exposure-management/media/classify-critical-assets/asset-criticality.png){Asset criticality combines cyber-role, production context and system}

![Screenshot of criticality levels diagram](https://learn.microsoft.com/en-us/security-exposure-management/media/classify-critical-assets/criticality-levels.png){Four levels: Very High, High, Medium, Low}

![Screenshot of the Critical asset management window](https://learn.microsoft.com/en-us/security-exposure-management/media/classify-critical-assets/critical-asset-management-window.png){Critical asset management: predefined and custom classifications}

![Screenshot of the page where you create critical asset classifications](https://learn.microsoft.com/en-us/security-exposure-management/media/classify-critical-assets/create-critical-asset-classification.png){Custom classification: the query builder}

![Screenshot of the Critical asset management criticality editing feature](https://learn.microsoft.com/en-us/security-exposure-management/media/classify-critical-assets/edit-criticality-levels.png){Changing a classification's criticality level}

![Screenshot of predefined classifications in the asset management interface](https://learn.microsoft.com/en-us/security-exposure-management/media/classify-critical-assets/add-assets.png){Predefined classifications — the Pending Approval column flags assets below the auto-classify threshold}

![Screenshot of the pending approval tab in asset management](https://learn.microsoft.com/en-us/security-exposure-management/media/classify-critical-assets/pending-approval.png){Pending Approval: add lower-confidence matches with the plus button}

![Screenshot of the assets tab in asset management](https://learn.microsoft.com/en-us/security-exposure-management/media/classify-critical-assets/assets-tab.png){Assets tab: remove an asset with the X}

![Screenshot of the Device inventory window showing criticality sorting](https://learn.microsoft.com/en-us/security-exposure-management/media/classify-critical-assets/device-inventory.png){Device inventory sorted by criticality level}

![Screenshot of the Device inventory window with an emphasis on the criticality level section](https://learn.microsoft.com/en-us/security-exposure-management/media/critical-asset-management/device-inventory-criticality-level.png){Criticality level on a device page}

![Screenshot of the critical assets column on the security recommendations page](https://learn.microsoft.com/en-us/security-exposure-management/media/critical-asset-management/security-recommendations-critical-assets.png){Recommendations show how many critical assets each one exposes}

![Screenshot of an asset viewed in the exposure map in the context of other connections](https://learn.microsoft.com/en-us/security-exposure-management/media/critical-asset-management/attack-surface-exposure-map.png){On the map, the crown and halo mark high criticality}

### Attack surface map

![Screenshot of the attack surface exposure map](https://learn.microsoft.com/en-us/security-exposure-management/media/value-data-connectors/attack%20map%20data%20connectors.png){Attack surface map: nodes, edges, indicators and discovery source}

![Screenshot of attack surface map side pane](https://learn.microsoft.com/en-us/security-exposure-management/media/enterprise-exposure-map/attack-surface-exposure-map-sidepane.png){Asset side pane: General, All data, Top Vulnerabilities (up to 100 CVEs), Findings}

### Attack paths, choke points, blast radius

![Screenshot of attack path dashboard](https://learn.microsoft.com/en-us/security-exposure-management/media/work-attack-paths-overview/attack-paths-dashboard.png){Attack path dashboard: paths over time, top choke points, scenarios, targets, entry points}

![Screenshot of attack path list](https://learn.microsoft.com/en-us/security-exposure-management/media/review-attack-paths/attack-path-list.png){Attack surface > Attack path: the list}

![Screenshot of choke point and blast radius](https://learn.microsoft.com/en-us/security-exposure-management/media/review-attack-paths/choke%20points%20and%20blast%20radius.png){Choke points tab > select one > View blast radius}

![Screenshot of choke point on attack map](https://learn.microsoft.com/en-us/security-exposure-management/media/review-attack-paths/choke-points%20on%20map.png){A choke point on the map}

![Screenshot of an Attack path graph detail screen](https://learn.microsoft.com/en-us/security-exposure-management/media/review-attack-paths/attack-path-graph-details.png){One attack path as a graph — hover a node or edge for detail}

![Diagram showing graph enabled defense capabilities pre-breach and post breach](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/sentinel-graph-overview/graph-based-capabilities.png){Sentinel graph: Exposure Management attack paths (pre-breach) and incident blast radius and hunting graph (post-breach) share one graph}

### Initiatives and scores

![Screenshot of the Security Exposure Management Initiatives window](https://learn.microsoft.com/en-us/security-exposure-management/media/initiatives/initiatives-window.png){Exposure insights > Initiatives: 14-day trend, current score, programs}

![Screenshot of device group filter](https://learn.microsoft.com/en-us/security-exposure-management/media/initiatives/filter-by-dg.png){Filter by device groups}

![Screenshot of the filter by device groups side pane](https://learn.microsoft.com/en-us/security-exposure-management/media/initiatives/filter-by-dg-pane.png){Endpoint-based scores recalculate for the groups you pick}

![Screenshot of the ransomware initiative](https://learn.microsoft.com/en-us/security-exposure-management/media/initiatives/initiatives-ransomware.png){One initiative page: score, target, metrics, recommendations}

![Screenshot of the window to set the initiative target](https://learn.microsoft.com/en-us/security-exposure-management/media/initiatives/set-initiative-target-score.png){Set target score}

![Screenshot of history side panel](https://learn.microsoft.com/en-us/security-exposure-management/media/exposure-insights-overview/initiatives-history-details-redcued.jpg){History: why the score changed, and up to 100 changed assets}

![Screenshot of the initiative's security recommendation tab](https://learn.microsoft.com/en-us/security-exposure-management/media/initiatives/initiatives-security-recommendations.png){Initiative recommendations — Manage opens the owning product}

![Exposure score card in the Exposure management experience](https://learn.microsoft.com/en-us/defender/media/defender-vulnerability-management/endpoint-exposure-score.png){Endpoint exposure score card (Exposure management > Vulnerability management) — lower is better}

![Exposure score card on the Vulnerability management dashboard](https://learn.microsoft.com/en-us/defender/media/defender-vulnerability-management/exposure-score.png){The same score on the older Vulnerability management dashboard}

## What the exam assumes you know

- Exposure Management is ==@pre-breach== posture. Incidents and alerts are post-breach. ==!An attack path is not an incident.==
- **Nodes = assets, edges = relationships.** The tables are `ExposureGraphNodes` and `ExposureGraphEdges`, in **advanced hunting** (not in a Sentinel workspace).
- **Critical assets** drive everything. Four levels, highest matching rule wins, crown icon.
- **Choke point** = where paths converge, fix first. **Blast radius** = what one compromised asset could reach.
- Blast radius in an incident needs the **Sentinel data lake** plus **Exposure Management (read)** (D2.1.9).
- No Defender workloads → empty graph. E3 alone → Secure Score only.

## Skip list

- **Skip:** the long predefined-classification catalogue (every server role, Kubernetes rule and SaaS app with its default level). Know a few examples and the four levels.
- **Skip:** external data connectors (ServiceNow, Tenable, Qualys, Rapid7) setup and their future pricing. Know they exist and feed the graph.
- **Skip:** posture policies, exemptions and the MDC Baseline Policy. That is cloud-posture admin work (Defender for Cloud territory), not SOC analysis.
- **Skip:** External Attack Surface Management (EASM) initiative setup. Know it is one initiative type.
- **Skip:** metric weights, score-calculation formulas and the exposure-score model transition. Know only which way each score should move.
- **Skip:** Defender Vulnerability Management workflows (remediation tickets, exceptions, software inventory). Vulnerability management is its own product area.
- **Skip:** the NIST criticality references in the classification article. Background reading, never tested.
- **Skip here, learn on the objective page:** `make-graph`/`graph-match` queries and the hunting-graph scenarios (D3.1.5), blast radius in the incident graph and hop limits (D2.1.9), picking the right hunting table (D3.1.1).
