+++
slug = "device-management-and-mde-onboarding"
title = "Device management and Defender for Endpoint onboarding"
summary = "What device management is (Intune, Group Policy, Configuration Manager), how a device gets onboarded to Defender for Endpoint and shows up in the device inventory, how tags differ from device groups, and which licences give you which Defender for Endpoint features."
order = 9
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/intune/fundamentals/what-is-intune",
  "https://learn.microsoft.com/en-us/intune/configmgr/comanage/overview",
  "https://learn.microsoft.com/en-us/intune/device-security/microsoft-defender/security-settings-management",
  "https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-endpoint",
  "https://learn.microsoft.com/en-us/defender-endpoint/onboarding",
  "https://learn.microsoft.com/en-us/defender-endpoint/onboard-client",
  "https://learn.microsoft.com/en-us/defender-endpoint/onboard-server",
  "https://learn.microsoft.com/en-us/defender-endpoint/configure-device-connectivity",
  "https://learn.microsoft.com/en-us/defender-endpoint/devices-overview",
  "https://learn.microsoft.com/en-us/defender-endpoint/machines-view-overview",
  "https://learn.microsoft.com/en-us/defender-endpoint/device-discovery",
  "https://learn.microsoft.com/en-us/defender-endpoint/machine-tags",
  "https://learn.microsoft.com/en-us/defender-xdr/configure-asset-rules",
  "https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-compatibility",
  "https://learn.microsoft.com/en-us/defender-endpoint/defender-antivirus-compatibility-without-mde",
  "https://learn.microsoft.com/en-us/office365/servicedescriptions/microsoft-365-service-descriptions/microsoft-365-tenantlevel-services-licensing-guidance/microsoft-defender-service-description",
  "https://learn.microsoft.com/en-us/defender-business/mdb-overview",
  "https://learn.microsoft.com/en-us/microsoft-365/education/guide/3-standard/security/standard-security-threat-protection",
  "https://learn.microsoft.com/en-us/azure/defender-for-cloud/plan-defender-for-servers-select-plan",
]
captured = 2026-11-12
related_objectives = ["D1.1.3", "D1.1.4", "D1.1.5", "D1.1.6", "D1.1.7", "D1.1.8", "D1.1.9"]
+++

## In one sentence

**Device management** tools (Intune, Group Policy, Configuration Manager) *push settings* to laptops and servers, while **Microsoft Defender for Endpoint (MDE)** *watches* those devices through a small sensor — a device is **onboarded** when that sensor reports to the Defender portal, and from then on you sort it with **tags** and **device groups**.

## Why it exists

A company with 5,000 laptops cannot walk to each one to switch on a firewall rule. It needs a remote control. That remote control is **device management**: one console that sends settings, apps and updates to every device.

Protecting those same laptops is a different job. Someone has to notice the malware, record what each process did, and let an analyst isolate the machine. That is **Defender for Endpoint**, Microsoft's **EDR** product (endpoint detection and response: a recorder plus an alarm on each device).

Think of a hotel. **Facilities management** sets the thermostat and changes the locks in every room — that is Intune or Group Policy. **CCTV and the guard desk** watch what happens in the rooms — that is Defender for Endpoint. The two work together, but they are not the same team.

An **endpoint** is any device a person or service uses: a laptop, desktop, server, phone or tablet.

## Mental model

