+++
slug = "ai-agents-and-mcp-basics"
title = "Generative AI, agents, MCP and Security Copilot basics"
summary = "You will know what a large language model, a prompt, grounding and a hallucination are and why a human must review AI output; what an AI agent is (goal, instructions, tools, trigger, identity, approval); how the Model Context Protocol connects an AI host to tool servers; what Microsoft Security Copilot is (standalone versus embedded, Security Compute Units, plugins, promptbooks, agents); and that a Microsoft Sentinel MCP Server exists."
order = 22
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/agent-framework/journey/llm-fundamentals",
  "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/",
  "https://learn.microsoft.com/en-us/agent-framework/journey/adding-tools",
  "https://learn.microsoft.com/en-us/dotnet/ai/get-started-mcp",
  "https://learn.microsoft.com/en-us/azure/container-apps/mcp-overview",
  "https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-mcp-overview",
  "https://learn.microsoft.com/en-us/copilot/security/microsoft-security-copilot",
  "https://learn.microsoft.com/en-us/copilot/security/experiences-security-copilot",
  "https://learn.microsoft.com/en-us/copilot/security/manage-usage",
  "https://learn.microsoft.com/en-us/copilot/security/plugin-overview",
  "https://learn.microsoft.com/en-us/copilot/security/using-promptbooks",
  "https://learn.microsoft.com/en-us/copilot/security/agents-overview",
  "https://learn.microsoft.com/en-us/copilot/security/prompting-tips",
  "https://learn.microsoft.com/en-us/copilot/security/security-copilot-inclusion",
  "https://learn.microsoft.com/en-us/copilot/security/security-copilot-application-card",
]
captured = 2026-11-12
related_objectives = ["D2.1.8", "D3.2.4", "D2.1.1"]
+++

## In one sentence

A **large language model (LLM)** writes text by predicting the next word-piece. An **AI agent** wraps an LLM with instructions, tools and a trigger so it can act. **MCP** is the standard plug that connects an AI to those tools. **Microsoft Security Copilot** is Microsoft's security product built from all three.

## Why it exists

A SOC (security operations centre) drowns in alerts. Many triage steps are reading and summarising: what does this script do, what happened in this incident, is this email phishing? Language models are good at reading and summarising. So Microsoft put one next to the analyst.

Think of a very fast, very well-read **intern**. They write a neat summary in seconds and know the jargon. But they have never seen *your* network. They sometimes state a wrong fact with total confidence. And you would not let them disable a user's account without asking. Every rule on this page follows from that picture: feed the intern your real data (grounding), check their work (human review), and limit what they may do alone (approval).

For SC-200 this is the background for D2.1.8 (agentic AI and embedded Security Copilot), the Phishing Triage Agent in D2.1.1, and the Sentinel MCP Server in D3.2.4.

## Mental model

