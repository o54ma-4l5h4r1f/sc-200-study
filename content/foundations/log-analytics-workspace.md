+++
slug = "log-analytics-workspace"
title = "Log Analytics workspace"
summary = "What a Log Analytics workspace is (a regional database of log tables), how Microsoft Sentinel is enabled on top of one, and the basics of access control modes, table plans, retention, the daily cap, cost and one-versus-many workspace design."
order = 10
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-workspace-overview",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/data-platform-logs",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/manage-access",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/data-retention-configure",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/daily-cap",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/workspace-design",
  "https://learn.microsoft.com/en-us/azure/sentinel/quickstart-onboard",
]
captured = 2026-11-12
related_objectives = ["D1.2.2"]
+++

## In one sentence

A **Log Analytics workspace** is a database in one Azure region that stores log data in **tables**, and **Microsoft Sentinel is switched on *on top of* a workspace** — the "Sentinel workspace" is just a Log Analytics workspace with Sentinel enabled.

## Why it exists

Every security tool needs somewhere to keep the evidence. Firewalls, laptops, servers, Azure itself and Microsoft 365 all produce **logs** — timestamped records of what happened. Spread across a hundred places, logs are useless. Put in one searchable store, they become evidence.

Think of a **filing room**. The room is the workspace. Each **filing cabinet** is a table: one for Windows security events, one for sign-ins, one for firewall logs. Every drawer in a cabinet holds the same kind of form, with the same boxes to fill in. That form layout is the table's **schema** — its list of columns and their types. Some cabinets are cheap basement storage, some are the expensive desk-side kind you open all day. Those are **table plans**.

A workspace is an **Azure resource**. It sits in a **resource group** inside a **subscription**, and it lives in one **region** (for example, West Europe). Creating it costs nothing. You pay for the data you put in and for how long you keep it.

## Mental model

```svg
<svg viewBox="0 0 780 360" role="img" aria-label="A Log Analytics workspace in one region holds tables, each table has a plan and retention; Microsoft Sentinel is enabled on the workspace and reads its tables">
  <defs>
    <marker id="law-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <rect class="box" x="15" y="20" width="170" height="44" rx="6"/>
  <text x="100" y="47" text-anchor="middle">Azure resources</text>
  <rect class="box" x="15" y="78" width="170" height="44" rx="6"/>
  <text x="100" y="105" text-anchor="middle">Servers (via agent)</text>
  <rect class="box" x="15" y="136" width="170" height="44" rx="6"/>
  <text x="100" y="163" text-anchor="middle">Microsoft 365 / Entra</text>
  <rect class="box" x="15" y="194" width="170" height="44" rx="6"/>
  <text x="100" y="221" text-anchor="middle">Firewalls, other vendors</text>
  <line x1="185" y1="42" x2="228" y2="120" class="line-accent" marker-end="url(#law-arrow)"/>
  <line x1="185" y1="100" x2="228" y2="130" class="line-accent" marker-end="url(#law-arrow)"/>
  <line x1="185" y1="158" x2="228" y2="140" class="line-accent" marker-end="url(#law-arrow)"/>
  <line x1="185" y1="216" x2="228" y2="150" class="line-accent" marker-end="url(#law-arrow)"/>
  <rect class="box-accent" x="230" y="15" width="330" height="330" rx="12"/>
  <text x="395" y="40" text-anchor="middle" class="label-accent">Log Analytics workspace</text>
  <text x="395" y="60" text-anchor="middle" class="muted">one region · one resource group</text>
  <rect class="box" x="250" y="78" width="290" height="46" rx="6"/>
  <text x="395" y="98" text-anchor="middle">SecurityEvent</text>
  <text x="395" y="117" text-anchor="middle" class="muted">Analytics plan</text>
  <rect class="box" x="250" y="132" width="290" height="46" rx="6"/>
  <text x="395" y="152" text-anchor="middle">SigninLogs</text>
  <text x="395" y="171" text-anchor="middle" class="muted">Analytics plan</text>
  <rect class="box" x="250" y="186" width="290" height="46" rx="6"/>
  <text x="395" y="206" text-anchor="middle">Verbose firewall logs</text>
  <text x="395" y="225" text-anchor="middle" class="muted">Basic or Auxiliary plan · cheaper</text>
  <text x="395" y="262" text-anchor="middle">each table = rows and typed columns</text>
  <text x="395" y="284" text-anchor="middle">each table has its own plan + retention</text>
  <text x="395" y="314" text-anchor="middle" class="muted">daily cap and access mode set per workspace</text>
  <line x1="560" y1="180" x2="598" y2="180" class="line-accent" marker-end="url(#law-arrow)"/>
  <rect class="box-ok" x="600" y="120" width="165" height="120" rx="10"/>
  <text x="682" y="150" text-anchor="middle" class="label-accent">Microsoft Sentinel</text>
  <text x="682" y="174" text-anchor="middle">enabled ON the</text>
  <text x="682" y="194" text-anchor="middle">workspace</text>
  <text x="682" y="222" text-anchor="middle" class="muted">reads its tables</text>
</svg>
```

