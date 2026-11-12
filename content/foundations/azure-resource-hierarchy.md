+++
slug = "azure-resource-hierarchy"
title = "Azure resource hierarchy: tenant, management groups, subscriptions, resource groups, resources"
summary = "How Azure is organised as nested boxes — Entra tenant, management groups, subscriptions, resource groups, resources, regions — how to read a resource ID, where a Microsoft Sentinel workspace sits in that tree, and why access, policy and billing flow downward."
order = 3
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/6-describe-azure-management-infrastructure",
  "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview",
  "https://learn.microsoft.com/en-us/azure/governance/management-groups/overview",
  "https://learn.microsoft.com/en-us/azure/role-based-access-control/scope-overview",
  "https://learn.microsoft.com/en-us/entra/fundamentals/how-subscriptions-associated-directory",
  "https://learn.microsoft.com/en-us/azure/reliability/regions-overview",
  "https://learn.microsoft.com/en-us/azure/sentinel/quickstart-onboard",
  "https://learn.microsoft.com/en-us/azure/templates/microsoft.operationalinsights/workspaces",
]
captured = 2026-11-12
+++

## In one sentence

Everything in Azure lives inside nested boxes — **tenant > management groups > subscriptions > resource groups > resources** — and anything you set on a box (who may access it, what rules apply, who pays) flows down to everything inside it.

## Why it exists

Think of a company's filing system. There is the **company** itself. Inside are **departments**. Each department has **filing cabinets**. Each cabinet has **drawers**. Each drawer holds **files**. If you give someone the key to a cabinet, they can open every drawer in it. If head office says "no files leave the building", that rule covers every cabinet.

Azure works the same way, for the same reasons:

- **Access.** Give a person rights once, high up, instead of on 500 separate things.
- **Rules.** Apply a rule once ("only create servers in Europe") and it covers everything below.
- **Money.** Each subscription gets its own bill, so costs split cleanly.

For a SOC analyst this matters on day one. Microsoft Sentinel is not a standalone app. It sits **inside** a subscription and resource group, so your access to Sentinel depends on where you were given rights in this tree.

## Mental model