```svg
<svg viewBox="0 0 780 380" role="img" aria-label="Two separate jobs: management tools push settings to a device; the Defender for Endpoint sensor on the device reports to the Defender portal, where the device appears in the inventory, gets tags, and lands in one device group">
  <defs>
    <marker id="dmmo-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <text x="110" y="24" text-anchor="middle" class="label-accent">PUSH settings</text>
  <rect class="box" x="15" y="36" width="190" height="44" rx="6"/>
  <text x="110" y="63" text-anchor="middle">Microsoft Intune (MDM)</text>
  <rect class="box" x="15" y="90" width="190" height="44" rx="6"/>
  <text x="110" y="117" text-anchor="middle">Group Policy (domain)</text>
  <rect class="box" x="15" y="144" width="190" height="44" rx="6"/>
  <text x="110" y="171" text-anchor="middle">Configuration Manager</text>
  <rect class="box" x="15" y="198" width="190" height="56" rx="6"/>
  <text x="110" y="221" text-anchor="middle">MDE security settings</text>
  <text x="110" y="241" text-anchor="middle" class="muted">management (no Intune)</text>
  <line x1="205" y1="58" x2="268" y2="140" class="line-accent" marker-end="url(#dmmo-arrow)"/>
  <line x1="205" y1="112" x2="268" y2="150" class="line-accent" marker-end="url(#dmmo-arrow)"/>
  <line x1="205" y1="166" x2="268" y2="160" class="line-accent" marker-end="url(#dmmo-arrow)"/>
  <line x1="205" y1="226" x2="268" y2="172" class="line-accent" marker-end="url(#dmmo-arrow)"/>
  <rect class="box-accent" x="270" y="90" width="190" height="130" rx="10"/>
  <text x="365" y="116" text-anchor="middle" class="label-accent">The device</text>
  <text x="365" y="142" text-anchor="middle">Defender Antivirus</text>
  <text x="365" y="164" text-anchor="middle">+ MDE sensor (Sense)</text>
  <text x="365" y="194" text-anchor="middle" class="muted">onboarding package</text>
  <text x="365" y="212" text-anchor="middle" class="muted">switches the sensor on</text>
  <line x1="460" y1="155" x2="518" y2="155" class="line-accent" marker-end="url(#dmmo-arrow)"/>
  <text x="489" y="143" text-anchor="middle" class="muted">reports</text>
  <rect class="box" x="520" y="20" width="245" height="340" rx="10"/>
  <text x="642" y="44" text-anchor="middle" class="label-accent">Defender portal</text>
  <text x="642" y="64" text-anchor="middle" class="muted">security.microsoft.com</text>
  <rect class="box-ok" x="535" y="78" width="215" height="56" rx="6"/>
  <text x="642" y="102" text-anchor="middle">Device inventory</text>
  <text x="642" y="122" text-anchor="middle" class="muted">Onboarded / discovered</text>
  <rect class="box" x="535" y="146" width="215" height="56" rx="6"/>
  <text x="642" y="170" text-anchor="middle">Tags (many per device)</text>
  <text x="642" y="190" text-anchor="middle" class="muted">manual or dynamic</text>
  <rect class="box" x="535" y="214" width="215" height="76" rx="6"/>
  <text x="642" y="238" text-anchor="middle">Device group (exactly one)</text>
  <text x="642" y="258" text-anchor="middle" class="muted">who may see it +</text>
  <text x="642" y="278" text-anchor="middle" class="muted">automation level</text>
  <line x1="642" y1="134" x2="642" y2="144" class="line-accent" marker-end="url(#dmmo-arrow)"/>
  <line x1="642" y1="202" x2="642" y2="212" class="line-accent" marker-end="url(#dmmo-arrow)"/>
  <text x="642" y="318" text-anchor="middle" class="muted">alerts · incidents · hunting</text>
  <text x="642" y="340" text-anchor="middle" class="muted">response actions</text>
</svg>
```

Left side: **who configures** the device. Right side: **who watches** it. The device sits in the middle. A device can be onboarded to MDE without being enrolled in Intune — that combination is common for servers.

## What actually matters

**1. The three ways to manage a Windows device.**

