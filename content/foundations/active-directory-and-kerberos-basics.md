+++
slug = "active-directory-and-kerberos-basics"
title = "Active Directory and Kerberos basics: the on-premises directory attackers go after"
summary = "What on-premises Active Directory is (forest, domain, domain controller, OU, users, computers, groups), which groups are the crown jewels, how NTLM and Kerberos sign people in (KDC, TGT, service ticket, SPN), the five classic AD attacks in one line each, how AD links to Entra ID through Entra Connect or Cloud Sync, and why Defender for Identity puts its sensors on domain controllers."
order = 25
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview",
  "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/understanding-the-active-directory-logical-model",
  "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/appendix-b--privileged-accounts-and-groups-in-active-directory",
  "https://learn.microsoft.com/en-us/windows-server/security/kerberos/kerberos-authentication-overview",
  "https://learn.microsoft.com/en-us/windows-server/security/kerberos/ntlm-overview",
  "https://learn.microsoft.com/en-us/windows/win32/ad/service-principal-names",
  "https://learn.microsoft.com/en-us/defender-for-identity/alerts-mdi-classic",
  "https://learn.microsoft.com/en-us/defender-for-identity/alerts-xdr",
  "https://learn.microsoft.com/en-us/defender-for-identity/what-is",
  "https://learn.microsoft.com/en-us/defender-for-identity/entity-tags",
  "https://learn.microsoft.com/en-us/entra/identity/hybrid/whatis-hybrid-identity",
  "https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/whatis-azure-ad-connect",
  "https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-post-installation",
  "https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/what-is-cloud-sync",
  "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-identitylogonevents-table",
  "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-identitydirectoryevents-table",
  "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-identityqueryevents-table",
]
captured = 2026-11-12
related_objectives = ["D2.1.6", "D2.1.9"]
+++

## In one sentence

**Active Directory Domain Services (AD DS)** — everyone just says "AD" — is the directory of users, computers and groups that most companies run on their own Windows servers; it checks every office sign-in, which is exactly why an attacker inside the network tries to take it over.

## Why it exists

Picture a company's key office. It lists every employee and room, hands out keys, and one master-key holder can open everything.

AD is that key office for a Windows network. It stores **user accounts** (names, passwords, phone numbers), **computer accounts**, **groups**, printers and file shares. One username and password work on any company PC.

AD is **not** Microsoft Entra ID. Entra ID is the *cloud* directory (see [Entra ID basics](entra-id-basics.html)). AD lives on servers in the company's own building or data centre — "on-premises". Most organisations run **both** and copy accounts from AD up to Entra ID. That link is called **hybrid identity**.

For a SOC analyst, an attacker who owns AD owns every account and every domain-joined machine. Microsoft Defender for Identity watches it; you work its alerts in lessons [D2.1.6](../objective/D2.1.6.html) and [D2.1.9](../objective/D2.1.9.html).

## Mental model

Nested boxes: **forest** > **domains** > **organizational units (OUs)** > users, computers and groups. **Domain controllers (DCs)** are the servers that store a domain and answer sign-ins.

