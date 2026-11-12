+++
slug = "defender-portal-tour"
title = "Microsoft Defender portal tour"
summary = "A guided walk through the Microsoft Defender portal (security.microsoft.com): where incidents, alerts, hunting, the Action center, threat analytics, assets, the Microsoft Sentinel section, settings and permissions live, and what each tab of an incident page shows."
order = 8
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/defender-xdr/microsoft-365-defender-portal",
  "https://learn.microsoft.com/en-us/defender-xdr/incidents-overview",
  "https://learn.microsoft.com/en-us/defender-xdr/incident-queue",
  "https://learn.microsoft.com/en-us/defender-xdr/investigate-incidents",
  "https://learn.microsoft.com/en-us/defender-xdr/investigate-alerts",
  "https://learn.microsoft.com/en-us/defender-xdr/m365d-action-center",
  "https://learn.microsoft.com/en-us/defender-xdr/threat-analytics",
  "https://learn.microsoft.com/en-us/azure/sentinel/microsoft-sentinel-defender-portal",
  "https://learn.microsoft.com/en-us/defender-xdr/prerequisites",
]
captured = 2026-11-12
related_objectives = []
+++

## In one sentence

The **Microsoft Defender portal** at `https://security.microsoft.com` is the single website where a SOC analyst works: it collects **alerts** from every Microsoft security product (and from Microsoft Sentinel), groups them into **incidents**, and gives you the tools to investigate, hunt and respond from one place.

## Why it exists

Picture a building with a separate CCTV room for each floor. A burglar who walks from the car park to the lift to the third floor shows up on three different screens, watched by three different guards. Nobody sees the whole route.

Microsoft used to work like that. Defender for Endpoint (laptops and servers), Defender for Office 365 (email), Defender for Identity (on-premises Active Directory) and Defender for Cloud Apps (cloud services) each had their own console. The Defender portal is the **one control room** with every camera on one wall. Its correlation engine notices that the phishing email, the malware on the laptop and the strange sign-in are the same attack, and shows them as **one incident**.

