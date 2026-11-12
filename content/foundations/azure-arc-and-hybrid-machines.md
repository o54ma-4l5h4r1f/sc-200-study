+++
slug = "azure-arc-and-hybrid-machines"
title = "Azure Arc and hybrid machines"
summary = "How a server that lives outside Azure (on-premises or in another cloud) gets an Azure identity through Azure Arc, so the Azure Monitor Agent, data collection rules, Defender for Cloud and Microsoft Sentinel can treat it like an Azure VM."
order = 17
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/azure/azure-arc/servers/overview",
  "https://learn.microsoft.com/en-us/azure/azure-arc/servers/agent-overview",
  "https://learn.microsoft.com/en-us/azure/azure-arc/servers/learn/quick-enable-hybrid-vm",
  "https://learn.microsoft.com/en-us/azure/azure-arc/servers/prerequisites",
  "https://learn.microsoft.com/en-us/azure/azure-arc/servers/security-identity-authorization",
  "https://learn.microsoft.com/en-us/azure/azure-arc/servers/managed-identity-authentication",
  "https://learn.microsoft.com/en-us/azure/azure-arc/servers/scenario-onboard-azure-sentinel",
  "https://learn.microsoft.com/en-us/azure/defender-for-cloud/quickstart-onboard-machines",
  "https://learn.microsoft.com/en-us/azure/sentinel/connect-services-windows-based",
]
captured = 2026-11-12
related_objectives = ["D1.3.1", "D1.3.2", "D1.3.3"]
+++

## In one sentence

**Azure Arc-enabled servers** gives a machine that runs *outside* Azure — a physical server in your office, a VM in your own datacenter, or a VM in AWS or Google Cloud — a record and an identity *inside* Azure, so Azure tools can manage it as if it were an Azure virtual machine.

## Why it exists

Azure tools only know how to talk to Azure *resources*. A resource is anything Azure tracks with a Resource ID (a unique address like a postal address) and keeps in a resource group (a folder of related resources). An Azure VM is born as a resource. Your on-premises file server is not.

That matters to a SOC (security operations centre) because most companies are **hybrid**: some servers in Azure, many still on-premises or in other clouds. The **Azure Monitor Agent (AMA)** — the program that ships logs to a Log Analytics workspace — is configured by **data collection rules (DCRs)**, and a DCR is attached to a *resource*. No resource, no DCR, no logs in Microsoft Sentinel.

Think of a visitor badge. A contractor who walks into your building is unknown to the access-control system. Reception issues a badge with their name and photo. Now the doors, cameras and sign-in log all recognise them. Azure Arc is the reception desk. The **Azure Connected Machine agent** is the badge printer.

## Mental model

