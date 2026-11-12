# Content changelog

Outline drift, ID remaps, learn-map corrections and retired-doc notices. Newest first.

## 2026-11-12 — converted from AZ-104 to SC-200

- System converted from the AZ-104 study system (same engine, doctrine, agent fleet). All AZ-104
  content removed.
- Blueprint captured: SC-200 "Skills measured as of October 21, 2026" — 3 domains / 9 subdomains /
  54 bullets, verbatim from
  https://learn.microsoft.com/credentials/certifications/resources/study-guides/sc-200 via the
  Microsoft Learn MCP.
- Learner baseline: full beginner, Azure subscription only (no M365 E5). New **Foundations** content
  type (`content/foundations/`) and mandatory `## Azure first` section + `foundations = [...]`
  frontmatter on every objective page.
- Engine: `window.AZ104` → `window.SC200`, localStorage keys `az104.*` → `sc200.*` (old browser
  progress does not carry over), exam code read from `domains.toml`, learn-map module flag
  `az104_native` → `exam_native`.

### Learn-map corrections from the D1 authoring pass (2026-11-12)

- `mitigate-incidents-microsoft-365-defender#8`: noted outdated custom-detection limits (100 → 150 alerts/run; required → recommended columns).
- `use-entity-behavior-analytics-azure-sentinel#5`: `thin_coverage`, superseded by product docs (anomaly rules on by default).
- `analyze-data-in-sentinel#4`: D1.4.5 mapping marked weak.
- `query-data-sentinel#3`: also mapped to D3.1.2 (it is a Logs/KQL tour).
- `threat-response-sentinel-playbooks#4`: D1.1.10 mapping removed (playbook content only).
- `mitigate-incidents-microsoft-365-defender#13`: portal has three notification tabs (Incidents, Actions, Threat analytics).
- Foundations: `m365-tenants-and-licensing` attack-disruption licence line now shows Microsoft's two conflicting sources.
- `connect-windows-hosts-to-azure-sentinel#5` (Sysmon): also mapped to D1.3.3 (only unit configuring Windows Forwarded Events).
- `connect-data-to-azure-sentinel-with-data-connectors#3`: also mapped to D1.3.4; noted retired HTTP Data Collector API.
- Threat-intel units (`connect-threat-indicators-to-azure-sentinel#2,#6`, `utilize-threat-intelligence-azure-sentinel#4`): stale table / retired TIP connector noted.
- CEF/Syslog units: wrong port (514 vs AMA TCP 28330) and pre-1.28.11 Unix-socket claims noted.

### D3.2 authoring pass (2026-11-12)

- Sentinel **livestream retired**; `hunt-threats-sentinel` unit 5 (`5-livestream`) now teaches hunts — noted in learn-map.
- Doc redirect: Sentinel `summary-rules-tutorial` now redirects to the KQL jobs article.

### D2 / D3.1 authoring pass (2026-11-12)

- Learn-map stale-unit notes: ID Protection exercise (legacy risk policies retired 1 Oct 2026), `AADSignInEventsBeta` → `EntraIdSignInEvents`, Defender for DNS folded into Defender for Servers P2, hunting-graph tab naming, stale TI table in `query-logs-azure-sentinel#3`, threat-analytics unit only teaches the Briefing Agent, MDCA walkthrough is video-only.
- `domains.toml`: D3.1.5 (hunting graphs / blast radius) → `license_blocked = true` (needs Sentinel data lake + Exposure Management data from Defender workloads).
- Product changes captured on pages: DLP signals now recorded as behaviors (Oct 2026), MDCA file policies retire 6 Jan 2027, classic eDiscovery retired 31 Aug 2025, blast radius replaces attack path analysis.
- D2.1.6–D2.1.10: Defender for Identity lateral-movement-path articles retired (redirect to doc index; LMPs now on identity page Attack paths tab + Identity Explorer); `m365-threat-safeguard/review-compromised-accounts` lists outdated MDI alert categories; module `security-copilot-describe-agents` not in learn-map — check whether it is in an SC-200 path; incident cases (preview) now Microsoft's recommended experience.

### D2/D3 review pass (2026-11-12)

- Independent reviews of all D2 and D3 pages: 20 verified, 7 draft (D2.1.3/4/5/8/9, D3.1.1/2). Key corrections: `MailItemsAccessed` is Audit (Standard) per product doc; device timeline 180 days; `DisruptionAndResponseEvents` has no `IncidentId`; eDiscovery holds are core; Defender for Identity covers Entra ID/Okta via connectors; search jobs at Microsoft Sentinel > Search.
- Stale training units (noted, map unchanged): `m365-threat-remediate/automate-investigate-remediate` (overstates auto email remediation), `manage-azure-active-directory-identity-protection` #6–#8, `incident-management-sentinel` #5 (Directory Readers for all investigators). D2.1.8 thin: Security Store and newer Copilot agents are docs-only.
- 7 new Foundations: conditional-access, purview, jupyter-and-python, ai-agents-and-mcp, sentinel-data-lake, exposure-management, active-directory-and-kerberos (25 total).