```svg
<svg viewBox="0 0 900 430" role="img" aria-label="AI building blocks: an analyst or a trigger sends a prompt to an agent; the agent's LLM reads instructions and grounding data, and asks for tool calls; an MCP host and client connect to MCP servers such as the Sentinel MCP Server which expose tools, resources and prompts; risky actions wait for human approval; every output goes back to the analyst for review because LLMs can hallucinate">
  <defs>
    <marker id="aimbarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <rect class="box" x="20" y="40" width="160" height="70" rx="8"/>
  <text x="100" y="68" text-anchor="middle">Analyst prompt</text>
  <text x="100" y="92" text-anchor="middle" class="muted">or a trigger (schedule, alert)</text>
  <rect class="box-accent" x="230" y="20" width="300" height="210" rx="10"/>
  <text x="380" y="46" text-anchor="middle" class="label-accent">Agent</text>
  <rect class="box" x="250" y="60" width="260" height="36" rx="6"/>
  <text x="380" y="83" text-anchor="middle">Instructions (goal, limits)</text>
  <rect class="box" x="250" y="104" width="260" height="36" rx="6"/>
  <text x="380" y="127" text-anchor="middle">LLM = reasoning engine</text>
  <rect class="box" x="250" y="148" width="260" height="36" rx="6"/>
  <text x="380" y="171" text-anchor="middle">Grounding data + memory</text>
  <text x="380" y="212" text-anchor="middle" class="muted">runs as an identity with permissions</text>
  <rect class="box" x="590" y="20" width="290" height="210" rx="10"/>
  <text x="735" y="46" text-anchor="middle" class="label-accent">MCP host + client</text>
  <text x="735" y="68" text-anchor="middle" class="muted">e.g. VS Code + GitHub Copilot</text>
  <rect class="box-ok" x="610" y="84" width="250" height="56" rx="6"/>
  <text x="735" y="107" text-anchor="middle">MCP server: Sentinel</text>
  <text x="735" y="127" text-anchor="middle" class="muted">tools, resources, prompts</text>
  <rect class="box-ok" x="610" y="152" width="250" height="56" rx="6"/>
  <text x="735" y="175" text-anchor="middle">MCP server: anything else</text>
  <text x="735" y="195" text-anchor="middle" class="muted">TI lookup, ticketing...</text>
  <line class="line-accent" x1="180" y1="75" x2="228" y2="75" marker-end="url(#aimbarrow)"/>
  <line class="line-accent" x1="530" y1="122" x2="588" y2="122" marker-end="url(#aimbarrow)"/>
  <rect class="box-risk" x="230" y="260" width="300" height="70" rx="8"/>
  <text x="380" y="288" text-anchor="middle" class="label-risk">Approval gate</text>
  <text x="380" y="312" text-anchor="middle" class="muted">risky action waits for a human</text>
  <line class="line" x1="380" y1="230" x2="380" y2="258" marker-end="url(#aimbarrow)"/>
  <rect class="box-risk" x="20" y="350" width="510" height="64" rx="8"/>
  <text x="275" y="376" text-anchor="middle" class="label-risk">Human review of every answer</text>
  <text x="275" y="398" text-anchor="middle" class="muted">LLMs can hallucinate: confident, plausible, wrong</text>
  <line class="line" x1="380" y1="330" x2="380" y2="348" marker-end="url(#aimbarrow)"/>
  <text x="735" y="280" text-anchor="middle" class="muted">The LLM never runs a tool itself.</text>
  <text x="735" y="302" text-anchor="middle" class="muted">It asks; the host runs it.</text>
</svg>
```

## What actually matters

**1. Generative AI words, in plain English.**

| Term | Meaning |
|---|---|
| **LLM** | A model trained on huge amounts of text to predict the next **token** (a word-piece, roughly ¾ of an English word). |
| **Prompt** | The text you give it: your question plus any instructions. |
| **Context window** | The maximum number of tokens the model can hold at once — prompt, history and answer together. |
| **Grounding** | Adding real, relevant data (your incident, your logs) to the prompt before the model answers, so the answer is about *your* world. |
| **Hallucination** | A confident, plausible-sounding answer that is factually wrong. |
| **Non-deterministic** | The same prompt can give a different answer next time. |

LLMs have no knowledge after their training cutoff, no memory between calls, and ==!no ability to act on their own== — they only produce text. Microsoft's guidance for Security Copilot is explicit: output may be inaccurate or incomplete, so ==+review and verify every response before you act on it==. AI is there to augment the analyst, not replace them.

**2. What an agent adds.** Microsoft describes an agent as a program that uses a generative AI model to read inputs, reason, and decide on actions. Its parts:

- **Model** — the reasoning engine.
- **Instructions** — the goal and the boundaries.
- **Retrieval / knowledge** — grounding data. Good data reduces hallucinations.
- **Tools / actions** — functions and APIs it may call.
- **Memory** — conversation history and state.

Security Copilot adds three setup words. A **trigger** starts the agent, on a schedule or on demand. **Permissions** say which data it may read. An **identity** is what it signs in as: either a dedicated **agent identity** (Microsoft Entra Agent ID, Microsoft-built agents only for now) or *your own user account*, inheriting your rights.

**Autonomy and approval.** Agents range from *retrieval* agents that only read, to *action* agents that do defined tasks, to *autonomous* agents that plan many steps alone. The more an agent can do, the more it needs **human-in-the-loop** approval: the agent pauses before a sensitive tool call (delete, send, disable) and waits for a person to say yes.

**3. MCP — the plug between AI and tools.** The **Model Context Protocol (MCP)** is an open standard for how a language model reaches external tools and data. Think of it as USB for AI: any compliant AI app can use any compliant tool server.

| Part | What it is | Example |
|---|---|---|
| **MCP host** | the AI app the person uses | **VS Code** |
| **MCP client** | the connector inside the host, one per server | GitHub Copilot agent mode in VS Code |
| **MCP server** | a program that offers capabilities | the **Microsoft Sentinel MCP Server** |