Data is not a single "log file". It lands as **rows in a table**. Every row has a `TimeGenerated` column (when the event happened). The KQL basics page shows how to query those rows.

## What actually matters

- **Sentinel lives on a workspace.** You create (or pick) a Log Analytics workspace, then add Microsoft Sentinel to it. Once Sentinel is enabled, **all data in that workspace is charged at Sentinel pricing**, even operational data that has nothing to do with security. You ==!cannot move a Sentinel workspace== to another resource group or subscription afterwards. You also cannot install Sentinel on the default workspaces that Defender for Cloud creates.
- **Tables and schemas.** Azure Monitor creates standard tables automatically (for example `AzureActivity`, `SecurityEvent`, `SigninLogs`). You create **custom tables** for data from non-Azure sources.
- **Three table plans.** Each table has one plan:

| Plan | Best for | Ingestion cost | Querying |
|---|---|---|---|
| ==@Analytics== | High-value data for continuous monitoring and real-time detection | Standard | Full KQL, query price included, all alerts |
| ==@Basic== | Medium-touch data for troubleshooting and incident response | Reduced | Full KQL, charged per query, 30 days of querying, simple log alerts only |
| ==@Auxiliary== (shown as **Auxiliary / Lake**) | Low-touch, verbose, audit and compliance data | Minimal | Full KQL but slower, charged per query, no alerts |

- **Two retention states.** **Interactive (analytics) retention** is the period you can query directly. **Long-term retention** is cheap storage after that. **Total retention** is the two added together, up to **12 years**. Defaults: tables keep data for **30 days**; Analytics retention can be extended to **2 years**. A workspace with Sentinel gets **90 days** of retention free instead of 31. Older data comes back with a **search job**.
- **Access control mode (per workspace).** **Use resource or workspace permissions** (default for workspaces created after March 2019) lets someone with access to a VM read only that VM's logs. **Require workspace permissions** (default before March 2019) means you need rights on the workspace or table itself.
- **Access mode (how *you* opened it).** **Workspace-context**: you opened Logs from Azure Monitor or the workspace, so you see every table you have rights to. **Resource-context**: you opened Logs from a VM or other resource, so you see only that resource's records.
- **Two built-in roles to recognise.** **Log Analytics Reader** can run queries. **Log Analytics Contributor** can change workspace settings such as the daily cap. Both are Azure RBAC roles (see the RBAC primer).
- **Daily cap.** A per-workspace limit in GB per day. When reached, collection of billable data in Analytics and Basic tables **stops** until the reset hour. Auxiliary tables are not capped. Data over the cap is still billed. It is a safety net against surprise bills, not a cost-control tool. ==!Hitting it blinds your SOC.==
- **One workspace or many.** Start with **one**. Split only for a real reason: data must stay in a region, separate Entra tenants, split billing, different retention needs, or separate operational and security data.

## Where it lives

- **Create a workspace:** Azure portal > search **Log Analytics workspaces** > **Create** (subscription, resource group, name, region).
- **Enable Microsoft Sentinel on it:** Azure portal > search **Microsoft Sentinel** > **Create** > pick the workspace > **Add** (or **Create a new workspace**). To enable Sentinel you need **Contributor** on the subscription.
- **See workspaces in the Defender portal:** **System** > **Settings** > **Microsoft Sentinel** > **Workspaces**.
- **Access control mode:** shown on the workspace **Overview** page; change it on the workspace **Properties** page.
- **Default retention:** **Log Analytics workspaces** > your workspace > **Usage and estimated costs** > **Data Retention** (slider). CLI: `az monitor log-analytics workspace update --retention-time 90`.
- **Per-table plan and retention:** workspace > **Tables** > the table's context menu (**...**) > **Manage table**.
- **Daily cap:** workspace > **Usage and estimated costs** > **Daily Cap** > **ON**, then set GB/day.
- **Query the data:** workspace > **Logs** (Azure portal), or **Advanced hunting** in the Defender portal once Sentinel is onboarded there.

### Structure and table plans

![Diagram that shows the Azure Monitor Logs structure](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/data-platform-logs/logs-structure.png)

![Screenshot that shows the Log Analytics Workspace insights overview tab](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/log-analytics-workspace-insights-overview/at-resource.png)

![A diagram that shows how Azure Monitor and Azure Monitor Logs provide an end-to-end solution for collecting, managing, retrieving, and working with log data](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/data-platform-logs/azure-monitor-logs-overview.png)