```svg
<svg viewBox="0 0 820 440" role="img" aria-label="Active Directory logical structure: a forest containing two domains linked by a two-way trust; each domain contains organizational units holding users, computers and groups; domain controllers hold a full replicated copy of their domain">
  <defs>
    <marker id="akbarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <rect class="box-accent" x="10" y="10" width="800" height="420" rx="12"/>
  <text x="410" y="36" text-anchor="middle" class="label-accent">Forest — shared schema, global catalog, the security boundary</text>
  <rect class="box" x="30" y="55" width="360" height="355" rx="10"/>
  <text x="210" y="80" text-anchor="middle" class="label-accent">Domain: contoso.com (forest root)</text>
  <text x="210" y="100" text-anchor="middle" class="muted">Enterprise Admins + Schema Admins live here</text>
  <rect class="box" x="50" y="115" width="320" height="140" rx="8"/>
  <text x="210" y="138" text-anchor="middle">OU: Staff</text>
  <rect class="box-ok" x="65" y="152" width="90" height="40" rx="6"/>
  <text x="110" y="177" text-anchor="middle">users</text>
  <rect class="box-ok" x="165" y="152" width="90" height="40" rx="6"/>
  <text x="210" y="177" text-anchor="middle">computers</text>
  <rect class="box-ok" x="265" y="152" width="90" height="40" rx="6"/>
  <text x="310" y="177" text-anchor="middle">groups</text>
  <text x="210" y="222" text-anchor="middle" class="muted">OU = folder for Group Policy</text>
  <text x="210" y="242" text-anchor="middle" class="muted">and delegated admin rights</text>
  <rect class="box-risk" x="50" y="270" width="150" height="120" rx="8"/>
  <text x="125" y="295" text-anchor="middle" class="label-risk">DC 1</text>
  <text x="125" y="318" text-anchor="middle">full copy of</text>
  <text x="125" y="338" text-anchor="middle">the domain</text>
  <text x="125" y="362" text-anchor="middle" class="muted">runs the KDC</text>
  <rect class="box-risk" x="220" y="270" width="150" height="120" rx="8"/>
  <text x="295" y="295" text-anchor="middle" class="label-risk">DC 2</text>
  <text x="295" y="318" text-anchor="middle">full copy of</text>
  <text x="295" y="338" text-anchor="middle">the domain</text>
  <text x="295" y="362" text-anchor="middle" class="muted">runs the KDC</text>
  <line class="line-accent" x1="200" y1="330" x2="218" y2="330" marker-end="url(#akbarrow)" marker-start="url(#akbarrow)"/>
  <text x="210" y="408" text-anchor="middle" class="muted">replication keeps every DC identical</text>
  <rect class="box" x="430" y="55" width="360" height="355" rx="10"/>
  <text x="610" y="80" text-anchor="middle" class="label-accent">Domain: emea.contoso.com</text>
  <text x="610" y="100" text-anchor="middle" class="muted">its own Domain Admins group</text>
  <rect class="box" x="450" y="115" width="320" height="140" rx="8"/>
  <text x="610" y="138" text-anchor="middle">OU: Paris</text>
  <rect class="box-ok" x="465" y="152" width="90" height="40" rx="6"/>
  <text x="510" y="177" text-anchor="middle">users</text>
  <rect class="box-ok" x="565" y="152" width="90" height="40" rx="6"/>
  <text x="610" y="177" text-anchor="middle">computers</text>
  <rect class="box-ok" x="665" y="152" width="90" height="40" rx="6"/>
  <text x="710" y="177" text-anchor="middle">groups</text>
  <rect class="box-risk" x="535" y="270" width="150" height="120" rx="8"/>
  <text x="610" y="295" text-anchor="middle" class="label-risk">DC 3</text>
  <text x="610" y="318" text-anchor="middle">full copy of</text>
  <text x="610" y="338" text-anchor="middle">emea domain</text>
  <text x="610" y="362" text-anchor="middle" class="muted">runs the KDC</text>
  <line class="line-accent" x1="390" y1="200" x2="430" y2="200" marker-end="url(#akbarrow)" marker-start="url(#akbarrow)"/>
  <text x="410" y="230" text-anchor="middle" class="muted">trust</text>
</svg>
```

Four facts carry the whole picture:

- **Forest.** One or more domains that share one **schema** (the rulebook of object types and attributes) and one **global catalog** (a forest-wide search index). Domains in the same forest trust each other automatically — two-way and transitive. A **trust** means "I accept sign-ins checked by your DCs."
- **Domain.** A slice of the forest. An account is created once in a domain and works on any computer joined to that forest.
- **Domain controller (DC).** A Windows server that stores the accounts *and their credentials* (password hashes, certificates). Every DC in a domain holds a complete copy. A change on one DC is **replicated** — copied — to all the others.
- **OU.** A folder inside a domain. Admins use it to apply **Group Policy** (settings pushed to machines) and to **delegate** rights, such as "the Paris helpdesk may reset passwords in OU Paris."

## What actually matters

**1. The crown-jewel groups.** AD ships with built-in groups. Four are the most powerful:

| Group | Where it exists | Power |
|---|---|---|
| ==@Enterprise Admins== (EA) | Forest root domain only | Forest-wide changes. Member of the **Administrators** group in **every** domain |
| ==@Domain Admins== (DA) | One per domain | "All-powerful" in its domain. Member of the **local Administrators group on every domain-joined computer** |
| **Administrators** (built-in) | One per domain | Most direct rights on the directory and on DCs. DA and EA are nested inside it |
| **Schema Admins** | Forest root domain only | Can change the schema. Narrow, but can wreck the whole forest |

