+++
slug = "azure-monitor-agent-and-dcr"
title = "Azure Monitor Agent and data collection rules"
summary = "How logs get off a machine and into a Log Analytics workspace: the Azure Monitor Agent does the shipping, a data collection rule says what to ship, how to trim it and where to send it."
order = 14
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-overview",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-migration",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-manage",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/data-collection-rule-overview",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/data-collection-rule-structure",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/data-collection-rule-create-portal",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/data-collection-transformations",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/data-collection-endpoint-overview",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/vm/data-collection-windows-events",
  "https://learn.microsoft.com/en-us/azure/sentinel/connect-services-windows-based",
  "https://learn.microsoft.com/en-us/azure/sentinel/ama-migrate",
]
captured = 2026-11-12
related_objectives = ["D1.3.2", "D1.3.3", "D1.3.4"]
+++

## In one sentence

The **Azure Monitor Agent (AMA)** is a small program installed on a server that reads its logs and sends them to Azure; a **data collection rule (DCR)** is a separate Azure resource that tells the agent *which* logs to read, how to trim them, and *which* Log Analytics workspace to send them to.

## Why it exists

Think of a large office with a mailroom. Every desk (server) produces paper (logs). Someone must collect it (the agent). The mailroom also needs a written instruction sheet: "collect only invoices and contracts, shred the flyers, file them in cabinet B" (the DCR). If you change the instruction sheet once, every collector follows the new version.

Without an agent, Azure can see only the *outside* of a virtual machine (CPU, disk, network numbers from the host). It cannot see what happens *inside* the operating system — who logged on, which process started. That inside view is called **guest OS data**, and the agent exists to collect it.

For a SOC (security operations centre — the team that watches for attacks), this is how Windows Security events and Linux Syslog reach **Microsoft Sentinel**. Sentinel is Microsoft's SIEM (security information and event management system — the central place logs are searched for attacks). Sentinel reads from a **Log Analytics workspace**, which is the log database (see the workspace primer). AMA plus a DCR is the pipe that fills it.

## Mental model

Two separate things move in two separate lanes:

- **Control lane:** the DCR is a set of instructions stored in Azure. The agent downloads it and checks for updates.
- **Data lane:** the actual log records travel from the agent to Azure Monitor, get optionally trimmed, and land in a table.

Microsoft is explicit: ==!telemetry does not flow through the DCR resource==. The DCR is configuration. It is the instruction sheet, not the mailbag.

```svg
<svg viewBox="0 0 760 330" role="img" aria-label="Azure Monitor Agent data flow: the DCR is control-plane instructions, logs travel separately from the machine through Azure Monitor's ingestion pipeline with an optional transformation into workspace tables">
  <defs>
    <marker id="amadarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <rect class="box-accent" x="250" y="20" width="260" height="70" rx="8"/>
  <text x="380" y="48" text-anchor="middle" class="label-accent">Data collection rule (DCR)</text>
  <text x="380" y="72" text-anchor="middle" class="muted">what to collect · transform · where</text>
  <line class="divider" x1="20" y1="112" x2="740" y2="112"/>
  <text x="30" y="106" class="muted">control lane (instructions)</text>
  <text x="30" y="134" class="muted">data lane (log records)</text>
  <rect class="box" x="20" y="160" width="160" height="90" rx="8"/>
  <text x="100" y="188" text-anchor="middle">Server / VM</text>
  <text x="100" y="210" text-anchor="middle" class="muted">Windows or Linux</text>
  <text x="100" y="232" text-anchor="middle" class="label-accent">AMA installed</text>
  <rect class="box" x="230" y="160" width="160" height="90" rx="8"/>
  <text x="310" y="188" text-anchor="middle">Azure Monitor</text>
  <text x="310" y="210" text-anchor="middle" class="muted">ingestion pipeline</text>
  <rect class="box-accent" x="430" y="160" width="140" height="90" rx="8"/>
  <text x="500" y="188" text-anchor="middle">Transformation</text>
  <text x="500" y="210" text-anchor="middle" class="muted">transformKql</text>
  <text x="500" y="232" text-anchor="middle" class="muted">(optional)</text>
  <rect class="box-ok" x="610" y="160" width="130" height="90" rx="8"/>
  <text x="675" y="188" text-anchor="middle">Workspace</text>
  <text x="675" y="210" text-anchor="middle" class="muted">SecurityEvent</text>
  <text x="675" y="232" text-anchor="middle" class="muted">Syslog · Event</text>
  <line class="line-accent" x1="290" y1="90" x2="120" y2="158" marker-end="url(#amadarrow)"/>
  <text x="150" y="128" class="muted">agent downloads</text>
  <line class="line" x1="180" y1="205" x2="228" y2="205" marker-end="url(#amadarrow)"/>
  <line class="line" x1="390" y1="205" x2="428" y2="205" marker-end="url(#amadarrow)"/>
  <line class="line" x1="570" y1="205" x2="608" y2="205" marker-end="url(#amadarrow)"/>
  <line class="line-accent" x1="440" y1="90" x2="500" y2="158" marker-end="url(#amadarrow)"/>
  <text x="480" y="128" class="muted">pipeline reads</text>
  <rect class="box" x="20" y="270" width="160" height="44" rx="8"/>
  <text x="100" y="297" text-anchor="middle">DCR association</text>
  <text x="200" y="297" class="muted">= the link "this machine uses this DCR" (one machine ↔ one DCR per link)</text>
</svg>
```

