+++
slug = "windows-and-linux-logging"
title = "Windows and Linux logging: event logs, Syslog and CEF"
summary = "What the logs a SOC reads actually are — Windows event logs and the Security event IDs that matter, Linux Syslog facilities and severities, CEF from firewalls — and which Sentinel table each lands in."
order = 13
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/appendix-l--events-to-monitor",
  "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/advanced-audit-policy-configuration",
  "https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon",
  "https://learn.microsoft.com/en-us/azure/sentinel/windows-security-event-id-reference",
  "https://learn.microsoft.com/en-us/azure/sentinel/cef-syslog-ama-overview",
  "https://learn.microsoft.com/en-us/azure/sentinel/connect-cef-syslog-ama",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/vm/data-collection-syslog",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/vm/data-collection-windows-events",
  "https://learn.microsoft.com/en-us/azure/sentinel/connect-services-windows-based",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/vm/monitor-virtual-machine-data-collection",
]
captured = 2026-11-12
related_objectives = ["D1.3.2", "D1.3.3"]
+++

## In one sentence

Every computer and network device keeps a diary of what happened on it — **Windows** writes *event logs* full of numbered events, **Linux** and most network appliances write **Syslog** messages, and security appliances often write Syslog in a stricter shape called **CEF** — and a SOC's job starts with getting those diaries into one searchable place.

## Why it exists

A building's CCTV only helps if the cameras are switched on and the footage reaches the guard desk. Logs are the CCTV of computers. If a server never recorded "someone logged on as administrator at 03:12", no tool can detect it later.

A **SOC** (security operations centre) analyst reads these logs to answer three questions: *who* did something, *what* they did, and *on which machine*. Microsoft Sentinel (the SIEM — the central log search and detection system) can only detect what was logged *and* collected. This page is about the first half: what is logged. The collection pipe — the **Azure Monitor Agent (AMA)** and **data collection rules (DCRs)** — is the next primer.

## Mental model

Think of three kinds of diaries, three ways they travel, and four filing drawers at the end.

```svg
<svg viewBox="0 0 780 360" role="img" aria-label="Log sources and where they land: Windows event logs via AMA to SecurityEvent, Event or WindowsEvent tables; Linux Syslog via AMA to the Syslog table; firewall CEF via a Linux log forwarder to the CommonSecurityLog table">
  <defs>
    <marker id="wllarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <text x="90" y="24" text-anchor="middle" class="label-accent">Source</text>
  <text x="390" y="24" text-anchor="middle" class="label-accent">How it travels</text>
  <text x="680" y="24" text-anchor="middle" class="label-accent">Sentinel table</text>
  <rect class="box" x="10" y="40" width="160" height="80" rx="8"/>
  <text x="90" y="68" text-anchor="middle">Windows server</text>
  <text x="90" y="90" text-anchor="middle" class="muted">Security · System</text>
  <text x="90" y="110" text-anchor="middle" class="muted">Application · Sysmon</text>
  <rect class="box" x="10" y="150" width="160" height="70" rx="8"/>
  <text x="90" y="180" text-anchor="middle">Linux server</text>
  <text x="90" y="202" text-anchor="middle" class="muted">rsyslog / syslog-ng</text>
  <rect class="box-risk" x="10" y="250" width="160" height="70" rx="8"/>
  <text x="90" y="280" text-anchor="middle">Firewall / appliance</text>
  <text x="90" y="302" text-anchor="middle" class="muted">cannot run an agent</text>
  <rect class="box-accent" x="300" y="60" width="180" height="60" rx="8"/>
  <text x="390" y="86" text-anchor="middle">AMA on the server</text>
  <text x="390" y="106" text-anchor="middle" class="muted">XPath filter</text>
  <rect class="box-accent" x="300" y="160" width="180" height="50" rx="8"/>
  <text x="390" y="190" text-anchor="middle">AMA on the server</text>
  <rect class="box-accent" x="280" y="250" width="220" height="70" rx="8"/>
  <text x="390" y="278" text-anchor="middle">Linux log forwarder</text>
  <text x="390" y="300" text-anchor="middle" class="muted">port 514 → AMA</text>
  <rect class="box-ok" x="590" y="40" width="180" height="40" rx="8"/>
  <text x="680" y="65" text-anchor="middle">SecurityEvent</text>
  <rect class="box" x="590" y="88" width="180" height="40" rx="8"/>
  <text x="680" y="113" text-anchor="middle">Event / WindowsEvent</text>
  <rect class="box-ok" x="590" y="165" width="180" height="40" rx="8"/>
  <text x="680" y="190" text-anchor="middle">Syslog</text>
  <rect class="box-ok" x="590" y="265" width="180" height="40" rx="8"/>
  <text x="680" y="290" text-anchor="middle">CommonSecurityLog</text>
  <line class="line" x1="170" y1="80" x2="298" y2="90" marker-end="url(#wllarrow)"/>
  <line class="line" x1="170" y1="185" x2="298" y2="185" marker-end="url(#wllarrow)"/>
  <line class="line" x1="170" y1="285" x2="278" y2="285" marker-end="url(#wllarrow)"/>
  <line class="line-accent" x1="480" y1="82" x2="588" y2="60" marker-end="url(#wllarrow)"/>
  <line class="line" x1="480" y1="98" x2="588" y2="108" marker-end="url(#wllarrow)"/>
  <line class="line-accent" x1="480" y1="185" x2="588" y2="185" marker-end="url(#wllarrow)"/>
  <line class="line-accent" x1="500" y1="285" x2="588" y2="285" marker-end="url(#wllarrow)"/>
  <line class="line" x1="500" y1="270" x2="588" y2="195" marker-end="url(#wllarrow)"/>
  <text x="520" y="232" class="muted">plain Syslog</text>
  <text x="20" y="348" class="muted">Which Windows table depends on the connector — see "What actually matters" point 5.</text>
</svg>
```

