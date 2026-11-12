+++
slug = "sentinel-content-hub-and-solutions"
title = "Microsoft Sentinel Content hub and solutions"
summary = "What the Sentinel Content hub is, what a solution packages, how installing and updating work, why an installed rule template is not a running rule, how support models differ, and where Repositories fit."
order = 11
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/azure/sentinel/sentinel-solutions",
  "https://learn.microsoft.com/en-us/azure/sentinel/sentinel-solutions-deploy",
  "https://learn.microsoft.com/en-us/azure/sentinel/sentinel-solutions-delete",
  "https://learn.microsoft.com/en-us/azure/sentinel/ci-cd",
  "https://learn.microsoft.com/en-us/training/modules/manage-content-microsoft-sentinel/2-use-solutions-from-content-hub",
]
captured = 2026-11-12
related_objectives = ["D1.1.11", "D1.2.3", "D1.2.4", "D1.3.1", "D1.3.2", "D1.3.3", "D1.3.4", "D1.3.5", "D1.3.6", "D1.4.3"]
+++

## In one sentence

The **Content hub** is Microsoft Sentinel's app store: you install **solutions** (bundles of data connectors, analytics rule templates, workbooks, hunting queries, parsers and playbooks for one product or scenario) or single **standalone** items — and installing gives you **templates**, ==!not running detections==.

## Why it exists

A fresh Sentinel workspace is empty. It has no connectors, no detection rules and no dashboards. Writing all of that yourself for every firewall, cloud and identity product would take years.

Vendors and Microsoft have already written it. The Content hub is where you fetch it. Think of a **phone app store**. Searching "Palo Alto" and pressing **Install** gives you the app. But the app does nothing until you open it, sign in and switch features on. Installing a solution works the same way: the parts arrive on your workspace, and you still connect the data and turn the rules on.

**Microsoft Sentinel** is Microsoft's cloud **SIEM** (security information and event management: the system that collects logs and raises alerts). It runs on a **Log Analytics workspace** (the database that holds the log tables). Every SC-200 Sentinel lesson — connectors, rules, workbooks, playbooks — starts with "install the solution from Content hub".

## Mental model

```svg
<svg viewBox="0 0 780 360" role="img" aria-label="A solution from the Content hub installs templates and a connector into the workspace; you then create active items from templates: a connector is connected, a rule template becomes an active rule, a workbook template is saved, a playbook template becomes a playbook">
  <defs>
    <marker id="schs-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <rect class="box-accent" x="15" y="20" width="200" height="320" rx="10"/>
  <text x="115" y="46" text-anchor="middle" class="label-accent">Content hub</text>
  <text x="115" y="66" text-anchor="middle" class="muted">Microsoft · partner · community</text>
  <rect class="box" x="30" y="84" width="170" height="150" rx="6"/>
  <text x="115" y="106" text-anchor="middle">Solution</text>
  <text x="115" y="128" text-anchor="middle" class="muted">connector(s)</text>
  <text x="115" y="148" text-anchor="middle" class="muted">rule templates</text>
  <text x="115" y="168" text-anchor="middle" class="muted">workbook templates</text>
  <text x="115" y="188" text-anchor="middle" class="muted">hunting queries</text>
  <text x="115" y="208" text-anchor="middle" class="muted">parsers · playbooks</text>
  <rect class="box" x="30" y="250" width="170" height="70" rx="6"/>
  <text x="115" y="278" text-anchor="middle">Standalone item</text>
  <text x="115" y="300" text-anchor="middle" class="muted">one piece, auto-updates</text>
  <line x1="215" y1="170" x2="268" y2="170" class="line-accent" marker-end="url(#schs-arrow)"/>
  <text x="241" y="158" text-anchor="middle" class="muted">Install</text>
  <rect class="box" x="270" y="20" width="230" height="320" rx="10"/>
  <text x="385" y="46" text-anchor="middle" class="label-accent">Your workspace: templates</text>
  <text x="385" y="66" text-anchor="middle" class="muted">installed, NOT yet doing anything</text>
  <text x="385" y="110" text-anchor="middle">Connector: Disconnected</text>
  <text x="385" y="160" text-anchor="middle">Rule template (not running)</text>
  <text x="385" y="210" text-anchor="middle">Workbook template</text>
  <text x="385" y="260" text-anchor="middle">Playbook template</text>
  <text x="385" y="306" text-anchor="middle" class="muted">parsers = ready workspace functions</text>
  <line x1="500" y1="105" x2="553" y2="105" class="line-accent" marker-end="url(#schs-arrow)"/>
  <line x1="500" y1="155" x2="553" y2="155" class="line-accent" marker-end="url(#schs-arrow)"/>
  <line x1="500" y1="205" x2="553" y2="205" class="line-accent" marker-end="url(#schs-arrow)"/>
  <line x1="500" y1="255" x2="553" y2="255" class="line-accent" marker-end="url(#schs-arrow)"/>
  <rect class="box-ok" x="555" y="20" width="210" height="320" rx="10"/>
  <text x="660" y="46" text-anchor="middle" class="label-accent">Active items</text>
  <text x="660" y="66" text-anchor="middle" class="muted">YOU create these</text>
  <text x="660" y="110" text-anchor="middle">Configure → Connected</text>
  <text x="660" y="160" text-anchor="middle">Create rule → Active rule</text>
  <text x="660" y="210" text-anchor="middle">Save → My workbooks</text>
  <text x="660" y="260" text-anchor="middle">Create playbook</text>
  <text x="660" y="306" text-anchor="middle" class="muted">updates never overwrite these</text>
</svg>
```

