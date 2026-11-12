+++
slug = "azure-policy-basics"
title = "Azure Policy basics"
summary = "What Azure Policy is (rules that resources must follow), its four objects — definition, initiative, assignment, remediation task — the effects, why deployIfNotExists needs a managed identity, and why Sentinel uses Policy to switch on log collection at scale."
order = 16
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/azure/governance/policy/overview",
  "https://learn.microsoft.com/en-us/azure/governance/policy/concepts/effect-basics",
  "https://learn.microsoft.com/en-us/azure/governance/policy/concepts/assignment-structure",
  "https://learn.microsoft.com/en-us/azure/governance/policy/how-to/remediate-resources",
  "https://learn.microsoft.com/en-us/azure/governance/policy/assign-policy-portal",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-policy",
  "https://learn.microsoft.com/en-us/azure/sentinel/connect-services-diagnostic-setting-based",
  "https://learn.microsoft.com/en-us/azure/sentinel/quickstart-onboard",
]
captured = 2026-11-12
+++

## In one sentence

**Azure Policy** is a rulebook for your Azure resources: you write (or pick) a rule like "every VM must send its logs to this workspace", attach it to a part of your Azure estate, and Azure then reports who breaks the rule, blocks new breakers, or fixes them for you.

## Why it exists

Think of a building code. An inspector does not care *who* built the extension. He cares whether it has a fire exit. Azure Policy is that inspector for cloud resources.

A company may have thousands of resources. Nobody can click into each one to check that logging is on. Policy checks every resource against the rule, automatically.

For a SOC analyst this matters for one practical reason: **getting logs into Microsoft Sentinel at scale**. Sentinel is the SIEM (the central log-search and alerting system — see `soc-fundamentals`). It can only detect what it receives. Many Sentinel data connectors (the setup pages that switch a log source on) do not configure each resource by hand. They create a **policy assignment** that says "every resource of this type in this subscription must stream its logs to the Sentinel workspace", and Policy does the work. The same trick installs the **Azure Monitor Agent** (AMA, the log-shipping program on each machine — see `azure-monitor-agent-and-dcr`) on every VM.

## Mental model

Four objects, in the order you meet them:

| Object | Everyday analogy | What it is |
|---|---|---|
| **Policy definition** | One rule in the building code | A JSON rule: an *if* condition plus **one** effect. Hundreds are built in. |
| **Initiative** (also called **policySet**) | A chapter of the code ("fire safety") | A bundle of definitions with one goal, assigned as one item. |
| **Assignment** | "This code applies to *this* street" | A definition or initiative attached to a scope. Children inherit it. |
| **Remediation task** | The contractor sent to fix old buildings | A job that brings *existing* non-compliant resources into line. |

```svg
<svg viewBox="0 0 760 330" role="img" aria-label="Azure Policy flow: a definition or initiative is assigned to a scope, resources are evaluated, the effect decides what happens, and a remediation task using the assignment's managed identity fixes existing resources">
  <defs>
    <marker id="apbarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <rect class="box" x="20" y="30" width="170" height="70" rx="8"/>
  <text x="105" y="60" text-anchor="middle">Policy definition</text>
  <text x="105" y="82" text-anchor="middle" class="muted">if + one effect</text>
  <rect class="box" x="20" y="120" width="170" height="70" rx="8"/>
  <text x="105" y="150" text-anchor="middle">Initiative</text>
  <text x="105" y="172" text-anchor="middle" class="muted">bundle of definitions</text>
  <rect class="box-accent" x="250" y="75" width="190" height="70" rx="8"/>
  <text x="345" y="105" text-anchor="middle" class="label-accent">Assignment</text>
  <text x="345" y="127" text-anchor="middle" class="muted">at MG / sub / RG / resource</text>
  <line class="line-accent" x1="190" y1="65" x2="248" y2="100" marker-end="url(#apbarrow)"/>
  <line class="line-accent" x1="190" y1="155" x2="248" y2="122" marker-end="url(#apbarrow)"/>
  <rect class="box" x="500" y="75" width="240" height="70" rx="8"/>
  <text x="620" y="105" text-anchor="middle">Evaluate resources</text>
  <text x="620" y="127" text-anchor="middle" class="muted">on create/update + every 24 h</text>
  <line class="line-accent" x1="440" y1="110" x2="498" y2="110" marker-end="url(#apbarrow)"/>
  <rect class="box-risk" x="420" y="210" width="150" height="80" rx="8"/>
  <text x="495" y="240" text-anchor="middle" class="label-risk">deny</text>
  <text x="495" y="262" text-anchor="middle" class="muted">block new breakers</text>
  <rect class="box" x="590" y="210" width="150" height="80" rx="8"/>
  <text x="665" y="240" text-anchor="middle">audit</text>
  <text x="665" y="262" text-anchor="middle" class="muted">just report</text>
  <rect class="box-ok" x="200" y="210" width="200" height="80" rx="8"/>
  <text x="300" y="238" text-anchor="middle">deployIfNotExists / modify</text>
  <text x="300" y="260" text-anchor="middle" class="muted">fix it, using the</text>
  <text x="300" y="278" text-anchor="middle" class="muted">assignment's managed identity</text>
  <line class="line" x1="620" y1="145" x2="495" y2="208" marker-end="url(#apbarrow)"/>
  <line class="line" x1="640" y1="145" x2="665" y2="208" marker-end="url(#apbarrow)"/>
  <line class="line" x1="600" y1="145" x2="320" y2="208" marker-end="url(#apbarrow)"/>
  <rect class="box-ok" x="20" y="225" width="160" height="50" rx="8"/>
  <text x="100" y="255" text-anchor="middle">Remediation task</text>
  <line class="line-accent" x1="200" y1="250" x2="182" y2="250" marker-end="url(#apbarrow)"/>
  <text x="100" y="305" text-anchor="middle" class="muted">fixes EXISTING resources</text>
</svg>
```

