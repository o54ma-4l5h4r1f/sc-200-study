+++
slug = "sentinel-data-lake-basics"
title = "Microsoft Sentinel data lake basics"
summary = "What the Microsoft Sentinel data lake is (a cheap, tenant-wide long-term store next to the Analytics tier), who can switch it on and what onboarding changes, how Data lake exploration works in the Defender portal, how it is billed at a concept level, and how Sentinel graph, lake notebooks and the Sentinel MCP Server sit on top of it."
order = 23
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-overview",
  "https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-onboarding",
  "https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-onboard-defender",
  "https://learn.microsoft.com/en-us/azure/sentinel/datalake/kql-overview",
  "https://learn.microsoft.com/en-us/azure/sentinel/datalake/kql-queries",
  "https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-graph-overview",
  "https://learn.microsoft.com/en-us/azure/sentinel/datalake/notebooks-overview",
  "https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-mcp-overview",
  "https://learn.microsoft.com/en-us/azure/sentinel/roles",
  "https://learn.microsoft.com/en-us/azure/sentinel/billing",
]
captured = 2026-11-12
related_objectives = ["D1.2.2", "D3.1.5", "D3.1.6", "D3.2.2", "D3.2.3", "D3.2.4"]
+++

## In one sentence

The **Microsoft Sentinel data lake** is a cheap, long-term store for security data that sits **next to** the expensive, fast **Analytics tier** — one per tenant, holding data for up to **12 years**, queried with KQL and notebooks from the **Defender portal**, and switched on once by an admin.

## Why it exists

Sentinel stores data in a **Log Analytics workspace**. Keeping data there (the Analytics tier) is fast but costly. Firewall, DNS and proxy logs arrive in terabytes. Keeping a year of them at top price is unrealistic. Deleting them hurts forensics and compliance.

Think of an office. The **desk drawers** (Analytics tier) hold what you touch every day: detection rules and hunting read them constantly. The **basement archive** (data lake tier) holds years of boxes for a fraction of the price. Searching it is slower, and you pay per search. Every desk-drawer file is **also** copied to the basement automatically.

For a SOC analyst it matters three ways. You **query old data** that has left the Analytics tier. You **park noisy logs** cheaply. And **KQL jobs**, **lake notebooks**, **Sentinel graph**, **blast radius**, the **hunting graph** and the **Sentinel MCP Server** only work once the lake exists.

## Mental model