| Tool | What it is | Where it lives |
|---|---|---|
| ==@Microsoft Intune== | Cloud **MDM** (mobile device management) service. A device is **enrolled** in it, then Intune manages the whole device: settings, security, apps, wipe. Also does **MAM** (mobile application management — only the work apps, typical for personal phones). | Cloud. Intune admin center. |
| **Group Policy (GPO)** | The older Windows-domain way. Settings flow from Active Directory domain controllers to domain-joined PCs. | On-premises. |
| **Configuration Manager** (ConfigMgr, formerly SCCM) | On-premises management server for Windows clients and servers. **Co-management** lets ConfigMgr and Intune manage the same device, splitting the workloads. | On-premises. |

Intune does not store identities. It relies on **Microsoft Entra ID** for sign-in, for the **groups** you assign policies to, and for Conditional Access.

**2. Defender for Endpoint security settings management.** This lets Intune **endpoint security policies** (antivirus, ASR, firewall, EDR) reach a device that is onboarded to MDE but ==!not enrolled in Intune==. The MDE sensor fetches the policy itself. If the device has no Entra registration, MDE creates a **synthetic registration** so it can sit in an Entra **device** group. In the inventory such devices show **Managed by: MDE**. Policies target ==+device objects, not users==. Full detail: D1.1.6.

**3. Defender Antivirus is not Defender for Endpoint.**

- **Microsoft Defender Antivirus** is the antivirus built into Windows. It scans files.
- **Defender for Endpoint** is the cloud EDR service. Its **sensor** is the `Sense` service on Windows. It records behaviour and sends it to the Defender portal.
- Antivirus has three states. **Active mode**: it is the main antivirus. **Passive mode**: another vendor's antivirus is primary; Defender scans and reports but does not fix. **Disabled/uninstalled**.
- ==!Passive mode needs MDE.== It works only on onboarded devices (Plan 1, Plan 2 or Defender for Business). Many MDE features (ASR rules, network protection) need Defender Antivirus in **active** mode.

**4. Onboarding.** You download an **onboarding package** from the Defender portal and deploy it. That package switches on the sensor and ties the device to *your* tenant. Choices on the page:

- **Operating system** (Windows, Windows Server, macOS, Linux, iOS, Android).
- **Connectivity type**: **Streamlined** (core traffic goes to one domain, `*.endpoint.security.microsoft.com`; the default since 8 May 2024) or **Standard** (the older, longer URL list).
- **Deployment method** for Windows clients: **Local script** (==@up to 10 devices== — for testing), **Microsoft Intune / MDM**, **Microsoft Configuration Manager**, **Group Policy**, **VDI scripts**. Windows 7 SP1 and 8.1 use the old **Microsoft Monitoring Agent**.
- **Servers** can be onboarded **automatically** by **Defender for Servers** (in Defender for Cloud) for Azure VMs and Azure Arc machines — no script needed.

Prove it worked: the device appears in the inventory, alerts reach the dashboard, and a **detection test** raises an alert.

**5. Onboarded vs discovered devices.** The inventory holds two kinds of device.

| Kind | How it got there | Onboarding status |
|---|---|---|
| Onboarded | Sensor installed and reporting | ==@Onboarded== (sensor health usually **Active**) |
| Discovered | Seen on the network by onboarded devices — no sensor | **Can be onboarded**, **Unsupported**, or **Insufficient info** |

**Device discovery** runs on onboarded devices. **Standard discovery** (the default) actively probes unmanaged devices, at most about once every three weeks. **Basic discovery** only listens to traffic. Only networks MDE decides are **corporate** are scanned. Sensor health values to know: **Active**, **Inactive**, **Misconfigured**.

**6. Tags vs device groups — the distinction the exam leans on.**

| | Device tag | Device group |
|---|---|---|
| What | A label: `Finance`, `Internet-Facing`, `VIP` | A named slice of devices with **settings** attached |
| How many per device | **Many** | **Exactly one** — the highest-ranked group it matches |
| Controls access? | ==!No.== Everyone can see tags. | ==+Yes.== Assigned Entra user groups decide who sees and acts on those devices. |
| Sets automation level? | No | ==+Yes== — Full, Semi or No automated response |
| Typical use | Filter the inventory, scope hunting, feed group rules | RBAC scoping, remediation level, ASR policy targets |

