+++
slug = "m365-tenants-and-licensing"
title = "Microsoft 365 tenants and licensing"
summary = "What a Microsoft 365 tenant is, how it shares one Microsoft Entra tenant with your Azure subscriptions, which licence unlocks which SC-200 feature, and why Microsoft Sentinel and Defender for Cloud are billed by usage while Defender XDR is billed per user."
order = 7
ms_learn_urls = ["https://learn.microsoft.com/defender-xdr/configure-attack-disruption", 
  "https://learn.microsoft.com/en-us/microsoft-365/enterprise/subscriptions-licenses-accounts-and-tenants-for-microsoft-cloud-offerings",
  "https://learn.microsoft.com/en-us/defender-xdr/prerequisites",
  "https://learn.microsoft.com/en-us/office365/servicedescriptions/microsoft-365-service-descriptions/microsoft-365-tenantlevel-services-licensing-guidance/microsoft-defender-service-description",
  "https://learn.microsoft.com/en-us/defender-office-365/mdo-about",
  "https://learn.microsoft.com/en-us/entra/fundamentals/licensing",
  "https://learn.microsoft.com/en-us/office365/servicedescriptions/microsoft-365-service-descriptions/microsoft-365-tenantlevel-services-licensing-guidance/microsoft-purview-service-description",
  "https://learn.microsoft.com/en-us/azure/sentinel/billing",
  "https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-cloud-introduction",
  "https://learn.microsoft.com/en-us/defender-xdr/setup-m365deval",
]
captured = 2026-11-12
related_objectives = []
+++

## In one sentence

A **Microsoft 365 tenant** is your organisation's private space in Microsoft's cloud, built on one **Microsoft Entra tenant** (the directory of users and groups), and what you can *do* in it depends on the **licences** you buy — per user for Microsoft 365 and Defender XDR, but by usage for Azure services like Microsoft Sentinel and Defender for Cloud.

## Why it exists

Think of a block of flats. The **building** is your organisation (usually named after its domain, like `contoso.com`). The **residents' register** at the front desk is the Microsoft Entra tenant — every person, once. The building then signs separate **contracts**: a cable TV package for each flat (Microsoft 365 — a fee per user), and an electricity meter for the whole building (Azure — you pay for what you use).

Microsoft uses one register for all its clouds so that one person has one sign-in everywhere. The bill is split because the products work differently. Microsoft 365 is software you *use* per person. Azure is infrastructure you *consume* by the hour or by the gigabyte.

For a SOC analyst this matters on day one. If a screen in the Defender portal is missing, the usual reason is not a bug. It is a licence your organisation did not buy.

## Mental model

Learn the four words in this order:

- **Organisation** — the business, usually identified by its domain name.
- **Subscription** — a contract with Microsoft for a service. An organisation can have many: a Microsoft 365 E5 subscription, several Azure subscriptions, and so on.
- **Licence** — inside a *per-user* subscription, the right for **one user account** to use the service. A Microsoft 365 E5 subscription with 100 licences covers up to 100 users.
- **User account** — stored once, in the shared Microsoft Entra tenant.

```svg
<svg viewBox="0 0 780 380" role="img" aria-label="One organisation shares one Microsoft Entra tenant; Microsoft 365 subscriptions are billed per user licence, Azure subscriptions are billed by consumption and host Microsoft Sentinel and Defender for Cloud">
  <defs>
    <marker id="mtl-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <rect class="box" x="240" y="15" width="300" height="50" rx="8"/>
  <text x="390" y="38" text-anchor="middle">Organisation — contoso.com</text>
  <text x="390" y="56" text-anchor="middle" class="muted">container for subscriptions</text>
  <rect class="box-accent" x="200" y="100" width="380" height="64" rx="8"/>
  <text x="390" y="126" text-anchor="middle" class="label-accent">Microsoft Entra tenant</text>
  <text x="390" y="148" text-anchor="middle">every user and group, stored once</text>
  <line x1="390" y1="65" x2="390" y2="98" class="line-accent" marker-end="url(#mtl-arrow)"/>
  <line x1="300" y1="164" x2="190" y2="210" class="line-accent" marker-end="url(#mtl-arrow)"/>
  <line x1="480" y1="164" x2="590" y2="210" class="line-accent" marker-end="url(#mtl-arrow)"/>
  <rect class="box-ok" x="20" y="212" width="340" height="150" rx="10"/>
  <text x="190" y="238" text-anchor="middle" class="label-accent">Microsoft 365 subscriptions</text>
  <text x="190" y="262" text-anchor="middle">billed per user licence</text>
  <text x="190" y="290" text-anchor="middle" class="muted">E3 / E5 · Defender for Endpoint</text>
  <text x="190" y="310" text-anchor="middle" class="muted">Defender for Office 365 · Entra ID P1/P2</text>
  <text x="190" y="340" text-anchor="middle">→ features in security.microsoft.com</text>
  <rect class="box" x="420" y="212" width="340" height="150" rx="10"/>
  <text x="590" y="238" text-anchor="middle" class="label-accent">Azure subscriptions</text>
  <text x="590" y="262" text-anchor="middle">billed by consumption</text>
  <text x="590" y="290" text-anchor="middle" class="muted">Microsoft Sentinel (per GB ingested)</text>
  <text x="590" y="310" text-anchor="middle" class="muted">Defender for Cloud paid plans</text>
  <text x="590" y="340" text-anchor="middle">→ Azure bill, not a user licence</text>
</svg>
```