```svg
<svg viewBox="0 0 900 470" role="img" aria-label="Sentinel data lake mental model: Sentinel workspaces connected to the Defender portal in the primary workspace region write to the Analytics tier, which is mirrored to the data lake tier at no extra charge; lake-only tables and system asset tables also land in the lake; KQL queries, KQL jobs, notebooks, Sentinel graph and the MCP Server read the lake; jobs can promote results back to the Analytics tier">
  <defs>
    <marker id="sdlbarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <rect class="box" x="15" y="30" width="200" height="70" rx="8"/>
  <text x="115" y="60" text-anchor="middle">Data connectors</text>
  <text x="115" y="82" text-anchor="middle" class="muted">Defender, Entra, firewalls…</text>
  <rect class="box" x="15" y="300" width="200" height="70" rx="8"/>
  <text x="115" y="328" text-anchor="middle">Asset data (auto)</text>
  <text x="115" y="350" text-anchor="middle" class="muted">Entra, M365, Azure Resource Graph</text>
  <rect class="box-accent" x="270" y="20" width="300" height="110" rx="10"/>
  <text x="420" y="48" text-anchor="middle" class="label-accent">Analytics tier ("desk drawer")</text>
  <text x="420" y="74" text-anchor="middle">rules, advanced hunting, workbooks</text>
  <text x="420" y="98" text-anchor="middle" class="muted">fast · expensive · up to 2 years hot</text>
  <text x="420" y="118" text-anchor="middle" class="muted">in your Sentinel workspaces</text>
  <line x1="215" y1="65" x2="266" y2="65" class="line-accent" marker-end="url(#sdlbarrow)"/>
  <line x1="420" y1="130" x2="420" y2="196" class="line-accent" marker-end="url(#sdlbarrow)"/>
  <text x="430" y="168" class="muted">mirrored, no extra charge</text>
  <line class="divider" x1="250" y1="182" x2="590" y2="182"/>
  <rect class="box-ok" x="270" y="200" width="300" height="190" rx="10"/>
  <text x="420" y="228" text-anchor="middle" class="label-accent">Data lake tier ("basement")</text>
  <text x="420" y="254" text-anchor="middle">one lake per tenant, up to 12 years</text>
  <text x="420" y="278" text-anchor="middle" class="muted">mirrored Analytics data</text>
  <text x="420" y="300" text-anchor="middle" class="muted">+ lake-only tables (cheap ingest)</text>
  <text x="420" y="322" text-anchor="middle" class="muted">+ System tables (assets, federated)</text>
  <text x="420" y="350" text-anchor="middle" class="muted">open Parquet files</text>
  <text x="420" y="372" text-anchor="middle" class="muted">storage and compute separated</text>
  <line x1="215" y1="335" x2="266" y2="320" class="line-accent" marker-end="url(#sdlbarrow)"/>
  <path d="M215,90 C240,200 240,260 266,280" class="line" fill="none" marker-end="url(#sdlbarrow)"/>
  <text x="140" y="200" text-anchor="middle" class="muted">or lake only</text>
  <rect class="box" x="640" y="20" width="245" height="56" rx="8"/>
  <text x="762" y="44" text-anchor="middle">KQL queries</text>
  <text x="762" y="64" text-anchor="middle" class="muted">ad hoc, interactive / async</text>
  <rect class="box" x="640" y="88" width="245" height="56" rx="8"/>
  <text x="762" y="112" text-anchor="middle">KQL jobs</text>
  <text x="762" y="132" text-anchor="middle" class="muted">one-time or scheduled (D3.2.2)</text>
  <rect class="box" x="640" y="156" width="245" height="56" rx="8"/>
  <text x="762" y="180" text-anchor="middle">Notebooks (VS Code, Spark)</text>
  <text x="762" y="200" text-anchor="middle" class="muted">Python analysis (D3.2.4)</text>
  <rect class="box" x="640" y="224" width="245" height="56" rx="8"/>
  <text x="762" y="248" text-anchor="middle">Sentinel graph</text>
  <text x="762" y="268" text-anchor="middle" class="muted">blast radius, hunting graph</text>
  <rect class="box" x="640" y="292" width="245" height="56" rx="8"/>
  <text x="762" y="316" text-anchor="middle">Sentinel MCP Server</text>
  <text x="762" y="336" text-anchor="middle" class="muted">AI agents query the lake</text>
  <line x1="570" y1="290" x2="636" y2="48" class="line" marker-end="url(#sdlbarrow)"/>
  <line x1="570" y1="295" x2="636" y2="116" class="line" marker-end="url(#sdlbarrow)"/>
  <line x1="570" y1="300" x2="636" y2="184" class="line" marker-end="url(#sdlbarrow)"/>
  <line x1="570" y1="305" x2="636" y2="252" class="line" marker-end="url(#sdlbarrow)"/>
  <line x1="570" y1="310" x2="636" y2="320" class="line" marker-end="url(#sdlbarrow)"/>
  <path d="M640,116 C600,60 600,60 574,70" class="line-accent" fill="none" marker-end="url(#sdlbarrow)"/>
  <text x="610" y="150" text-anchor="middle" class="label-accent">promote</text>
  <text x="450" y="440" text-anchor="middle" class="muted">Everything on the right is in the Defender portal or VS Code — there is no data lake page in the Azure portal.</text>
</svg>
```

Data lands in the Analytics tier and is **copied** to the lake, or goes to the lake **only**. Tools on the right read the lake. A **job** can **promote** results back up, where detection rules can use them.

## What actually matters

**1. Two tiers, one copy.** The **Analytics tier** is the Sentinel you already know: alerting, advanced hunting, incident management. The **data lake tier** is cheap long-term storage for querying and Python analytics, for up to **12 years**. After onboarding, Analytics-tier data is **mirrored** to the lake ==+without extra charge== from that point forward. Storage is open-format **Parquet**, separate from compute. Tier choice and retention numbers are exam depth for **D1.2.2**.

**2. It is tenant-wide and lives in the Defender portal.** You get exactly **one data lake per tenant**. It is built in the **same region as your primary Sentinel workspace**. Every workspace that is **connected to the Defender portal** and sits in **that same region** is attached automatically. ==!You cannot pick which workspaces join==, and you cannot remove one yourself — that needs a Microsoft support request. Workspaces created **after** onboarding are not added automatically; open a support ticket.

**3. Onboarding prerequisites and who can do it.**

