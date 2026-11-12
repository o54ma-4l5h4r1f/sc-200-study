+++
slug = "azure-rbac-and-entra-roles"
title = "Azure RBAC, Microsoft Entra roles and Defender unified RBAC"
summary = "The three separate permission systems a SOC analyst meets — Azure RBAC for Azure resources, Microsoft Entra roles for the directory and Microsoft 365 admin portals, and Defender unified RBAC for the Defender portal — and where each one is assigned."
order = 6
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/azure/role-based-access-control/overview",
  "https://learn.microsoft.com/en-us/azure/role-based-access-control/rbac-and-directory-admin-roles",
  "https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/concept-understand-roles",
  "https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference",
  "https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/manage-roles-portal",
  "https://learn.microsoft.com/en-us/defender-xdr/manage-rbac",
  "https://learn.microsoft.com/en-us/defender-xdr/create-custom-rbac-roles",
  "https://learn.microsoft.com/en-us/azure/sentinel/roles",
]
captured = 2026-11-12
related_objectives = ["D1.2.1"]
+++

## In one sentence

Microsoft has **three separate permission systems** a SOC analyst runs into: **Azure RBAC** decides who can touch Azure *resources* (like the workspace Microsoft Sentinel lives in), **Microsoft Entra roles** decide who can run the *directory* and the Microsoft 365 / security admin portals, and **Defender unified RBAC** decides what you can see and do *inside* the Microsoft Defender portal.

## Why it exists

Think of a large office building. The **landlord's key system** controls which floors and rooms you can enter (Azure RBAC — rooms are Azure resources). The **HR department** controls who is on staff, who gets a badge and who is a manager (Entra roles — the directory of people). The **security desk's own rota** controls who may watch which CCTV screens and press which alarm buttons (Defender unified RBAC).

Each system grew up for a different job. A key to the server room does not make you an HR manager. Being an HR manager does not give you a key to the server room. The exam tests exactly this separation.

**RBAC** stands for *role-based access control*: you do not give people individual permissions; you give them a **role**, which is a named bundle of permissions. **Least privilege** means giving each person the smallest role that lets them do their job, and nothing more.

## Mental model

```svg
<svg viewBox="0 0 780 360" role="img" aria-label="Three separate permission systems: Azure RBAC for Azure resources, Microsoft Entra roles for the directory and Microsoft 365 portals, and Defender unified RBAC for the Defender portal">
  <text x="390" y="26" text-anchor="middle" class="muted">One person, three separate locks</text>
  <rect class="box-accent" x="20" y="45" width="235" height="290" rx="10"/>
  <text x="137" y="72" text-anchor="middle" class="label-accent">Azure RBAC</text>
  <text x="137" y="96" text-anchor="middle">Azure resources</text>
  <text x="137" y="126" text-anchor="middle" class="muted">subscriptions, resource groups,</text>
  <text x="137" y="146" text-anchor="middle" class="muted">Log Analytics workspace, VMs</text>
  <text x="137" y="182" text-anchor="middle">Owner · Contributor · Reader</text>
  <text x="137" y="206" text-anchor="middle">Microsoft Sentinel Reader /</text>
  <text x="137" y="226" text-anchor="middle">Responder / Contributor</text>
  <text x="137" y="266" text-anchor="middle" class="muted">assigned in</text>
  <text x="137" y="288" text-anchor="middle">Azure portal</text>
  <text x="137" y="308" text-anchor="middle">Access control (IAM)</text>
  <rect class="box" x="272" y="45" width="235" height="290" rx="10"/>
  <text x="389" y="72" text-anchor="middle" class="label-accent">Microsoft Entra roles</text>
  <text x="389" y="96" text-anchor="middle">the directory + M365 admin</text>
  <text x="389" y="126" text-anchor="middle" class="muted">users, groups, passwords,</text>
  <text x="389" y="146" text-anchor="middle" class="muted">security portals tenant-wide</text>
  <text x="389" y="182" text-anchor="middle">Global Administrator</text>
  <text x="389" y="206" text-anchor="middle">Security Administrator</text>
  <text x="389" y="226" text-anchor="middle">Security Operator · Security Reader</text>
  <text x="389" y="266" text-anchor="middle" class="muted">assigned in</text>
  <text x="389" y="288" text-anchor="middle">Entra admin center</text>
  <text x="389" y="308" text-anchor="middle">Entra ID > Roles &amp; admins</text>
  <rect class="box-ok" x="524" y="45" width="235" height="290" rx="10"/>
  <text x="641" y="72" text-anchor="middle" class="label-accent">Defender unified RBAC</text>
  <text x="641" y="96" text-anchor="middle">inside the Defender portal</text>
  <text x="641" y="126" text-anchor="middle" class="muted">incidents, hunting, devices,</text>
  <text x="641" y="146" text-anchor="middle" class="muted">email, Sentinel workspaces</text>
  <text x="641" y="182" text-anchor="middle">custom roles built from</text>
  <text x="641" y="206" text-anchor="middle">permission groups +</text>
  <text x="641" y="226" text-anchor="middle">data sources</text>
  <text x="641" y="266" text-anchor="middle" class="muted">assigned in</text>
  <text x="641" y="288" text-anchor="middle">security.microsoft.com</text>
  <text x="641" y="308" text-anchor="middle">Permissions > Defender XDR > Roles</text>
</svg>
```