```svg
<svg viewBox="0 0 820 520" role="img" aria-label="Azure hierarchy tree from Entra tenant to tenant root group, management groups, subscriptions, resource groups and resources, with a Log Analytics workspace running Microsoft Sentinel inside a security resource group, and inheritance flowing downward">
  <defs>
    <marker id="arharrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="currentColor"/>
    </marker>
  </defs>
  <rect class="box-accent" x="20" y="15" width="620" height="44" rx="8"/>
  <text x="330" y="43" text-anchor="middle" class="label-accent">Microsoft Entra tenant (the organisation's identity directory)</text>
  <rect class="box" x="170" y="80" width="320" height="40" rx="8"/>
  <text x="330" y="105" text-anchor="middle">Tenant Root Group (root management group)</text>
  <rect class="box" x="60" y="145" width="220" height="40" rx="8"/>
  <text x="170" y="170" text-anchor="middle">Management group: Production</text>
  <rect class="box" x="380" y="145" width="220" height="40" rx="8"/>
  <text x="490" y="170" text-anchor="middle">Management group: Dev</text>
  <rect class="box" x="40" y="215" width="260" height="44" rx="8"/>
  <text x="170" y="236" text-anchor="middle">Subscription: Prod-Security</text>
  <text x="170" y="253" text-anchor="middle" class="muted">billing + access boundary</text>
  <rect class="box" x="380" y="215" width="220" height="44" rx="8"/>
  <text x="490" y="242" text-anchor="middle">Subscription: Dev-Sandbox</text>
  <rect class="box" x="20" y="290" width="300" height="44" rx="8"/>
  <text x="170" y="311" text-anchor="middle">Resource group: rg-soc</text>
  <text x="170" y="328" text-anchor="middle" class="muted">same lifecycle, one location for metadata</text>
  <rect class="box" x="380" y="290" width="220" height="44" rx="8"/>
  <text x="490" y="317" text-anchor="middle">Resource group: rg-test</text>
  <rect class="box-ok" x="20" y="365" width="300" height="70" rx="8"/>
  <text x="170" y="390" text-anchor="middle" class="label-accent">Resource: Log Analytics workspace</text>
  <text x="170" y="410" text-anchor="middle">+ Microsoft Sentinel enabled on it</text>
  <text x="170" y="428" text-anchor="middle" class="muted">region: e.g. West Europe</text>
  <rect class="box" x="380" y="365" width="100" height="44" rx="8"/>
  <text x="430" y="392" text-anchor="middle">VM</text>
  <rect class="box" x="500" y="365" width="100" height="44" rx="8"/>
  <text x="550" y="392" text-anchor="middle">Storage</text>
  <line class="line" x1="330" y1="59" x2="330" y2="80"/>
  <line class="line" x1="250" y1="120" x2="170" y2="145"/>
  <line class="line" x1="410" y1="120" x2="490" y2="145"/>
  <line class="line" x1="170" y1="185" x2="170" y2="215"/>
  <line class="line" x1="490" y1="185" x2="490" y2="215"/>
  <line class="line" x1="170" y1="259" x2="170" y2="290"/>
  <line class="line" x1="490" y1="259" x2="490" y2="290"/>
  <line class="line" x1="170" y1="334" x2="170" y2="365"/>
  <line class="line" x1="460" y1="334" x2="430" y2="365"/>
  <line class="line" x1="520" y1="334" x2="550" y2="365"/>
  <line class="line-accent" x1="700" y1="90" x2="700" y2="420" marker-end="url(#arharrow)"/>
  <text x="720" y="200" class="label-accent">inherits</text>
  <text x="720" y="220" class="label-accent">downward:</text>
  <text x="720" y="245">RBAC roles</text>
  <text x="720" y="265">Azure Policy</text>
  <text x="720" y="310" class="muted">tags do NOT</text>
  <text x="720" y="328" class="muted">inherit</text>
  <text x="330" y="475" text-anchor="middle" class="muted">A role at the subscription reaches the workspace. A role on rg-test does not.</text>
  <text x="330" y="500" text-anchor="middle" class="muted">Each subscription trusts exactly one tenant; a tenant can hold many subscriptions.</text>
</svg>
```

Read top to bottom. A setting made on a box applies to every box drawn beneath it — and to nothing beside it.

## What actually matters

**1. The five levels, defined.**

| Level | What it is | Key facts |
|---|---|---|
| **Microsoft Entra tenant** | Your organisation's identity directory (users, groups, apps). Also called the *directory*. | Every subscription trusts **exactly one** tenant to sign people in. One tenant can be trusted by many subscriptions. |
| **Management group** | A folder that holds subscriptions (and other management groups) | Nests up to **six levels** deep (not counting root or subscription). Up to **10,000** per directory. Each has one parent. |
| **Tenant Root Group** | The single top management group every tenant gets | Its ID equals the Entra tenant ID. Can't be moved or deleted. New subscriptions land here by default. |
| **Subscription** | The unit of **billing** and an **access-control boundary** | Each subscription gets its own invoice. Common split: one for production, one for development. |
| **Resource group** | A container for resources that share a lifecycle | Every resource is in **exactly one** resource group. Groups **can't be nested** or **renamed**. ==!Deleting a resource group deletes everything in it.== |
| **Resource** | One thing you create: a VM, a storage account, a Log Analytics workspace | Resource groups, subscriptions, management groups and tags are technically resources too. |

**2. Inheritance flows down, never up or sideways.** Microsoft states it plainly: "Lower levels inherit settings from higher levels." A **role** (Azure RBAC — role-based access control, the system that grants permissions) assigned on a subscription applies to every resource group and resource in it. An **Azure Policy** (a rule such as "only these regions") assigned on a management group applies to all subscriptions under it, and the subscription owner can't override it. ==!Tags are the exception==: a tag on a resource group is **not** inherited by its resources.

**3. Resource IDs are the address.** Every resource has a unique path called its **resource ID**. It spells out the hierarchy:

```
/subscriptions/{subscriptionId}
  /resourceGroups/{resourceGroupName}
    /providers/{providerName}/{resourceType}/{resourceName}
```