| You need | Detail |
|---|---|
| Defender + Sentinel set up | A Sentinel **primary** workspace connected to the Defender portal (`security.microsoft.com`). ==@A Defender XDR licence is not required.== |
| Billing home | An Azure **subscription** and **resource group**. The lake is billed there and ==!can't be moved== to another subscription or resource group later. |
| Azure role | Subscription **Owner** (direct, not inherited from a management group). The roles list also accepts **Subscription Contributor** — see the note below. |
| Entra role | **Global Administrator** or **Security Administrator**, to authorise ingestion from Entra, Microsoft 365 and Azure. |
| Workspace access | **Read** access to every workspace that will be attached. |

**The two Microsoft sentences disagree.** The prerequisites list says you "must be the direct subscription owner". The *Required roles* list in the same article says "Azure Subscription owner or Subscription contributor for billing setup". The troubleshooting section adds a third combination: Security Administrator plus Subscription Owner, or User Access Administrator plus Microsoft Sentinel Contributor. ==+Safe exam answer: direct Subscription Owner plus Security Administrator (or Global Administrator).==

==!Customer-managed keys (CMK) are not supported in the lake==; CMK workspaces aren't reachable from lake experiences. Microsoft 365 data in another region is copied into the lake's region.

**4. What onboarding changes.** Setup takes **up to 60 minutes**. Data in newly enabled or moved tables takes **90–120 minutes** to appear.

| Change | What it means for you |
|---|---|
| **Asset data** arrives automatically | Entra, Microsoft 365 and Azure Resource Graph inventories land in **System tables** |
| **Auxiliary log tables** join the lake | ==!They disappear from Advanced hunting==; query them in Data lake exploration |
| Billing meters switch | Search jobs, Auxiliary logs and long-term retention ("archive") move to **data lake meters** — costs can rise |
| Managed identity `msg-resources-{GUID}` created | Has **Reader** on onboarded subscriptions. ==!Don't delete it.== Give it **Log Analytics Contributor** so jobs can create Analytics-tier tables (D3.2.2) |
| Off switch | None in the portal — turning the lake off needs a Microsoft Defender **support request** |

An **Azure Policy** can block setup (error **DL103**). Fix: a policy exemption for `Microsoft.SentinelPlatformServices/sentinelplatformservices`.