Tags come in two kinds:

- **Manual tags** — typed onto a device in the portal (or set by registry, API, or Intune profile). Quick, but you maintain them by hand.
- **Dynamic tags** — applied by rules in ==@Asset rule management==. Conditions: device name, domain, OS platform, internet-facing status, onboarding status, existing manual tags. They update about **every hour** and cannot be edited by hand. ==!Custom data collection (D1.1.5) needs dynamic tags==; manual tags are not supported there.

Device groups usually match **on tags**. So: tag the device, the group rule picks it up, and the group carries the access and automation settings (D1.1.9).

**7. Licences — who gets what.**

| Licence | What it adds | Comes with |
|---|---|---|
| **MDE Plan 1** | Next-generation antivirus, **ASR rules**, device control, firewall, network protection, **manual** response actions, device groups | Standalone, or Microsoft 365 E3/A3/G3 |
| **MDE Plan 2** | Everything in P1 **plus EDR**, **automated investigation and remediation (AIR)**, **advanced hunting**, vulnerability management, threat analytics, six months of data retention | Standalone, Microsoft 365 E5/A5/G5, Windows E5 |
| **Defender for Business** | P1 plus some P2 features (EDR, AIR, attack disruption), simplified setup. For ==@up to 300 users== | Standalone, or Microsoft 365 Business Premium |
| **Defender for Servers Plan 1 / Plan 2** | Licenses servers. Plan 1 is the EDR from the MDE integration; Plan 2 adds server extras | Defender for Cloud (Azure subscription) |

==!Standalone MDE Plan 1 and Plan 2 do not include server licences.== Servers need Defender for Servers, MDE for Servers, or Defender for Business servers.

## Where it lives

| Task | Portal | Path |
|---|---|---|
| Download an onboarding package | Defender portal | **System** > **Settings** > **Endpoints** > **Device management** > **Onboarding** |
| See every device | Defender portal | **Assets** > **Devices** (`security.microsoft.com/machines`) |
| Add a manual tag | Defender portal | device page > **Manage tags** |
| Create a dynamic tag rule | Defender portal | **Settings** > **Microsoft Defender XDR** > **Asset Rule Management** > **Create a new rule** |
| Discovery mode | Defender portal | **System** > **Settings** > **Device discovery** > **Discovery mode** |
| Device groups | Defender portal | **System** > **Settings** > **Endpoints** > **Permissions** > **Device groups** |
| Turn on security settings management | Defender portal | **Settings** > **Endpoints** > **Configuration Management** > **Enforcement Scope** |
| Same switch, Intune side | Intune admin center | **Endpoint security** > **Microsoft Defender for Endpoint** > **Allow Microsoft Defender for Endpoint to enforce Endpoint Security Configurations** = **On** |

Check the antivirus mode on a Windows device:

```powershell
Get-MpComputerStatus | Select-Object AMRunningMode   # Normal = active, or Passive Mode
```

Registry tag (Windows, one tag only, syncs daily):

```text
HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Advanced Threat Protection\DeviceTagging\
  Group (REG_SZ) = Finance-Servers
```

### Device management — Intune and Configuration Manager