Three columns, three states. The catalogue (left). What install puts on your workspace (middle). What you must create yourself (right). Most exam traps sit on the arrow between middle and right.

## What actually matters

**1. What the hub carries.** Eight content types:

| Type | What it does | Where it shows up after install |
|---|---|---|
| ==@Data connectors== | Bring logs in | **Data connectors** page |
| ==@Analytics rules== | Detect threats, raise alerts and incidents (D1.4.3) | **Analytics** > **Rule templates** |
| Hunting queries | Saved KQL for proactive searching | **Hunting** |
| Parsers | KQL functions that reshape vendor logs into **ASIM** (Advanced Security Information Model, a common schema) | Workspace **functions** in Logs |
| Playbooks (and Logic Apps custom connectors) | Automated response (D1.1.11) | **Automation** > playbook templates |
| Watchlists | Reference lists, such as VIP users | **Watchlists** |
| Workbooks | Dashboards (D1.2.3) | **Workbooks** > **Templates** |
| Summary rule templates | Pre-aggregate verbose logs to save cost | **Summary rules** |

**2. Solution vs standalone.** A **solution** is a package for one product, domain or industry — for example *Azure Activity* or a firewall vendor. It contains **packaged content** (the items above) and sometimes **integrations** (tools built on Sentinel APIs). The solutions catalogue runs on **Azure Marketplace**. A **standalone** item is a single piece of content with no package. ==!To use any item that is part of a solution, you must install the whole solution.==

**3. Install is not enable.** After install:

- The **connector** shows **Disconnected** until you configure it and logs arrive. Then it shows **Connected**.
- Each **analytics rule** arrives as a **template**. You select it and choose **Create rule**. Only then does a scheduled query run. The **Created content** column counts how many active rules you made from it.
- **Workbook** templates need **Save** to become your own copy.
- **Hunting queries** are read-only templates. Run them as-is, or clone to edit.
- **Parsers** become workspace **functions** immediately — the one item that is "live" straight away.
- **Playbook** templates need **Create playbook**.

**4. Updates.** If a newer version of an installed solution exists, the list view shows **Update** in the status column and an **Updates** count at the top. You update solutions yourself. **Standalone content updates automatically.** Updates never touch the **active or custom** items you already created from templates. A rule built from an older template shows an update notice on the Analytics page instead (D1.4.3).

**5. Who can install.** ==@Microsoft Sentinel Contributor at the resource-group level== — to install, update or delete solutions and standalone content.

**6. Support models — who answers the phone.**