![Diagram that shows data collection rule associations connecting each VM to a single DCR](https://learn.microsoft.com/en-us/azure/azure-monitor/agents/media/azure-monitor-agent-overview/data-collection-rule-associations.png){Several machines, one DCR — each line is a separate association}

![Two-panel diagram: one baseline DCR linked to four resources; a workload DCR and a specialised DCR linked to subsets](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-rule-overview/data-collection-rule-centralized-control.svg){Design DCRs around a shared need: one baseline rule for every machine, extra rules layered on only where needed. Lines are associations, not data flow}

![Clients sending data along a separate data path where Azure Monitor applies DCR configuration](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-rule-overview/azure-monitor-pipeline-simple.png){The data path is separate from the DCR resource}

![Basic operation for Azure Monitor agent using DCR](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-rule-overview/data-collection-virtual-machine.png){The AMA scenario — the one SC-200 cares about}

## What actually matters

1. **AMA replaced the legacy Log Analytics agent.** The old agent is called the *Log Analytics agent*, also known as **MMA** (Microsoft Monitoring Agent) on Windows and **OMS** on Linux. It was ==@retired on August 31, 2024==. After **March 2, 2026**, uploads from it can stop at any time without notice. It configured collection at the *workspace*; AMA configures it with DCRs. Any exam answer that installs MMA for new collection is a distractor.
2. **One DCR, many machines — through associations.** A **data collection rule association (DCRA)** links one resource to one DCR. To apply one DCR to 50 machines you need 50 associations. One machine can also have several DCRs. The overall relationship is many-to-many. When you create a DCR in the portal and add machines, the portal installs AMA if needed and creates the associations for you.
3. **A DCR has four main parts** (all JSON properties under `properties`):
   - `dataSources` — what to collect (Windows event logs, Syslog, performance counters, text files).
   - `streams` — the named shape of the data, such as `Microsoft-SecurityEvent` or `Microsoft-Syslog`. Custom shapes start with `Custom-` and are declared in `streamDeclarations`.
   - `destinations` — where it goes, for SC-200 almost always a Log Analytics workspace.
   - `dataFlows` — which stream goes to which destination, with an optional `transformKql` and `outputStream` (the target table).
4. **Transformations trim or reshape data at ingestion time.** A transformation is a KQL query (KQL is the Kusto Query Language — the log query language; see the KQL primer). It always starts from the word `source` (the incoming records) and runs on each record after Azure Monitor receives it and before it is stored. Use it to drop noisy rows, remove a column holding sensitive data, or add a column. Example: `source | where message has 'error'`. A **workspace transformation DCR** is a special one-per-workspace rule for data that does not arrive through a DCR. It is ignored for AMA data, because AMA data already has its own DCR. When Sentinel is enabled on the workspace, filtering with a transformation into Analytics tables carries no extra processing charge.
5. **XPath filters Windows events at the source.** In the portal you can pick logs and severity levels, or choose **Custom** and write an XPath query in the form `LogName!XPathQuery`, for example `Security!*[System[(EventID=4624)]]`. XPath is a query language for XML; Windows events are XML underneath. The filter runs on the machine, so dropped events never cost ingestion. Limits: XPath 1.0 only, up to 20 expressions per box, up to 100 boxes in a rule. Test a query locally with `Get-WinEvent -LogName 'Security' -FilterXPath '*[System[EventID=4624]]'`.
6. **A data collection endpoint (DCE) is usually not needed.** A DCE is an Azure resource that gives the agent private, regional URLs for downloading config and uploading data. AMA uses public endpoints by default. You need a DCE when using **Private Link** (private network access to Azure Monitor), and for a few data sources such as **Windows Firewall Logs**.

![Diagram that shows relationship between the different sections of a DCR](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-rule-structure/dcr-flow-diagram.png){DCR anatomy: data sources → input streams → data flows (with optional transformation) → destinations}

![Ingestion-time transformation for incoming data](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-transformations/transformation-overview.png){A transformation query runs on each incoming record — here only rows whose message contains "error" are kept}

![Operation of the workspace transformation DCR](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-transformations/workspace-transformation-dcr.png){The workspace transformation DCR — one per workspace, only for data that has no DCR of its own}

![Comparison of standard DCR transformations with workspace transformation DCR](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-transformations/transformation-comparison.png){Standard DCR transformation vs workspace transformation DCR}

![Flow of data from pipeline transformation to Azure Monitor transformation to Log Analytics workspace](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/pipeline-transformations/workflow.png){Azure Monitor pipeline (edge) transformation happens before data even reaches Azure — out of scope for SC-200, shown for completeness}

### The DCR in JSON — what a Sentinel connector creates

This is the shape of the rule the **Windows Security Events via AMA** connector builds (trimmed from Microsoft's sample):

```json
{
  "properties": {
    "dataSources": {
      "windowsEventLogs": [{
        "name": "eventLogsDataSource",
        "streams": ["Microsoft-SecurityEvent"],
        "xPathQueries": ["Security!*[System[(EventID=4624) or (EventID=4688)]]"]
      }]
    },
    "destinations": {
      "logAnalytics": [{ "name": "centralWorkspace", "workspaceResourceId": "/subscriptions/.../workspaces/centralTeamWorkspace" }]
    },
    "dataFlows": [{ "streams": ["Microsoft-SecurityEvent"], "destinations": ["centralWorkspace"] }]
  }
}
```

### How Sentinel connectors create DCRs

Many Sentinel data connectors (Windows Security Events via AMA, Syslog via AMA, Common Event Format via AMA, Windows Forwarded Events) are simply a guided way to build a DCR. You open the connector, select **+Add data collection rule**, pick machines on **Resources**, and pick events on **Collect**. On the **Collect** tab the Windows Security Events connector offers **All events**, **Common**, **Minimal** or **Custom** (XPath). Saving creates the DCR, the associations, and installs AMA on machines that lack it. Machines outside Azure must first be **Azure Arc**-enabled (see the Arc primer).

![Configuration of a Windows event data source in a data collection rule](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/media/data-collection-windows-event/data-source-windows-event.png){Basic mode: tick logs and severity levels}

![Custom configuration of a Windows event data source in a data collection rule](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/media/data-collection-windows-event/data-source-windows-event-custom.png){Custom mode: write XPath queries in the form LogName!XPathQuery}

![Steps to create an XPath query in the Windows Event Viewer](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/media/data-collection-rule-azure-monitor-agent/data-collection-rule-extract-xpath.png){Build the filter in Event Viewer, copy the XPath, then prefix it with the log name and "!"}

![Configuration of an Azure Monitor Logs destination in a data collection rule](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/media/data-collection/destination-workspace.png){Destination: an Azure Monitor Logs (Log Analytics) workspace. Adding two workspaces sends duplicate data and doubles cost}

![Records returned from the Event table](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/media/data-collection-windows-event/verify-event.png){Verifying collection: a plain Azure Monitor DCR lands Windows events in the Event table}

![AMA migration workbook in Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/media/ama-migrate/migrate-workbook.png){Sentinel's migration workbook shows which machines still run the legacy agent}

## Where it lives

| Task | Where |
|---|---|
| Create or view DCRs | **Azure portal > Monitor > Settings > Data Collection Rules > Create** |
| Create a DCR from Sentinel | **Microsoft Sentinel > Configuration > Data connectors >** *connector* **> Open connector page > +Add data collection rule** |
| Create a DCE | **Azure portal > Monitor > Settings > Data collection endpoints > Create** |
| See the agent on a VM | **Azure portal > Virtual machines >** *VM* **> Extensions + applications** — look for `AzureMonitorWindowsAgent` or `AzureMonitorLinuxAgent` |
| Role to create DCRs and associations | **Monitoring Contributor** on the subscription, resource group or DCR |

Install AMA by CLI (Windows VM, system-assigned managed identity):

```bash
az vm extension set --name AzureMonitorWindowsAgent --publisher Microsoft.Azure.Monitor --ids <vm-resource-id> --enable-auto-upgrade true
```

Create a DCR from a JSON file:

```bash
az monitor data-collection rule create --location 'eastus' --resource-group 'my-rg' --name 'my-dcr' --rule-file 'my-dcr.json'
```

Create the DCR in the **same region** as its destination workspace. The machines it applies to can be in any subscription or resource group in the tenant. Install at scale with **Azure Policy** (see the Policy primer).

![Data collection endpoints in the Azure Monitor menu](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-endpoint-overview/data-collection-endpoint-overview.png){Monitor > Data collection endpoints}

![Data collection endpoint basics tab](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-endpoint-overview/data-collection-endpoint-basics.png){Creating a DCE: name, subscription, resource group, region}

![Resources for a DCE in the Azure portal](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-endpoint-overview/data-collection-endpoint-resources.png){Agents associated with a DCE}

![DCR overview page with DCE](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-endpoint-overview/data-collection-rule-dce.png){A DCR's Overview page shows which DCE it uses — "Configure DCE" to change it}

![Resources in a single region using one data collection endpoint](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-endpoint-overview/data-collection-endpoint-one-region.png){Same region: one DCE serves config and receives data}

![Resources in two regions using data collection endpoints](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-endpoint-overview/data-collection-endpoint-regionality.png){Machines in another region: a config DCE near the machines, an ingestion DCE near the workspace}

![Resources in multiple regions sending to multiple workspaces using DCEs](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-endpoint-overview/data-collection-endpoint-regionality-multiple-workspaces.png){Multiple workspaces in multiple regions: one ingestion DCE per workspace region}

## What the exam assumes you know

- ==!Installing the Log Analytics agent (MMA/OMS)== for new collection is wrong; ==+AMA with a DCR== is right.
- ==!A DCE is always required== is false. It is needed for Private Link and a few sources such as Windows Firewall logs.
- The same Security events land in **different tables** depending on the route. Plain Azure Monitor DCR: `Event` table. Sentinel's **Windows Security Events via AMA** connector: ==@SecurityEvent==. **Windows Forwarded Events** connector: `WindowsEvent`. Many built-in Sentinel rules query `SecurityEvent` only.
- Cheapest filter for Windows events = **XPath in the DCR** (dropped at the machine). Filter for any table after arrival = **transformation** (`transformKql`).
- Non-Azure machines need **Azure Arc** before AMA-based connectors work.

## Skip list

- **Skip:** multi-stage transformations and the processor families (`header.*`, `filter.Basic`, `parse.*`, `enrich.DNSLookup`). They are in public preview. The exam tests the single `transformKql` query.
- **Skip:** the Event Hubs, platform metrics, platform logs and direct-ingestion (Logs Ingestion API) DCR scenarios below. SC-200 collection is AMA-centric; the Logs Ingestion API matters only for custom connectors (named in D1.3, not taught here).
- **Skip:** the transformation billing formula and the Auxiliary table examples. Remember one line: with Sentinel enabled, filtering into Analytics tables costs nothing extra.
- **Skip:** DCE regional design (config endpoint vs ingestion endpoint per region). Know *when* a DCE is needed, not how to lay out three regions.
- **Skip:** the Azure Monitor pipeline (edge) transformations, OpenTelemetry `directDataSources`, `agentSettings`, `references`, and the Windows MSI client installer. Not on the blueprint.
- **Skip:** the AMA-vs-legacy feature comparison tables (VM insights, change tracking, SQL assessment). Only "AMA is the supported agent; Sentinel works with it" matters.

![Basic operation for event hub data sent to Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-rule-overview/data-collection-event-hubs.png){Skip-list scenario: Event Hubs ingestion through a DCR (preview)}

![Basic operation for DCR collecting platform metrics](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-rule-overview/data-collection-platform-metrics.png){Skip-list scenario: platform metrics export through a DCR (preview)}

![Basic operation for DCR using Logs ingestion API](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-rule-overview/data-collection-direct-ingestion.png){Skip-list scenario: direct ingestion with the Logs Ingestion API — the basis of custom connectors}

![Basic operation of workspace transformation DCR](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-rule-overview/data-collection-workspace-transformation.png){Workspace transformation DCR applied directly to the workspace}