![An example organization with multiple subscriptions for Microsoft's cloud offerings](https://learn.microsoft.com/en-us/microsoft-365/media/subscriptions/subscriptions-fig1.png){Figure 1: one organisation, several Microsoft 365, Dynamics 365 and Azure subscriptions}

![An example of multiple licenses within subscriptions for Microsoft's SaaS-based cloud offerings](https://learn.microsoft.com/en-us/microsoft-365/media/subscriptions/subscriptions-fig2.png){Figure 2: per-user licences live inside the SaaS subscriptions}

![An example organization with multiple subscriptions all using the same Microsoft Entra tenant](https://learn.microsoft.com/en-us/microsoft-365/media/subscriptions/subscriptions-fig3.png){Figure 3: every subscription uses the same Microsoft Entra tenant}

![Identity as a Service (IDaaS) for your organization](https://learn.microsoft.com/en-us/microsoft-365/media/subscriptions/subscriptions-fig4.png){Figure 4: on-premises Active Directory synced into the shared Entra tenant with Microsoft Entra Connect}

## What actually matters

- **One Entra tenant, many subscriptions.** Every paid or trial Microsoft 365 subscription comes with a free Entra tenant. That tenant is ==!not== an Azure subscription. You add an Azure subscription to it separately, from the Azure portal.
- **E3 versus E5 is the line that matters most.** Microsoft 365 **E3** includes **Defender for Endpoint Plan 1**, **Defender for Office 365 Plan 1** and **Entra ID P1**. Microsoft 365 **E5** includes **Defender for Endpoint Plan 2**, **Defender for Office 365 Plan 2** and **Entra ID P2**. "Plan 2" is where the SOC tools live.
- **Licences that open the Defender portal (Defender XDR).** Any of: Microsoft 365 E5 or A5; E3 plus the **Microsoft Defender Suite** add-on; E3 plus **Enterprise Mobility + Security E5**; Office 365 E5; Windows 10/11 Enterprise E5; or a standalone Defender for Endpoint, Defender for Identity, Defender for Cloud Apps or Defender for Office 365 Plan 2 licence. The **Microsoft Defender Suite** was formerly called **Microsoft 365 E5 Security**.
- **Threat analytics needs Defender for Endpoint Plan 2.** **Automatic attack disruption** is where Microsoft's own docs disagree: the Defender XDR prerequisites page says it needs Defender for Endpoint Plan 2, while the *Configure automatic attack disruption* page accepts any one of a longer list (E5/A5, Defender for Endpoint Plan 2, Defender for Identity, Defender for Cloud Apps, Defender for Office 365 Plan 2, Defender for Business, and others). The configure page is the more specific source. Either way, each disruption *action* only works where the matching Defender product is deployed — containing a device needs Defender for Endpoint.
- **Microsoft Sentinel and Defender for Cloud are Azure services.** You do not assign them to users. Sentinel bills per GB of data ingested into its workspace (pay-as-you-go by default, or **commitment tiers** starting at **100 GB per day**). Defender for Cloud has free **Foundational CSPM** and paid Defender plans, all billed through the Azure subscription.
- **Purview is licensed separately in practice.** Insider Risk Management needs Microsoft 365 E5 (or the **Microsoft Purview Suite**, or an E5 Insider Risk Management add-on). Some Purview features also use **pay-as-you-go** billing through a linked Azure subscription.
- **Admin accounts do not need a licence** for the service they administer. A dedicated admin account without a mailbox is normal.

| Licence | What it unlocks for a SOC analyst |
|---|---|
| Entra ID Free | Users, groups, basic MFA (security defaults). Included with any Microsoft cloud subscription. |
| ==@Entra ID P1== | Conditional Access. In E3, E5, Business Premium, EMS E3. |
| ==@Entra ID P2== | Risk-based Conditional Access (Entra ID Protection). In E5, Microsoft Defender Suite, EMS E5. |
| Built-in mailbox protection | Anti-malware, anti-spam, anti-phishing for every cloud mailbox. Free. |
| ==@Defender for Office 365 P1== | Safe Links, Safe Attachments, impersonation protection, **Real-time detections**. In E3 and Business Premium. |
| ==@Defender for Office 365 P2== | Everything in P1 plus **Threat Explorer**, Threat Trackers, automated investigation and response (AIR), Attack simulation training, advanced hunting. In E5. |
| ==@Defender for Endpoint P1== | Next-generation anti-malware, attack surface reduction rules, device control, endpoint firewall, network protection, application control. In E3. |
| ==@Defender for Endpoint P2== | P1 plus endpoint detection and response (EDR), automated investigation and remediation, vulnerability management, threat analytics, sandbox (deep analysis). In E5. |
| Defender for Cloud | Foundational CSPM free; Defender plans (Servers, Storage, SQL and others) paid by Azure usage. |
| Microsoft Sentinel | Per GB on the Azure bill. Some data sources are free (below). |

![Diagram about protections in Defender for Office 365 and their relationships to one another](https://learn.microsoft.com/en-us/defender-office-365/media/eop-mdop1-mdop2-comparison.png){The Defender for Office 365 ladder: built-in protection, then Plan 1, then Plan 2}

![Screenshot of the Real-time detections selection in the Email & collaboration section in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-office-365/media/te-rtd-select-real-time-detections.png){Plan 1 tell-tale: Email & collaboration > Real-time detections}

![Screenshot of the Explorer selection in the Email & collaboration section in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-office-365/media/te-rtd-select-threat-explorer.png){Plan 2 tell-tale: Email & collaboration > Explorer (Threat Explorer)}

![Diagram showing the core functionality of Defender for Cloud](https://learn.microsoft.com/en-us/azure/defender-for-cloud/media/defender-for-cloud-introduction/cloud-security-pillars.png){Defender for Cloud: posture (CSPM) and workload protection (CWPP) pillars}

![Conceptual image of CNAPP and how the Defender for Cloud plans protect all of your resources](https://learn.microsoft.com/en-us/azure/defender-for-cloud/media/defender-for-cloud-introduction/defender-plans.png){Each Defender for Cloud plan covers a resource type — and each is billed through Azure}

## Where it lives

- **See what you own:** Microsoft 365 admin center (`admin.microsoft.com`) > **Billing** > **Licenses**. You need **Billing Administrator** or higher in Entra ID.
- **Assign licences to users:** Microsoft 365 admin center > **Users** > **Active users** > select the user > **Manage product licenses**. Entra ID P1/P2 licences are assigned here too.
- **Start Defender trials:** Defender portal > **Microsoft 365 trials** page (`security.microsoft.com/trialHorizontalHub`).
- **See Sentinel's pricing tier:** Microsoft Sentinel > **Settings** > **Pricing** tab. The charges themselves arrive on the Azure subscription's bill.

### Free and trial

| What | Free part | Source of the rule |
|---|---|---|
| Microsoft Sentinel free trial | First **10 GB/day** on the Analytics plan, free for **31 days**, up to **20 workspaces** per tenant | Sentinel billing |
| Sentinel free data sources | **Azure Activity**, **Office 365 audit logs** (SharePoint, Exchange admin, Teams), and **security alerts** from Defender XDR, Defender for Endpoint, Office 365, Identity, Cloud Apps and Defender for Cloud | Sentinel billing |
| Sentinel retention | First **90 days** of retention included | Sentinel billing |
| Defender for Office 365 Plan 2 | **90-day** trial from the Defender portal trials hub | Defender for Office 365 overview |
| Microsoft 365 E5 trial | **25 user licences** for **one month** | Defender XDR trial lab guide |
| Defender for Cloud | **Foundational CSPM** is always free | Defender for Cloud overview |

==!Alerts are free; raw logs are not.== Ingesting the raw Defender for Endpoint or Entra ID sign-in tables into Sentinel is billed per GB, even though the alerts from those products are free.

![Screenshot showing the Microsoft Sentinel section of a sample Azure bill](https://learn.microsoft.com/en-us/azure/sentinel/media/billing/sample-bill-classic.png){Sentinel shows up as line items on the Azure bill — not as a user licence}

![Screenshot of the connector page for Defender for Cloud Apps, with the free security alerts selected and paid MCAS Shadow IT Reporting not enabled](https://learn.microsoft.com/en-us/azure/sentinel/media/billing/data-types.png){A connector that mixes free (alerts) and paid (raw log) data types}

## What the exam assumes you know

- Sentinel needs an **Azure subscription**, not an E5 licence. Defender XDR needs a **per-user licence**, not an Azure subscription.
- "Plan 2" versions (Defender for Endpoint P2, Defender for Office 365 P2, Entra ID P2) are where hunting, automated investigation and risk-based features live.
- ==+Alerts from Microsoft Defender products into Sentinel are free.== ==!Raw Defender and Entra log tables are paid.==

## Skip list

- **Skip:** list prices and the full licence matrices. They change every quarter and are never on the exam. Price numbers belong in a reference page, not here.
- **Skip:** the 30-row Entra authentication-feature table (phone call, SMS, custom caller ID). Know only that Conditional Access needs P1 and risk-based Conditional Access needs P2.
- **Skip:** Microsoft 365 E7, the Microsoft Entra Suite, Entra Agent ID and Microsoft Agent 365. They are new bundles outside the SC-200 blueprint.
- **Skip:** A (education), G (government) and F (frontline) plan letters. Read "E5/A5/G5" as "the top enterprise tier".
- **Skip:** Sentinel commitment-tier maths, the classic versus simplified pricing meters, and data lake billing meters. The D1 pages on workspaces and retention cover what the exam needs.
- **Skip:** Defender for Endpoint "mixed licensing" (P1 and P2 in one tenant) and Defender for Business. Real-world detail, not exam content.
- **Skip:** Dynamics 365 and the VM software-licensing notes in the subscriptions article. Not security operations.