## What actually matters

### 1. Windows event logs

Windows keeps several separate logs, viewed in the **Event Viewer** program:

| Log | What it records | SOC value |
|---|---|---|
| **Security** | Audited actions: logons, privilege use, account and group changes, process starts, policy changes | Highest — most detections use it |
| **System** | Windows itself: services, drivers, startup and shutdown | Medium — e.g. new services |
| **Application** | Programs: crashes, app-specific messages | Low for security |
| **Sysmon/Operational** | Extra detail from **Sysmon** (see 3 below) | High, if installed |

Each entry is an **event** with an **Event ID** (a number naming the kind of event), a time, a computer name, a level (Critical, Error, Warning, Information, Verbose) and an XML body of fields. Microsoft Sentinel's **All events** set takes the Security log plus the AppLocker logs. It ==!does not include System or Application==.

### 2. The Security event IDs worth memorising

Wording below is Microsoft's own event summary:

| Event ID | Meaning | Why a SOC cares |
|---|---|---|
| ==@4624== | An account was successfully logged on | Who got in, from where |
| ==@4625== | An account failed to log on | Password guessing, brute force |
| 4634 | An account was logged off | Session length (audit trail) |
| 4648 | A logon was attempted using explicit credentials | `runas`, credential reuse |
| ==@4672== | Special privileges assigned to new logon | An admin-level logon |
| ==@4688== | A new process has been created | What ran — malware, scripts |
| 4697 | Attempt to install a service | Persistence |
| 4698 | A scheduled task was created | Persistence |
| ==@4720== | A user account was created | Backdoor accounts |
| 4726 | A user account was deleted | Covering tracks |
| 4728 / 4732 | A member was added to a security-enabled global / local group | Privilege escalation |
| 4740 | A user account was locked out | Brute force side effect |
| 4768 / 4769 / 4771 | Kerberos TGT requested / service ticket requested / pre-authentication failed | Domain controller attacks |
| 4776 | The domain controller attempted to validate the credentials for an account | NTLM logons |
| ==!1102== | The audit log was cleared | An attacker wiping evidence |

### 3. Audit policy decides what Windows records

Windows logs a Security event only if the matching **audit policy** is on. An audit policy is a switch per category, such as **Audit Logon** (4624, 4625, 4648) or **Audit Process Creation** (4688). You set it in Group Policy at `Computer Configuration\Windows Settings\Security Settings\Advanced Audit Policy Configuration\System Audit Policies`. Each switch can record **Success**, **Failure**, or both. ==!If auditing is off, no event exists==, so no agent or connector can collect it.

**Sysmon** (System Monitor) is a free Microsoft Sysinternals tool that installs a service and driver and writes richer events to `Applications and Services Logs/Microsoft/Windows/Sysmon/Operational`. Examples: Event ID 1 (process creation, with full command line and file hash), Event ID 3 (network connection), Event ID 22 (DNS query). Note the clash: ==!Sysmon Event ID 1 is not Security Event ID 1==; IDs are only unique within one log.