Microsoft states that a member of any of EA, DA or Administrators can make itself a member of the other two. ==!Treat all three as equivalent.== Attackers hunt for any account in them.

![Default Domain Controllers GPO user rights assignment](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/media/appendix-b--privileged-accounts-and-groups-in-active-directory/sad_8.gif){User rights in the Default Domain Controllers Group Policy — which built-in groups (Administrators, Server Operators, Print Operators) hold powers such as debug programs, change the system time or load device drivers}

**2. NTLM versus Kerberos — the two ways Windows proves who you are.**

| | NTLM | Kerberos (v5) |
|---|---|---|
| How it proves you | **Challenge-response**: the server sends a challenge, your computer answers using a **hash** of your password | **Tickets** issued by a trusted third party |
| Who checks | The server asks the DC **every time** | The server reads the ticket itself; no DC call per connection |
| Server proves itself to you? | ==!No== | Yes — **mutual authentication** |
| When used | Workgroup machines, local sign-ins, old apps | The **preferred** method in an AD domain |
| What an attacker steals | The **password hash** | The **ticket** |

**3. How Kerberos works.** Three parties: you (the client), the service you want, and the **Key Distribution Center (KDC)**. The KDC runs on **every DC** and uses AD as its account database.

```svg
<svg viewBox="0 0 820 330" role="img" aria-label="Kerberos flow: the user's PC proves the password to the KDC on a domain controller and gets a ticket-granting ticket; the PC shows the TGT to get a service ticket for a named SPN; the PC presents the service ticket to the server. Attack points: Kerberoasting cracks the service ticket offline, pass-the-ticket replays a stolen ticket, golden ticket forges a TGT with the KRBTGT secret">
  <defs>
    <marker id="akbarrow2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <rect class="box" x="20" y="110" width="170" height="90" rx="8"/>
  <text x="105" y="145" text-anchor="middle" class="label-accent">User's PC</text>
  <text x="105" y="168" text-anchor="middle" class="muted">ticket cache</text>
  <rect class="box-accent" x="320" y="20" width="200" height="110" rx="8"/>
  <text x="420" y="50" text-anchor="middle" class="label-accent">KDC on the DC</text>
  <text x="420" y="75" text-anchor="middle">uses AD as its</text>
  <text x="420" y="95" text-anchor="middle">account database</text>
  <text x="420" y="117" text-anchor="middle" class="muted">TGTs signed by KRBTGT</text>
  <rect class="box-ok" x="620" y="110" width="180" height="90" rx="8"/>
  <text x="710" y="140" text-anchor="middle" class="label-accent">File / SQL server</text>
  <text x="710" y="165" text-anchor="middle" class="muted">named by its SPN</text>
  <line class="line-accent" x1="190" y1="125" x2="318" y2="60" marker-end="url(#akbarrow2)"/>
  <text x="200" y="72" class="muted">1. sign in → get TGT</text>
  <line class="line-accent" x1="190" y1="160" x2="318" y2="110" marker-end="url(#akbarrow2)"/>
  <text x="140" y="245" class="muted">2. show TGT → get service ticket for SPN</text>
  <line class="line-accent" x1="190" y1="185" x2="618" y2="185" marker-end="url(#akbarrow2)"/>
  <text x="404" y="178" text-anchor="middle" class="muted">3. present service ticket</text>
  <rect class="box-risk" x="20" y="265" width="250" height="55" rx="6"/>
  <text x="145" y="288" text-anchor="middle" class="label-risk">Pass-the-ticket</text>
  <text x="145" y="308" text-anchor="middle">steal a ticket, replay it elsewhere</text>
  <rect class="box-risk" x="285" y="265" width="250" height="55" rx="6"/>
  <text x="410" y="288" text-anchor="middle" class="label-risk">Golden ticket</text>
  <text x="410" y="308" text-anchor="middle">forge a TGT with KRBTGT's key</text>
  <rect class="box-risk" x="550" y="265" width="250" height="55" rx="6"/>
  <text x="675" y="288" text-anchor="middle" class="label-risk">Kerberoasting</text>
  <text x="675" y="308" text-anchor="middle">crack a service ticket offline</text>
</svg>
```