## What actually matters

**1. A definition has exactly one effect.** The effect is what happens when the rule's *if* matches. The full list is `addToNetworkGroup`, `append`, `audit`, `auditIfNotExists`, `deny`, `denyAction`, `deployIfNotExists`, `disabled`, `manual`, `modify`, `mutate`. For SC-200 you need five:

| Effect | What it does | SOC example |
|---|---|---|
| `audit` | Lets the resource in, marks it non-compliant | "Report VMs without managed disks" |
| `deny` | Blocks the create or update | "No resources outside approved regions" |
| `auditIfNotExists` | Reports when a *related* thing is missing | "Report storage accounts with no diagnostic setting" |
| `deployIfNotExists` | Deploys the missing related thing | ==@Create the diagnostic setting== that streams logs to Sentinel; install AMA |
| `modify` | Changes properties (often tags) on the resource | "Add a cost-centre tag" |

`disabled` switches the rule off without deleting it.

**2. Scope and inheritance.** You assign at a **management group** (a folder of subscriptions), a **subscription**, a **resource group**, or one **resource** (see `azure-resource-hierarchy`). Everything below inherits the assignment. You can **exclude** a sub-scope (the JSON calls it `notScopes`). Several assignments on one resource are each evaluated independently. The net result is "cumulative most restrictive": if any one denies, it is denied. A looser policy lower down does **not** override a deny above it.

**3. When evaluation happens.** On create or update of a resource, when a new assignment lands, when an assigned definition changes, and in a standard compliance cycle **once every 24 hours**. A new assignment takes a few minutes before compliance results show.

**4. Remediation and the managed identity.** `deny` and `audit` only act on requests as they arrive. To fix resources that **already exist** you run a **remediation task**. It works only for `deployIfNotExists` and `modify`. The task needs something to log in as. That is a **managed identity** — an identity Azure creates for a service so it can authenticate without a password (see `entra-id-basics`). Each assignment has **one** managed identity: system-assigned (created for you) or user-assigned (one you made earlier). In the portal, Policy grants that identity the roles the definition lists (`roleDefinitionIds`) automatically. From PowerShell, CLI or an SDK, you must grant them yourself, or the remediation fails. One task remediates up to **50,000** resources (default 500).

**5. Enforcement mode.** Every assignment has `enforcementMode`. **Default** (portal: *Policy enforcement = Enabled*) enforces the effect. **DoNotEnforce** (portal: *Disabled*) evaluates and reports but does not block, and writes no Activity log entry — use it to test. Remediation tasks can still run under DoNotEnforce.

**6. Policy is not RBAC.** This is the classic confusion.

| | Azure RBAC | Azure Policy |
|---|---|---|
| Question it answers | ==@Who== may do this action? | ==@What state== must the resource be in? |
| Cares who made the change? | Yes — that is the point | No (except the newer `requestContext().identity` rules) |
| Typical outcome | Request refused: no permission | Request refused: rule broken, or resource reported/fixed |
| Example | Analyst can read the workspace but not delete it | Every VM must send logs to the workspace |

Even an **Owner** is blocked by a `deny` policy.

**Who can manage Policy:** **Resource Policy Contributor** covers most Policy operations. **Owner** has full rights. **Contributor** and **Reader** can read all Policy objects; Contributor can trigger remediation but ==!cannot create or update definitions or assignments==. **User Access Administrator** (or Owner) is needed to grant the managed identity its roles. Sentinel's policy-managed connectors ask for ==@Owner on the assignment scope==.

**Hybrid reach:** with **Azure Arc** (see `azure-arc-and-hybrid-machines`), the same Policy assignments can govern machines on-premises or in other clouds — that is how AMA gets pushed to them too.

