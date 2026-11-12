+++
slug = "logic-apps-basics"
title = "Azure Logic Apps basics (and why playbooks are Logic Apps)"
summary = "You will know what a Logic Apps workflow, trigger, action and connector are, how Consumption differs from Standard, how a workflow signs in with a managed identity, where run history lives, and why every Microsoft Sentinel playbook is a Logic App that needs specific roles to run."
order = 18
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-overview",
  "https://learn.microsoft.com/en-us/azure/logic-apps/view-workflow-status-run-history",
  "https://learn.microsoft.com/en-us/azure/sentinel/automation/logic-apps-playbooks",
  "https://learn.microsoft.com/en-us/azure/sentinel/automation/automate-responses-with-playbooks",
  "https://learn.microsoft.com/en-us/azure/sentinel/automation/create-playbooks",
  "https://learn.microsoft.com/en-us/azure/sentinel/authenticate-playbooks-to-sentinel",
]
captured = 2026-11-12
related_objectives = ["D1.1.10", "D1.1.11"]
+++

## In one sentence

**Azure Logic Apps** is an Azure service that runs "when this happens, do these steps" recipes. A **Microsoft Sentinel playbook** is simply one of those recipes, started by a Sentinel incident, alert or entity.

## Why it exists

Think of a smoke detector that also phones the fire brigade and texts the building manager. The detector spots the problem. Something else has to *do* the follow-up jobs, every time, at 3 a.m.

In a SOC (security operations centre), Microsoft Sentinel is the detector. It raises **alerts** (one suspicious event) and groups them into **incidents** (the case an analyst works). The follow-up jobs are things like "post in Teams", "open a ServiceNow ticket" or "disable this user". Logic Apps gives you a visual designer and ready-made plug-ins, so an analyst can build them without writing code.

Microsoft did not build a separate automation engine for Sentinel. It reused Logic Apps. That is the single most important fact on this page: ==@a playbook IS a Logic Apps workflow==. It lives in a resource group, it is billed as a Logic App, and it is edited in the Logic Apps designer.

## Mental model

A workflow is a **recipe card**:

- **Trigger** — the first line, "Start when…". Every workflow has ==exactly one== trigger. Examples: an email arrives, a file lands in storage, a timer fires, a Sentinel incident is created.
- **Actions** — every step after the trigger. Send an email, call an API, add a comment to the incident. Actions can run in sequence, in parallel, or inside conditions and loops.
- **Connectors** — the plug-in for one product (Outlook, Teams, ServiceNow, Microsoft Sentinel). A connector supplies the triggers and actions for that product. Logic Apps lists **1,400+** prebuilt connectors.
- **Connection** — the saved sign-in a connector uses. Logic Apps stores it as a separate Azure resource called an **API connection**.

```svg
<svg viewBox="0 0 900 330" role="img" aria-label="Sentinel playbook flow: incident triggers an automation rule, which runs a Logic Apps workflow; the workflow uses connectors signed in with a managed identity to act on other systems; every run is recorded in run history">
  <defs>
    <marker id="labarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <rect class="box" x="15" y="40" width="160" height="90" rx="8"/>
  <text x="95" y="72" text-anchor="middle" class="label-accent">Sentinel</text>
  <text x="95" y="95" text-anchor="middle">incident / alert</text>
  <text x="95" y="116" text-anchor="middle" class="muted">or an entity</text>
  <rect class="box" x="215" y="40" width="160" height="90" rx="8"/>
  <text x="295" y="72" text-anchor="middle">Automation rule</text>
  <text x="295" y="95" text-anchor="middle">or analyst clicks</text>
  <text x="295" y="116" text-anchor="middle" class="muted">"Run playbook"</text>
  <rect class="box-accent" x="415" y="20" width="250" height="210" rx="10"/>
  <text x="540" y="46" text-anchor="middle" class="label-accent">Logic App = playbook</text>
  <rect class="box" x="435" y="60" width="210" height="40" rx="6"/>
  <text x="540" y="85" text-anchor="middle">1 trigger (Sentinel)</text>
  <rect class="box" x="435" y="110" width="210" height="40" rx="6"/>
  <text x="540" y="135" text-anchor="middle">action: condition</text>
  <rect class="box" x="435" y="160" width="210" height="40" rx="6"/>
  <text x="540" y="185" text-anchor="middle">actions via connectors</text>
  <text x="540" y="220" text-anchor="middle" class="muted">every run → run history</text>
  <rect class="box-ok" x="710" y="20" width="175" height="60" rx="8"/>
  <text x="797" y="56" text-anchor="middle">Teams / email</text>
  <rect class="box-ok" x="710" y="95" width="175" height="60" rx="8"/>
  <text x="797" y="131" text-anchor="middle">ServiceNow ticket</text>
  <rect class="box-ok" x="710" y="170" width="175" height="60" rx="8"/>
  <text x="797" y="206" text-anchor="middle">update incident</text>
  <rect class="box-risk" x="415" y="255" width="250" height="60" rx="8"/>
  <text x="540" y="280" text-anchor="middle" class="label-risk">Identity it signs in as</text>
  <text x="540" y="302" text-anchor="middle" class="muted">managed identity (recommended)</text>
  <line class="line-accent" x1="175" y1="85" x2="213" y2="85" marker-end="url(#labarrow)"/>
  <line class="line-accent" x1="375" y1="85" x2="433" y2="85" marker-end="url(#labarrow)"/>
  <line class="line" x1="665" y1="180" x2="708" y2="50" marker-end="url(#labarrow)"/>
  <line class="line" x1="665" y1="180" x2="708" y2="125" marker-end="url(#labarrow)"/>
  <line class="line" x1="665" y1="180" x2="708" y2="200" marker-end="url(#labarrow)"/>
  <line class="divider" x1="540" y1="230" x2="540" y2="255"/>
</svg>
```