### 4. Linux Syslog and CEF

**Syslog** is a standard way for Unix/Linux systems and network devices to send text log messages. A **Syslog daemon** — a background program, usually `rsyslog` or `syslog-ng` — receives them, by default on **TCP or UDP port 514**. AMA supports messages in **RFC 3164** (BSD Syslog) and **RFC 5424** (IETF Syslog) formats.

Every message carries two labels:

- **Facility** — *which part of the system* sent it: `kern`, `user`, `mail`, `daemon`, `auth`, `syslog`, `lpr`, `news`, `uucp`, `cron`, `authpriv`, `ftp`, `ntp`, `audit`, `alert`, `clock`, `local0`–`local7`. For security, `auth` and `authpriv` hold logon messages. `local0`–`local7` are free for appliances to use.
- **Severity** — *how bad*, from least to most severe: Debug, Info, Notice, Warning, Error, Critical, Alert, Emergency. Choosing a **minimum log level** collects that level and everything more severe. Example: picking `LOG_ERR` also collects `LOG_CRIT`, `LOG_ALERT` and `LOG_EMERG`.

**CEF (Common Event Format)** is a vendor-neutral layout for security appliances: firewalls, routers, intrusion detection systems. It is ==@an extension of Syslog==. It is a Syslog message whose text starts with a fixed header (device vendor, product, version, event class ID, name, severity), followed by `key=value` extensions such as source IP, destination IP, user and action. Because the fields are already labelled, Sentinel can split them into proper columns.

### 5. Why a log forwarder exists, and where each lands

A firewall cannot install AMA. So you build a **log forwarder**: a dedicated Linux machine (in Azure, on-premises or another cloud) with a Syslog daemon and AMA. Appliances send to it on port 514; the daemon hands messages to AMA (TCP port 28330 on AMA version 1.28.11 and later); AMA uploads them. A Linux server can instead run AMA itself.

| Table | What lands there | How |
|---|---|---|
| ==@SecurityEvent== | Windows Security log events | **Windows Security Events via AMA** connector |
| `WindowsEvent` | Windows events forwarded by **Windows Event Forwarding** (WEF), including Security events | **Windows Forwarded Events** connector |
| `Event` | Windows System/Application (and Security, if picked) through a plain Azure Monitor DCR | DCR, no Sentinel connector |
| ==@Syslog== | Plain Syslog | **Syslog via AMA** connector |
| ==@CommonSecurityLog== | CEF messages | **Common Event Format (CEF) via AMA** connector |

Connector set-up detail lives in D1.3.

