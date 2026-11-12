+++
slug = "entra-id-basics"
title = "Microsoft Entra ID basics: users, groups, apps and managed identities"
summary = "What Microsoft Entra ID is and the identity objects a SOC analyst meets every day — member and guest users, security and Microsoft 365 groups, assigned and dynamic membership, sign-in and audit logs, app registrations versus enterprise apps, managed identities (and why Sentinel playbooks use them), MFA, Conditional Access, and which licence (P1 or P2) unlocks what."
order = 5
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/entra/fundamentals/whatis",
  "https://learn.microsoft.com/en-us/entra/fundamentals/new-name",
  "https://learn.microsoft.com/en-us/entra/external-id/user-properties",
  "https://learn.microsoft.com/en-us/entra/fundamentals/concept-learn-about-groups",
  "https://learn.microsoft.com/en-us/entra/identity/users/groups-dynamic-membership",
  "https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-ins",
  "https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-audit-logs",
  "https://learn.microsoft.com/en-us/entra/identity/monitoring-health/howto-access-activity-logs",
  "https://learn.microsoft.com/en-us/entra/identity/monitoring-health/reference-reports-data-retention",
  "https://learn.microsoft.com/en-us/entra/identity-platform/app-objects-and-service-principals",
  "https://learn.microsoft.com/en-us/graph/api/resources/applications-api-overview",
  "https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview",
  "https://learn.microsoft.com/en-us/azure/sentinel/automation/authenticate-playbooks-to-sentinel",
  "https://learn.microsoft.com/en-us/entra/identity/authentication/concept-mfa-howitworks",
  "https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview",
  "https://learn.microsoft.com/en-us/entra/id-protection/overview-identity-protection",
  "https://learn.microsoft.com/en-us/entra/fundamentals/licensing",
]
captured = 2026-11-12
+++

## In one sentence

**Microsoft Entra ID** (formerly Azure Active Directory) is Microsoft's cloud identity service: the directory that holds every user, group and application of an organisation, checks who they are when they sign in, and records every sign-in and change.

## Why it exists

Think of an office badge system. Reception keeps the list of staff and visitors. Doors check badges; some also want a PIN. Every swipe is logged.