A server offers three kinds of thing. **Tools** are functions the model can ask to run (with user approval). **Resources** are read-only data, such as a table schema. **Prompts** are pre-written templates. The client discovers tools at run time by asking the server to list them.

**Microsoft Sentinel's MCP Server** is a Microsoft-hosted MCP endpoint, signed in with Microsoft Entra, with nothing to deploy. Its tool *collections* let an AI client explore the Sentinel data lake in plain English, analyse entities such as users and URLs, triage incidents and hunt, and build Security Copilot agents. How to connect it and which roles it needs is D3.2.4.

**4. Microsoft Security Copilot at a glance.**

| Piece | What it is |
|---|---|
| **Standalone experience** | the full portal at `https://securitycopilot.microsoft.com` |
| **Embedded experience** | a Copilot side panel inside other products: Defender XDR (incident summary, guided response, script and file analysis, KQL from plain English), Sentinel, Entra, Intune, Purview, Defender for Cloud and others |
| **Security Compute Units (SCUs)** | the unit of AI compute capacity. Every prompt, promptbook and agent run uses some. ==!Closing the embedded panel does not stop SCU use== — an incident summary keeps generating in the background. |
| **Plugins** | connectors that give Copilot data and actions from Microsoft and third-party products (Defender XDR, Sentinel, Entra, ServiceNow...). A plugin is a collection of **tools** (also called skills). MCP servers can be added as plugins. |
| **Promptbooks** | saved chains of prompts for a task, each building on the last — like a playbook for questions. Built-ins include *Incident investigation*, *Suspicious script analysis*, *Threat actor profile* and *Vulnerability impact assessment*. |
| **Agents** | Security Copilot agents that run on a trigger and automate a task, for example phishing triage, alert triage or Conditional Access optimisation. They also use SCUs. |

How it answers: your prompt goes to Security Copilot, which **grounds** it using plugins, sends it to the language model, enriches the reply with plugin data again, and returns it for you to review.

**Licensing, high level.** Without an inclusion, capacity is bought as provisioned SCUs per hour through Azure. ==@Security Copilot is now included with Microsoft 365 E5 and E7==: rollout started **18 November 2025**, with **400 SCUs per month for every 1,000 paid user licences**, up to **10,000 SCUs per month**. Unused SCUs don't roll over. ==!Sentinel customers without Microsoft 365 E5 or E7 aren't eligible== for the inclusion. An Azure-only learner has neither, so treat it as screenshots.

## Where it lives

| Task | Where |
|---|---|
| Standalone Security Copilot | `https://securitycopilot.microsoft.com` |
| Embedded Copilot in incidents | Defender portal `security.microsoft.com` > an incident > Copilot side panel |
| Promptbook library | Security Copilot prompt bar > Prompts icon > **See all promptbooks** |
| SCU usage dashboard | Security Copilot > **Home menu > Owner settings > Usage monitoring** |
| Change provisioned / overage SCUs | Security Copilot **Settings** (or the Azure portal) — needs Azure capacity **owner or contributor** |
| Sentinel MCP Server | added to an MCP host such as VS Code — steps in D3.2.4 |