## Where it lives

**Azure portal** only (not the Defender portal). Search **Policy** at the top of the portal, or **All services > Policy**. Left menu:

- **Policy > Definitions** — browse built-in definitions and initiatives; filter by category (e.g. *Monitoring*).
- **Policy > Assignments > Assign policy** (or **Assign initiative**) — the wizard: **Basics** (Scope, Exclusions, Policy definition, Policy enforcement) → **Parameters** → **Remediation** (managed identity, *Create a remediation task*) → **Non-compliance messages** → **Review + create**.
- **Policy > Compliance** — the compliance dashboard: per assignment, how many resources are compliant vs non-compliant. Drill in for per-resource detail.
- **Policy > Remediation** — tabs **Policies to remediate** and **Remediation tasks** (progress, per-resource errors).

From Sentinel: **Microsoft Sentinel > Configuration > Data connectors > (connector) > Open connector page > Launch Azure Policy Assignment wizard**. On **Parameters**, choose the Sentinel workspace; on **Remediation**, tick **Create a remediation task** so existing resources are covered, not just new ones.

Command line:

```bash
az policy assignment create --name <name> --policy <definition> --scope <scope> --mi-system-assigned --location <region>
az policy remediation create --name myRemediation --policy-assignment <assignmentId>
```

```powershell
New-AzPolicyAssignment -Name <name> -Scope <scope> -PolicyDefinition $def -Location 'westus' -IdentityType 'SystemAssigned'
Start-AzPolicyRemediation -Name 'myRemediation' -PolicyAssignmentId <assignmentId>
```

### Screenshots — assigning a policy and reading compliance