A real Sentinel workspace looks like `/subscriptions/0000…/resourceGroups/rg-soc/providers/Microsoft.OperationalInsights/workspaces/law-soc`. `{subscriptionId}` is a GUID (a long unique number). `{providerName}` is the **resource provider**, the Azure service that makes that kind of resource — for example `Microsoft.Compute` for VMs or `Microsoft.Storage` for storage. A management group's ID is different: `/providers/Microsoft.Management/managementGroups/{name}`. When a command asks for a `--scope`, it wants one of these strings.

**4. Regions.** A **region** is one or more datacenters in one metropolitan area, joined by a fast network. You choose a region when you create most resources, for example *West Europe*. Each region sits in a **geography**, which is a data-residency boundary. A resource group has a region too: it stores the *metadata* about its resources there. Its resources can live in other regions, but Microsoft recommends the same one. Azure has over 70 regions.

**5. Where Sentinel lives.** Sentinel is switched on **on top of a Log Analytics workspace** — a resource that stores log data in tables. So the chain is: tenant > subscription > resource group > workspace (with Sentinel). Three consequences you will meet in SC-200:

- Enabling Sentinel needs **Contributor** on the **subscription**. Using it needs **Microsoft Sentinel Contributor** or **Microsoft Sentinel Reader** on the **resource group** that holds the workspace.
- Data stays inside its workspace. You can run Sentinel on several workspaces, but each one's data is isolated.
- ==!Once Sentinel is on a workspace, you can't move that workspace to another resource group or subscription.== Plan the location first.

## Where it lives

- **Azure portal > Management groups** — the tree. **Azure portal > Subscriptions** and **Azure portal > Resource groups** — the lists.
- **Any resource > Properties** shows its **Resource ID**.
- **Switching tenant:** if your account belongs to more than one tenant, use the portal's directory switcher (screenshot below).
- **A workspace's resource type** is `Microsoft.OperationalInsights/workspaces`. You will see it inside workspace resource IDs.
- Command-line equivalents (`az account show`, `az group list`) are on the Azure portal and CLI basics page.

![Diagram that illustrates the four levels of scope in Azure: management groups, subscriptions, resource groups, and resources](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/media/overview/scope-levels.png){The four scope levels — settings applied at one level reach every level below}

![Diagram that shows the role of Resource Manager during Azure requests](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/media/overview/consistent-management-layer.png){Portal, CLI, PowerShell and REST all go through one front door: Azure Resource Manager}