| Support model | Who authored it | Who supports it |
|---|---|---|
| ==@Microsoft-supported== | Microsoft (sometimes for non-Microsoft data) | Microsoft, under Azure support plans |
| ==@Partner-supported== | A vendor, MSSP or integrator | That partner — contact on the details pane |
| ==@Community-supported== | Microsoft or partner developers, no listed support contact | GitHub issues in the Microsoft Sentinel community repo |

The **Support** box on each item's details pane names the model. The **Usage information & support** tab gives the publisher, provider and plan ID that a support ticket asks for.

**7. Content source.** Every item in Sentinel carries a source: **Solution** (lifecycle-managed by the hub), **Standalone** (auto-updated), **Custom** (you edited or wrote it), or **Repositories** (deployed from source control).

**8. Removing content.** In a solution (version **2.0.0** or higher), **Manage** lists its items. You can delete single items, or delete the whole solution. ==!Deleting a solution does not delete active, cloned, saved or custom items== built from it. **Reinstall** brings the templates back.

**9. Repositories — one paragraph.** For content *you* write, Sentinel can connect a **GitHub** or **Azure DevOps** repository (**Content management** > **Repositories**). You need **Owner** on the workspace's resource group. Commits deploy analytics rules, automation rules, hunting queries, parsers, playbooks and workbooks to the workspace through a generated workflow or pipeline. Edit content in the repository, not in Sentinel, or the next deployment overwrites your change. Deleting a file from the repository does **not** delete it from Sentinel. The rule of thumb from Microsoft: Content hub manages updates for out-of-the-box content; **Repositories** manages updates for custom content.

## Where it lives

| Task | Defender portal | Azure portal |
|---|---|---|
| Open the hub | **Microsoft Sentinel** > **Content management** > **Content hub** | **Microsoft Sentinel** > **Content management** > **Content hub** |
| Install one solution | select it > **View details** > **Create** (or **Update**) > wizard tabs > **Review + create** | same |
| Install several | switch to **list view** > tick items > **Install/Update** | same |
| Pull in required connectors | **Install with dependencies** (for example, vendor solutions that need **CEF via AMA** or **Syslog via AMA**) | same |
| Work with a solution's items | select an installed solution > **Manage** | same |
| Deploy as code | wizard link **Download a template for automation** (an ARM template) | same |
| Connect a repository | **Microsoft Sentinel** > **Content management** > **Repositories** > **Add new** | **Content management** > **Repositories** |

The wizard's **Basics** tab asks for **subscription**, **resource group** and **workspace**. Search uses AI fuzzy matching and returns at most **50** results. Sentinel in the Azure portal is supported until **31 March 2027**; after that it is Defender portal only.

### The Content hub

![Content hub in the Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/media/sentinel-solutions-deploy/solutions-list-defender.png){Content hub in the Defender portal — list view with filters for status, content type, support, provider and category}