Microsoft Sentinel — the SIEM (the system that stores and analyses everyone's logs) — now lives here too. Microsoft states that after **March 31, 2027** Sentinel will no longer be supported in the Azure portal, only in the Defender portal.

## Mental model

Two words carry the whole portal:

- **Alert** — one signal. "This file looks malicious on this laptop." A smoke detector going off in one room.
- **Incident** — a container of related alerts that tells the full story of one attack. The fire brigade's case file for the whole building.

You triage **incidents**, not alerts. The alert queue exists for checking one signal on its own.

```svg
<svg viewBox="0 0 780 330" role="img" aria-label="Alerts from several Defender products are correlated into one incident; the incident page has tabs for attack story, alerts, assets, investigations and evidence and response">
  <defs>
    <marker id="dpt-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <text x="120" y="24" text-anchor="middle" class="muted">Alerts (one signal each)</text>
  <rect class="box" x="20" y="38" width="200" height="44" rx="6"/>
  <text x="120" y="65" text-anchor="middle">Office 365: phishing email</text>
  <rect class="box" x="20" y="96" width="200" height="44" rx="6"/>
  <text x="120" y="123" text-anchor="middle">Endpoint: malware on laptop</text>
  <rect class="box" x="20" y="154" width="200" height="44" rx="6"/>
  <text x="120" y="181" text-anchor="middle">Identity: odd sign-in</text>
  <rect class="box" x="20" y="212" width="200" height="44" rx="6"/>
  <text x="120" y="239" text-anchor="middle">Sentinel: analytics rule hit</text>
  <line x1="220" y1="60" x2="300" y2="140" class="line-accent" marker-end="url(#dpt-arrow)"/>
  <line x1="220" y1="118" x2="300" y2="146" class="line-accent" marker-end="url(#dpt-arrow)"/>
  <line x1="220" y1="176" x2="300" y2="152" class="line-accent" marker-end="url(#dpt-arrow)"/>
  <line x1="220" y1="234" x2="300" y2="158" class="line-accent" marker-end="url(#dpt-arrow)"/>
  <rect class="box-accent" x="302" y="105" width="170" height="90" rx="10"/>
  <text x="387" y="138" text-anchor="middle" class="label-accent">Incident</text>
  <text x="387" y="160" text-anchor="middle">one attack story</text>
  <text x="387" y="180" text-anchor="middle" class="muted">correlated automatically</text>
  <line x1="472" y1="150" x2="520" y2="150" class="line-accent" marker-end="url(#dpt-arrow)"/>
  <text x="650" y="24" text-anchor="middle" class="muted">Incident page tabs</text>
  <rect class="box-ok" x="522" y="38" width="240" height="34" rx="6"/>
  <text x="642" y="60" text-anchor="middle">Attack story — graph + timeline</text>
  <rect class="box" x="522" y="78" width="240" height="34" rx="6"/>
  <text x="642" y="100" text-anchor="middle">Alerts — the alerts inside</text>
  <rect class="box" x="522" y="118" width="240" height="34" rx="6"/>
  <text x="642" y="140" text-anchor="middle">Assets — devices, users, mail, apps</text>
  <rect class="box" x="522" y="158" width="240" height="34" rx="6"/>
  <text x="642" y="180" text-anchor="middle">Investigations — automated runs</text>
  <rect class="box" x="522" y="198" width="240" height="34" rx="6"/>
  <text x="642" y="220" text-anchor="middle">Evidence and Response</text>
  <rect class="box" x="522" y="238" width="240" height="34" rx="6"/>
  <text x="642" y="260" text-anchor="middle">Activities — who did what</text>
  <rect class="box" x="522" y="278" width="240" height="34" rx="6"/>
  <text x="642" y="300" text-anchor="middle">Summary · Similar incidents</text>
</svg>
```

## What actually matters

- **The portal only shows what you are licensed for.** If you have Defender for Office 365 but not Defender for Endpoint, the device pages are simply missing. A missing menu is usually a licence, not a fault.
- **Four core experiences.** Microsoft names them **Incidents & alerts**, **Hunting**, **Actions & submissions** and **Threat analytics**.
- **Incident queue.** The default filter shows incidents with status **New** and **In progress** and severity **High**, **Medium** or **Low**. Click a row (not the name) for a summary side pane. Click the name to open the full incident page.
- **Priority score.** The incident queue's **Defender Queue Assistant** ranks incidents with a machine-learning priority score and shows why. The row side pane shows that score.
- **Go hunt.** From an entity in the attack story, **Go hunt** runs a ready-made advanced hunting query about that entity. You can then **Link to incident** any result.
- **Alert queue.** By default it shows **new and in-progress alerts from the last seven days**, newest first.
- **Incident page tabs.** **Attack story** (a graph and timeline; you can act on entities without leaving it), **Alerts**, **Assets** (Devices, Users, Mailboxes, Apps, Cloud resources), **Investigations** (automated investigations triggered by the alerts), **Evidence and Response** (files, processes, emails and the actions taken or pending approval), **Activities** (a timeline of manual and automated actions), plus **Summary** and **Similar incidents**.
- **Action center.** One list of **remediation actions** across devices, email and identities. The **Pending** tab holds actions waiting for approval. The **History** tab is the audit log, and lets you undo some actions.
- **Threat analytics.** Reports written by Microsoft security researchers on active threat actors, attack techniques, vulnerabilities and malware. Each report shows the **related incidents** and **impacted assets** in *your* tenant. It needs **Defender for Endpoint Plan 2**.
- **Advanced hunting.** Where you write KQL (Kusto Query Language — see the KQL basics page) against the raw event tables. It is also where **custom detection rules** are created.
- **Incident cases** are a newer, preview incident experience that Microsoft now recommends. The classic incident page described here remains available.

```svg
<svg viewBox="0 0 780 300" role="img" aria-label="Map of the Defender portal left navigation: Investigation and response, Threat intelligence, Assets, Microsoft Sentinel, and System groups with their main pages">
  <rect class="box-accent" x="15" y="15" width="245" height="160" rx="8"/>
  <text x="137" y="40" text-anchor="middle" class="label-accent">Investigation &amp; response</text>
  <text x="137" y="68" text-anchor="middle">Incidents &amp; alerts</text>
  <text x="137" y="88" text-anchor="middle" class="muted">Incidents · Alerts</text>
  <text x="137" y="116" text-anchor="middle">Hunting</text>
  <text x="137" y="136" text-anchor="middle" class="muted">Advanced hunting · Custom detections</text>
  <text x="137" y="160" text-anchor="middle">Actions &amp; submissions</text>
  <rect class="box" x="275" y="15" width="230" height="75" rx="8"/>
  <text x="390" y="40" text-anchor="middle" class="label-accent">Threat intelligence</text>
  <text x="390" y="66" text-anchor="middle" class="muted">Threat analytics · Intel management</text>
  <rect class="box" x="275" y="100" width="230" height="75" rx="8"/>
  <text x="390" y="125" text-anchor="middle" class="label-accent">Assets</text>
  <text x="390" y="151" text-anchor="middle" class="muted">Devices · Identities</text>
  <rect class="box-ok" x="520" y="15" width="245" height="160" rx="8"/>
  <text x="642" y="40" text-anchor="middle" class="label-accent">Microsoft Sentinel</text>
  <text x="642" y="68" text-anchor="middle" class="muted">Search</text>
  <text x="642" y="92" text-anchor="middle" class="muted">Threat management (workbooks,</text>
  <text x="642" y="112" text-anchor="middle" class="muted">hunting, notebooks, MITRE ATT&amp;CK)</text>
  <text x="642" y="136" text-anchor="middle" class="muted">Content management</text>
  <text x="642" y="158" text-anchor="middle" class="muted">Configuration (connectors, analytics)</text>
  <rect class="box" x="15" y="195" width="750" height="90" rx="8"/>
  <text x="390" y="220" text-anchor="middle" class="label-accent">System (bottom of the menu)</text>
  <text x="390" y="246" text-anchor="middle">Settings > Endpoints · Settings > Microsoft Defender XDR · Settings > Microsoft Sentinel</text>
  <text x="390" y="270" text-anchor="middle">Permissions > Microsoft Defender XDR > Roles</text>
</svg>
```

## Where it lives

All paths below are in the Microsoft Defender portal (`https://security.microsoft.com`). Menu group names move around; the page names are stable.

| You want to… | Path |
|---|---|
| Triage incidents | **Investigation & response** > **Incidents & alerts** > **Incidents** |
| See single alerts | **Investigation & response** > **Incidents & alerts** > **Alerts** |
| Write a KQL hunt | **Investigation & response** > **Hunting** > **Advanced hunting** |
| Approve or review remediation | **Actions & submissions** > **Action center** (or **View pending actions** on the home page card) |
| Submit a file, email or URL to Microsoft | **Actions & submissions** > **Submissions** |
| Read threat reports | **Threat intelligence** > **Threat analytics** |
| Manage threat indicators | **Threat intelligence** > **Intel management** |
| Look at a device or user | **Assets** > **Devices** / **Assets** > **Identities** |
| Sentinel data connectors, analytics rules, automation, watchlists | **Microsoft Sentinel** > **Configuration** > … |
| Sentinel workbooks, hunting queries, notebooks | **Microsoft Sentinel** > **Threat management** > … |
| Defender for Endpoint settings (advanced features, device groups) | **System** > **Settings** > **Endpoints** |
| Defender XDR settings (email notifications, streaming API, alert tuning, critical assets) | **System** > **Settings** > **Microsoft Defender XDR** |
| Sentinel workspace settings | **System** > **Settings** > **Microsoft Sentinel** |
| Roles and permissions | **System** > **Permissions** |

The **search bar** at the top finds devices, users, files, IPs and URLs across all products. The **bell icon** opens notifications.

### The portal home, search and Sentinel menu

![The Incidents page in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/incidents-ss-incidents.png)

![Screenshot that shows the attack story page for an incident in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/microsoft-365-defender-portal/incidents-ss-incident-summary.png)

![Screenshot of the search bar in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/microsoft-365-defender-portal/search-panel.png)

![Screenshot of the notifications icon in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/microsoft-365-defender-portal/notifications-panel.png)

![Screenshot of the Defender portal left navigation with the Microsoft Sentinel section](https://learn.microsoft.com/en-us/azure/sentinel/media/microsoft-sentinel-defender-portal/navigation-defender-portal.png)

### The incident queue

![Screenshot of 24-hour incident graph](https://learn.microsoft.com/en-us/defender-xdr/media/incidents-queue/most-recent-incidents.png)

![Screenshot of the Incidents queue in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/incidents-queue/incidents-page.png)

![Screenshot of the time selector for the incident queue](https://learn.microsoft.com/en-us/defender-xdr/media/incidents-queue/time-selector.png)

![Screenshot of Incident page filter and column controls](https://learn.microsoft.com/en-us/defender-xdr/media/incidents-queue/incident-toolbar.png)

![The incident queue filters list](https://learn.microsoft.com/en-us/defender-xdr/media/incidents-queue/incidents-filter-bar.png)

![The Filters pane for the incident queue in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/incidents-queue/incident-filters-small.png)

![The create filter sets option for the incident queue in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/incidents-queue/fig2-newfilters.png)

![Defender Boxed as shown in the incident queue](https://learn.microsoft.com/en-us/defender-xdr/media/incident-queue/defender-boxed-recording.gif)

![Screenshot of Defender Boxed slide with the download summary option highlighted](https://learn.microsoft.com/en-us/defender-xdr/media/incident-queue/defender-boxed-summary-small.png)

![Screenshot of Defender Boxed slide with the frequency highlighted](https://learn.microsoft.com/en-us/defender-xdr/media/incident-queue/defender-boxed-frequency-small.png)

![Screenshot of Defender Boxed slide with the save option highlighted](https://learn.microsoft.com/en-us/defender-xdr/media/incident-queue/defender-boxed-save-small.png)

![Screenshot of the Defender Boxed option highlighted in the Incidents page](https://learn.microsoft.com/en-us/defender-xdr/media/incident-queue/defender-boxed-incident-small.png)

### Inside an incident

![Selecting an incident in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incident-side-panel.png)

![Screenshot that shows playing of the alerts and nodes on the attack story graph page](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/play-alert-attack-story.gif)

![Screenshot that shows the review of the entity details on the attack story graph page](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/review-entity-details-attack-story.gif)

![Screenshot where the Go Hunt option is selected on a device in an attack story](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/gohunt-attackstory.png)

![Highlighting the link to incident option in go hunt query results](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/fig2-gohunt-attackstory.png)

![Screenshot showing the blast radius context menu item](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/blast-radius.png)

![Screenshot showing the blast radius graph](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/blast-radius-graph.png)

![Screenshot showing the blast radius list](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/blast-radius-list.png)

![An example of incident details where the description is highlighted](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incident-desc-small.png)

![Screenshot of the incident graph in the Defender portal with add filter option highlighted](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incident-graph-filter-criteria.png)

![Screenshot of the incident graph in the Defender portal with add Severity filter highlighted](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incident-graph-apply-filter.png)

![Screenshot of the incident graph in the Defender portal with Entity types option highlighted](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incident-graph-hide-entity.png)

![The Alerts pane for an incident in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incident-page-alerts-small.png)

![The details of an alert within an incident in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incident-alert-page-small.png)

![Screenshot of an incident with the Activities tab opened](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incident-activities-tab.png)

![The Assets page for an incident in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incident-assets-tab-small.png)

![The Devices page for an incident in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incident-devices2.png)

![The Devices options in the Assets page in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incident-devicebar.png)

![The Users page in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incident-users2.png)

![The Mailboxes page for an incident in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incident-mailboxes2.png)

![The Apps page for an incident in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incident-apps.png)

![The Cloud resources page for an incident in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incident-assets-cloudresource-small.png)

![Screenshot of an incident with the Investigations tab showing zero investigations](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incident-investigationspage-small.png)

![The Evidence and Response page for an incident in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incidents-evidenceresponse-small.png)

![The Approve/Reject option in the Evidence and Response management pane for an incident in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/evidence-approve-small.png)

![Screenshot that shows the summary information for an incident in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incident-summary.png)

![Screenshot that shows the Similar incidents tab for an incident in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-incidents/incident-similartab-small.png)

### The alert queue

![The Alerts section in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-alerts/alerts-page-defender-small.png)

![All the filters available in the Alerts queue in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-alerts/alert-filters-small.png)

![Highlighting the custom range option in the date and time picker in the Alerts queue](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-alerts/alerts-custom-range.png)

![Highlighting the search bar in the Alerts queue](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-alerts/alerts-search-bar-small.png)

![Screenshot showing the details of an alert in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-alerts/alerts-ss-alerts-main.png)

![Screenshot of Microsoft Entra ID Protection alerts setting in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-alerts/alert-service-settings-entra.png)

![Screenshot of the Manage alert section in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-alerts/alerts-ss-alerts-manage.png)

![Screenshot of selecting an alert in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-alerts/alerts-ss-alerts-manage-select.png)

![Screenshot of managing related alerts in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-alerts/alerts-ss-alerts-select-related.png)

![Screenshot of an example of selecting recommendations for an alert](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-alerts/alerts-ss-alerts-recommendations.png)

![Screenshot of an example of alert recommendations](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-alerts/alerts-ss-alerts-recommendations-example.png)

![Screenshot of a built-in alert tuning rule details pane with the Disable action](https://learn.microsoft.com/en-us/defender-xdr/media/built-in-alert-tuning-rules/disable-built-in-alert-tuning-rule.png)

![Screenshot of Alert tuning option in Microsoft Defender XDR's Settings page](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-alerts/alert-tuning-settings.png)

![Screenshot of the Service/Detection sources area with detection sources expanded in the Tune alert pane](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-alerts/alert-tuning-select-service.png)

![Screenshot of the IOC menu in Tune an alert page](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-alerts/alert-tuning-choose-ioc2.png)

![Screenshot of the Tune alert option from an alert details pane](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-alerts/tune-alert-alert-details.png)

![Screenshot of the Tune alert pane from the Alerts page](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-alerts/tune-alert-pane-alert-details.png)

![Screenshot of the Service/Detection sources area with detection sources expanded in the Tune alert pane](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-alerts/alert-tuning-alert-details-service-sources.png)

![Screenshot of the Conditions area in the Alert tuning pane](https://learn.microsoft.com/en-us/defender-xdr/media/investigate-alerts/alert-tuning-alert-details-conditions.png)

### The Action center

![The unified Action center in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/m3d-action-center-unified.png)

![Screenshot that shows the sort, filter, and customize capabilities of the Action center](https://learn.microsoft.com/en-us/defender-xdr/media/m365d-action-center/m3d-action-center-columnsfilters.png)

### Threat analytics

![Screenshot of the threat analytics landing page](https://learn.microsoft.com/en-us/defender-xdr/media/threat-analytics/ta_inlandingpage_mtp.png)

![Screenshot of the threat analytics dashboard](https://learn.microsoft.com/en-us/defender-xdr/media/threat-analytics/ta_dashboard_mtp.png)

![Screenshot of the threat analytics report types](https://learn.microsoft.com/en-us/defender-xdr/media/threat-analytics/ta-dashboard-tags.png)

![Screenshot of the threat analytics Add filters option](https://learn.microsoft.com/en-us/defender-xdr/media/threat-analytics/ta-taglist-mtp.png)

![Screenshot of the Filters list in Threat tags](https://learn.microsoft.com/en-us/defender-xdr/media/threat-analytics/ta-threattag-filters-mtp.png)

![Screenshot of the overview section of a threat analytics report](https://learn.microsoft.com/en-us/defender-xdr/media/threat-analytics/ta_overview_mtp.png)

![Screenshot of the related incidents section of a threat analytics report](https://learn.microsoft.com/en-us/defender-xdr/media/threat-analytics/ta_related_incidents_mtp.png)

![Screenshot of the impacted assets section of a threat analytics report](https://learn.microsoft.com/en-us/defender-xdr/media/threat-analytics/ta_impacted_assets_mtp.png)

![The Endpoints exposure section of a threat analytics report](https://learn.microsoft.com/en-us/defender-xdr/media/threat-analytics/ta_mitigations_mtp2.png)

![The Recommended actions section of a threat analytics report showing vulnerability details](https://learn.microsoft.com/en-us/defender-xdr/media/threat-analytics/ta_mitigations_mtp.png)

![Screenshot of the Indicators tab in a threat analytics report](https://learn.microsoft.com/en-us/defender-xdr/media/ta-indicators/indicators-full.png)

![Screenshot of the Threat Intelligence Briefing Agent banner on top of the Threat analytics page](https://learn.microsoft.com/en-us/defender-xdr/media/ti-briefing-agent/agent.png)

![Screenshot of custom detection setup page with Threat analytics option highlighted](https://learn.microsoft.com/en-us/defender-xdr/media/threat-analytics/ta-custom-detection.png)

## What the exam assumes you know

- An **incident** groups **alerts**. You close, assign and classify the incident.
- Which portal: Defender XDR work happens at `security.microsoft.com`. Since Sentinel moved in, nearly all SC-200 analyst work is here. The Azure portal remains for Azure resources: the workspace, roles, Logic Apps.
- ==!The Action center is not the incident queue.== It lists *remediation actions* (quarantine a file, isolate a device), not incidents.
- ==+Pending actions need approval in the Action center or on the incident's Evidence and Response tab.==

## Skip list

- **Skip:** **Defender Boxed** (the yearly "your year in security" slideshow in the incident queue). Its screenshots are above because they are in the cited article. It is not exam content.
- **Skip:** **blast radius** graphs in the attack story. They are built on the Sentinel data lake and are new. Know that the attack story graph exists; skip the blast-radius walk-through.
- **Skip:** every filter in the incident and alert queues. Know that filters exist and the defaults above.
- **Skip:** **alert tuning** rule fields (IOC selection, scope, conditions). It appears in the alerts article; it gets its own treatment in the Defender XDR objective pages.
- **Skip:** the notifications panel types (Success, Ongoing, Information, Warning, Error) and how search history is stored. Pure UI.
- **Skip:** the Threat Intelligence Briefing Agent banner and Security Copilot add-ons on these pages. Copilot is covered in its own domain.
- **Skip:** the Defender for IoT and Insider Risk Management filters in the queue. Know only that these sources can feed the same queue.
