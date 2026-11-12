+++
slug = "diagnostic-settings-and-activity-log"
title = "Diagnostic settings and the Activity log"
summary = "You will know the three kinds of Azure platform logs (Activity log, resource logs, Entra sign-in and audit logs), why most of them need a diagnostic setting before Sentinel can see them, and how the Azure Activity connector uses Azure Policy to do that at scale."
order = 15
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/activity-log",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/diagnostic-settings",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/resource-logs",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/data-sources",
  "https://learn.microsoft.com/en-us/entra/identity/monitoring-health/howto-configure-diagnostic-settings",
  "https://learn.microsoft.com/en-us/azure/sentinel/connect-azure-active-directory",
  "https://learn.microsoft.com/en-us/azure/sentinel/connect-services-diagnostic-setting-based",
  "https://learn.microsoft.com/en-us/azure/sentinel/quickstart-onboard",
]
captured = 2026-11-12
related_objectives = []
+++

## In one sentence

Azure keeps its own logs about what happens to your cloud resources, and a **diagnostic setting** is the small forwarding rule that copies those logs to a place Microsoft Sentinel can read — without it, most of them never leave the resource.

## Why it exists

Think of an office building. The front desk keeps a **visitor book**: who came in, which room they changed, when. That book exists whether you ask for it or not, but it is thrown away after a few months. Each room also has its **own logbook** — the safe records every time it is opened — but nobody collects those unless you ask.

Azure works the same way:

- The **Activity log** is the visitor book. It records changes made *to* resources: someone created a virtual machine (VM), deleted a storage account, changed a firewall rule. Azure writes it automatically.
- **Resource logs** are the per-room logbooks. They record work done *inside* a resource: a secret read from a key vault, a query run against a database. Azure does **not** collect them unless you tell it to.
- **Microsoft Entra ID** (Microsoft's cloud identity service) keeps its own **sign-in logs** and **audit logs** — who signed in, and who changed users, groups and apps.

A security operations centre (SOC) needs all of these in one searchable place. That place is a **Log Analytics workspace** — the database Microsoft Sentinel sits on. A **diagnostic setting** is the instruction "copy these log categories from this resource to that destination". It is the courier between the logbook and the archive.

## Mental model

Two words you will meet everywhere:

- **Control plane** — managing a resource *from outside*: create, update, delete, change settings. Goes through Azure Resource Manager (ARM), Azure's front door for management requests. Logged in the **Activity log**.
- **Data plane** — using the resource *from inside*: read a blob, fetch a secret, query a table. Logged in **resource logs**.

```svg
<svg viewBox="0 0 760 360" role="img" aria-label="Three platform log types flow through diagnostic settings to four destinations; Sentinel reads only the Log Analytics workspace">
  <defs>
    <marker id="dsalarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="currentColor"/>
    </marker>
  </defs>
  <rect class="box-ok" x="20" y="20" width="220" height="90" rx="8"/>
  <text x="130" y="46" text-anchor="middle" class="label-accent">Activity log</text>
  <text x="130" y="68" text-anchor="middle">control plane, per subscription</text>
  <text x="130" y="90" text-anchor="middle" class="muted">on by default, kept 90 days</text>
  <rect class="box-risk" x="20" y="135" width="220" height="90" rx="8"/>
  <text x="130" y="161" text-anchor="middle" class="label-risk">Resource logs</text>
  <text x="130" y="183" text-anchor="middle">data plane, per resource</text>
  <text x="130" y="205" text-anchor="middle" class="muted">OFF until you add a setting</text>
  <rect class="box" x="20" y="250" width="220" height="90" rx="8"/>
  <text x="130" y="276" text-anchor="middle">Entra sign-in + audit</text>
  <text x="130" y="298" text-anchor="middle">identity, per tenant</text>
  <text x="130" y="320" text-anchor="middle" class="muted">set in Entra admin center</text>
  <rect class="box-accent" x="300" y="120" width="160" height="120" rx="8"/>
  <text x="380" y="160" text-anchor="middle" class="label-accent">Diagnostic</text>
  <text x="380" y="180" text-anchor="middle" class="label-accent">setting</text>
  <text x="380" y="205" text-anchor="middle" class="muted">which categories,</text>
  <text x="380" y="223" text-anchor="middle" class="muted">which destinations</text>
  <line class="line" x1="240" y1="65" x2="298" y2="140" marker-end="url(#dsalarrow)"/>
  <line class="line" x1="240" y1="180" x2="298" y2="180" marker-end="url(#dsalarrow)"/>
  <line class="line" x1="240" y1="295" x2="298" y2="220" marker-end="url(#dsalarrow)"/>
  <rect class="box-ok" x="530" y="20" width="210" height="70" rx="8"/>
  <text x="635" y="48" text-anchor="middle">Log Analytics workspace</text>
  <text x="635" y="70" text-anchor="middle" class="label-accent">Sentinel reads this</text>
  <rect class="box" x="530" y="105" width="210" height="60" rx="8"/>
  <text x="635" y="132" text-anchor="middle">Storage account</text>
  <text x="635" y="152" text-anchor="middle" class="muted">cheap archive</text>
  <rect class="box" x="530" y="180" width="210" height="60" rx="8"/>
  <text x="635" y="207" text-anchor="middle">Event Hubs</text>
  <text x="635" y="227" text-anchor="middle" class="muted">stream to another SIEM</text>
  <rect class="box" x="530" y="255" width="210" height="60" rx="8"/>
  <text x="635" y="282" text-anchor="middle">Partner solution</text>
  <text x="635" y="302" text-anchor="middle" class="muted">Azure Native ISV</text>
  <line class="line-accent" x1="460" y1="150" x2="528" y2="58" marker-end="url(#dsalarrow)"/>
  <line class="line" x1="460" y1="170" x2="528" y2="135" marker-end="url(#dsalarrow)"/>
  <line class="line" x1="460" y1="195" x2="528" y2="210" marker-end="url(#dsalarrow)"/>
  <line class="line" x1="460" y1="215" x2="528" y2="282" marker-end="url(#dsalarrow)"/>
</svg>
```

![Diagram showing collection of activity logs, resource logs, and platform metrics](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/diagnostic-settings/platform-logs-metrics.png){Microsoft's version of the same picture: activity log, resource logs and platform metrics all leave Azure through diagnostic settings}

## What actually matters

**1. The Activity log is automatic, free, read-only, and short-lived.** Azure collects it with no setup. You cannot edit or delete entries. Azure keeps them for ==@90 days== and then deletes them, at no charge. It usually shows an event within 3 to 20 minutes. It records writes, deletes and actions — it does ==!not normally record reads==. It is also the **only** place that records *who created* a resource, which is the main reason to keep it longer.

**2. The Activity log is not a sign-in log.** If Azure Resource Manager rejects a request at authentication or authorization, no entry is written. Failed sign-ins live in the **Entra sign-in logs**, not here.

**3. Resource logs are off by default.** You must create a diagnostic setting **on each resource**. In a workspace they land in one of two shapes, called the **collection mode**:

| Collection mode | Where data goes | Notes |
|---|---|---|
| Azure diagnostics (legacy) | one shared table, `AzureDiagnostics` | used by a minority of services; very wide table |
| ==+Resource-specific== | one table per log category | easier to query; Microsoft says pick this for new settings |

**4. Platform metrics** — numbers like CPU percent — are also collected automatically. A diagnostic setting can copy them too (category `AllMetrics`). SOC work rarely needs them.

**5. Diagnostic setting rules worth remembering.**

| Rule | Value |
|---|---|
| Destinations | Log Analytics workspace, Storage account, Event Hubs, Azure Monitor partner solution |
| Settings per resource | up to ==@5== |
| Destinations of the same type per setting | one (two workspaces = two settings) |
| Destination must already exist | yes |
| Storage / Event Hubs region | same region as the monitored resource |
| Destination in another subscription | allowed if you have RBAC on both |
| Category groups | `allLogs` (everything) or `audit` (who touched data or settings) |
| Filter inside a category | ==!not possible== in the setting — use a transformation |
| First data arrives | within 90 minutes |

**Event Hubs** is Azure's message-streaming service; you pick it when logs must go to a non-Microsoft SIEM (security information and event management tool). **Storage** is the cheap long-term archive. For Sentinel, the answer is always the **workspace**.

**6. Activity log in a workspace = table `AzureActivity`.** Ingesting it costs nothing; you pay only for keeping it beyond 90 days (up to 12 years). Sentinel's analytics rules for Azure changes query this table.

```kql
AzureActivity
| summarize count() by CategoryValue
```

**7. Entra logs use Entra's own diagnostic settings.** You configure them in the **Microsoft Entra admin center**, not on an Azure resource. You need at least **Security Administrator** (or **Attribute Log Administrator** for custom security attribute logs). Logs can take up to three days to start. In the workspace they become `SigninLogs`, `AuditLogs`, `AADNonInteractiveUserSignInLogs` and others. A Microsoft Entra ID **P1 or P2** licence is required to ingest sign-in logs into Sentinel; audit logs work with any licence.

**8. Sentinel connectors are often just diagnostic settings.** Many Azure-service connectors in Sentinel are "diagnostic settings-based". Some are **standalone** — you open the resource and add the setting by hand, which needs read and write on the workspace. Others are **managed by Azure Policy** (Azure's rule engine that can create settings for you across a whole subscription). For those, the connector opens the **Azure Policy Assignment wizard**: you pick a scope, pick the Sentinel workspace, and tick **Create a remediation task** so *existing* resources get the setting too — otherwise only new ones do. You need the **Owner** role on the policy assignment scope. The connector shows green only if data arrived in the past 14 days.

## Where it lives

| Task | Where |
|---|---|
| View the Activity log | Azure portal > **Monitor** > **Activity log** (or any resource > **Activity log**) |
| Tenant-level events | Monitor > Activity log > change **Activity** to **Directory Activity** |
| Send Activity log to a workspace | Monitor > Activity log > **Export Activity Logs** |
| Resource logs | *resource* > **Monitoring** > **Diagnostic settings** > **Add diagnostic setting** |
| All settings in one list | Monitor > **Settings** > **Diagnostic settings** |
| Entra sign-in / audit logs | Entra admin center (`entra.microsoft.com`) > **Entra ID** > **Monitoring & health** > **Diagnostic settings** |
| Sentinel connector | Sentinel > **Configuration** > **Data connectors** > *connector* > **Open connector page** |

```bash
# read the Activity log for the last 14 days
az monitor activity-log list --offset 14d
# resource-scope diagnostic setting
az monitor diagnostic-settings create --name <name> --resource <resourceId> --workspace <workspaceId> --logs '[{"categoryGroup":"allLogs","enabled":true}]'
# Activity log export is a SUBSCRIPTION-scope setting
az monitor diagnostic-settings subscription create ...
```

PowerShell uses `Get-AzActivityLog` and `New-AzDiagnosticSetting`. `New-AzDiagnosticSetting` cannot export the Activity log; use a template or the subscription-scope CLI command.

### The Activity log in the portal

![Screenshot that shows the activity log](https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/media/activity-log/view-activity-log.png){Monitor > Activity log, filtered to one subscription}

![Directory Activity option selected in the Activity log blade](https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/media/activity-log/directory-activity-logs.png){Directory Activity shows tenant-level events such as new subscriptions or management groups}

![Activity log blade for a management group](https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/media/activity-log/management-group-scope.png){Management groups > select one > Activity log — policy assignments and membership changes}

![Change history list for an event](https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/media/activity-log/change-history-event.png){Open an event > Change history tab — changes up to 30 minutes either side}

![Change history page showing differences](https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/media/activity-log/change-history-event-details.png){The before/after view — here a VM size change}

![Activity log insights dashboards](https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/media/activity-log/activity-logs-insights-main-screen.png){Activity Logs Insights workbook — only works once the log is exported to a workspace (AzureActivity)}

![Opening the Activity Logs Insights workbook at subscription level](https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/media/activity-log/open-activity-log-insights-workbook.png){Monitor > Workbooks > Activity Logs Insights}

![Opening Activity Logs Insights at resource level](https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/media/activity-log/activity-log-resource-level.png){The same workbook from a single resource's menu}

![Download as CSV button in the activity log](https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/media/activity-log/export-csv.png){Download as CSV — a one-off file, not ongoing collection}

![Azure Monitor menu with Export activity logs highlighted](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/diagnostic-settings/menu-activity-log.png){Export Activity Logs opens the subscription's diagnostic settings — this is how the Activity log reaches Sentinel}

### Diagnostic settings on a resource

![Adding a diagnostic setting where settings already exist](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/diagnostic-settings/edit-setting.png){A key vault's Diagnostic settings list — Add diagnostic setting or Edit setting}

![Diagnostic setting details](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/diagnostic-settings/setting-new-blank.png){Name, log categories or category groups, AllMetrics, and destination checkboxes}

![Diagnostics settings mode selector](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/resource-logs/diagnostic-settings-mode-selector.png){Where a service offers the choice: Azure diagnostics vs Resource specific}

![AzureDiagnostics table in a Log Analytics workspace](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/resource-logs/azure-diagnostics-table.png){The legacy shared AzureDiagnostics table — many services, one wide table}

### Entra ID diagnostic settings

![Microsoft Entra diagnostic settings page](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/media/howto-configure-diagnostic-settings/diagnostic-settings-start.png){Entra admin center > Entra ID > Monitoring & health > Diagnostic settings}

![Custom security attributes page for diagnostic settings](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/media/howto-configure-diagnostic-settings/custom-security-attributes.png){The separate Custom security attributes tab — needs Attribute Log Administrator}

![Log categories in diagnostic settings](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/media/howto-configure-diagnostic-settings/diagnostic-settings-log-categories.png){Pick AuditLogs, SignInLogs, NonInteractiveUserSignInLogs and the rest}

![Destination options in diagnostic settings](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/media/howto-configure-diagnostic-settings/diagnostic-settings-destination-details.png){Same four destinations as an Azure resource}

![Create diagnostic settings page with logs going to a workspace](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/media/howto-configure-diagnostic-settings/diagnostic-settings-save.png){A finished Entra setting sending several logs to a Log Analytics workspace}

### Sentinel's Azure Activity connector (quickstart walk-through)

![Searching for Microsoft Sentinel in the Azure portal](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/search-sentinel.png){Azure portal > search Microsoft Sentinel}

![Selecting Create to start a new Log Analytics workspace](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/log-analytics-workspace-create.png){Sentinel is added to a workspace — Create}

![Selecting Create a new workspace](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/log-analytics-workspace-create-a-new-workspace.png){Create a new workspace if you have none}

![Creating a workspace with a new resource group](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/log-analytics-workspace-resource-group-create-new-with-name-both-selected.png){Subscription > Resource group > Create new}

![Microsoft Sentinel in the Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/defender-portal-initial-view.png){Sentinel inside the Defender portal (security.microsoft.com)}

![Content hub in the Defender portal with the Azure Activity solution selected](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/content-hub-azure-activity-defender.png){Install the Azure Activity solution from Content hub (Defender portal). Learn reuses this image for the AzureActivity query step.}

![Content hub in the Azure portal with the Azure Activity solution selected](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/content-hub-azure-activity.png){The same solution in the Azure portal Content hub}

![Azure Activity data connector showing Connected](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/azure-activity-connected-status.png){Connector status Connected — data arrived within the last 14 days}

![AzureActivity query in the Logs page of the Azure portal](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/azure-activity-logs-query.png){Proof it worked: run AzureActivity in Logs}

> **Two Microsoft pages disagree on the Azure Activity connector.** The Sentinel quickstart says the connector page uses **Launch Azure Policy Assignment Wizard** (scope = subscription, parameter = primary workspace). The diagnostic-settings connector article says Azure Activity "now uses the diagnostic settings pipeline" and points to the *standalone* steps. Both routes end in the same place: a **subscription-level diagnostic setting** sending the Activity log to the Sentinel workspace's `AzureActivity` table. Follow whatever your own connector page shows — the product UI wins over the docs.

## What the exam assumes you know

- ==@Activity log== = control plane, automatic, 90 days, table `AzureActivity`. ==@Resource logs== = data plane, need a diagnostic setting per resource.
- ==!"Resource logs are collected by default"== is false. ==+Create a diagnostic setting== is the fix in almost every "logs are missing" question.
- For Sentinel, the destination is the **Log Analytics workspace**. Event Hubs is for *another* SIEM; Storage is for archive.
- Entra sign-in/audit logs are configured in the **Entra admin center**, need **Security Administrator**, and sign-in logs need **P1 or P2**.
- Policy-managed connectors need **Owner** on the scope and a **remediation task** to cover existing resources.

## Skip list

- **Skip** the REST `$filter` patterns, the 75-second `Prefer` header and the Event Hubs/Storage JSON samples and blob naming (`insights-activity-logs/...PT1H.json`). That is developer plumbing; SC-200 never asks for it.
- **Skip** management-group diagnostic settings and the `hierarchy` property duplicate-event problem. Real, but an architect topic — know only that the Activity log is normally exported per subscription.
- **Skip** metrics limitations (multidimensional flattening, back-off on inactive resources). Sentinel works on logs, not metrics.
- **Skip** the Application Insights diagnostic-setting caveats. App monitoring is not a SOC topic.
- **Skip** Activity Logs Insights, Change history and Download as CSV beyond recognising them in the screenshots above. Sentinel queries `AzureActivity` directly.
- **Skip** the legacy "log profiles" export method and the legacy Azure Activity connector — both retired paths. Just know to disconnect the legacy method if a connector page asks.
- **Skip** firewall details (trusted Microsoft services bypass, compacted event hubs, Premium storage not supported, `ListKey`). These matter only if your destination is Storage or Event Hubs.
- **Skip** the per-service resource-log category lists. Use category group `allLogs` or what the Sentinel connector recommends; nobody memorises the lists.