Entra ID is that badge system for the cloud. The list is the **tenant** (the organisation's directory). The badges are **user accounts**. Groups of people share door rights through **groups**. Programs that act on their own — a script, a playbook — need badges too: **service principals** and **managed identities**. The PIN is **multifactor authentication (MFA)**. The door rules are **Conditional Access**. The swipe log is the **sign-in log**.

Every Microsoft 365 or Azure customer already has one. Microsoft states: "every tenant is automatically a Microsoft Entra tenant". For a SOC analyst, Entra ID matters twice. It is the **front door attackers try to steal keys to** (phishing, password spray). And its logs are among the first data you connect to Microsoft Sentinel.

![Diagram showing the new name for Azure AD and Azure AD External Identities](https://learn.microsoft.com/en-us/entra/fundamentals/media/new-name/azure-ad-new-name.png){Azure Active Directory was renamed Microsoft Entra ID — older docs and exam-prep sites still say "Azure AD"}

## Mental model

```svg
<svg viewBox="0 0 820 470" role="img" aria-label="Inside an Entra tenant: human identities (member and guest users), groups (security and Microsoft 365, assigned or dynamic), and workload identities (app registration with its service principal, and managed identities, system-assigned and user-assigned), with a Sentinel playbook using a managed identity">
  <rect class="box-accent" x="10" y="10" width="800" height="450" rx="12"/>
  <text x="410" y="36" text-anchor="middle" class="label-accent">Microsoft Entra tenant — contoso.onmicrosoft.com</text>
  <rect class="box" x="30" y="55" width="240" height="180" rx="10"/>
  <text x="150" y="80" text-anchor="middle" class="label-accent">People (users)</text>
  <rect class="box-ok" x="45" y="95" width="210" height="55" rx="6"/>
  <text x="150" y="118" text-anchor="middle">Member</text>
  <text x="150" y="138" text-anchor="middle" class="muted">employee, full member rights</text>
  <rect class="box-risk" x="45" y="160" width="210" height="60" rx="6"/>
  <text x="150" y="184" text-anchor="middle">Guest</text>
  <text x="150" y="204" text-anchor="middle" class="muted">outsider, restricted rights</text>
  <rect class="box" x="290" y="55" width="240" height="180" rx="10"/>
  <text x="410" y="80" text-anchor="middle" class="label-accent">Groups</text>
  <text x="410" y="108" text-anchor="middle">Type: Security | Microsoft 365</text>
  <text x="410" y="132" text-anchor="middle" class="muted">access rights | collaboration</text>
  <line class="divider" x1="305" y1="148" x2="515" y2="148"/>
  <text x="410" y="174" text-anchor="middle">Membership: Assigned | Dynamic</text>
  <text x="410" y="198" text-anchor="middle" class="muted">added by hand | added by rule</text>
  <text x="410" y="220" text-anchor="middle" class="muted">(dynamic needs P1)</text>
  <rect class="box" x="550" y="55" width="240" height="180" rx="10"/>
  <text x="670" y="80" text-anchor="middle" class="label-accent">Workload identities</text>
  <text x="670" y="104" text-anchor="middle">(programs, not people)</text>
  <text x="670" y="134" text-anchor="middle">App registration</text>
  <text x="670" y="154" text-anchor="middle" class="muted">= application object</text>
  <text x="670" y="184" text-anchor="middle">Enterprise application</text>
  <text x="670" y="204" text-anchor="middle" class="muted">= service principal</text>
  <rect class="box-ok" x="30" y="255" width="500" height="190" rx="10"/>
  <text x="280" y="280" text-anchor="middle" class="label-accent">Managed identity — Azure holds the secret for you</text>
  <rect class="box" x="45" y="295" width="225" height="135" rx="6"/>
  <text x="157" y="320" text-anchor="middle">System-assigned</text>
  <text x="157" y="344" text-anchor="middle" class="muted">switched on inside one</text>
  <text x="157" y="364" text-anchor="middle" class="muted">resource; dies with it;</text>
  <text x="157" y="384" text-anchor="middle" class="muted">can't be shared</text>
  <rect class="box" x="290" y="295" width="225" height="135" rx="6"/>
  <text x="402" y="320" text-anchor="middle">User-assigned</text>
  <text x="402" y="344" text-anchor="middle" class="muted">its own Azure resource;</text>
  <text x="402" y="364" text-anchor="middle" class="muted">lives on independently;</text>
  <text x="402" y="384" text-anchor="middle" class="muted">shareable by many</text>
  <rect class="box-accent" x="550" y="255" width="240" height="190" rx="10"/>
  <text x="670" y="282" text-anchor="middle" class="label-accent">SOC example</text>
  <text x="670" y="310" text-anchor="middle">Sentinel playbook</text>
  <text x="670" y="330" text-anchor="middle">(a Logic App)</text>
  <text x="670" y="358" text-anchor="middle">turns on its system-</text>
  <text x="670" y="378" text-anchor="middle">assigned identity, gets</text>
  <text x="670" y="398" text-anchor="middle">Microsoft Sentinel</text>
  <text x="670" y="418" text-anchor="middle">Responder role — no password</text>
</svg>
```

A tenant holds **people**, **groups** and **programs**. All of them can sign in, so all of them appear in sign-in logs — and can be attacked.

## What actually matters

**1. Tenant.** One organisation's instance of Entra ID. Every new tenant gets a starting domain like `contoso.onmicrosoft.com`; the organisation can add its own (`contoso.com`). Azure subscriptions trust one tenant for sign-in (see the Azure resource hierarchy page).

**2. Users: member versus guest.** The user property **UserType** says how the person relates to your organisation.

| UserType | Who | Default rights |
|---|---|---|
| ==@Member== | Your employees | Member-level permissions |
| ==@Guest== | Outsiders: partners, contractors, customers | Restricted — for example, guests can't read all directory information |

Guests usually arrive through **B2B collaboration** (business-to-business) and sign in with their *own* organisation's or social account. A guest's user name contains `#EXT#`. UserType states only the relationship — not how someone signs in or which roles they hold.

**3. Groups.** Two **types**, two **membership** styles:

| | What it's for | Members can be |
|---|---|---|
| **Security group** | Granting access to resources | Users, devices, service principals, other groups |
| **Microsoft 365 group** | Collaboration (shared mailbox, Teams, files) | Users only, including people outside the organisation |

- **Assigned** membership: an admin adds members by hand.
- **Dynamic** membership: a rule adds and removes members automatically from their attributes, for example `user.department -eq "SOC"`. A dynamic group holds users **or** devices, never both. ==!Dynamic membership needs Microsoft Entra ID P1== for each user in such groups.

**4. Sign-in logs and audit logs.** Your two main Entra evidence sources.

| Log | Answers | Contains |
|---|---|---|
| **Sign-in logs** | *Who signed in, from where, did it work?* | Four kinds: interactive user, non-interactive user, **service principal**, **managed identity** sign-ins |
| **Audit logs** | *What changed?* | Changes to users, groups, applications and licences |

Retention in the portal: **7 days** on Entra ID Free, **30 days** on P1 or P2. ==!Upgrading later doesn't bring back older data.== To keep logs longer, stream them to a **Log Analytics workspace** — which is exactly what the Sentinel Entra ID connector does. The least-privileged role that can read them is **Reports Reader**.

**5. App registrations versus enterprise applications.** Every application that uses Entra ID for sign-in has two objects:

- the **application object** — the *definition* (name, permissions it wants, secrets). One per app, in its "home" tenant. You see it under **App registrations**.
- the **service principal** — the app's *identity inside one tenant*, the thing that actually signs in and gets permissions. One per tenant that uses the app. You see it under **Enterprise applications**.

Analogy: the application object is a job description; the service principal is the person hired to do it. Registering an app in the portal creates both in your tenant. A service principal signs in with a **client ID** plus a **client secret** or certificate — and that secret is a password that someone must store, rotate, and could leak.

**6. Managed identities.** A **managed identity** is a service principal whose secret Azure keeps and rotates for you. Nobody — not even you — can see the credential. Two kinds:

| | System-assigned | User-assigned |
|---|---|---|
| Created | Switched on inside one Azure resource | As its own Azure resource |
| Lifetime | Deleted when that resource is deleted | Lives until you delete it |
| Sharing | One resource only | Many resources can share it |

Managed identities cost nothing extra. Their sign-ins appear in the sign-in logs; their creation and deletion appear in the Azure **Activity log**.

**Why Sentinel playbooks use them.** A playbook is a **Logic App** (Azure's no-code workflow tool). To read or update an incident, it must authenticate to Sentinel. It can do so as a **managed identity**, a **service principal**, or a **user**. With a managed identity you enable it on the Logic App, then give it a role on the workspace: **Microsoft Sentinel Responder** if it updates incidents, **Microsoft Sentinel Reader** if it only reads them. No secret to leak, and no dependence on one person's account.

**7. MFA in one paragraph.** **Multifactor authentication** asks for two or more of: something you **know** (password), something you **have** (phone, hardware key), something you **are** (fingerprint, face). Methods include Microsoft Authenticator, passkeys (FIDO2), Windows Hello for Business, OATH tokens, SMS and voice call. A stolen password alone is no longer enough. In sign-in investigations you will check whether MFA was required and passed.

**8. Conditional Access in one paragraph.** **Conditional Access** is Entra's if-then rule engine: *if* this user, from this location, on this device, to this app, at this risk level — *then* block, or allow only with MFA, a compliant device or a password change. It runs **after** the first sign-in step (the password). It needs **Entra ID P1**. Using **risk** as a condition (from Entra ID Protection) needs **P2**. With P2, a risky sign-in can therefore trigger MFA or a secure password reset automatically, and completing it clears the risk.

**9. Licences in one table.**

| Licence | Comes with | Unlocks (SC-200-relevant) |
|---|---|---|
| **Entra ID Free** | Any Azure or Microsoft 365 subscription | Users, groups, basic sign-in and audit logs (7 days) |
| **Entra ID P1** | Microsoft 365 E3/E5, EMS E3, Business Premium | Conditional Access, dynamic groups, 30-day logs |
| **Entra ID P2** | Microsoft 365 E5, Microsoft Defender Suite, EMS E5 | Everything in P1 + ==@Entra ID Protection== (risky users, risky sign-ins, risk-based Conditional Access) |

## Where it lives

Everything is in the **Microsoft Entra admin center** — `https://entra.microsoft.com`:

| Task | Path |
|---|---|
| Users, guests | **Entra ID > Users** |
| Groups | **Entra ID > Groups** |
| App registrations (application objects) | **Entra ID > App registrations** |
| Enterprise applications (service principals) | **Entra ID > Enterprise applications** |
| Sign-in and audit logs | **Entra ID > Monitoring & health > Sign-in logs** / **Audit logs** |
| Conditional Access | **Entra ID > Conditional Access** |
| ID Protection reports | **ID Protection > Dashboard** |

Managed identities are switched on in the **Azure portal**, on the resource itself (for a playbook: on the Logic App workflow resource). Giving the playbook a Sentinel role is **Microsoft Sentinel > Settings > Workspace settings > Access control (IAM) > Add role assignment**.

![Diagram showing B2B collaboration users](https://learn.microsoft.com/en-us/entra/external-id/media/user-properties/table-user-properties.png){The four combinations: internal or external sign-in, member or guest relationship}

![Screenshot of user profile before redemption](https://learn.microsoft.com/en-us/entra/external-id/media/user-properties/before-redemption.png){A guest's profile before they accept the invitation}

![Screenshot of user profile after redemption](https://learn.microsoft.com/en-us/entra/external-id/media/user-properties/after-redemption-state-1.png){...and after}

![Screenshot showing how to add a User type filter for guests](https://learn.microsoft.com/en-us/entra/external-id/media/user-properties/add-guest-filter.png){Filtering the user list by User type}

![Screenshot showing the filter for guest users](https://learn.microsoft.com/en-us/entra/external-id/media/user-properties/filter-guest-users.png){Only guests shown — useful when hunting for unexpected outsiders}

![Screenshot showing the External users option in the user settings](https://learn.microsoft.com/en-us/entra/external-id/media/user-properties/remove-guest-limitations.png){The setting that controls how much guests can see}

![Screenshot that shows the rule builder, with the action for adding an expression highlighted](https://learn.microsoft.com/en-us/entra/identity/users/media/groups-dynamic-membership/update-dynamic-group-rule.png){Building a dynamic membership rule}

![Screenshot of the Usage & insights report](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/media/concept-sign-ins/usage-insights.png){Usage & insights — a summary built from sign-in logs}

![Screenshot of the audit logs, with the Directory and Custom Security tabs highlighted](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/media/concept-audit-logs/audit-log-tabs.png){Audit logs — every change to users, groups and apps}

![App registrations blade](https://learn.microsoft.com/en-us/entra/identity-platform/media/app-objects-and-service-principals/app-registrations-blade.png){App registrations: application objects homed in your tenant}

![Enterprise apps blade](https://learn.microsoft.com/en-us/entra/identity-platform/media/app-objects-and-service-principals/enterprise-apps-blade.png){Enterprise applications: service principals in your tenant, including apps made by others}

![Screen shot that shows the Managed application in local directory option in the overview](https://learn.microsoft.com/en-us/entra/identity-platform/media/app-objects-and-service-principals/find-service-principal.png){From an app registration, "Managed application in local directory" jumps to its service principal}

![Relationship between app object and service principal object](https://learn.microsoft.com/en-us/entra/identity-platform/media/app-objects-and-service-principals/application-objects-relationship.svg){One application object in the home tenant; one service principal in each tenant that uses the app}

How a Sentinel playbook picks its identity:

![Screenshot of the Microsoft Sentinel connector showing where to select Change connection](https://learn.microsoft.com/en-us/azure/sentinel/media/authenticate-playbooks-to-sentinel/change-connection.png){In the Logic Apps designer: Change connection}

![Screenshot of Microsoft Sentinel connector authentication options with Connect with managed identity selected](https://learn.microsoft.com/en-us/azure/sentinel/media/authenticate-playbooks-to-sentinel/auth-methods-msi-choice.png){Option 1: managed identity — no secret to manage}

![Screenshot of the Microsoft Sentinel connector showing the connection name and system-assigned managed identity options](https://learn.microsoft.com/en-us/azure/sentinel/media/authenticate-playbooks-to-sentinel/auth-methods-msi.png){Choose System-assigned managed identity}

![Screenshot of the Microsoft Sentinel connector authentication options with Connect with Service Principal selected](https://learn.microsoft.com/en-us/azure/sentinel/media/authenticate-playbooks-to-sentinel/auth-methods-spn-choice.png){Option 2: service principal}

![Screenshot of Microsoft Sentinel connector fields for service principal authentication](https://learn.microsoft.com/en-us/azure/sentinel/media/authenticate-playbooks-to-sentinel/auth-methods-spn.png){A service principal needs tenant ID, client ID and a client secret — a secret someone must protect}

![Screenshot of the Sign in button selected](https://learn.microsoft.com/en-us/azure/sentinel/media/authenticate-playbooks-to-sentinel/auth-methods-sign-in.png){Option 3: sign in as a user — the playbook then runs on one person's account}

MFA and Conditional Access:

![Conceptual image of the various forms of multifactor authentication](https://learn.microsoft.com/en-us/entra/identity/authentication/media/concept-mfa-howitworks/methods.png){Know, have, are}

![MFA sign-in screen](https://learn.microsoft.com/en-us/entra/identity/authentication/media/concept-mfa-howitworks/sign-in-screen.png){What the user sees}

![Diagram that shows how Conditional Access works to secure the sign-in process](https://learn.microsoft.com/en-us/entra/identity/authentication/media/tutorial-enable-azure-mfa/conditional-access-overview.png){Conditional Access decides when to ask for MFA}

![Diagram showing concept of Conditional Access signals plus decision to enforce organizational policy](https://learn.microsoft.com/en-us/entra/identity/conditional-access/media/common-conditional-access-media/conditional-access-signal-decision-enforcement.png){Signals in, decision, enforcement out}

![Diagram that shows Conditional Access as the Zero Trust policy engine aggregating signals from various sources](https://learn.microsoft.com/en-us/entra/identity/conditional-access/media/overview/conditional-access-central-policy-engine-zero-trust.png){Signals include user, location, device, app and ID Protection risk}

![Screenshot of the Conditional Access overview page](https://learn.microsoft.com/en-us/entra/identity/conditional-access/media/overview/conditional-access-overview.png){Conditional Access overview}

![Screenshot of the Conditional Access coverage tab showing application policy coverage](https://learn.microsoft.com/en-us/entra/identity/conditional-access/media/overview/conditional-access-coverage-tab.png){Coverage: apps with and without a policy in the last seven days}

![Screenshot of the Conditional Access policies list page](https://learn.microsoft.com/en-us/entra/identity/conditional-access/media/overview/conditional-access-policies-list.png){The policy list, including report-only policies}

![Diagram showing how ID Protection works at a high level](https://learn.microsoft.com/en-us/entra/id-protection/media/overview-identity-protection/identity-protection-overview.png){ID Protection (P2) feeds risk into Conditional Access and into your SIEM}

## What the exam assumes you know

- ==!App registration and enterprise application are not two apps.== They are two objects for one app: definition versus in-tenant identity.
- ==+For a playbook, prefer a managed identity== over a service principal with a secret or a user account.
- ==!System-assigned identities can't be shared.== If several Logic Apps need the same rights, the question wants **user-assigned**.
- Playbook role choice: **Microsoft Sentinel Responder** to update incidents, **Microsoft Sentinel Reader** to only read. Granting a role needs **Owner** or **User Access Administrator** on the workspace.
- ==!Entra ID Protection needs P2.== Conditional Access needs P1. Risk-based Conditional Access needs P2.
- Guests are users too. A compromised guest account still signs in and still shows in sign-in logs.
- Sign-in logs include **service principal** and **managed identity** sign-ins — not only people.

## Skip list

- **Skip** Entra Domain Services, Verified ID, Private Access, Internet Access, Workload ID premium and Agent ID. Not SC-200.
- **Skip** group best practices (naming policies, expiry, sensitivity labels, access packages, access reviews). Identity governance, not SOC work.
- **Skip** B2B invitation redemption, cross-cloud collaboration and email one-time passcode settings. Know member versus guest and `#EXT#`.
- **Skip** multitenant app consent flows and the "legacy" service principal type. Know application object versus service principal.
- **Skip** managed identity token code (MSAL, Azure.Identity SDK) and federated identity credentials. Developer material.
- **Skip** the full MFA method list detail and the legacy MFA settings page. Know the three factor types and that Conditional Access enforces MFA.
- **Skip** the Conditional Access Optimization Agent and the full grant-control list. Know if-then, P1, and that risk conditions need P2. Microsoft Entra roles versus Azure RBAC roles are covered on the RBAC page.