![Screenshot that shows the workflow designer with an example order review workflow that uses condition and switch actions.](https://learn.microsoft.com/en-us/azure/logic-apps/media/logic-apps-overview/example-enterprise-workflow.png){A general Logic Apps workflow: one trigger at the top, then actions, a condition and a switch. A Sentinel playbook looks the same — only the trigger and connectors differ.}

## What actually matters

**1. Logic app resource vs workflow.** The **logic app** is the Azure resource you create. The **workflow** is the recipe inside it. Behind the visual designer, each workflow is stored as a JSON definition, so it can be deployed as an ARM (Azure Resource Manager) template.

**2. Consumption vs Standard.** You pick a hosting model when you create the logic app.

| | Consumption | Standard |
|---|---|---|
| Runs in | multitenant Azure Logic Apps (shared) | single-tenant Azure Logic Apps (dedicated), ASEv3, or hybrid |
| Workflows per logic app | ==@only one== | many |
| Billing | pay per execution | hosting plan (Workflow Service Plan) |
| Private network access | no | virtual network integration, private endpoints |
| Stateful / stateless | — | both exist; ==!Sentinel supports stateful only== |
| Sentinel playbook templates | supported | ==!not supported== — build manually |
| Run history location | logic app **Overview > Runs history** | workflow menu **Tools > Run history** |
| Shown in Sentinel as | playbook name | `LogicApp/Workflow` |

A **stateful** workflow saves each step's inputs and outputs, so it has run history. A **stateless** one does not, and Sentinel cannot use it as a playbook.

**3. The three Sentinel triggers.** The **Microsoft Sentinel** connector offers three triggers. The **incident** trigger hands the playbook the incident plus all its alerts and entities. The **alert** trigger hands it one alert. The **entity** trigger hands it one **entity** — a thing in the incident such as a user account, host, IP address or URL. After the trigger, **dynamic content** (the lightning icon) lets later actions use fields the trigger produced, such as the incident's severity. The **expression editor** (function icon) adds functions.

In the Defender portal the create menu now says **Playbook with case trigger**. Defender calls an incident a *case*. The trigger it creates in Logic Apps is still named **Microsoft Sentinel incident**. The older incident, alert and entity choices are labelled **(Legacy)** there.

**4. How a playbook signs in.** A connector must authenticate to every system it touches, Sentinel included. The Sentinel connector supports three identity types:

- **Managed identity** — an identity Azure creates for the logic app itself, with no password to store. Microsoft recommends it. The create wizard's **Connections** tab sets it up by default.
- **Service principal** — the identity of a registered Microsoft Entra application (tenant ID, client ID, client secret).
- **Microsoft Entra user** — a person's account (**Sign in**). It breaks when that person leaves.

Whatever the identity, give it an Azure role on the Sentinel workspace. **Microsoft Sentinel Reader** allows triggers and read actions. **Microsoft Sentinel Responder** or **Microsoft Sentinel Contributor** also allows write actions, such as adding a comment. To assign that role you need **Owner** or **User Access Administrator**.

**5. Who may build, attach and run playbooks.** This is the most-tested part. All are Azure RBAC roles, assigned in the Azure portal.

| Role | What it lets you do |
|---|---|
| **Logic App Contributor** | edit and manage Consumption logic apps; run playbooks; cannot grant access |
| **Logic App Operator** | read, enable, disable Consumption logic apps; cannot edit |
| **Logic Apps Standard Operator / Developer / Contributor** | Standard equivalents: enable/resubmit/disable · create/edit · manage everything |
| **Microsoft Sentinel Contributor** | attach a playbook to an analytics or automation rule |
| **Microsoft Sentinel Responder** | open the incident to run a playbook manually — ==!but cannot run the playbook itself== |
| **Microsoft Sentinel Playbook Operator** | run a playbook manually |
| **Microsoft Sentinel Automation Contributor** | given to ==@Sentinel's own service account== on the playbook's resource group, so automation rules can run playbooks; used for nothing else |
| **Owner** / **User Access Administrator** | grant Sentinel that Automation Contributor role |

Two rules follow. First, Sentinel runs incident-triggered playbooks with its own service account. That account needs **Microsoft Sentinel Automation Contributor** on the resource group that holds the playbook. Second, by default a playbook can be used only inside its own subscription unless you grant Sentinel permissions on the playbook's resource group.

**6. Run history is your debugger.** Each time a trigger fires, Logic Apps creates a **run**. Run history shows each run's status — Succeeded, Failed, Running, Waiting, Cancelled, Aborted, Timed out — and every step's inputs, outputs and errors. **Trigger history** separately shows each trigger check (Succeeded, Skipped, Failed). **Resubmit** reruns a finished run with the same inputs. When a playbook "did nothing", look here first.

## Where it lives

Playbooks are created from Sentinel, but they live and are edited in the **Azure portal** as Logic Apps.

- **Create a playbook:** Microsoft Defender portal (`security.microsoft.com`) or Azure portal **> Microsoft Sentinel > Configuration > Automation > Create > Logic App playbook**. Sentinel in the Azure portal is supported only until **March 31, 2027**; after that it is Defender portal only.
- **See playbooks:** same page, **Active playbooks** tab (columns **Status**, **Plan**, **Trigger kind**). Templates are on the **Playbook templates** tab and in **Content hub**.
- **Edit / run history:** select the playbook to open its Logic Apps page in the Azure portal.
- **API connections:** Azure portal, search *API connections*. They sit in the playbook's resource group. **Edit API connection** changes how one signs in.
- **Grant a playbook's managed identity access:** **Microsoft Sentinel > Settings > Workspace settings > Access control (IAM) > Add > Add role assignment**, assign access to **Logic App**.

![Screenshot showing the Logic App playbook creation menu in the Defender portal, including alert, case, blank, and legacy playbook options.](https://learn.microsoft.com/en-us/azure/sentinel/media/create-playbooks/sentinel-logic-app-playbook-light-mode.png){Defender portal: Automation > Create > Logic App playbook. Note "case trigger" and the (Legacy) entries.}

![Screenshot shows Azure portal and Microsoft Sentinel Automation page with Create selected.](https://learn.microsoft.com/en-us/azure/sentinel/media/create-playbooks/add-new-playbook.png){The same menu in the Azure portal. Here the choices are incident, alert, entity trigger, or Blank playbook (Standard).}

![Screenshot shows Create playbook wizard and Basics tab for a Consumption workflow-based playbook.](https://learn.microsoft.com/en-us/azure/sentinel/media/create-playbooks/create-playbook-basics-consumption.png){Consumption wizard, Basics tab. Region follows the Log Analytics workspace. You can send the playbook's diagnostics logs to a workspace.}

![Screenshot shows Consumption workflow designer with selected trigger.](https://learn.microsoft.com/en-us/azure/sentinel/media/create-playbooks/designer-consumption.png){After creation the Consumption designer opens with the chosen Sentinel trigger already in place}

![Screenshot shows Consumption workflow playbook with entity trigger, and available entity types to select for setting the playbook schema.](https://learn.microsoft.com/en-us/azure/sentinel/media/create-playbooks/entity-trigger-types.png){Entity trigger: choose which entity type (account, host, IP, URL…) the playbook receives}

![Screenshot shows hosting options page for creating a logic app.](https://learn.microsoft.com/en-us/azure/sentinel/media/create-playbooks/logic-apps-hosting-options.png){Standard path: "Blank playbook" opens Create Logic App with Standard – Workflow Service Plan selected}

![Screenshot shows Create Logic App wizard and Basics tab for a Standard logic app.](https://learn.microsoft.com/en-us/azure/sentinel/media/create-playbooks/create-logic-app-basics-standard.png){Standard Basics tab: you pick a region, a Windows plan and a pricing plan yourself. After this you still have to add a Stateful workflow.}

![Screenshot shows designer in Standard logic app workflow.](https://learn.microsoft.com/en-us/azure/sentinel/media/create-playbooks/designer-standard.png){Standard designer starts empty: Add a trigger}

![Screenshot shows how to select a trigger for your playbook.](https://learn.microsoft.com/en-us/azure/sentinel/media/create-playbooks/sentinel-triggers.png){The three Microsoft Sentinel triggers: entity, alert, incident}

![Screenshot shows extra condition to add before the Incident ARM ID field.](https://learn.microsoft.com/en-us/azure/sentinel/media/create-playbooks/no-incident-id.png){An entity playbook run during hunting has no incident, so Incident ARM ID is null. Add a condition that checks it first.}

![Screenshot shows custom details defined in an analytics rule.](https://learn.microsoft.com/en-us/azure/sentinel/media/create-playbooks/custom-details-values.png){Custom details are defined on the analytics rule (key = new field, value = event column)}

![Screenshot shows selected Alert Custom Details in dynamic content list.](https://learn.microsoft.com/en-us/azure/sentinel/media/create-playbooks/custom-details-dynamic-field.png){Alert Custom Details picked from dynamic content. A For each loop is added because an incident holds many alerts.}

![Screenshot shows selection for Use sample payload to generate schema link.](https://learn.microsoft.com/en-us/azure/sentinel/media/create-playbooks/generate-schema-link.png){Parse JSON: Use sample payload to generate schema}

![Screenshot shows sample JSON payload.](https://learn.microsoft.com/en-us/azure/sentinel/media/create-playbooks/sample-payload.png){A sample custom-details payload}

![Screenshot shows ready to use dynamic fields from the schema.](https://learn.microsoft.com/en-us/azure/sentinel/media/create-playbooks/custom-fields-ready-to-use.png){The parsed custom fields now appear as dynamic content for later actions}

![Screenshot of the Microsoft Sentinel connector showing where to select Change connection to update authentication.](https://learn.microsoft.com/en-us/azure/sentinel/media/authenticate-playbooks-to-sentinel/change-connection.png){Any Sentinel step: Change connection to swap the identity it signs in with}

![Screenshot of Microsoft Sentinel connector authentication options with Connect with managed identity selected.](https://learn.microsoft.com/en-us/azure/sentinel/media/authenticate-playbooks-to-sentinel/auth-methods-msi-choice.png){Connect with managed identity}

![Screenshot of the Microsoft Sentinel connector showing the connection name and system-assigned managed identity options.](https://learn.microsoft.com/en-us/azure/sentinel/media/authenticate-playbooks-to-sentinel/auth-methods-msi.png){Name the connection and choose System-assigned managed identity}

![Screenshot of Microsoft Sentinel connector authentication options with Connect with Service Principal selected as the authorization method.](https://learn.microsoft.com/en-us/azure/sentinel/media/authenticate-playbooks-to-sentinel/auth-methods-spn-choice.png){Connect with Service Principal}

![Screenshot of Microsoft Sentinel connector fields for service principal authentication, including tenant ID, client ID, and client secret.](https://learn.microsoft.com/en-us/azure/sentinel/media/authenticate-playbooks-to-sentinel/auth-methods-spn.png){Service principal needs tenant ID, client ID and client secret}

![Screenshot of the Sign in button selected.](https://learn.microsoft.com/en-us/azure/sentinel/media/authenticate-playbooks-to-sentinel/auth-methods-sign-in.png){Sign in = a Microsoft Entra user account. Least preferred.}

### Run history and trigger history

![Screenshot shows Consumption workflow and Overview page with selected tab named Runs history.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/run-history-consumption.png){Consumption: logic app Overview > Runs history}

![Screenshot shows a selected Consumption workflow run.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/select-run-consumption.png){Select one run to open it}

![Screenshot shows Consumption workflow run history with each action in the run.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/run-history-pane-consumption.png){Each step shows its own status}

![Screenshot shows run details for each step in the Consumption workflow.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/run-details-consumption.png){Run details lists every step as a table, including the Correlation Id}

![Screenshot shows Consumption workflow run history page with selected failed example step plus inputs, outputs, and errors for the failed step.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/inputs-outputs-errors-consumption.png){A failed step: inputs, outputs and the error. Here a broken email connection.}

![Screenshot shows Consumption workflow, and pane named Logic app run details. The pane shows the selected example failed step.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/select-failed-step-consumption.png){The same failed step reached from Run details}

![Screenshot shows Azure portal, Consumption workflow, and Overview page with selected tab named Trigger history.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/trigger-history-consumption.png){Consumption: Overview > Trigger history}

![Screenshot shows Overview page with Consumption workflow and multiple trigger attempts for different items.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/triggers-history-consumption.png){Each trigger attempt is listed; each successful fire starts its own run}

![Screenshot shows Consumption workflow trigger history and selected entry.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/select-trigger-event-consumption.png){Select one trigger attempt}

![Screenshot shows selected Consumption workflow trigger history information.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/trigger-details-consumption.png){Trigger attempt details}

![Screenshot shows Standard workflow, run history page, and selected tab named Run history.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/run-history-standard.png){Standard: open the workflow, then Tools > Run history. Stateful workflows only.}

![Screenshot shows selected Standard workflow run.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/select-run-standard.png){Select a Standard run}

![Screenshot shows Standard workflow and each action in the selected run.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/run-history-pane-standard.png){Per-step status in a Standard run}

![Screenshot shows Standard workflow with failed step inputs.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/failed-action-inputs-standard.png){Failed step inputs (Standard)}

![Screenshot shows Standard workflow with failed step outputs.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/failed-action-outputs-standard.png){Failed step outputs: the RSS feed was not found}

![Screenshot shows Azure portal, Standard workflow, and Overview page with selected tab named Trigger history.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/trigger-history-standard.png){Standard: Run history page > Trigger history tab}

![Screenshot shows Standard workflow and Run history page with tab named Trigger history, which shows multiple trigger attempts for different items.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/triggers-history-standard.png){Multiple trigger attempts (Standard)}

![Screenshot shows Standard workflow trigger entry selected.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/select-trigger-event-standard.png){Select a trigger attempt by its identifier}

![Screenshot shows Standard workflow trigger inputs.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/trigger-inputs-standard.png){Trigger inputs}

![Screenshot shows Standard workflow trigger outputs.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/trigger-outputs-standard.png){Trigger outputs: what the trigger passed to the next step}

![Screenshot shows Consumption logic app resource with alert condition.](https://learn.microsoft.com/en-us/azure/logic-apps/media/view-workflow-status-run-history/set-up-alert-condition.png){Optional: an Azure Monitor alert on the logic app, e.g. "Triggers Failed >= 1"}

## What the exam assumes you know

- ==+A Sentinel playbook is a Logic Apps workflow.== Not a script, not a KQL query, not an Azure Automation runbook.
- An **automation rule** is Sentinel's built-in, no-code rule that can *run* a playbook. They are not the same thing.
- ==!Microsoft Sentinel Responder cannot run a playbook.== It can only open the incident. **Microsoft Sentinel Playbook Operator** runs one manually.
- ==!Microsoft Sentinel Automation Contributor is not for people.== It goes to Sentinel's service account on the playbook's resource group.
- Running playbooks also needs **Logic App Contributor** on that resource group.
- Detail on triggers, automation rules and running playbooks is in D1.1.10 and D1.1.11.

## Skip list

- **Skip:** integration accounts and B2B messaging (EDI, AS2, X12, EDIFACT, RosettaNet). Business-to-business plumbing. Never on SC-200.
- **Skip:** AI agentic workflows, MCP servers and Microsoft Foundry tools in Logic Apps. New platform features, not playbook basics.
- **Skip:** running custom code (inline JavaScript, C#, PowerShell, Azure Functions, custom connectors). Know only that it is possible.
- **Skip:** ASEv3 and hybrid hosting, zone redundancy, Windows plan sizing and pricing tiers. Know "Standard = dedicated, can reach private networks"; the rest is architecture.
- **Skip:** the "compare automation services" table (Functions, Power Automate, Azure Automation runbooks). The exam does not ask you to choose between them for Sentinel — playbooks are Logic Apps.
- **Skip:** run statuses beyond Succeeded / Failed / Running, the rerun-from-action limits (40 actions, no parallel paths), and the run history retention setting. Know where run history is; that is enough.
- **Skip:** the Parse JSON / custom-details schema steps in the screenshots above. Know that custom details reach a playbook as dynamic content; the click path is lab material.
- **Skip:** Azure Monitor alerts on the logic app itself. Production hygiene, not tested.
- **Skip:** the status icon legend in the run history article. Pure furniture.