**5. Data lake exploration (the analyst's view).** Under **Microsoft Sentinel > Data lake exploration** in the Defender portal you get:

- **KQL queries** — a query editor for lake data and **federated tables** (outside data you query in place). Pick the **Selected workspaces** (same-name tables are combined with `union()`; `workspace("Name").Table` targets one). Choose **System tables** for federated and asset tables. Time range up to **12 years**. **Query history** keeps **30 days**.
- **Async queries** for long runs. Results stay cached for **24 hours**.
- **Jobs** — one-time or scheduled KQL queries that write results to a table, often **promoting** lake data into the Analytics tier (D3.2.2). The same page lists notebook and graph jobs.
- Search jobs and restore are **not** under Data lake exploration in current docs — they live at **Microsoft Sentinel > Search** (the training unit still shows an older *Search & restore* entry). Covered on D1.2.2.

Limits are **per tenant**: **30 queries per minute** and **10 concurrent** (interactive and async combined). A query returns at most **500,000 rows or 64 MB**. ==!Requests over the rate or concurrency limit are rejected, not queued.== Lake queries are ==!slower than the Analytics tier==, and new data takes about **15 minutes** to become queryable. Not supported: `adx()`, `arg()`, `externaldata()`, `ingestion_time()`, `estimate_data_size()`, functions, and legacy tables such as `AzureDiagnostics`.

**Timeout: two numbers on one page.** The notes in *Run KQL queries on the data lake* say queries "time out after **8 minutes**". The limits table at the bottom of the same article says **Query timeout: 4 minutes**. After **2 minutes** the editor offers async, which times out after **1 hour**. Remember: minutes, not hours — go async for long runs.

**6. Who can read and write.** Lake permissions mix **Microsoft Entra roles** (whole lake) and **Azure RBAC roles** (one workspace).

| Action | Roles |
|---|---|
| Read all workspaces in the lake | Entra **Global Reader**, **Security Reader**, **Security Operator**, **Security Administrator**, **Global Administrator** |
| Read one workspace | Azure **Log Analytics Reader**, **Microsoft Sentinel Reader**, **Reader** (or the Contributor/Owner equivalents) on it |
| Write via jobs or notebooks; create or manage scheduled jobs | Entra **Security Operator**, **Security Administrator**, **Global Administrator** |

**7. Billing, as a concept.** No prices here — they move. After onboarding, lake usage is billed on five meters:

| Meter | Charged for |
|---|---|
| **Data lake ingestion** | GB into **lake-only** tables. Not charged when a table keeps both tiers. |
| **Data processing** | GB processed for lake-only tables (transformations such as filtering or redaction). |
| **Data lake storage** | GB per month kept in the lake **after** Analytics retention ends. Billed on a fixed **6:1** compression: 600 GB raw = 100 GB billed. |
| **Data lake query** | GB of **uncompressed** data scanned by KQL queries or KQL jobs. |
| **Advanced data insights** | Compute hours for notebook sessions, notebook jobs and custom-graph building (pools of 12, 32 or 80 vCores). |

The cost pattern is the opposite of Analytics: ==@storing is cheap; every query costs.== Filter tightly. Lake spend shows in Sentinel **cost management** in the Defender portal.

**8. What sits on top of the lake.**

| Built on the lake | What it is | Cost note |
|---|---|---|
| **Sentinel graph** | Assets, identities and activity as **nodes and edges**. Powers **blast radius** in the incident graph and the **hunting graph** (D3.1.5, D3.1.6), auto-provisioned once the lake is on | ==+Embedded graphs carry no charge==; **custom graphs** (preview) use a graph meter |
| **Jupyter notebooks** | Python with Apache Spark over lake tables, from the **Microsoft Sentinel extension for VS Code** (D3.2.4) | Advanced data insights meter |
| **Sentinel MCP Server** | Microsoft-hosted endpoint that lets AI assistants (for example the VS Code chat agent) find tables and run KQL on the lake (D3.2.4) | ==!Server free==; its queries hit the Data lake query meter |
| **Workbooks** | Lake as a data source for long-range dashboards | Query meter |
| **Audit log** | Records lake queries, notebook runs and job changes; on by default | — |

## Where it lives

| Task | Where |
|---|---|
| Onboard (one time) | Defender portal > **System > Settings > Microsoft Sentinel > Data lake** > **Start setup** > pick **Subscription** and **Resource group** > **Set up data lake** |
| Check the primary workspace | Defender portal > **SIEM workspaces** > workspace shows **Connected** and **Primary** |
| Query the lake | Defender portal > **Microsoft Sentinel > Data lake exploration > KQL queries** |
| Jobs | **Microsoft Sentinel > Data lake exploration > Jobs** |
| Tier and retention per table | **Microsoft Sentinel > Configuration > Tables** (D1.2.2) |
| Lake costs | Sentinel **cost management** in the Defender portal (enabled by onboarding) |
| Graphs | **Microsoft Sentinel > Graphs**, the incident graph (**View blast radius**) and advanced hunting |
| Notebooks, MCP | VS Code: **Microsoft Sentinel** extension; `MCP: Add Server` |

```kql
// Data lake exploration > KQL queries: an old-data question the Analytics tier can't answer any more
SigninLogs
| where TimeGenerated between (ago(400d) .. ago(180d))
| where ResultType != "0"
| summarize Failures = count() by UserPrincipalName
| top 20 by Failures
```

### Overview

![Screenshot of the KQL query editor in the Microsoft Sentinel data lake](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/sentinel-lake-overview/data-lake-exploration.png){Data lake exploration: the KQL query editor in the Defender portal}

![Screenshot of a Jupyter notebook showing data analysis and visualization](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/sentinel-lake-overview/notebook.png){A lake notebook in VS Code — Python over the same single copy of data (D3.2.4)}

### Onboarding in the Defender portal

![A screenshot showing the Microsoft Sentinel data lake setup page](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/sentinel-lake-onboard-defender/setup-settings.png){System > Settings > Microsoft Sentinel > Data lake > Start setup}

![A screenshot showing the permissions required page in the Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/sentinel-lake-onboard-defender/permissions-required.png){Without the required roles you get this panel — ask an admin to finish onboarding}

![A screenshot showing the setup page for the Microsoft Sentinel data lake](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/sentinel-lake-onboard-defender/set-up-data-lake.png){Pick the billing subscription and resource group — it can't be moved afterwards}

![A screenshot showing the progress of the onboarding process](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/sentinel-lake-onboard-defender/setup-started.png){Setup runs for up to 60 minutes; you can close the panel}

![A screenshot showing the data lake setup completion page](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/sentinel-lake-onboard-defender/setup-complete-settings.png){Setup complete — the page now shows the configured subscription and resource group}

### Data lake exploration: KQL queries

![Screenshot of the KQL queries page in the Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/kql-queries/query-editor.png){Query tabs, Query history (30 days) and the editor}

![A screenshot showing the workspaces selection panel](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/kql-queries/select-a-workspace.png){Selected workspaces — choose System tables for federated and asset tables}

![A screenshot showing the time range selector](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/kql-queries/time-range-selector.png){Custom time range — up to 12 years}

![A screenshot showing the schema browser panel in the KQL editor](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/kql-queries/schema-browser.png){Schema browser: System tables under Assets; _CL, _KQL_CL, _SPARK and _SPARK_CL tables under Custom logs}

![A screenshot showing the results window in a KQL query editor](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/kql-queries/results-window.png){Results: Export to CSV, Show empty columns, Customize columns}

![Screenshot of the Sample queries tab in the KQL query editor](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/kql-queries/out-of-the-box-queries.png){The Queries tab: out-of-the-box samples}

![A screenshot showing the Async Queries tab in the KQL query editor](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/kql-queries/run-async-query.png){Run async query — results cached for 24 hours}

![A screenshot showing the prompt to change a long-running query to an async query](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/kql-queries/change-to-async-query.png){After 2 minutes the editor offers to switch to async}

![A screenshot showing the results of an async query in the KQL query editor](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/kql-queries/fetch-async-query-results.png){Fetch results for a finished async query}

### Sentinel graph

![Diagram showing graph enabled defense capabilities pre-breach and post breach](https://learn.microsoft.com/en-us/azure/sentinel/datalake/media/sentinel-graph-overview/graph-based-capabilities.png){Sentinel graph across pre-breach (attack paths) and post-breach (blast radius, hunting graph, Purview data risk graphs)}

### Billing article

Both images come from the billing article; neither shows a lake meter.

![Screenshot showing the Microsoft Sentinel section of a sample Azure bill](https://learn.microsoft.com/en-us/azure/sentinel/media/billing/sample-bill-classic.png){A sample Azure invoice for classic Sentinel pricing tiers — example figures only, not lake meters}

![Screenshot of the connector page for Defender for Cloud Apps, with the free security alerts selected](https://learn.microsoft.com/en-us/azure/sentinel/media/billing/data-types.png){Free versus paid data types on a connector — an Analytics-tier billing point, not a lake one}

## What the exam assumes you know

- The lake is a ==@tenant-wide== store, not one per workspace. Only **Defender-connected** workspaces in the **primary workspace's region** join it.
- Analytics-tier data is **mirrored** to the lake. "Lake only" is the cheap option for noisy, low-value logs.
- ==!Lake-only tables don't feed analytics rules or advanced hunting.== Promote with a **KQL job** if a detection needs them.
- Lake features (Data lake exploration, jobs, blast radius, hunting graph, MCP data tools) ==!require onboarding first==.
- Who onboards: **Subscription Owner** (billing) plus **Security Administrator** or **Global Administrator** (ingestion).
- Lake cost model: cheap to keep, **pay per GB scanned** to query.

## Skip list

- **Skip:** the Purview onboarding path and its data risk graph. It is Purview Insider Risk Management, not SC-200 SOC work, and the data risk graph is being retired in late 2026.
- **Skip:** the DL102 error and the regional-capacity workaround. Know DL103 (Azure Policy blocks setup) as the one onboarding error worth remembering.
- **Skip:** querying the lake from Azure Data Explorer with `external_table()`. It is an engineering side door; the exam uses the Defender portal.
- **Skip:** `.show` control commands and per-query limit overrides. Trivia.
- **Skip:** the graph-meter maths. Embedded graphs are free; custom graphs are billed.
- **Skip:** the Sentinel classic pricing tiers in the billing article. Pricing detail is reference material, not exam content.
- **Skip:** row-level scoping RBAC (preview). Know the Entra-role versus workspace-RBAC split above.
- **Skip here, learn on the objective page:** tier and retention numbers (D1.2.2), job wizard and limits (D3.2.2), summary rules (D3.2.3), notebook pools and the MCP tool list (D3.2.4), blast radius and the hunting graph (D3.1.5, D3.1.6).
