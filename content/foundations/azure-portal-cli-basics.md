+++
slug = "azure-portal-cli-basics"
title = "Azure portal, Cloud Shell, Azure CLI and PowerShell basics"
summary = "How to find your way around the Azure portal, open Cloud Shell, sign in and pick a subscription with the Azure CLI (az) and Azure PowerShell (Az), what an ARM template is, and when a SOC analyst should be in the Defender portal instead."
order = 4
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/azure/azure-portal/azure-portal-overview",
  "https://learn.microsoft.com/en-us/azure/cloud-shell/overview",
  "https://learn.microsoft.com/en-us/azure/cloud-shell/get-started/classic",
  "https://learn.microsoft.com/en-us/cli/azure/manage-azure-subscriptions-azure-cli",
  "https://learn.microsoft.com/en-us/cli/azure/manage-azure-groups-azure-cli",
  "https://learn.microsoft.com/en-us/powershell/azure/get-started-azureps",
  "https://learn.microsoft.com/en-us/powershell/azure/manage-subscriptions-azureps",
  "https://learn.microsoft.com/en-us/powershell/azure/context-persistence",
  "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-powershell",
  "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview",
  "https://learn.microsoft.com/en-us/azure/sentinel/microsoft-sentinel-defender-portal",
  "https://learn.microsoft.com/en-us/defender-xdr/microsoft-365-defender",
]
captured = 2026-11-12
+++

## In one sentence

The **Azure portal** (`https://portal.azure.com`) is the website for creating and managing Azure resources by clicking; the **Azure CLI** (`az`) and **Azure PowerShell** (`Az` module) do the same jobs by typing; **Cloud Shell** is a ready-made terminal in your browser with both already installed and signed in.

## Why it exists

Think of a bank. You can go to the counter and fill in forms (the portal). You can use the bank's app and type commands (the CLI or PowerShell). Either way, the same back office processes the request.

In Azure that back office is **Azure Resource Manager (ARM)** — the single front door every request goes through. The portal, the CLI, PowerShell and the REST API (programs talking directly to Azure) all hit ARM. So permissions and results are the same whichever tool you use.

Why both? Clicking is easiest for one-off tasks and for learning. Typing is faster for repeating a task, scripting it, or doing it to 50 things at once. SC-200 is mostly portal work, but labs and some questions expect you to read a short command.

One more door matters for a SOC analyst: the **Microsoft Defender portal** (`https://security.microsoft.com`). It is *not* the Azure portal. It is where incidents, hunting and, increasingly, Microsoft Sentinel live.

## Mental model

```svg
<svg viewBox="0 0 800 380" role="img" aria-label="Four ways in to Azure Resource Manager — Azure portal, Azure CLI, Azure PowerShell, Cloud Shell — and the separate Microsoft Defender portal used for security operations">
  <defs>
    <marker id="apcarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="currentColor"/>
    </marker>
  </defs>
  <rect class="box-accent" x="20" y="30" width="170" height="60" rx="8"/>
  <text x="105" y="56" text-anchor="middle" class="label-accent">Azure portal</text>
  <text x="105" y="76" text-anchor="middle" class="muted">click (portal.azure.com)</text>
  <rect class="box" x="20" y="110" width="170" height="60" rx="8"/>
  <text x="105" y="136" text-anchor="middle">Azure CLI</text>
  <text x="105" y="156" text-anchor="middle" class="muted">az ... commands</text>
  <rect class="box" x="20" y="190" width="170" height="60" rx="8"/>
  <text x="105" y="216" text-anchor="middle">Azure PowerShell</text>
  <text x="105" y="236" text-anchor="middle" class="muted">Verb-AzNoun cmdlets</text>
  <rect class="box-ok" x="220" y="110" width="160" height="140" rx="8"/>
  <text x="300" y="140" text-anchor="middle" class="label-accent">Cloud Shell</text>
  <text x="300" y="165" text-anchor="middle">browser terminal,</text>
  <text x="300" y="185" text-anchor="middle">CLI + PowerShell</text>
  <text x="300" y="205" text-anchor="middle">preinstalled,</text>
  <text x="300" y="225" text-anchor="middle">already signed in</text>
  <rect class="box-accent" x="460" y="80" width="200" height="130" rx="10"/>
  <text x="560" y="110" text-anchor="middle" class="label-accent">Azure Resource</text>
  <text x="560" y="130" text-anchor="middle" class="label-accent">Manager (ARM)</text>
  <text x="560" y="158" text-anchor="middle">checks who you are</text>
  <text x="560" y="178" text-anchor="middle">and what you may do</text>
  <rect class="box" x="690" y="110" width="100" height="70" rx="8"/>
  <text x="740" y="140" text-anchor="middle">Resources</text>
  <text x="740" y="160" text-anchor="middle" class="muted">VMs, workspaces</text>
  <line class="line" x1="190" y1="60" x2="456" y2="105" marker-end="url(#apcarrow)"/>
  <line class="line" x1="380" y1="180" x2="456" y2="160" marker-end="url(#apcarrow)"/>
  <line class="line" x1="190" y1="140" x2="216" y2="150" marker-end="url(#apcarrow)"/>
  <line class="line" x1="190" y1="220" x2="216" y2="210" marker-end="url(#apcarrow)"/>
  <line class="line" x1="660" y1="145" x2="686" y2="145" marker-end="url(#apcarrow)"/>
  <line class="divider" x1="20" y1="280" x2="790" y2="280"/>
  <rect class="box-risk" x="20" y="300" width="770" height="64" rx="10"/>
  <text x="405" y="326" text-anchor="middle" class="label-risk">Microsoft Defender portal — security.microsoft.com — a different website</text>
  <text x="405" y="348" text-anchor="middle">incidents, alerts, advanced hunting, Defender XDR, Microsoft Sentinel menus</text>
</svg>
```