An **Azure role assignment** always has three parts. Learn it as a sentence: *who* gets *what* *where*.

- **Security principal** (who) — a user, a group, a **service principal** (an app's identity) or a **managed identity** (an identity Azure creates and manages for a resource).
- **Role definition** (what) — the bundle of permissions, for example Reader.
- **Scope** (where) — one of four levels: **management group**, **subscription**, **resource group** or **resource**.

```svg
<svg viewBox="0 0 760 170" role="img" aria-label="Azure RBAC scope levels from management group down to resource; an assignment at a higher level is inherited by everything below it">
  <defs>
    <marker id="arer-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <rect class="box" x="15" y="40" width="160" height="60" rx="8"/>
  <text x="95" y="67" text-anchor="middle">Management group</text>
  <text x="95" y="88" text-anchor="middle" class="muted">folder of subscriptions</text>
  <rect class="box" x="205" y="40" width="160" height="60" rx="8"/>
  <text x="285" y="67" text-anchor="middle">Subscription</text>
  <text x="285" y="88" text-anchor="middle" class="muted">billing + access boundary</text>
  <rect class="box-accent" x="395" y="40" width="160" height="60" rx="8"/>
  <text x="475" y="67" text-anchor="middle" class="label-accent">Resource group</text>
  <text x="475" y="88" text-anchor="middle" class="muted">e.g. rg-soc</text>
  <rect class="box-ok" x="585" y="40" width="160" height="60" rx="8"/>
  <text x="665" y="67" text-anchor="middle">Resource</text>
  <text x="665" y="88" text-anchor="middle" class="muted">e.g. the workspace</text>
  <line x1="175" y1="70" x2="203" y2="70" class="line-accent" marker-end="url(#arer-arrow)"/>
  <line x1="365" y1="70" x2="393" y2="70" class="line-accent" marker-end="url(#arer-arrow)"/>
  <line x1="555" y1="70" x2="583" y2="70" class="line-accent" marker-end="url(#arer-arrow)"/>
  <text x="380" y="135" text-anchor="middle">Assign once at a parent — every child below inherits it.</text>
  <text x="380" y="158" text-anchor="middle" class="muted">Permissions add up across all your assignments.</text>
</svg>
```

![Diagram showing the security principal types for a role assignment](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/shared/rbac-security-principal.png){Who: the four kinds of security principal — user, group, service principal, managed identity}

![Diagram showing role definition example for a role assignment](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/shared/rbac-role-definition.png){What: a role definition is a list of allowed actions}

![Diagram showing scope levels for a role assignment](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/shared/rbac-scope.png){Where: the four scope levels}

![Diagram showing how security principal, role definition, and scope create a role assignment](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/overview/rbac-overview.png){A full role assignment: the Marketing group gets Contributor on the pharma-sales resource group}

## What actually matters

- **Azure RBAC is additive.** Your effective permission is the *sum* of all your assignments. Contributor on the subscription plus Reader on one resource group still means Contributor on that resource group. Group membership counts too, even through nested groups.
- **Inheritance flows down.** Assign Microsoft Sentinel Responder on the resource group that holds the workspace, and it covers the workspace too.
- **The big three Azure roles.** **Owner** = full control *and* can assign roles. **Contributor** = full control, but ==!cannot assign roles==. **Reader** = view only. Two more manage access only: **User Access Administrator** and **Role Based Access Control Administrator**.
- **The four security Entra roles** work tenant-wide, across the security portals:

| Entra role | In plain words |
|---|---|
| ==@Global Administrator== | Everything in Entra ID and Microsoft 365. Keep for emergencies only. |
| ==@Security Administrator== | Manage security policies and settings, and manage threats and alerts, across the security portals. |
| ==@Security Operator== | Everything Security Reader can do, plus investigate and respond to alerts and take identity containment actions. |
| ==@Security Reader== | Read-only view of security information and reports. |

- **Global Administrator does ==!not== automatically control Azure resources.** It can flip an *elevate access* switch (**Access management for Azure resources**) that grants itself User Access Administrator on all subscriptions. Without that, a Global Administrator cannot open your Sentinel workspace.
- **Defender unified RBAC** replaces the separate per-product permission screens with one place. You build **custom roles** from four permission groups: **Security operations**, **Security posture**, **Authorization and settings**, and **Data operations** (preview). You then assign them to users or groups, per **data source** (Defender for Endpoint, Defender for Office 365, Microsoft Sentinel workspaces, and so on). It only takes over a workload after you **activate** it. Sentinel workspaces are activated one by one.
- **Microsoft Sentinel has its own Azure roles** — Microsoft Sentinel Reader, Responder, Contributor, Playbook Operator and Automation Contributor. They are Azure RBAC roles on the workspace's resource group. The detail and the exam traps are on the D1.2.1 objective page.

![Diagram showing how role assignments are transitive for groups](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/overview/rbac-groups-transitive.png){Nested groups: a user inherits roles assigned to a parent group}

![Diagram showing how multiple role assignments overlap](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/overview/rbac-multiple-roles.png){Additive model: Contributor at subscription plus Reader on a resource group still gives Contributor everywhere below}

![Evaluation logic flowchart for determining access to a resource](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/overview/evaluation-logic.png){How Azure decides: deny assignments first, then roles, then optional conditions}

![Diagram showing Azure RBAC data in multiple regions](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/overview/rbac-data-stored.png){Role assignments are stored globally, so they work in every region}

![Diagram of the different roles in Azure](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/rbac-and-directory-admin-roles/rbac-admin-roles.png){How Azure roles, Entra roles and the retired classic administrator roles relate}

![Diagram that shows Azure RBAC versus Microsoft Entra roles](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/rbac-and-directory-admin-roles/azure-roles-entra-roles.png){Azure roles cover Azure resources; Entra roles cover the directory and Microsoft 365}

![Azure RBAC versus Microsoft Entra roles](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/media/concept-understand-roles/azure-roles-azure-ad-roles.png){The same split, drawn from the Entra documentation}

![The three categories of Microsoft Entra built-in roles](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/media/concept-understand-roles/role-overlap-diagram.png){Entra roles come in three kinds: Entra-only, service-specific, and cross-service (Global Administrator, Security Administrator, Security Reader)}

## Where it lives

| System | Portal | Path |
|---|---|---|
| Azure RBAC | Azure portal (`portal.azure.com`) | Any scope (subscription, resource group, resource) > **Access control (IAM)** > **Add** > **Add role assignment** |
| Microsoft Entra roles | Microsoft Entra admin center (`entra.microsoft.com`) | **Entra ID** > **Roles & admins** > pick a role > **Add assignments** (older screenshots say **Identity** > **Roles & admins**) |
| Defender unified RBAC | Microsoft Defender portal (`security.microsoft.com`) | **System** > **Permissions** > **Microsoft Defender XDR** > **Roles** > **Create custom role** |

To *manage* roles in Defender unified RBAC you must be at least **Security Administrator** in Entra ID, or hold a custom role that includes the **Authorization** permission. To *activate* a Sentinel workspace in unified RBAC you need Security Administrator **and** either subscription Owner, or User Access Administrator plus Sentinel Contributor on the workspace.

CLI equivalents exist for Azure RBAC (`az role assignment create`) and for Entra roles (`New-MgRoleManagementDirectoryRoleAssignment` in Microsoft Graph PowerShell). You will not need them for SC-200.

![Screenshot of Access control (IAM) page in the Azure portal](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/shared/sub-role-assignments.png){Azure portal: the Access control (IAM) page at subscription scope}

![Screenshot of built-in roles in the Azure portal](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/shared/roles-list.png){The Roles tab lists built-in and custom Azure roles}

![Screenshot of Microsoft Entra roles in the Azure portal](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/rbac-and-directory-admin-roles/directory-admin-roles.png){Entra roles listed on the Roles and administrators page}

![Screenshot of Roles and administrators page in Microsoft Entra admin center](https://learn.microsoft.com/en-us/entra/media/common/entra-roles-admins.png){Entra admin center: Roles and admins}

![Screenshot of Roles and administrators page with mouse over role name](https://learn.microsoft.com/en-us/entra/media/common/entra-roles-admins-mouse.png){Select the role name itself, not the check box, to open it}

![Screenshot of Add assignments pane for selected role](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/media/manage-roles-portal/add-assignments.png){Add assignments: pick users or role-assignable groups}

![Screenshot of App registrations in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/media/manage-roles-portal/app-reg.png){Entra roles can also be scoped to a single app registration}

![Screenshot of Roles for an app registration in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/media/manage-roles-portal/app-reg-roles.png){Roles and administrators inside one app registration}

![Screenshot of Add role assignment scoped to an app registration in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/media/manage-roles-portal/app-reg-add-assignment.png){Assigning a role over one app only}

![Screenshot of administrative units in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/media/manage-roles-portal/admin-units.png){Administrative units: a sub-set of the directory that a role can be limited to}

![Screenshot of Roles and administrators menu under administrative units in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/media/manage-roles-portal/admin-units-roles.png){Roles that can be assigned over an administrative unit}

![Screenshot of the permissions and roles page](https://learn.microsoft.com/en-us/defender-xdr/media/create-custom-rbac-roles/m365-defender-rbac-authorization-role.png){Defender portal: a custom unified RBAC role with the Authorization permission}

## What the exam assumes you know

- Which system a task belongs to. "Let an analyst close Sentinel incidents" → Azure RBAC (Microsoft Sentinel Responder). "Let an analyst respond to alerts across the security portals" → Entra **Security Operator**, or a Defender unified RBAC role. "Let someone reset passwords" → an Entra role, never Azure RBAC.
- ==!Contributor cannot grant access.== Only Owner, User Access Administrator or Role Based Access Control Administrator can.
- ==!Security Reader is not "Reader".== One is an Entra role (security portals); the other is an Azure role (Azure resources).
- Least privilege: the right answer is the *smallest* role that works. ==+Assign to a group, at the narrowest scope.== Global Administrator is almost never the right answer.

## Skip list

- **Skip:** the 100+ Azure built-in roles in the reference list. Know Owner, Contributor, Reader, User Access Administrator, and the Sentinel roles (on D1.2.1). The rest belong to other products.
- **Skip:** the classic subscription administrator roles (Account Administrator, Service Administrator, Co-Administrator). They are fully retired as of May 2026. The article still spends a whole section on them.
- **Skip:** writing Azure custom role JSON (`Actions`, `NotActions`, `DataActions`). Know that custom roles exist in all three systems. SC-200 does not ask you to author one.
- **Skip:** Entra role *permission strings* such as `microsoft.directory/...`. The plain-words table above is what gets tested.
- **Skip:** administrative units and app-registration scope for Entra roles. They are shown above because the screenshots are in the cited article. For SC-200, assume Entra roles are tenant-wide.
- **Skip:** the unified RBAC migration, import and multi-tenant (GDAP) pages. That is admin rollout work, not analyst work.
- **Skip:** Privileged Identity Management (PIM) *eligible* versus *active* assignments. The Add assignments screen looks different with Entra ID P2 and PIM; know only that PIM exists to make admin roles time-limited.
- **Skip:** Azure ABAC role assignment *conditions*. They appear in the evaluation flowchart above, but SC-200 does not test them.