![Image of how Security Copilot works.](https://learn.microsoft.com/en-us/copilot/security/media/security-copilot-diagram.png){How Security Copilot works: prompt, grounding through plugins, language model, post-processing, response}

![Screenshot showing Copilot panel in embedded experience of Microsoft Defender XDR.](https://learn.microsoft.com/en-us/copilot/security/media/sidecar-embedded-experience.png){Embedded Copilot in Defender XDR: the side panel on an incident}

![List of available promptbooks](https://learn.microsoft.com/en-us/copilot/security/media/prompt-elements.png){A good prompt has a goal, context, expectations and a source}

![Screenshot of incident investigation promptbook.](https://learn.microsoft.com/en-us/copilot/security/media/promptbook-incident-tb.png){The Incident investigation promptbook takes an incident number}

![Screenshot shows suspicious script analysis in a promptbook.](https://learn.microsoft.com/en-us/copilot/security/media/promptbook-script-tb.png){Suspicious script analysis takes the script text}

![Screenshot of check impact of an external threat article promptbook.](https://learn.microsoft.com/en-us/copilot/security/media/promptbook-threat-article-tb.png){Check impact of an external threat article takes a URL}

![Screenshot of Microsoft user analysis promptbook.](https://learn.microsoft.com/en-us/copilot/security/media/promptbook-user-tb.png){Microsoft User analysis takes a UPN and a time range}

![Screenshot of threat actor promptbook.](https://learn.microsoft.com/en-us/copilot/security/media/promptbook-actor-tb.png){Threat actor profile takes an actor name}

![Screenshot of TI report promptbook.](https://learn.microsoft.com/en-us/copilot/security/media/promptbook-ti-report-tb.png){Threat Intelligence 360 report takes a Defender Threat Intelligence article name}

![Screenshot of vulnerability impact assessment promptbook.](https://learn.microsoft.com/en-us/copilot/security/media/promptbook-vuln-tb.png){Vulnerability impact assessment takes a CVE ID}

![Screenshot showing the usage monitoring dashboard filter button.](https://learn.microsoft.com/en-us/copilot/security/media/usage-monitor-filter.png){Usage monitoring: SCUs by session, user, plugin, category (prompt, promptbook, agent)}

![Screenshot showing the usage monitoring dashboard export button.](https://learn.microsoft.com/en-us/copilot/security/media/usage-monitor-export.png){Export usage to Excel}

![Image showing security agents in your daily workflow](https://learn.microsoft.com/en-us/copilot/security/media/agents-in-workflow.png){Security Copilot agents built into Defender, Entra, Intune and Purview}

![Image of the message center post messaging.](https://learn.microsoft.com/en-us/copilot/security/media/message-center-post.png){The Microsoft 365 message center post announcing E5 inclusion}

Agents and MCP in general:

![Diagram showing agent architecture with four components feeding into a language model.](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/images/agent-overview.png){Agent anatomy: instructions, knowledge, tools and memory around a language model}

![Diagram showing a spectrum of three agent types from left to right.](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/images/spectrum-agents.png){From read-only agents to autonomous agents — more autonomy needs more governance}

![Diagram showing a horizontal workflow with four connected phases for adopting AI agents.](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/images/ai-agent-adoption.svg){Microsoft's agent adoption process: plan, govern and secure, build, manage}

![Diagram showing the tool-calling loop: the LLM interacts with external tools and memory in a loop before returning a final response.](https://learn.microsoft.com/en-us/agent-framework/workflows/resources/images/ai-agent.png){An agent loop: the model decides, tools act, results come back to the model}

![A diagram showing the architecture pattern of MCP, including hosts, clients, and servers.](https://learn.microsoft.com/en-us/dotnet/ai/media/mcp/model-context-protocol-architecture-diagram.png){MCP: one host, one client per server, many servers}

## What the exam assumes you know

- ==!AI output is not evidence until a human checks it.== Hallucinations are confident and wrong.
- **Standalone** = securitycopilot.microsoft.com. **Embedded** = the Copilot panel inside Defender, Entra, Purview and others.
- **SCUs** measure Security Copilot capacity. Prompts, promptbooks and agents all consume them.
- A **promptbook** is a reusable chain of prompts. An **agent** runs on a trigger with its own identity and permissions.
- MCP roles: ==+host = the app, client = the connector inside it, server = the tool provider==. The Sentinel MCP Server is a *server*.
- Detail: embedded Copilot and agents in D2.1.8, Phishing Triage Agent in D2.1.1, Sentinel MCP Server in D3.2.4.

## Skip list

- **Skip** how LLMs are trained (pretraining, supervised fine-tuning, RLHF, reasoning models), temperature, KV-cache and tokenizers. Developer depth; never on SC-200.
- **Skip** MCP wire messages (`InitializeRequest`, `CallToolRequest`, JSON-RPC, streamable HTTP). Know host, client, server, tools.
- **Skip** writing custom plugins, the OpenAI plugin schema, Agent Builder and the Security Store. Developer scenarios.
- **Skip** provisioned versus overage SCU billing maths, the $6 per SCU overage price and capacity deletion. Pricing moves; the exam tests what SCUs are.
- **Skip** the CAF agent adoption phases and RAG versus agent theory. Strategy for architects.
- **Skip** the full embedded-experience list for Azure Firewall, Intune and Defender for Cloud. Learn the Defender XDR, Sentinel, Entra and Purview ones on the objective pages.
- **Skip** the Conditional Access Optimization Agent detail. Named on the Conditional Access primer.