Above the dashed line: four ways to build and manage Azure resources, all through ARM. Below it: where security operations actually happen.

## What actually matters

**1. The Azure portal's parts.** Learn five names and you can follow any instruction:

| Part | What it does |
|---|---|
| **Global search** (top bar) | Find any service, resource or document by typing. Usually the fastest way anywhere. |
| **Portal menu** (top-left icon) | *Create a resource*, *Favorites*, *All services*. Flyout (hidden) or docked. |
| **Global controls** (top right) | Cloud Shell, Notifications, Settings, Support, Feedback |
| **Your account** (far top right) | Switch directory (tenant), sign out |
| **Service menu** (left side, inside a resource) | The commands for *that* resource. Microsoft also calls it the resource menu; many people say "blade". |
| **Breadcrumb** | The trail of links at the top to step back a level |

Instructions in this course look like `Azure portal > Microsoft Sentinel > Configuration > Data connectors`. That means: search **Microsoft Sentinel**, open it, then in the service menu open **Configuration > Data connectors**.

**2. Cloud Shell.** Click the Cloud Shell icon in the top bar, or go to `https://shell.azure.com`. Choose **Bash** or **PowerShell**. Both shells have the Azure CLI and Azure PowerShell. You are signed in automatically. Facts worth knowing: the session times out after **20 minutes** with no activity; your files persist in a **5 GB** file share; the shell itself is free, but that file share lives in a **storage account** you pay normal storage costs for. On first start you pick a subscription and let Cloud Shell create the storage account.

**3. Azure CLI basics.** Commands start with `az`. Most act on your *active subscription* unless you add `--subscription`.

```bash
az login                                   # sign in (opens a browser or gives a code)
az login --tenant <tenantId>               # sign in to a specific tenant
az account show --output table             # which subscription am I using?
az account list --output table             # which subscriptions can I see?
az account set --subscription "My Demos"   # switch subscription (name or ID)
az group list --output table               # list resource groups in it
```

`--output table` gives readable columns. Switching to a subscription in another tenant also switches your active tenant.

**4. Azure PowerShell basics.** The module is called **Az**. Cmdlets are `Verb-Noun` and every noun starts with `Az` (for example `Get-AzResourceGroup`).

```powershell
Connect-AzAccount                           # sign in
Get-AzSubscription                          # list subscriptions you can access
Set-AzContext -Subscription "My Demos"      # switch subscription
Get-AzResourceGroup                         # list resource groups in it
```

The *context* is PowerShell's word for "current tenant + subscription + account". Since **September 2025**, signing in to Azure PowerShell with an Entra ID user requires **multifactor authentication (MFA)**. In Cloud Shell you can skip `Connect-AzAccount` — you're already in.

| Task | Azure CLI | Azure PowerShell |
|---|---|---|
| Sign in | `az login` | `Connect-AzAccount` |
| Show current subscription | `az account show` | `Get-AzContext` |
| List subscriptions | `az account list` | `Get-AzSubscription` |
| Switch subscription | `az account set --subscription` | `Set-AzContext -Subscription` |
| List resource groups | `az group list` | `Get-AzResourceGroup` |

**5. ARM templates exist.** An **ARM template** is a JSON file that describes resources so ARM can create them the same way every time. **Bicep** is a friendlier language for the same job. You may meet one later as a way to deploy something in one click. You do not need to write one for SC-200.

**6. Defender portal versus Azure portal.** Use this rule:

| You want to... | Go to |
|---|---|
| Work incidents and alerts, hunt with KQL, respond on a device or user | **Defender portal** — `https://security.microsoft.com` |
| Use Microsoft Sentinel (connectors, analytics rules, automation, workbooks) | **Defender portal > Microsoft Sentinel** (the Azure portal works only until **31 March 2027**) |
| Create the Log Analytics workspace, a VM, a Logic App, a resource group; assign Azure roles | **Azure portal** |
| Manage Defender for Cloud | Azure portal today; moving into the Defender portal |

## Where it lives