1. At sign-in, your PC proves your password to the KDC and gets a **ticket-granting ticket (TGT)** — a day pass it caches, so you don't retype the password.
2. To reach a file server, your PC shows the TGT to the KDC and asks for a **service ticket** for that one service.
3. Your PC hands the service ticket to the server. The server lets you in without phoning the DC.

How does the KDC know which service you mean? By its **service principal name (SPN)** — a unique name for one service instance, such as `MSSQLSvc/sql01.contoso.com:1433`. An SPN is registered on the account the service runs as. ==!An SPN on an ordinary user account is a Kerberoasting target== (point 4).

**4. Why attackers target AD — the five you must recognise.** Each maps to a **MITRE ATT&CK** technique (MITRE is the public catalogue of attacker behaviour; see [SOC fundamentals](soc-fundamentals.html)).

| Attack | One line | MITRE | Defender for Identity alert (classic name) |
|---|---|---|---|
| **Pass-the-hash** | Steal a user's NTLM hash from one computer and use it to sign in to another — no password needed | T1550.002 | Suspected identity theft (pass-the-hash) |
| **Pass-the-ticket** | Steal a Kerberos ticket from one computer and reuse it on another | T1550.003 | Suspected identity theft (pass-the-ticket) |
| **Kerberoasting** | Ask for service tickets for accounts with SPNs, then crack them offline to get the service account's password | T1558.003 | Suspected Kerberos SPN exposure |
| **Golden ticket** | With the **KRBTGT** account's secret, forge a TGT that grants access to anything, for as long as you like | T1558.001 | Suspected Golden Ticket usage |
| **DCSync** | Pretend to be a DC and ask a real DC to "replicate" — it hands over password hashes | T1003.006 | Suspected DCSync attack (replication of directory services) |

Newer Defender-format alerts rename some of these ("Possible Kerberoasting attack"); D2.1.6 covers both formats.

**5. Hybrid identity: how AD reaches Entra ID.** Two Microsoft tools copy users, groups and (optionally) password hashes from AD to Entra ID:

| | Microsoft Entra Connect (Connect Sync) | Microsoft Entra Cloud Sync |
|---|---|---|
| What runs on-premises | A full sync application on a server | A lightweight **provisioning agent** (outbound connections only) |
| Where settings live | On that server | In the cloud, in the Entra admin center |
| Resilience | One active server | Several active agents, automatic failover |
| Extras | Password hash sync, pass-through authentication, AD FS federation setup, Connect Health | Disconnected forests (mergers), device sync for hybrid join, group provisioning back to AD |

Microsoft calls Cloud Sync "the future of synchronization" and says it replaces Entra Connect. Entra Connect itself is free with the subscription; Connect Health needs Entra ID P1.