![Content hub in the Azure portal](https://learn.microsoft.com/en-us/azure/sentinel/media/sentinel-solutions-deploy/solutions-list.png){The same catalogue in the Azure portal}

![Solution installation wizard, Basics tab](https://learn.microsoft.com/en-us/azure/sentinel/media/sentinel-solutions-deploy/wizard-basics.png){Install wizard, Basics tab: subscription, resource group, workspace}

![Installing multiple solution dependencies in bulk](https://learn.microsoft.com/en-us/azure/sentinel/media/sentinel-solutions-deploy/install-update-dependencies.png){Install with dependencies — the connector solution comes along}

![Solutions list view with multiple solutions selected](https://learn.microsoft.com/en-us/azure/sentinel/media/sentinel-solutions-deploy/bulk-install-update.png){Bulk Install/Update from list view}

### Managing a solution's items

![Manage button on the Azure Activity solution](https://learn.microsoft.com/en-us/azure/sentinel/media/sentinel-solutions-deploy/content-hub-manage-option.png){Manage appears on installed solutions version 2.0.0 or higher}

![Content items of the Azure Activity solution](https://learn.microsoft.com/en-us/azure/sentinel/media/sentinel-solutions-deploy/manage-solution-azure-activity.png){One solution, many items — note the Created content column}

![Data connector item, status disconnected](https://learn.microsoft.com/en-us/azure/sentinel/media/sentinel-solutions-deploy/manage-solution-data-connector-open-connector.png){Installed connector still says Disconnected until you configure it}

![Analytics rule item in the solution](https://learn.microsoft.com/en-us/azure/sentinel/media/sentinel-solutions-deploy/manage-solution-analytics-rule.png){Rule template with 2 items under Content created — two active rules made from it}

![Cloned hunting query item](https://learn.microsoft.com/en-us/azure/sentinel/media/sentinel-solutions-deploy/manage-solution-hunting-query.png){Hunting query: Run query, or clone the read-only template to edit}

![Saved workbook item](https://learn.microsoft.com/en-us/azure/sentinel/media/sentinel-solutions-deploy/manage-solution-workbook.png){Workbook template saved as your own copy}

![Parser content type](https://learn.microsoft.com/en-us/azure/sentinel/media/sentinel-solutions-deploy/manage-solution-parser.png){Parser: Load the function code, or Use in editor}

![Playbook content type](https://learn.microsoft.com/en-us/azure/sentinel/media/sentinel-solutions-deploy/manage-solution-playbook.png){Playbook template → Create playbook}

### Support and removal

![Support model for a solution](https://learn.microsoft.com/en-us/azure/sentinel/media/sentinel-solutions-deploy/find-support-details.png){The Support box names Microsoft or the partner}

![Usage and support details for a solution](https://learn.microsoft.com/en-us/azure/sentinel/media/sentinel-solutions-deploy/usage-support.png){Usage information & support: publisher, provider, plan ID}

![Solution with content items selected for deletion](https://learn.microsoft.com/en-us/azure/sentinel/media/sentinel-solutions-delete/manage-solution-delete-item.png){Delete individual items from Manage; Reinstall restores them}

![Confirmation prompt to delete the solution](https://learn.microsoft.com/en-us/azure/sentinel/media/sentinel-solutions-delete/manage-solution-delete.png){Deleting a solution removes templates, not the active items you built}

### Repositories

![New GitHub repository connection](https://learn.microsoft.com/en-us/azure/sentinel/media/ci-cd/create-new-connection-github.png){Create new deployment connection — GitHub}

![New Azure DevOps repository connection](https://learn.microsoft.com/en-us/azure/sentinel/media/ci-cd/create-new-connection-devops.png){Create new deployment connection — Azure DevOps}

![Repository connection deployment logs](https://learn.microsoft.com/en-us/azure/sentinel/media/ci-cd/deployment-logs-status.png){Repositories page shows last deployment status and a log link}

![Analytics rules filtered by repository source](https://learn.microsoft.com/en-us/azure/sentinel/media/ci-cd/delete-repo-content.png){Filter by source name to find repository content — delete it in both places}

## What the exam assumes you know

- "A connector is missing from the Data connectors page." ==+Install its solution from Content hub.==
- ==!Installing a solution turns on its detections.== ==+You must create active rules from the templates.==
- ==!A solution update rewrites my edited rule.== ==+Active and custom items are never overwritten.==
- ==!Deleting a solution deletes the rules I made from it.== ==+Only the templates go.==
- Install/update/delete needs ==+Microsoft Sentinel Contributor on the resource group==. Repositories need **Owner**.
- Partner-supported content → call **the partner**, not Microsoft.

## Skip list

- **Skip:** the 25 domain categories and 7 industry-vertical categories. They are search filters. Know only that categories exist.
- **Skip:** the install-by-API steps (Get Product Package API, `properties.mainTemplate`, ARM deployment). Know "Download a template for automation" exists.
- **Skip:** the Microsoft Sentinel Solutions Build Guide and Azure Marketplace publishing. That is for vendors writing solutions, not analysts using them.
- **Skip:** Repositories deep detail — GitHub app installation, Azure DevOps OAuth policy, smart deployments, Bicep support, removing the Azure-Sentinel app. One paragraph above is enough.
- **Skip:** card view vs list view mechanics beyond "list view does bulk install".
- **Skip:** training unit 2's Cisco Umbrella item counts. It is an example, not a fact to learn.