- **Azure portal:** `https://portal.azure.com` — **Home**, **+ Create a resource**, **All services**, global search.
- **Cloud Shell:** the terminal icon in the Azure portal header, or `https://shell.azure.com`.
- **Defender portal:** `https://security.microsoft.com` — after onboarding, **Microsoft Sentinel** appears in its left navigation, and Sentinel's Azure-portal **Logs** page becomes **Investigation & response > Hunting > Advanced hunting**.

![Screenshot showing the full screen portal view and a key to UI elements](https://learn.microsoft.com/en-us/azure/azure-portal/media/azure-portal-overview/portal-callouts.png){The Azure portal, labelled: 1 portal menu, 2 breadcrumb, 3 header, 4 global search, 5 Copilot, 6 global controls (Cloud Shell lives here), 7 your account, 8 command bar, 9 service menu, 10 working pane}

![Screenshot showing the Azure portal menu](https://learn.microsoft.com/en-us/azure/azure-portal/media/azure-portal-overview/azure-portal-menu.png){The portal menu: Create a resource, Favorites, All services}

![Screenshot of the Azure portal menu in flyout mode](https://learn.microsoft.com/en-us/azure/azure-portal/media/azure-portal-overview/azure-portal-overview-portal-menu-flyout.png){Portal menu in flyout mode — hidden until you click the menu icon}

![Screenshot of the Azure portal menu in docked mode](https://learn.microsoft.com/en-us/azure/azure-portal/media/azure-portal-overview/azure-portal-overview-portal-menu-expandcollapse.png){Portal menu in docked mode — always visible}

![Screenshot showing the icon to toggle service menu items between collapsed and expanded](https://learn.microsoft.com/en-us/azure/azure-portal/media/azure-portal-overview/service-menu-toggle.png){The expand/collapse icon that opens or closes every group in a service menu at once}

![Screenshot showing the star icon to add a service menu command to favorites](https://learn.microsoft.com/en-us/azure/azure-portal/media/azure-portal-overview/service-menu-add-favorite.png){Star a service-menu command you use often}

![Screenshot of the Favorites folder in a service menu](https://learn.microsoft.com/en-us/azure/azure-portal/media/azure-portal-overview/service-menu-favorites.png){Starred commands appear in a Favorites folder at the top of the service menu}

![Screenshot showing the prompt to select the shell](https://learn.microsoft.com/en-us/azure/cloud-shell/get-started/media/new-storage/choose-shell.png){First Cloud Shell launch: choose Bash or PowerShell}

![Screenshot showing the select subscription and optional storage prompt](https://learn.microsoft.com/en-us/azure/cloud-shell/get-started/media/new-storage/getting-started.png){Pick the subscription Cloud Shell will use}

![Screenshot showing the create storage account prompt](https://learn.microsoft.com/en-us/azure/cloud-shell/get-started/media/new-storage/create-storage.png){Let Cloud Shell create the storage account for your 5 GB file share}

![Diagram that shows the role of Resource Manager during Azure requests](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/media/overview/consistent-management-layer.png){Portal, PowerShell, CLI, REST — every tool goes through Azure Resource Manager}

![Diagram that illustrates the four levels of scope in Azure](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/media/overview/scope-levels.png){What those tools act on: management group, subscription, resource group, resource}

![Screenshot of the Defender portal left navigation with the Microsoft Sentinel section](https://learn.microsoft.com/en-us/azure/sentinel/media/microsoft-sentinel-defender-portal/navigation-defender-portal.png){The other portal: Microsoft Sentinel inside the Defender portal's left navigation}

## What the exam assumes you know

- ==!The Azure portal and the Defender portal are different sites.== A question saying "in the Microsoft Defender portal" means `security.microsoft.com`.
- Portal paths in questions use the **service menu** names: *Settings*, *Configuration*, *Monitoring*. Expect to recognise them, not type them.
- `az ...` is the Azure CLI. `Connect-AzAccount`, `Get-Az...`, `Set-Az...` are Azure PowerShell. ==!Don't mix them up== — `az` and `Az` look alike but are different tools.
- A command that "can't find the resource" usually means the wrong active subscription. Check with `az account show` or `Get-AzContext`.
- ==+Cloud Shell needs no install and no separate sign-in.==

## Skip list

- **Skip** portal dashboards, themes, startup-page settings and the Quickstart Center. Nice to have, never tested.
- **Skip** Azure Copilot in the portal header. Not the same product as Microsoft Security Copilot, and not SC-200.
- **Skip** Cloud Shell's editor, VS Code integration, mobile app and encryption-at-rest notes.
- **Skip** CLI output formats beyond `--output table`, JMESPath `--query` syntax, subscription locks and creating management groups from the CLI.
- **Skip** PowerShell context persistence, Web Account Manager sign-in details, sovereign-cloud `-Environment` switches and telemetry opt-out.
- **Skip** writing ARM templates or Bicep. One sentence above is all SC-200 needs.
