+++
slug = "conditional-access-basics"
title = "Microsoft Entra Conditional Access basics"
summary = "You will know what a Conditional Access policy is (if this sign-in, then that control), its parts (users, target resources, network, conditions incl. user risk and sign-in risk, grant and session controls), report-only mode, named locations, the P1 versus P2 licence split, where it lives in the Entra admin center, and why risk policies now live in Conditional Access instead of ID Protection."
order = 19
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview",
  "https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-policies",
  "https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-report-only",
  "https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-assignment-network",
  "https://learn.microsoft.com/en-us/entra/id-protection/concept-identity-protection-policies",
]
captured = 2026-11-12
related_objectives = ["D2.1.4", "D2.1.5"]
+++

## In one sentence

**Conditional Access** is the rule engine inside **Microsoft Entra ID** (Microsoft's cloud identity service) that looks at every sign-in and decides: allow it, allow it only after an extra check such as MFA, or block it.

## Why it exists

A password alone proves very little. Attackers phish passwords, guess them, or buy them. So the question "is this the right password?" is not enough. You also want to ask: *who* is this, *what* are they opening, *where* are they coming from, on *what device*, and *how suspicious* does it look?

Think of a building's door system. Your badge gets you in (the password). But the door system also knows the time, which door you are at, and whether security has flagged your badge. At 3 a.m. on the server-room door it asks for a PIN as well. If your badge was reported stolen, the door stays shut.

Conditional Access is that door system for Microsoft 365 and Azure sign-ins. Microsoft calls it its **Zero Trust policy engine**. Zero Trust means "never trust a sign-in just because it reached you; verify it every time."

For a SOC (security operations centre) analyst it matters in two ways. First, Conditional Access is often *why* a sign-in failed or succeeded, and the sign-in log tells you which policy applied. Second, it is the enforcement arm for identity risk: when **Microsoft Entra ID Protection** says a user is probably compromised, a Conditional Access policy is what forces the password change or the block (D2.1.5).

## Mental model

A policy is an **if-then** statement.

- **If** (the *assignments*): this user or group, opening this app, from this network, under these conditions...
- **Then** (the *access controls*): block, or grant only if they pass these checks, and shape the session like this.

```svg
<svg viewBox="0 0 900 400" role="img" aria-label="Conditional Access flow: signals such as user, app, network location, device and risk feed the Conditional Access engine after the password check; the engine evaluates every matching policy and ends in one of three outcomes: block, grant with controls such as MFA or password change, or grant; report-only policies are evaluated and logged but never enforced">
  <defs>
    <marker id="cabarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <text x="120" y="28" text-anchor="middle" class="label-accent">Signals (the "if")</text>
  <rect class="box" x="20" y="40" width="200" height="40" rx="6"/>
  <text x="120" y="65" text-anchor="middle">User / group / role</text>
  <rect class="box" x="20" y="88" width="200" height="40" rx="6"/>
  <text x="120" y="113" text-anchor="middle">Target app or action</text>
  <rect class="box" x="20" y="136" width="200" height="40" rx="6"/>
  <text x="120" y="161" text-anchor="middle">Network / location</text>
  <rect class="box" x="20" y="184" width="200" height="40" rx="6"/>
  <text x="120" y="209" text-anchor="middle">Device platform, client app</text>
  <rect class="box-risk" x="20" y="232" width="200" height="40" rx="6"/>
  <text x="120" y="257" text-anchor="middle">User risk / sign-in risk</text>
  <text x="120" y="292" text-anchor="middle" class="muted">risk comes from ID Protection (P2)</text>
  <rect class="box-accent" x="300" y="100" width="250" height="120" rx="10"/>
  <text x="425" y="135" text-anchor="middle" class="label-accent">Conditional Access</text>
  <text x="425" y="160" text-anchor="middle">runs after the password</text>
  <text x="425" y="183" text-anchor="middle">every matching policy</text>
  <text x="425" y="203" text-anchor="middle" class="muted">must be satisfied (AND)</text>
  <rect class="box-risk" x="630" y="40" width="250" height="60" rx="8"/>
  <text x="755" y="66" text-anchor="middle" class="label-risk">Block</text>
  <text x="755" y="88" text-anchor="middle" class="muted">stops here, nothing else asked</text>
  <rect class="box" x="630" y="125" width="250" height="70" rx="8"/>
  <text x="755" y="151" text-anchor="middle">Grant, if controls met</text>
  <text x="755" y="174" text-anchor="middle" class="muted">MFA, compliant device,</text>
  <text x="755" y="190" text-anchor="middle" class="muted">password change...</text>
  <rect class="box-ok" x="630" y="220" width="250" height="60" rx="8"/>
  <text x="755" y="246" text-anchor="middle">Session controls</text>
  <text x="755" y="268" text-anchor="middle" class="muted">sign-in frequency, App Control</text>
  <line class="line-accent" x1="220" y1="155" x2="298" y2="160" marker-end="url(#cabarrow)"/>
  <line class="line-accent" x1="550" y1="140" x2="628" y2="72" marker-end="url(#cabarrow)"/>
  <line class="line-accent" x1="550" y1="160" x2="628" y2="160" marker-end="url(#cabarrow)"/>
  <line class="line" x1="755" y1="195" x2="755" y2="218" marker-end="url(#cabarrow)"/>
  <line class="divider" x1="20" y1="320" x2="880" y2="320"/>
  <rect class="box" x="300" y="335" width="580" height="50" rx="8"/>
  <text x="590" y="358" text-anchor="middle">Report-only: evaluated and written to the sign-in log,</text>
  <text x="590" y="376" text-anchor="middle" class="muted">but never blocks or prompts the user</text>
  <text x="150" y="365" text-anchor="middle" class="muted">policy state: On / Off / Report-only</text>
</svg>
```

Two rules make the picture work. Conditional Access runs ==@after first-factor authentication== (after the password or other first factor). It is not a denial-of-service shield. And when several policies match one sign-in, ==all of them must be satisfied==. If one says MFA and another says compliant device, the user needs both.

![Diagram showing concept of Conditional Access signals plus decision to enforce organizational policy.](https://learn.microsoft.com/en-us/entra/identity/conditional-access/media/common-conditional-access-media/conditional-access-signal-decision-enforcement.png){Microsoft's own picture: signals, then a decision, then enforcement}

![Diagram that shows Conditional Access as the Zero Trust policy engine aggregating signals from various sources.](https://learn.microsoft.com/en-us/entra/identity/conditional-access/media/overview/conditional-access-central-policy-engine-zero-trust.png){Conditional Access as the central Zero Trust policy engine, pulling signals from identity, device, location, app and risk}

## What actually matters

**1. The parts of a policy.** A policy needs at least a **name**, **users or groups**, **target resources** and a **grant or block** control. Everything else is optional.

| Part | What you set | Example |
|---|---|---|
| **Users** | include / exclude users, groups, directory roles, guests | all users except the break-glass account |
| **Target resources** | cloud apps, **user actions** (e.g. registering security info), authentication contexts | Office 365, Azure management |
| **Network** (was *Location*) | any network, trusted networks, selected **named locations** | block countries you never work from |
| **Conditions** | ==@user risk==, ==@sign-in risk==, device platforms, client apps, filter for devices | sign-in risk Medium or High |
| **Grant** | **Block access**, or grant with: require MFA, authentication strength, compliant device, Microsoft Entra hybrid joined device, approved client app, app protection policy, **password change**, terms of use | require MFA |
| **Session** | app enforced restrictions, **Conditional Access App Control**, sign-in frequency, persistent browser session, continuous access evaluation | re-authenticate every time |

With several grant controls you choose **Require all the selected controls** (the default) or **Require one of the selected controls**.

**2. Block wins.** If any matching policy says **Block access**, enforcement stops and the user is blocked. Otherwise the user is prompted for any unmet controls in a fixed order, starting with MFA.

**3. Two kinds of risk.** **Sign-in risk** is "how likely is it that *this sign-in* isn't the real owner?" It is calculated in real time. **User risk** is "how likely is it that *this account* is compromised?" — for example, its password was found in a leak. Both come from ID Protection and arrive as **Low**, **Medium** or **High**. A user who passes the required control (MFA for sign-in risk, a secure password change for user risk) **self-remediates**: their risk is cleared with no admin action.

**4. Report-only mode.** Every policy has a state: **On**, **Off** or **Report-only**. Report-only evaluates the policy on every sign-in and logs what *would* have happened, without blocking or prompting anyone. Results show on the sign-in log's **Conditional Access** and **Report-only** tabs as *Report-only: Success*, *Failure*, *User action required* or *Not applied*. Policies that use the **User actions** scope can't run in report-only. Test in report-only, then flip the toggle to **On**.

**5. Named locations.** A **named location** is a saved list of public IP ranges (IPv4 or IPv6, CIDR notation) or countries/regions. You can **Mark as trusted location**. Limits: at most **195** named locations, **2,000** IP ranges each, and masks must be larger than **/8**. The IP is the *public* address the network uses to reach the internet, not the laptop's private 10.x address. Trusted locations also improve ID Protection's risk scoring.

**6. Licences.** Conditional Access needs ==@Microsoft Entra ID P1== (Microsoft 365 Business Premium also includes it). ==!Risk-based policies (user risk, sign-in risk) need Microsoft Entra ID P2==, because the risk scores come from ID Protection. If licences lapse, existing policies stay and still apply; you can view or delete them but not edit them. **Security defaults** are a free on/off baseline available to every tenant; they are not a rule engine.

**7. Risk policies moved here.** ID Protection used to have its own **user risk policy** and **sign-in risk policy** pages. ==!Those legacy policies were retired on 1 October 2026.== Today you build them as Conditional Access policies with the user-risk or sign-in-risk condition. Microsoft's reasons: one place to manage access, report-only mode, Graph API support, combining risk with location or other conditions, several risk policies for different groups, and clearer sign-in log diagnostics. The ID Protection **MFA registration policy** still exists.

![Diagram that shows a conceptual risk-based Conditional Access policy.](https://learn.microsoft.com/en-us/entra/id-protection/media/concept-identity-protection-policies/risk-based-conditional-access-diagram.png){ID Protection scores the risk; Conditional Access acts on it}

![Diagram that shows a conceptual risk-based Conditional Access policy with self-remediation.](https://learn.microsoft.com/en-us/entra/id-protection/media/concept-identity-protection-policies/risk-based-conditional-access-policy-example.png){Self-remediation: the user passes the control and the risk clears itself}

## Where it lives

Everything is in the **Microsoft Entra admin center** — `https://entra.microsoft.com` — not the Azure portal or the Defender portal.

| Task | Path | Minimum role |
|---|---|---|
| See policies and overview | **Entra ID > Conditional Access** (Overview, Coverage, Policies) | **Security Reader** |
| Create a policy | **Entra ID > Conditional Access > Policies** > new policy | **Conditional Access Administrator** |
| Define named locations | **Entra ID > Conditional Access > Named locations** | **Conditional Access Administrator** |
| See which policy hit a sign-in | sign-in log entry > **Conditional Access** / **Report-only** tabs | Security Reader |
| Policy impact (preview) | the policy's impact view, 24 hours / 7 days / 1 month | Security Reader |

A deleted policy or named location can be restored within a **30-day** soft-delete period.

![Screenshot of the Conditional Access overview page.](https://learn.microsoft.com/en-us/entra/identity/conditional-access/media/overview/conditional-access-overview.png){Conditional Access > Overview: how many policies are on versus report-only, plus recent activity}

![Screenshot of the Conditional Access coverage tab showing application policy coverage.](https://learn.microsoft.com/en-us/entra/identity/conditional-access/media/overview/conditional-access-coverage-tab.png){Coverage tab: which apps had sign-ins with and without a policy over the last seven days}

![Screenshot of the Conditional Access policies list page.](https://learn.microsoft.com/en-us/entra/identity/conditional-access/media/overview/conditional-access-policies-list.png){Policies: every policy, its state, plus What If and New policy}

![Blank Conditional Access policy](https://learn.microsoft.com/en-us/entra/identity/conditional-access/media/concept-conditional-access-policies/conditional-access-blank-policy.png){A blank policy: Assignments on top (the "if"), Access controls below (the "then"), Enable policy toggle at the bottom}

![Screenshot showing the network assignment condition in a Conditional Access policy.](https://learn.microsoft.com/en-us/entra/identity/conditional-access/media/concept-assignment-network/network-assignment.png){The Network assignment, which used to be called Location}

![Screenshot of named locations in the Microsoft Entra admin center.](https://learn.microsoft.com/en-us/entra/identity/conditional-access/media/concept-assignment-network/named-locations.png){Named locations: IP ranges and countries, with a Trusted column}

![Screenshot of creating a new location using countries.](https://learn.microsoft.com/en-us/entra/identity/conditional-access/media/concept-assignment-network/new-location-countries.png){A countries location, determined by IP address or GPS, with the Include unknown countries/regions option}

![Screenshot of a sign-in risk-based Conditional Access policy.](https://learn.microsoft.com/en-us/entra/id-protection/media/concept-identity-protection-policies/sign-in-risk-policy.png){A sign-in risk policy: the sign-in risk condition set to chosen levels}

![Screenshot of Conditional Access policy impact example.](https://learn.microsoft.com/en-us/entra/identity/conditional-access/media/concept-conditional-access-report-only/policy-impact-example-report-only.png){Policy impact: what a report-only policy would have done to real sign-ins}

![Screenshot showing the report-only tab in a sign-in log.](https://learn.microsoft.com/en-us/entra/identity/conditional-access/media/concept-conditional-access-report-only/report-only-detail-in-sign-in-log.png){The Report-only tab on one sign-in log entry — where an analyst checks what a test policy would have done}

## What the exam assumes you know

- Conditional Access is ==+if-then rules on sign-ins==, managed in the **Entra admin center**. It is not a firewall and not a SIEM rule.
- ==!Report-only does not block or prompt anyone.== It only logs.
- ==!Risk conditions need P2.== Plain Conditional Access needs P1.
- **User risk** is about the account; **sign-in risk** is about one sign-in. Don't swap them.
- ==+Since 1 October 2026, user-risk and sign-in-risk policies are built in Conditional Access==, not under ID Protection. Older training still shows the legacy pages.
- **Conditional Access App Control** is a *session control* that routes the session through Defender for Cloud Apps (D2.1.4).
- Detail on risky users, risky sign-ins and remediation is in D2.1.5.

## Skip list

- **Skip** the full grant-control prompt order (MFA, compliant device, hybrid join, approved client app, app protection, password change, terms of use, custom controls). Know that **Block** wins and MFA comes first.
- **Skip** GPS-based named locations and the Microsoft Authenticator hourly location check. Admin design detail, not SOC work.
- **Skip** MFA trusted IPs and Global Secure Access compliant network. Legacy setting and a separate product.
- **Skip** workload identity targeting, filter-for-devices syntax and authentication contexts. Admin configuration.
- **Skip** the Conditional Access Insights and Reporting workbook setup (needs a Log Analytics workspace receiving sign-in logs). Know report-only results show in the sign-in log.
- **Skip** the Conditional Access Optimization Agent (Security Copilot, needs P1 and SCUs). Agents in general are on the AI agents primer and D2.1.8.
- **Skip** the risk-remediation internals (AppId, attacker-added device handling). Covered at exam depth in D2.1.5.