![Diagram of a hybrid identity scenario](https://learn.microsoft.com/en-us/entra/identity/hybrid/media/common-scenarios/scenario-1.png){Hybrid identity: one identity for on-premises and cloud resources, built by synchronisation}

![What is Microsoft Entra Connect](https://learn.microsoft.com/en-us/entra/identity/hybrid/media/whatis-hybrid-identity/arch.png){Entra Connect: the sync engine plus the sign-in options — password hash sync, pass-through authentication, federation}

![What is Microsoft Entra Connect Health](https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/media/whatis-hybrid-identity-health/aadconnecthealth2.png){Connect Health monitors Connect Sync, AD FS and AD DS from the Entra admin center (needs Entra ID P1)}

![Diagram of basic cloud sync](https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/media/what-is-cloud-sync/architecture-2.png){Cloud Sync: lightweight agents on-premises, all configuration and processing in the cloud}

Why the SOC cares: ==!an on-premises compromise can walk into the cloud.== A synced account stolen in AD is the same person in Entra ID. Defender for Identity alerts on one such path: "Possible takeover of a Microsoft Entra seamless SSO account" (the `AZUREADSSOACC` object) — lateral movement from on-premises to cloud.

**6. Sensitive accounts and honeytokens.** Defender for Identity lets you **tag** entities:

- **Sensitive** — high-value users, devices and groups. Some detections, such as *sensitive group changes*, depend on this tag. Members of Domain Admins, Enterprise Admins, Schema Admins, Administrators, Account Operators, Backup Operators and other built-in groups (nested members included) are tagged **automatically**.
- **Honeytoken** — a bait user or device. It is normally dormant, so ==+any sign-in from a honeytoken account raises an alert.== Nobody legitimate uses it; whoever does is snooping.
- **Exchange server** — devices only. Exchange servers are tagged sensitive by default.

![Screenshot of tagging user accounts as sensitive](https://learn.microsoft.com/en-us/defender-for-identity/media/entity-tags/tag-entities.png){Settings > Identities: tagging users as Sensitive in the Defender portal}

**7. Why Defender for Identity sensors sit on DCs.** Every Kerberos ticket and every domain-account NTLM check passes through a DC — the front desk that sees every badge swipe. Defender for Identity's **sensor** runs on the DC and parses that traffic and the Windows events locally. ==!A DC without a sensor is a blind spot== — Microsoft's DCSync note says such DCs are not covered, and a new unprotected DC might not even be recognised as a DC. The DCSync alert fires precisely because a replication request came from a machine that is *not* a DC.

## Where it lives

| What | Where |
|---|---|
| AD itself | On-premises Windows servers (the DCs). ==!Not in the Azure portal== or any Microsoft cloud portal |
| Sync status (Connect Sync) | **Microsoft Entra admin center** (`entra.microsoft.com`) **> Entra ID > Entra Connect > Connect sync** |
| Cloud Sync configuration | Microsoft Entra admin center (cloud-managed; the agent is installed on-premises) |
| Sensitive / honeytoken tags | **Microsoft Defender portal** (`security.microsoft.com`) **> Settings > Identities** > **Sensitive**, **Honeytoken** or **Exchange server** |
| Defender for Identity alerts | Defender portal **> Incidents & alerts** — see D2.1.6 |
| Raw AD activity for hunting | Defender portal advanced hunting tables `IdentityLogonEvents` (AD sign-ins), `IdentityDirectoryEvents` (DC events, such as group changes), `IdentityQueryEvents` (queries against AD objects) |

![Directory sync time](https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/media/how-to-connect-post-installation/verify2.png){Entra Connect > Connect sync shows when the last synchronisation ran}

![List of additional tasks](https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/media/how-to-connect-post-installation/addtasks2.png){The Entra Connect wizard's additional-tasks list on the sync server — admin work, not SOC work}

## What the exam assumes you know

- ==!AD is not Entra ID.== AD = on-premises, Kerberos/NTLM, domain controllers. Entra ID = cloud. Defender for Identity watches **AD** (and also reads Entra ID and other identity sources).
- **TGT** = proof you signed in; **service ticket** = entry to one service; **KDC** issues both and runs on every DC.
- Match attack to protocol: ==@pass-the-hash → NTLM hash==; ==@pass-the-ticket, Kerberoasting, golden ticket → Kerberos==; ==@DCSync → replication==.
- **Golden ticket needs the KRBTGT secret.** That means the attacker already had domain-admin-level access — it is a persistence move, not a first step.
- **Honeytoken** = dormant bait account; any use alerts. **Sensitive** = high-value tag; built-in admin groups get it automatically.

## Skip list

- **Skip** forest and domain *design* (forest models, resource forests, domain functional levels, site topology, OU design worksheets). Architecture work. Know forest > domain > OU > objects.
- **Skip** the 50-plus default security groups and their SIDs. Know EA, DA, Administrators, Schema Admins, and that Defender for Identity auto-tags the built-in admin groups as sensitive.
- **Skip** AdminSDHolder, SDProp and protected-group internals. Hardening detail, not SOC triage.
- **Skip** Kerberos encryption types, delegation types (constrained, resource-based), PAC validation and the MS-KILE specification. The exam wants the ticket flow and the attack names.
- **Skip** NTLM restriction and auditing policy. Know NTLM is challenge-response, the older protocol, and pass-the-hash's target.
- **Skip** SPN registration syntax (`setspn`) and SQL Server SPN formats. Know what an SPN is and why it makes an account Kerberoastable.
- **Skip** the Connect-vs-Cloud-Sync feature matrix (object limits, writeback, attribute filtering) and migration guides. Know both exist, both sync AD to Entra ID, and Cloud Sync is cloud-managed with lightweight agents.
- **Skip** Connect Health usage analytics and AD FS deployment. Identity-admin territory.
- **Skip** every individual Defender for Identity alert beyond the five above. D2.1.6 teaches alert triage; the full catalogue (dozens of alerts, two formats) is reference material.