![Syslog collection from a single source](https://learn.microsoft.com/en-us/azure/sentinel/media/connect-cef-ama/syslog-diagram.png){A single Linux VM: its own Syslog daemon hands messages to AMA, which sends them to the Syslog table}

![Syslog and CEF collection from a log forwarder](https://learn.microsoft.com/en-us/azure/sentinel/media/connect-cef-ama/cef-forwarder-diagram.png){The log forwarder pattern: appliances send to port 514 on a dedicated Linux VM; CEF goes to CommonSecurityLog, plain Syslog to Syslog}

![Sysmon event in Event Viewer](https://learn.microsoft.com/en-us/sysinternals/downloads/media/sysmon/event-screen-optimized.png){A Sysmon event in Event Viewer — richer than the built-in Security log}

## Where it lives

| Thing | Where |
|---|---|
| Read logs on a Windows machine | **Event Viewer > Windows Logs > Security / System / Application** |
| Sysmon events | **Event Viewer > Applications and Services Logs > Microsoft > Windows > Sysmon > Operational** |
| Turn auditing on | Group Policy: `Computer Configuration\Windows Settings\Security Settings\Advanced Audit Policy Configuration\System Audit Policies` |
| Linux daemon config | `/etc/rsyslog.conf` and `/etc/rsyslog.d/`, or `/etc/syslog-ng/` |
| Sentinel connectors | Azure portal: **Microsoft Sentinel > Configuration > Data connectors**. Defender portal (`security.microsoft.com`): **Microsoft Sentinel > Configuration > Data connectors** |
| Pick facilities and severities | Connector **+Create data collection rule > Collect** tab |

Test an XPath filter for Windows events locally before using it in a DCR:

```powershell
Get-WinEvent -LogName 'Security' -FilterXPath '*[System[(EventID=4625)]]'
```

On a log forwarder, after the connector creates the DCR, run Microsoft's installer script. It configures the daemon and opens port 514 for UDP and TCP:

```bash
sudo wget -O Forwarder_AMA_installer.py https://raw.githubusercontent.com/Azure/Azure-Sentinel/master/DataConnectors/Syslog/Forwarder_AMA_installer.py && sudo python Forwarder_AMA_installer.py
```

Query them (KQL — see the KQL primer):

```kql
SecurityEvent
| where EventID == 4625
| summarize Failures = count() by Account, Computer
```

![Syslog via AMA connector page](https://learn.microsoft.com/en-us/azure/sentinel/media/connect-cef-ama/syslog-connector-page-create-dcr.png){The Syslog via AMA connector page — +Create data collection rule}

![CEF via AMA connector page](https://learn.microsoft.com/en-us/azure/sentinel/media/connect-cef-ama/cef-connector-page-create-dcr.png){The Common Event Format (CEF) via AMA connector page}

![DCR details in the Basic tab](https://learn.microsoft.com/en-us/azure/sentinel/media/connect-cef-ama/dcr-basics-tab.png){Basic tab: DCR name, subscription, resource group}

![Selecting resources when setting up the DCR](https://learn.microsoft.com/en-us/azure/sentinel/media/connect-cef-ama/dcr-select-resources.png){Resources tab: pick the log forwarder VM — AMA is installed on it}

![Selecting log levels when setting up the DCR](https://learn.microsoft.com/en-us/azure/sentinel/media/connect-cef-ama/dcr-log-levels.png){Collect tab: a minimum log level per facility}

![Reviewing and creating the DCR](https://learn.microsoft.com/en-us/azure/sentinel/media/connect-cef-ama/dcr-review-create.png){Review + create}

![Running the forwarder installation script](https://learn.microsoft.com/en-us/azure/sentinel/media/connect-cef-ama/run-install-script.png){The connector page gives you the installer command to run on the forwarder}

![Selecting data source type and minimum log level in an Azure Monitor DCR](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/media/data-collection-syslog/create-rule-data-source.png){The same choice in a plain Azure Monitor DCR: Linux Syslog, minimum log level per facility, or NONE}

![Azure Monitor Logs destination in a data collection rule](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/media/data-collection/destination-workspace.png){Syslog can only go to a Log Analytics workspace, into the Syslog table}

![View data collection rules in the Azure portal](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/media/data-collection-rule-overview/view-data-collection-rules.png){Azure portal > Monitor > Data Collection Rules — every DCR a connector creates shows up here}

![Records returned from the Syslog table](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/media/data-collection-syslog/verify-syslog.png){Checking that Syslog records have arrived}

## What the exam assumes you know

- 4624 = success, 4625 = failure, 4688 = process creation, 4720 = user created, 4672 = admin-level logon, 1102 = log cleared.
- ==!CEF goes to the Syslog table== is wrong. ==+CEF goes to CommonSecurityLog==; plain Syslog goes to `Syslog`.
- Sending CEF and plain Syslog on the **same facility** can duplicate data in both tables. Fix it by using separate facilities, or with a DCR transformation.
- Windows Security event sets in the connector: **All events**, **Common** (full audit trail, includes 4624 and 4634), **Minimal** (breach signals only — includes 4624, 4625 and 4688, excludes 4634), **Custom** (XPath).
- Forwarded events land in `WindowsEvent`. Many built-in rules query only `SecurityEvent`.
- A firewall or appliance never runs AMA. It needs a **Linux log forwarder**.

## Skip list

- **Skip:** the full Common and Minimal event-ID lists (over 150 IDs). Know what each set is *for*, and the handful of IDs in the table above.
- **Skip:** every Advanced Audit Policy subcategory and its event volume. Know that audit policy must be on, and that Audit Logon and Audit Process Creation exist.
- **Skip:** Sysmon's other event types, its XML configuration schema and its command-line switches. Know what Sysmon adds and where it writes.
- **Skip:** rsyslog/syslog-ng configuration files, Unix-socket vs TCP 28330 handover detail, SELinux notes and `tcpdump`/`logger` test commands. That is forwarder plumbing, covered at connector level in D1.3.3.
- **Skip:** the legacy (pre-Windows-Vista) event IDs listed next to each modern ID in Microsoft's appendix. Irrelevant on any supported system.
- **Skip:** the `TimeGenerated` vs `EventTime` time-zone difference on forwarded Syslog. It is a troubleshooting detail, not exam content.