![Diagram showing Microsoft Intune managing identities, devices, and apps](https://learn.microsoft.com/en-us/intune/fundamentals/media/shared/intune-overview.png){Intune's three pillars: identities (Entra ID), devices and apps — with Defender signals feeding in}

![Diagram provides an overview of co-management](https://learn.microsoft.com/en-us/intune/configmgr/comanage/media/co-management-overview.svg){Co-management: Configuration Manager and Intune share one Windows device, split by workload}

![Co-management dashboard in Configuration Manager](https://learn.microsoft.com/en-us/intune/configmgr/comanage/media/co-management-dashboard.png){The Configuration Manager co-management dashboard — admin tooling, shown for completeness}

### Security settings management (MDE without Intune enrollment)

![Conceptual presentation of the Microsoft Defender for Endpoint-Attach solution](https://learn.microsoft.com/en-us/intune/device-security/microsoft-defender/media/security-settings-management/endpoint-security-overview-2.png){Intune endpoint security policy reaching devices through the MDE channel}

![Conceptual diagram of the security configuration management solution](https://learn.microsoft.com/en-us/intune/device-security/microsoft-defender/media/security-settings-management/mde-architecture-2.png){1 onboard to MDE → 2 talk to Intune → 3 Entra registration (synthetic if needed) → 4 report status}

![Enable settings management in the Defender portal](https://learn.microsoft.com/en-us/intune/device-security/microsoft-defender/media/security-settings-management/enable-mde-settings-management-defender.png){Defender portal: Enforcement Scope — pick the platforms}

![Configure pilot mode and Configuration Manager authority](https://learn.microsoft.com/en-us/intune/device-security/microsoft-defender/media/security-settings-management/pilot-cmauthority-mde-settings-management-defender.png){Pilot on tagged devices (tag MDE-Management) before going to all devices}

![Enable settings management in the Intune admin center](https://learn.microsoft.com/en-us/intune/device-security/microsoft-defender/media/security-settings-management/enable-mde-settings-management-mem.png){The matching switch in the Intune admin center}

![Manage Security settings using Configuration Manager toggle set to Off](https://learn.microsoft.com/en-us/intune/device-security/microsoft-defender/media/security-settings-management/disable-configuration-manager-toggle.png){Turn the Configuration Manager toggle off so only one channel sets policy}

![Security settings management enrollment status on the device page](https://learn.microsoft.com/en-us/intune/device-security/microsoft-defender/media/security-settings-management/defender-enrollment-validation.png){Defender device page: Managed by MDE, MDE Enrollment status Success}

![Managed by status in the Intune admin center](https://learn.microsoft.com/en-us/intune/device-security/microsoft-defender/media/security-settings-management/intune-enrollment-validation.png){The same device in the Intune admin center}

![All devices page in the Azure portal](https://learn.microsoft.com/en-us/intune/device-security/microsoft-defender/media/security-settings-management/azure-enrollment-validation.png){The same device object in Entra ID (Azure portal, All devices)}

![Intune dynamic group for Windows workstations](https://learn.microsoft.com/en-us/intune/device-security/microsoft-defender/media/security-settings-management/windowworkstation.jpg){Dynamic Entra device group rule — Windows workstations}

![Intune dynamic group for Windows servers](https://learn.microsoft.com/en-us/intune/device-security/microsoft-defender/media/security-settings-management/windowsserver.jpg){Dynamic Entra device group rule — Windows Server}

![Intune dynamic group for Linux devices](https://learn.microsoft.com/en-us/intune/device-security/microsoft-defender/media/security-settings-management/linuxdevices.jpg){Dynamic Entra device group rule — Linux}

![Policy sync button on a device managed by MDE](https://learn.microsoft.com/en-us/intune/device-security/microsoft-defender/media/security-settings-management/policy-sync-from-mde.png){Policy sync forces a check-in instead of waiting 90 minutes}

### Onboarding

![Device onboarding in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-endpoint/media/mde-device-onboarding-ui.png){Settings > Endpoints > Onboarding: operating system, connectivity type, deployment method, download package}

![Diagram of the four-stage streamlined connectivity process](https://learn.microsoft.com/en-us/defender-endpoint/media/streamlined-connectivity-process.png){Streamlined connectivity: prepare the network, then onboard with the new package}

![The insider rings](https://learn.microsoft.com/en-us/defender-endpoint/media/insider-rings.png){macOS/Linux update channels: Beta → Preview → Current}

### Tags

![Manage tags button](https://learn.microsoft.com/en-us/defender-endpoint/media/manage-tags-option.png){Manage tags sits among the device's response actions}

![Adding tags on a device](https://learn.microsoft.com/en-us/defender-endpoint/media/create-new-tag.png){Type to find an existing tag or create a new one}

![Tag shown on the device](https://learn.microsoft.com/en-us/defender-endpoint/media/new-tag-label-display.png){The tag now shows on the device page and in the inventory}

![Rule conditions page](https://learn.microsoft.com/en-us/defender-xdr/media/configure-asset-rules/rule-conditions.png){Asset rule management: the conditions a dynamic rule matches on}

![Actions page](https://learn.microsoft.com/en-us/defender-xdr/media/configure-asset-rules/actions-to-apply.png){The action: which tag (or device value) the rule applies}

![Machine tags page showing dynamic tags](https://learn.microsoft.com/en-us/defender-xdr/media/configure-asset-rules/manage-machine-tags.png){Dynamic tags appear under Manage tags but cannot be edited by hand}

![Rule details page](https://learn.microsoft.com/en-us/defender-xdr/media/configure-asset-rules/update-rule.png){Edit, Delete or Turn off a rule — Turn off keeps it without applying it}

### Licences

![Defender for Business offering overview](https://learn.microsoft.com/en-us/defender-business/media/mdb-offering-overview.png){Defender for Business: vulnerability management, ASR, next-gen protection, EDR, AIR}

![Defender for Business compared with Microsoft 365 Business Premium](https://learn.microsoft.com/en-us/defender-business/media/mdb-m365bp-comparison.png){Business Premium includes Defender for Business plus Intune and more}

## What the exam assumes you know

- ==!Defender Antivirus and Defender for Endpoint are the same thing.== Antivirus scans files on the device. MDE is the cloud EDR service with a sensor. ASR rules need ==+Defender Antivirus in active mode==.
- ==!Every MDE feature needs Intune.== Onboarding works through GPO, ConfigMgr, script or VDI too, and **security settings management** pushes policy without Intune enrollment.
- ==!A tag controls who sees the device.== ==+Only a device group does.== Tags are labels; groups carry access and automation level.
- A device can carry **many tags** but sits in **one** device group.
- ==!Manual tags work for custom data collection.== ==+Dynamic tags only.==
- "Onboarded" means the sensor is reporting. "Can be onboarded" means MDE **saw** it on the network but has no sensor there.
- Plan 1 has **no EDR, no AIR and no advanced hunting**. Those are Plan 2 (or Defender for Business).

## Skip list

- **Skip:** the ring-based deployment table (Evaluate 50 devices → Pilot → Full) and the Security Update Validation Program. Rollout project management, not SOC work.
- **Skip:** the per-OS onboarding guides (macOS `.plist`, Linux `mdatp` installer, iOS/Android app configuration). Know that each OS has its own package; the exam does not ask for the steps.
- **Skip:** the device-discovery protocol table (ARP, mDNS, SNMP …) and authenticated network scans. Know Standard vs Basic and that discovered devices have no sensor.
- **Skip:** Intune MAM, Autopilot, Company Portal enrollment, and Configuration Manager workload sliders. Device administration, not security operations.
- **Skip:** the Defender for Business vs Business Premium bundle contents beyond "up to 300 users, P1 plus some P2".
- **Skip:** the Defender for Servers Plan 2 extras (file integrity monitoring, just-in-time VM access, agentless scanning). They belong to the Defender for Cloud objectives.
- **Skip:** the synthetic-registration history (MDEJoined/MDEManaged tags retired September 2023) and the `deviceOSType` change of May 2023. Know only that unregistered devices get a synthetic registration.
- **Skip:** inventory customisation (columns, CSV export, multi-column sort). You will find it by clicking.
- **Skip:** IoT/OT device discovery through Defender for IoT. Separate licence, not on the blueprint here.