![Diagram showing a management group hierarchy from Tenant Root Group down to resources](https://learn.microsoft.com/en-us/training/wwl-azure/describe-core-architectural-components-of-azure/media/management-group-hierarchy.png){The full tree, from Tenant Root Group to individual resources, with inheritance flowing down}

![Diagram showing three resource group rules](https://learn.microsoft.com/en-us/training/wwl-azure/describe-core-architectural-components-of-azure/media/resource-group-rules.png){Resource group rules: one group per resource, no nesting or renaming, delete the group and everything goes}

![Diagram showing two subscription boundary types: billing boundary and access control boundary](https://learn.microsoft.com/en-us/training/wwl-azure/describe-core-architectural-components-of-azure/media/subscription-boundaries.png){A subscription is both a billing boundary and an access boundary}

![Diagram of a sample management group hierarchy](https://learn.microsoft.com/en-us/azure/governance/media/mg-org.png){A realistic management group tree, several levels deep}

![Diagram of a subset of the sample management group hierarchy](https://learn.microsoft.com/en-us/azure/governance/media/mg-org-sub.png){A slice of that tree — moving a subscription between branches changes what it inherits}

![Screenshot of activity logs and operations related to a selected management group](https://learn.microsoft.com/en-us/azure/governance/management-groups/media/al-mg.png){Changes to management groups are recorded in the Activity log — a source a SOC can watch}

![Diagram of scope for a role assignment](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/scope-overview/rbac-scope-no-label.png){RBAC scope: a role assigned at one level covers everything beneath}

![Diagram of management group and subscription hierarchy](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/scope-overview/rbac-scope-management-groups.png){Management groups add scope levels above subscriptions}

![Screenshot of resource IDs for a storage account in Azure portal](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/scope-overview/scope-resource-id.png){Where to find a resource ID in the portal}

![Screenshot that shows the trust relationship between Azure subscriptions and Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/fundamentals/media/how-subscriptions-associated-directory/trust-relationship.png){Each subscription trusts one Entra tenant for sign-in}

![Screenshot that shows the Subscriptions page with Change directory](https://learn.microsoft.com/en-us/entra/fundamentals/media/how-subscriptions-associated-directory/change-directory-in-azure-subscriptions.png){A subscription can be moved to a different directory}

![Screenshot that shows the Change the directory page](https://learn.microsoft.com/en-us/entra/fundamentals/media/how-subscriptions-associated-directory/edit-directory-ui.png){Changing a subscription's directory}

![Screenshot that shows the Directory switcher page](https://learn.microsoft.com/en-us/entra/fundamentals/media/how-subscriptions-associated-directory/directory-switcher.png){Switching between tenants you belong to}

![Diagram that shows a geography with two Azure regions, each with three availability zones](https://learn.microsoft.com/en-us/azure/reliability/media/regions-overview/regions.svg){Regions inside a geography; availability zones inside a region}

Creating a Sentinel workspace shows the hierarchy in action — you pick subscription, resource group and region:

![Screenshot of searching for and selecting Microsoft Sentinel from the Azure portal](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/search-sentinel.png){Step 1: search for Microsoft Sentinel in the Azure portal}

![Screenshot of selecting Create to start creating a new Log Analytics workspace](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/log-analytics-workspace-create.png){Step 2: Create}

![Screenshot of selecting Create a new workspace](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/log-analytics-workspace-create-a-new-workspace.png){Step 3: create a new Log Analytics workspace}

![Screenshot of creating a Log Analytics workspace screen with Subscription and Resource group Create new selected](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/log-analytics-workspace-resource-group-create-new-with-name-both-selected.png){Step 4: choose subscription, create a resource group, name the workspace, pick a region}

![Screenshot of Microsoft Sentinel in the Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/defender-portal-initial-view.png){The same workspace, worked from the Defender portal}

![Screenshot of the content hub in the Defender portal with the solution for Azure Activity selected](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/content-hub-azure-activity-defender.png){Content hub, Defender portal — Microsoft reuses this image for the query step too}

![Screenshot of the content hub in the Azure portal with the solution for Azure Activity selected](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/content-hub-azure-activity.png){Content hub, Azure portal}

![Screenshot of data connector for Azure Activity with the status showing as connected](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/azure-activity-connected-status.png){The Azure Activity connector, which streams subscription-level changes into the workspace}

![Screenshot of the AzureActivity query in the Logs page of the Azure portal](https://learn.microsoft.com/en-us/azure/sentinel/media/quickstart-onboard/azure-activity-logs-query.png){Querying the AzureActivity table}

## What the exam assumes you know

- ==!Permissions do not flow up.== Owner of a resource group is not Owner of the subscription.
- ==+A role at a higher scope covers lower scopes.== To give a SOC team read access to Sentinel across many subscriptions, assign once at the management group.
- ==!A subscription is not a tenant.== The tenant is the identity directory. A subscription is a billing and access container that trusts one tenant.
- Resource groups can't be nested. Questions that suggest "a resource group inside a resource group" are wrong.
- Sentinel permissions are set on the **resource group of the workspace** (or higher).
- The Azure Activity connector is configured with an **Azure Policy assignment** scoped to a subscription — another example of scope in action.

## Skip list

- **Skip** management-group move permissions, custom-role assignable-scope errors and the full role-versus-action chart in the management groups article. That is Azure administration, not SOC work.
- **Skip** service groups, region pairs, sovereign clouds and logical-versus-physical availability-zone mapping. Know only "region" and "geography" here.
- **Skip** resource-group limits (800 instances of a resource type) and Microsoft Customer Agreement billing notes.
- **Skip** ARM template and Bicep authoring. Know only that a template is a JSON file describing resources — the CLI basics page covers it in one line.
- **Skip** extension-resource internals from the RBAC scope article. Know the resource ID format.