```svg
<svg viewBox="0 0 760 330" role="img" aria-label="An on-premises server gets an Azure identity through the Connected Machine agent, then the Azure Monitor Agent and a data collection rule send its logs to a Log Analytics workspace read by Microsoft Sentinel and Defender for Cloud">
  <defs>
    <marker id="aahm-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <line x1="250" y1="20" x2="250" y2="310" class="divider"/>
  <text x="125" y="30" text-anchor="middle" class="muted">Outside Azure</text>
  <text x="505" y="30" text-anchor="middle" class="muted">Inside Azure</text>
  <rect class="box" x="20" y="50" width="210" height="250" rx="8"/>
  <text x="125" y="75" text-anchor="middle">On-prem / AWS / GCP server</text>
  <rect class="box-accent" x="35" y="95" width="180" height="70" rx="6"/>
  <text x="125" y="120" text-anchor="middle" class="label-accent">Connected Machine</text>
  <text x="125" y="140" text-anchor="middle" class="label-accent">agent (azcmagent)</text>
  <text x="125" y="157" text-anchor="middle" class="muted">heartbeat every 5 min</text>
  <rect class="box-ok" x="35" y="190" width="180" height="60" rx="6"/>
  <text x="125" y="215" text-anchor="middle">Azure Monitor Agent</text>
  <text x="125" y="236" text-anchor="middle" class="muted">installed as an extension</text>
  <text x="125" y="285" text-anchor="middle" class="muted">Windows / Linux logs</text>
  <rect class="box-accent" x="280" y="60" width="210" height="90" rx="8"/>
  <text x="385" y="85" text-anchor="middle" class="label-accent">Arc machine resource</text>
  <text x="385" y="107" text-anchor="middle">Resource ID + resource group</text>
  <text x="385" y="129" text-anchor="middle" class="muted">system-assigned managed identity</text>
  <rect class="box" x="280" y="190" width="210" height="60" rx="8"/>
  <text x="385" y="215" text-anchor="middle">Data collection rule</text>
  <text x="385" y="236" text-anchor="middle" class="muted">what to collect, where to send</text>
  <rect class="box" x="530" y="190" width="210" height="60" rx="8"/>
  <text x="635" y="215" text-anchor="middle">Log Analytics workspace</text>
  <text x="635" y="236" text-anchor="middle" class="muted">SecurityEvent, Syslog…</text>
  <rect class="box-ok" x="530" y="270" width="100" height="45" rx="8"/>
  <text x="580" y="297" text-anchor="middle">Sentinel</text>
  <rect class="box-ok" x="530" y="60" width="210" height="90" rx="8"/>
  <text x="635" y="90" text-anchor="middle">Defender for Cloud</text>
  <text x="635" y="112" text-anchor="middle" class="muted">Defender for Servers plan,</text>
  <text x="635" y="131" text-anchor="middle" class="muted">Defender for Endpoint</text>
  <line x1="215" y1="125" x2="278" y2="105" class="line-accent" marker-end="url(#aahm-arrow)"/>
  <line x1="385" y1="150" x2="385" y2="188" class="line-accent" marker-end="url(#aahm-arrow)"/>
  <line x1="215" y1="220" x2="278" y2="220" class="line-accent" marker-end="url(#aahm-arrow)"/>
  <line x1="490" y1="220" x2="528" y2="220" class="line-accent" marker-end="url(#aahm-arrow)"/>
  <line x1="580" y1="250" x2="580" y2="268" class="line-accent" marker-end="url(#aahm-arrow)"/>
  <line x1="490" y1="105" x2="528" y2="105" class="line-accent" marker-end="url(#aahm-arrow)"/>
</svg>
```

Step 1: the Connected Machine agent registers the server and Azure creates a resource for it. Step 2: you install AMA as an *extension* (an add-on Azure pushes to the machine) and attach a DCR. Step 3: logs flow to the workspace for Sentinel. Defender for Cloud sees the same resource.

The agent itself is a bundle of a few services:

![Diagram of Azure Connected Machine agent architectural overview](https://learn.microsoft.com/en-us/azure/azure-arc/servers/media/agent-overview/connected-machine-agent.png){Inside the Connected Machine agent: HIMDS (identity and heartbeat), the machine configuration agent (policy), the extension manager (installs add-ons such as AMA) and the Arc Proxy}

## What actually matters

- **An Arc machine is a real Azure resource.** It has a Resource ID, sits in a resource group, takes tags, and shows up next to Azure VMs. Arc is ==!not for VMs already running in Azure== — Microsoft says it isn't designed or supported for that. Azure VMs are already resources.
- **The Connected Machine agent is not the log shipper.** It only gives the machine its Azure identity and manages extensions. ==@AMA is a separate agent== that you add afterwards. AMA replaces the old Log Analytics agent; it does *not* replace the Connected Machine agent. Arc does not collect logs.
- **Order matters for Sentinel.** For any machine that is not an Azure VM, ==+Azure Arc must be installed and enabled *before*== you enable an AMA-based Sentinel connector such as *Windows Security Events via AMA*. Otherwise the connector has nothing to attach a DCR to.
- **Every Arc machine gets a system-assigned managed identity.** A *managed identity* is an identity in Microsoft Entra ID (Microsoft's cloud directory) that Azure creates and rotates for you — no password to store. It shows up in Entra ID as an enterprise app with the same name as the server. Its certificate is valid for 90 days and the agent renews it when 45 or fewer days remain. Each one counts as one object against your directory quota.
- **Status tells you if it is still talking.** The agent sends a heartbeat every **5 minutes**. No heartbeat → status changes to **Disconnected** within 15–30 minutes. Disconnected for **45 days** → status may become **Expired**, and an expired machine must be disconnected and reconnected by an admin. For a SOC, a disconnected machine means a silent gap in logs.
- **Defender for Cloud uses the same door.** Defender for Cloud recommends onboarding on-premises machines through Arc. A connected machine in a subscription with the Defender for Servers plan appears in Defender for Cloud like any Azure resource. For AWS and GCP, Defender for Cloud's multicloud connectors can deploy the Arc agent for you.

```svg
<svg viewBox="0 0 700 150" role="img" aria-label="Arc machine status lifecycle: Connected, Disconnected after 15 to 30 minutes without heartbeat, Expired after 45 days disconnected, then manual reconnect">
  <defs>
    <marker id="aahm-arrow2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <rect class="box-ok" x="20" y="40" width="170" height="70" rx="8"/>
  <text x="105" y="70" text-anchor="middle">Connected</text>
  <text x="105" y="92" text-anchor="middle" class="muted">heartbeat every 5 min</text>
  <rect class="box" x="265" y="40" width="170" height="70" rx="8"/>
  <text x="350" y="70" text-anchor="middle">Disconnected</text>
  <text x="350" y="92" text-anchor="middle" class="muted">heartbeat resumes → back</text>
  <rect class="box-risk" x="510" y="40" width="170" height="70" rx="8"/>
  <text x="595" y="70" text-anchor="middle" class="label-risk">Expired</text>
  <text x="595" y="92" text-anchor="middle" class="muted">admin must reconnect</text>
  <line x1="190" y1="75" x2="263" y2="75" class="line-accent" marker-end="url(#aahm-arrow2)"/>
  <line x1="435" y1="75" x2="508" y2="75" class="line-accent" marker-end="url(#aahm-arrow2)"/>
  <text x="227" y="30" text-anchor="middle" class="muted">no beat 15–30 min</text>
  <text x="472" y="30" text-anchor="middle" class="muted">45 days</text>
</svg>
```

**Windows Event Forwarding (WEF), in one paragraph.** Some companies don't put an agent on every server. Instead they use *Windows Event Forwarding*, a feature built into Windows: many servers push their event logs to one central **Windows Event Collector (WEC)** server, like branch offices posting their mail to head office. You then install AMA on that one collector (which, if it is not an Azure VM, must itself be Arc-enabled) and use Sentinel's **Windows Forwarded Events** connector. Watch the table name: forwarded events land in ==@WindowsEvent==, ==!not SecurityEvent==, even when they came from the Security log. Many built-in Sentinel rules query `SecurityEvent`, so they won't fire on forwarded data unless you adapt them. Full detail is in D1.3.3.

## Where it lives

**Portal:** Azure portal (`portal.azure.com`) — not the Defender portal.

| Task | Path |
|---|---|
| See all Arc machines and their status | `Azure portal > Azure Arc > Machines` |
| Generate an onboarding script | `Azure portal > Azure Arc > Machines > Onboard/Create > Onboard existing machines` |
| Check who can manage a machine | the machine's `Access control (IAM)` page |
| See Arc machines in Defender for Cloud | `Azure portal > Microsoft Defender for Cloud > Inventory` |

The onboarding wizard asks for subscription, resource group, **Region** (where the machine's metadata is stored), operating system, connectivity method (public endpoint, private endpoint, or proxy) and authentication method. It then gives you a script to download. On Windows you run `./OnboardingScript.ps1` in an elevated 64-bit PowerShell; on Linux you run `bash ~/Install_linux_azcmagent.sh`. You need local Administrator (Windows) or root (Linux) on the machine.

![Screenshot showing a successful machine connection in the Azure portal](https://learn.microsoft.com/en-us/azure/azure-arc/servers/learn/media/quick-enable-hybrid-vm/enabled-machine.png){After the script runs, the server appears under Azure Arc > Machines with status Connected}

On the machine, the agent is driven by the `azcmagent` command line. Commands you will see named in docs: `azcmagent connect`, `azcmagent disconnect`, `azcmagent config list`.

**Azure roles** (Azure RBAC — who may do what to Azure resources):

| Role | What it allows |
|---|---|
| **Azure Connected Machine Onboarding** | Read and create Arc machines. Cannot delete them or manage extensions. Meant for the account or service principal that onboards machines. |
| **Azure Connected Machine Resource Administrator** | Read, modify, re-onboard and delete Arc machines, and deploy extensions (such as AMA). |
| Contributor | Also enough to onboard. Anyone with Contributor on an Arc machine can push extensions that run as admin, so treat them as an indirect server admin. |

![Screenshot of the Azure portal showing Azure Arc-enabled server access control](https://learn.microsoft.com/en-us/azure/azure-arc/servers/media/security-identity-authorization/access-control-page.png){Access control (IAM) on an Arc machine — same RBAC page as any Azure resource}

**Machine-side plumbing** you may meet when troubleshooting. The core agent service runs as the low-privilege account `NT SERVICE\himds`, which needs the *Log on as a service* right. If Group Policy strips that right, the agent stops working.

![Local Group Policy Editor showing the Log on as a service user right](https://learn.microsoft.com/en-us/azure/azure-arc/servers/media/prerequisites/arc-server-user-rights-assignment.png){Computer Configuration > Windows Settings > Security Settings > Local Policies > User Rights Assignment > Log on as a service — NT SERVICE\himds must be allowed}

Apps on the machine can borrow the machine's managed identity by asking a local endpoint, `http://localhost:40342`, for a token. On Windows only local Administrators and the **Hybrid agent extension applications** group may do this; on Linux, the `himds` group.

![Bash output example of requesting a managed identity token on a Linux Arc machine](https://learn.microsoft.com/en-us/azure/azure-arc/servers/media/managed-identity-authentication/bash-token-output-example.png){Linux: an app on the Arc machine fetches an access token from the local identity endpoint}

![PowerShell output example of requesting a managed identity token on a Windows Arc machine](https://learn.microsoft.com/en-us/azure/azure-arc/servers/media/managed-identity-authentication/powershell-token-output-example.png){Windows: the same token request from PowerShell}

## What the exam assumes you know

- Non-Azure Windows or Linux machine + Sentinel AMA connector → ==+onboard to Azure Arc first==, then AMA, then the DCR. A distractor will offer "install the Log Analytics agent" — that legacy agent is the one AMA replaces.
- Azure VM → ==!no Arc needed==. Arc is only for machines outside Azure.
- Arc gives the machine an Azure **resource and managed identity**; AMA does the collecting; the DCR says what to collect.
- WEF/WEC data via the Windows Forwarded Events connector lands in `WindowsEvent`; the Windows Security Events via AMA connector writes `SecurityEvent`.
- Defender for Cloud covers on-premises servers through Arc (Defender for Servers plan).

## Skip list

- **Skip** the agent's folder paths, log file paths, CPU-limit tables and service process names. Useful for an admin fixing a broken install; never asked on SC-200.
- **Skip** the long instance-metadata list (BIOS UUID, SMBIOS tag, AWS/GCP fields). Just know Arc records basic facts about the machine.
- **Skip** the Arc Proxy, Arc gateway, private endpoints/Private Link Scope and proxy settings. These are networking choices for the onboarding team. Know only that the machine needs outbound internet (direct, proxy or private) to reach Azure.
- **Skip** the at-scale onboarding methods (service principals, Ansible, Group Policy, Configuration Manager). Know that "at scale" exists and uses the Onboarding role.
- **Skip** the other "supported cloud operations": Azure Update Manager, Azure Automation runbooks, change tracking, VM insights, machine configuration, machine enrollment. They are server-management features, not SOC features.
- **Skip** cloning guidance, disaster recovery and data residency. Operations detail.
- **Skip** using the managed identity from your own apps (Key Vault, tokens) beyond the idea that the machine has one. The screenshots above are there so you recognise it, not to learn it.
- **Skip** SQL Server auto-onboarding and the `Microsoft.AzureArcData` provider — out of scope for SC-200.