![Searching for Policy in the Azure portal](https://learn.microsoft.com/en-us/azure/governance/policy/media/assign-policy-portal/search-policy.png){Step 1 — search "policy" in the portal search bar}

![The Assignments pane with Assign policy highlighted](https://learn.microsoft.com/en-us/azure/governance/policy/media/assign-policy-portal/select-assignments.png){Policy > Assignments — where every assignment is created}

![Choosing a policy definition from Available Definitions, with its version column](https://learn.microsoft.com/en-us/azure/governance/policy/media/assign-policy-portal/select-available-definition.png){Basics tab — pick the scope, then the definition. The Version column is a preview feature; ignore it for the exam}

![Policy definition version options](https://learn.microsoft.com/en-us/azure/governance/policy/media/assign-policy-portal/select-version.png){Version options (preview) — enrol in minor or preview versions. Not exam material}

![Policy Compliance page with a non-compliant assignment](https://learn.microsoft.com/en-us/azure/governance/policy/media/assign-policy-portal/policy-compliance.png){Policy > Compliance — the dashboard showing which assignments have non-compliant resources}

![Deleting a policy assignment from Compliance](https://learn.microsoft.com/en-us/azure/governance/policy/media/assign-policy-portal/delete-assignment.png){Clean-up — delete an assignment from Compliance (or Assignments) via the ellipsis menu}

### Screenshots — remediation and the managed identity

![Remediation tab creating a system-assigned managed identity with Log Analytics Contributor](https://learn.microsoft.com/en-us/azure/governance/policy/media/remediate-resources/remediation-tab.png){Remediation tab — a system-assigned managed identity gets the role the definition needs (here Log Analytics Contributor) automatically when you use the portal}

![Searching for Policy in All services](https://learn.microsoft.com/en-us/azure/governance/policy/media/remediate-resources/search-policy.png){Another route in: All services > search Policy}

![The Remediation node on the Policy page](https://learn.microsoft.com/en-us/azure/governance/policy/media/remediate-resources/select-remediation.png){Policy > Remediation — lists every deployIfNotExists and modify assignment that can be remediated}

![Grid of resources to remediate](https://learn.microsoft.com/en-us/azure/governance/policy/media/remediate-resources/select-resources.png){New remediation task — narrow by scope and location, then Remediate}

![Remediation tasks tab showing progress](https://learn.microsoft.com/en-us/azure/governance/policy/media/remediate-resources/task-progress.png){Remediation tasks tab — progress of running and finished tasks}

![Context menu for a resource in a remediation task](https://learn.microsoft.com/en-us/azure/governance/policy/media/remediate-resources/resource-task-context-menu.png){Per-resource menu — open the deployment or Related events to read the error when a fix fails}

### Screenshots — Policy deploying the Azure Monitor Agent

Built-in initiatives such as *Deploy the Azure Monitor Agent for Windows client machines by using user-assigned managed identity-based auth and associate it with a DCR* install AMA and link each machine to a **data collection rule** (DCR — the instruction sheet saying which logs to collect). VMs use a user-assigned identity; Arc-enabled servers use system-assigned, the only supported option there.

![A built-in Azure Policy definition for configuring the Azure Monitor Agent](https://learn.microsoft.com/en-us/azure/azure-monitor/agents/media/azure-monitor-agent-install/built-in-ama-dcr-policy.png){Single built-in definitions — use one if you only want one action, such as installing the agent}

![A built-in initiative listing its policies for the Azure Monitor Agent](https://learn.microsoft.com/en-us/azure/azure-monitor/agents/media/azure-monitor-agent-install/built-in-ama-dcr-initiatives.png){An initiative bundles the steps: identity, install agent, associate DCR}

![Initiative remediation for the Azure Monitor Agent](https://learn.microsoft.com/en-us/azure/azure-monitor/agents/media/azure-monitor-agent-install/built-in-ama-dcr-remediation.png){Remediation for an initiative — pick which policy inside it to remediate; existing VMs get the agent}

### Screenshots — Sentinel's Azure Activity connector (the Sentinel quickstart)

Two Learn articles disagree here. The Sentinel quickstart tells you to press **Launch Azure Policy Assignment Wizard** on the **Azure Activity** connector. The diagnostic-settings connector article says Azure Activity "now uses the diagnostic settings pipeline" and points to the standalone (non-Policy) path. ==!Trust what the connector page in your portal shows.== Both routes end with the same thing: a diagnostic setting sending the Activity log (the subscription's record of who changed what — see `diagnostic-settings-and-activity-log`) to the workspace's `AzureActivity` table. Policy-managed connectors show **connected** only if data arrived in the **past 14 days**.

![Searching for Microsoft Sentinel in the Azure portal](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/search-sentinel.png){Quickstart — find Microsoft Sentinel in the Azure portal}

![Selecting Create a new workspace](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/log-analytics-workspace-create-a-new-workspace.png){Sentinel lives on a Log Analytics workspace — create one first (see log-analytics-workspace)}

![Selecting Create to create a new Log Analytics workspace](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/log-analytics-workspace-create.png){Create the workspace}

![Create Log Analytics workspace screen with new resource group](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/log-analytics-workspace-resource-group-create-new-with-name-both-selected.png){Workspace basics — subscription, resource group, name, region}

![Microsoft Sentinel in the Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/defender-portal-initial-view.png){Sentinel as seen in the Defender portal}

![Content hub in the Azure portal with the Azure Activity solution selected](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/content-hub-azure-activity.png){Content hub — install the Azure Activity solution, which brings the connector}

![Content hub in the Defender portal with the Azure Activity solution selected](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/content-hub-azure-activity-defender.png){The same image file appears twice in the quickstart, captioned once as the Defender content hub and once as the AzureActivity query in Defender — shown once here}

![Azure Activity data connector showing Connected](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/azure-activity-connected-status.png){After the policy (or diagnostic setting) is in place and data flows, the connector shows Connected}

![AzureActivity query in the Azure portal Logs page](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/azure-activity-logs-query.png){Proof it works — query the AzureActivity table}

## What the exam assumes you know

- ==+deployIfNotExists== (and `modify`) are the effects that **change** things; ==!audit and deny never fix anything==.
- A new assignment only covers **new** resources unless you also run a **remediation task** — the "Create a remediation task" box in Sentinel's wizard is the usual answer to "existing resources aren't sending logs".
- Remediation needs the assignment's **managed identity** with the right role. Missing role = failed deployment.
- Policy ≠ RBAC. "Who can" → RBAC. "Every resource must" → Policy.
- An initiative is a bundle; CLI/PowerShell call it a **policySet**.
- Assigned at a management group, Policy still only evaluates resources in subscriptions and resource groups underneath.

## Skip list

- **Skip writing policy JSON** (aliases, functions, `if`/`then` operators, Resource Provider modes). SC-200 uses built-in definitions that Sentinel and Azure Monitor pick for you.
- **Skip** `append`, `denyAction`, `manual`, `mutate`, `addToNetworkGroup`. Name-only; they belong to governance, AKS and network-manager scenarios, not SOC log collection.
- **Skip** the effect evaluation order (disabled → append/modify → deny → audit …) beyond "deny is checked before audit".
- **Skip** initiative parameter options, definition **versions (preview)**, overrides, resource selectors, **Enroll** mode and the special Azure Virtual Network Manager permissions. Not tested here.
- **Skip** **exemptions** detail. Know only that a resource can be exempted from an assignment (up to 1,000 exemptions per scope).
- **Skip** the object-count limits table (500 definitions, 200 assignments per scope) — trivia.
- **Skip** remediation tuning flags (`-FailureThreshold`, `-ParallelDeploymentCount` 1–30, default 10). Remember the 50,000 resource ceiling only.
- **Skip** Policy-as-code workflows. Engineering practice, not analyst work.