![A diagram that shows data being collected from data sources and transformed and sent to tables in a Log Analytics workspace](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/data-platform-logs/azure-monitor-logs-collection-ingestion.png)

![A screenshot of a Log Analytics workspace in the Azure portal](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/data-platform-logs/log-analytics-workspace-for-all-log-data.png)

![Diagram that presents an overview of the capabilities provided by the Analytics, Basic, and Auxiliary table plans](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/data-platform-logs/azure-monitor-logs-data-plans.png)

![Screenshot that shows Log Analytics Simple mode](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/log-analytics-explorer/log-analytics-simple-mode-user-interface.png)

![A screenshot that shows the built-in Container Insights monitoring experience in Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/containers/media/kubernetes-monitoring-overview/containers-insights-experience.png)

### Access control mode

![Screenshot that shows the workspace access control mode](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/manage-access/view-access-control-mode.png)

![Screenshot that shows changing workspace access mode](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/manage-access/change-access-control-mode.png)

### Retention

![Diagram that shows analytics and long-term retention in Azure Monitor Logs](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/data-retention-configure/interactive-auxiliary-retention-log-analytics-workspace.png)

![Screenshot that shows changing the workspace data retention setting](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/manage-cost-storage/manage-cost-change-retention-01.png)

![Screenshot that shows the Manage table button for one of the tables in a workspace](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/logs-table-plans/log-analytics-table-configuration.png)

![Screenshot that shows the data retention settings on the table configuration screen](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/data-retention-configure/log-analytics-configure-table-retention-basic.png)

![Screenshot that shows the Manage table button for one of the tables in a workspace](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/data-retention-configure/log-analytics-view-table-retention-auxiliary.png)

### Daily cap

The second screenshot below is the **Application Insights** cap screen (Azure Monitor > Applications > your app > Usage and estimated costs > Data Cap). It is a different screen from the workspace daily cap. It appears here because it is in the cited article.

![Log Analytics configure data limit](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/manage-cost-storage/set-daily-volume-cap-01.png)

![Application Insights configure data limit](https://learn.microsoft.com/en-us/azure/azure-monitor/app/media/pricing/pricing-003.png)

### Enabling Microsoft Sentinel on a workspace

![Screenshot of searching for and selecting Microsoft Sentinel from the Azure portal](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/search-sentinel.png)

![Screenshot of selecting Create to start creating a new Log Analytics workspace](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/log-analytics-workspace-create.png)

![Screenshot of selecting Create a new workspace](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/log-analytics-workspace-create-a-new-workspace.png)

![Screenshot of creating a Log Analytics workspace screen. Under Subscription and resource group, Create New is selected](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/log-analytics-workspace-resource-group-create-new-with-name-both-selected.png)

![Screenshot of Microsoft Sentinel in the Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/defender-portal-initial-view.png)

![Screenshot of the content hub in the Defender portal with the solution for Azure Activity selected](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/content-hub-azure-activity-defender.png)

![Screenshot of the content hub in the Azure portal with the solution for Azure Activity selected](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/content-hub-azure-activity.png)

![Screenshot of data connector for Azure Activity with the status showing as connected](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/azure-activity-connected-status.png)

![Screenshot of the AzureActivity query in the Logs page of the Azure portal](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/azure-activity-logs-query.png)

## What the exam assumes you know

- "Sentinel workspace" = a Log Analytics workspace with Sentinel enabled. ==!Sentinel is not a separate database.==
- ==!Sentinel pricing applies to *all* data in the workspace==, not just security tables.
- Basic and Auxiliary plans are **cheaper to ingest but limited and charged to query**. Detections want Analytics.
- Resource-context access is the way to give an app team their own logs without opening the whole workspace.
- ==+Set a daily cap in a lab==, but in production watch for it, because collection stops when it hits.

## Skip list

- **Skip:** the Logs Ingestion API, data collection endpoints and workspace transformation DCRs. They belong to the Azure Monitor Agent and DCR primer and the D1 connector pages.
- **Skip:** the full KQL-capability matrix for Basic and Auxiliary plans and the search-job pricing. Retention-tier exam detail is on the **D1.2.2** objective page.
- **Skip:** `immediatePurgeDataOn30Days`, ARM/REST retention templates and PowerShell variants. Portal and one CLI line are enough.
- **Skip:** Log Analytics Workspace Insights dashboards and Container Insights. Operations tooling, not security operations.
- **Skip:** granular RBAC with row-level conditions and the long role table in the access article. Know the two access control modes and the two access modes.
- **Skip:** legacy-agent workspace limits, commitment-tier discount percentages and bandwidth-cost considerations in the design article.
- **Skip:** the Application Insights daily cap. Same idea, different product.
