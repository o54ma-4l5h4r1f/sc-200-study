+++
slug = "jupyter-and-python-basics"
title = "Jupyter notebooks and Python basics for analysts"
summary = "You will know what a Jupyter notebook is (cells, kernel, code versus markdown cells, why run order matters), the handful of Python ideas an analyst meets (variables, imports, installing packages with %pip, pandas DataFrames, print versus display), where Sentinel notebooks run (Azure Machine Learning, or VS Code with the Microsoft Sentinel extension for the data lake), and what MSTICPy is."
order = 21
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/azure/sentinel/notebooks-hunt",
  "https://learn.microsoft.com/en-us/azure/sentinel/notebooks",
  "https://learn.microsoft.com/en-us/azure/sentinel/notebook-get-started",
  "https://learn.microsoft.com/en-us/azure/machine-learning/how-to-run-jupyter-notebooks",
  "https://learn.microsoft.com/en-us/azure/sentinel/datalake/notebooks-overview",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/notebooks-azure-monitor-logs",
  "https://learn.microsoft.com/en-us/training/modules/explore-analyze-data-with-python/2-explore-data-numpy-pandas",
]
captured = 2026-11-12
related_objectives = ["D3.2.4"]
+++

## In one sentence

A **Jupyter notebook** is a document made of small boxes called **cells**. Some cells hold notes, others hold code (usually **Python**). You run a code cell and its result — a table, a number, a chart — appears right underneath.

## Why it exists

A KQL query in the Sentinel portal answers one question at a time. Real hunting is a chain: pull sign-ins, look up each IP in a threat-intelligence service, join the result with HR data, draw a timeline. Doing that by hand means copying results between tools.

A notebook is a **lab notebook that can also do the experiment**. You write the step, run it, see the result, and write your reasoning next to it. The next person can re-run the whole investigation from top to bottom. Microsoft lists what notebooks add over the portal: **machine learning**, custom **timelines** and **process trees**, and data **outside** Sentinel, such as on-premises data sets.

For SC-200 this is the background for D3.2.4 (hunting with notebooks and the Sentinel MCP Server).

## Mental model

A notebook has two halves that live in different places.

- The **page** you see in the browser or editor: the cells, their text and their saved output.
- The **kernel**: a running Python process on some computer that actually executes the code. In Azure it runs on a **compute instance**, a virtual machine (VM) you pay for while it runs.

```svg
<svg viewBox="0 0 900 400" role="img" aria-label="Notebook anatomy: the notebook page holds a markdown cell and code cells with output underneath; running a code cell sends it to the kernel, a Python process on a compute instance, which keeps variables in memory between cells and queries Log Analytics or the Sentinel data lake; restarting the kernel wipes the memory; Sentinel notebooks run in Azure Machine Learning, data lake notebooks run in VS Code with the Microsoft Sentinel extension on Spark">
  <defs>
    <marker id="jpbarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <text x="170" y="25" text-anchor="middle" class="label-accent">The notebook page (.ipynb)</text>
  <rect class="box" x="20" y="38" width="300" height="50" rx="6"/>
  <text x="170" y="60" text-anchor="middle">Markdown cell</text>
  <text x="170" y="78" text-anchor="middle" class="muted">notes, headings, instructions</text>
  <rect class="box-accent" x="20" y="100" width="300" height="50" rx="6"/>
  <text x="170" y="122" text-anchor="middle">[1] Code cell: import pandas</text>
  <text x="170" y="140" text-anchor="middle" class="muted">Shift+Enter runs it</text>
  <rect class="box-accent" x="20" y="162" width="300" height="50" rx="6"/>
  <text x="170" y="184" text-anchor="middle">[2] Code cell: df = query(...)</text>
  <text x="170" y="202" text-anchor="middle" class="muted">uses names from cell [1]</text>
  <rect class="box-ok" x="20" y="224" width="300" height="50" rx="6"/>
  <text x="170" y="254" text-anchor="middle">Output: table / chart</text>
  <rect class="box-accent" x="420" y="60" width="220" height="150" rx="10"/>
  <text x="530" y="90" text-anchor="middle" class="label-accent">Kernel</text>
  <text x="530" y="115" text-anchor="middle">Python process</text>
  <text x="530" y="140" text-anchor="middle">keeps variables in memory</text>
  <text x="530" y="165" text-anchor="middle" class="muted">on a compute instance (VM)</text>
  <text x="530" y="190" text-anchor="middle" class="label-risk">restart = memory wiped</text>
  <rect class="box" x="700" y="60" width="180" height="60" rx="8"/>
  <text x="790" y="86" text-anchor="middle">Log Analytics</text>
  <text x="790" y="106" text-anchor="middle" class="muted">workspace (KQL)</text>
  <rect class="box" x="700" y="140" width="180" height="60" rx="8"/>
  <text x="790" y="166" text-anchor="middle">TI, GeoIP, other</text>
  <text x="790" y="186" text-anchor="middle" class="muted">outside data</text>
  <line class="line-accent" x1="320" y1="150" x2="418" y2="135" marker-end="url(#jpbarrow)"/>
  <line class="line-accent" x1="418" y1="175" x2="322" y2="249" marker-end="url(#jpbarrow)"/>
  <line class="line" x1="640" y1="110" x2="698" y2="92" marker-end="url(#jpbarrow)"/>
  <line class="line" x1="640" y1="160" x2="698" y2="170" marker-end="url(#jpbarrow)"/>
  <line class="divider" x1="20" y1="295" x2="880" y2="295"/>
  <text x="450" y="318" text-anchor="middle" class="label-accent">Where Sentinel notebooks run</text>
  <rect class="box" x="20" y="330" width="420" height="58" rx="8"/>
  <text x="230" y="354" text-anchor="middle">Azure Machine Learning workspace</text>
  <text x="230" y="376" text-anchor="middle" class="muted">compute instance kernel; queries the Log Analytics workspace</text>
  <rect class="box" x="460" y="330" width="420" height="58" rx="8"/>
  <text x="670" y="354" text-anchor="middle">VS Code + Microsoft Sentinel extension</text>
  <text x="670" y="376" text-anchor="middle" class="muted">PySpark on Spark; reads the Sentinel data lake</text>
</svg>
```

Because variables live in the kernel's memory, ==the order you run cells matters, not the order they sit on the page==. Run cell [2] before cell [1] and Python says the name is not defined. Microsoft's instruction is blunt: ==+always run cells in sequence==. Restarting the kernel deletes every variable, so you re-run the setup and sign-in cells.

## What actually matters

**1. Two kinds of cell.** **Markdown** cells hold text, headings and images. **Code** cells hold code. Run the selected code cell with the **Play** icon or ==@Shift+Enter==. In Azure Machine Learning, **Ctrl+Enter** runs a cell without moving on, and **Alt+R** runs all. When a cell finishes, its execution count (the number in brackets) goes up and the output appears below it.

**2. The Python you will actually read.** You don't need to write Python from scratch for SC-200. You need to read it.

```python
# A line starting with # is a comment. Python ignores it.
import pandas as pd                 # import: load a package, give it a short name
threshold = 5                       # variable: a name that holds a value
print("Failed sign-in threshold:", threshold)   # print: show text in the output

df = pd.DataFrame({                 # a DataFrame: a table with named columns
    "Account": ["amy", "bob", "amy"],
    "FailedLogons": [7, 1, 9],
})
df.head()                           # last line of a cell is displayed automatically
```

- A **variable** is a labelled box: `threshold = 5`.
- A **package** (also called a library) is code someone else wrote. You must **install** it once into the kernel's environment and **import** it in every notebook. Azure Machine Learning compute already has most common packages.
- To install, use the **magic command** `%pip install PACKAGE-NAME` in a cell. In Azure Machine Learning, ==!don't use `!pip`==: it can install into a different Python environment from the kernel you are running.
- **pandas** is the spreadsheet of Python. Its **DataFrame** is a table of rows and named columns. Almost every security tool you'll call in a notebook hands results back as a DataFrame. `df.head()` shows the first five rows. `display(df)` renders it as a table.
- `print()` writes text. The value of the **last line** of a cell is shown automatically, even without `print()`.
- A line starting with `!` runs a shell command, for example `!git clone ...` to pull Microsoft's notebook library from GitHub.

**3. KQL goes inside Python as text.** A notebook doesn't replace KQL. You put a KQL query in a Python string, send it to the workspace with a query library, and get a DataFrame back. Libraries named in the docs: the **Azure Monitor Query** client library, **Kqlmagic**, and **MSTICPy**.

**4. MSTICPy.** **MSTICPy** (from the Microsoft Threat Intelligence Center) is the Python package Microsoft Sentinel's notebooks are built on. It bundles cybersecurity tools for **data retrieval, analysis, enrichment and visualization**: ready-made queries against your workspace, threat-intelligence and GeoIP lookups (for example VirusTotal and MaxMind GeoLite2), timelines and process trees. You start it with `init_notebook`, which reads its settings from a file called **msticpyconfig.yaml**. Its query provider runs KQL and returns a pandas DataFrame. Not every Sentinel notebook uses it — the **Credential Scanner** notebooks, for example, don't. The exact calls are in D3.2.4.

**5. Two places Sentinel notebooks run.**

| | Azure Machine Learning (AML) notebooks | Data lake notebooks |
|---|---|---|
| Where you open them | Sentinel > **Threat management > Notebooks** > launch into **AML studio** | **VS Code** with the **Microsoft Sentinel** extension |
| What runs the code | a Python kernel on a **compute instance** (VM) | **Apache Spark** sessions running **PySpark** (Python for Spark) |
| What data | the Log Analytics workspace (analytics tier) | the **Sentinel data lake** (lake and analytics tiers) |
| Cost to watch | ==!compute instance bills while running — stop it== | Spark session time |
| Roles | **Microsoft Sentinel Contributor** to save and launch; **Contributor** on the AML workspace; **Owner** or **Contributor** on the resource group to create one | covered in D3.2.4 |

**Visual Studio Code (VS Code)** is Microsoft's free code editor. Extensions add features to it; the Microsoft Sentinel extension adds lake browsing, Spark notebooks and scheduled **jobs**. Data lake notebook limits and the MCP connection are D3.2.4 material.

## Where it lives

| Task | Path |
|---|---|
| Notebook templates | Defender portal: **Microsoft Sentinel > Threat management > Notebooks** (Azure portal: **Threat management > Notebooks**) > **Templates** tab |
| Create the AML workspace | Notebooks > **Configure Azure Machine Learning > Create a new AML workspace** |
| Clone a template | pick a template > **Create from template** > **Save** > **Launch notebook** |
| Run, stop, restart | AML studio `ml.azure.com` > **Notebooks**; **Compute** dropdown; **Kernel operations > Restart kernel** |
| Install a package | a cell with `%pip install PACKAGE-NAME` |
| Data lake notebooks | VS Code > Extensions > **Microsoft Sentinel** |

The starter template is **A Getting Started Guide For Microsoft Sentinel ML Notebooks**. Only AML workspaces in the **same subscription** can be picked. New notebooks save to `/Users/YOUR-USER-NAME/` in that workspace. Only you can use the compute instances you create; your files are shared across all compute in the workspace.

Notebooks from Sentinel into Azure Machine Learning:

![Review + create your Machine Learning workspace from Microsoft Sentinel.](https://learn.microsoft.com/en-us/azure/sentinel/media/notebooks/machine-learning-create-last-step.png){Configure Azure Machine Learning: review and create the AML workspace}

![Screenshot of the Create private endpoint page in Microsoft Sentinel.](https://learn.microsoft.com/en-us/azure/sentinel/media/notebooks/create-private-endpoint.png){Private-endpoint option for locked-down networks}

![Screenshot of a private DNS zone resource selected.](https://learn.microsoft.com/en-us/azure/sentinel/media/notebooks/select-private-dns-zone.png){Private DNS zones created with a private-endpoint workspace}

![Select a default AML workspace for your notebooks.](https://learn.microsoft.com/en-us/azure/sentinel/media/notebooks/default-machine-learning.png){Pick the default AML workspace notebooks launch into}

![Save a notebook to clone it to your own workspace.](https://learn.microsoft.com/en-us/azure/sentinel/media/notebooks/save-notebook.png){Create from template > Save clones it into your workspace}

![Launch your notebook in your AML workspace.](https://learn.microsoft.com/en-us/azure/sentinel/media/notebooks/sentinel-notebooks-on-machine-learning.png){Launch notebook opens it in AML studio — pick a compute instance at the top}

![Screenshot of a machine learning environment ready to run code cells.](https://learn.microsoft.com/en-us/azure/sentinel/media/notebook-get-started/compute-ready.png){Ready: the compute and kernel are up and cells can run}

![Restart a notebook kernel.](https://learn.microsoft.com/en-us/azure/sentinel/media/notebooks/sentinel-notebooks-restart-kernel.png){Kernel operations > Restart kernel wipes all variables}

Working in the AML studio notebook editor:

![Create a new compute](https://learn.microsoft.com/en-us/azure/machine-learning/media/how-to-run-jupyter-notebooks/new-compute.png){+ New Compute next to the Compute dropdown}

![Start compute instance](https://learn.microsoft.com/en-us/azure/machine-learning/media/how-to-run-jupyter-notebooks/start-compute.png){Start compute for a stopped instance}

![Screenshot: Variable explorer tool](https://learn.microsoft.com/en-us/azure/machine-learning/media/how-to-run-jupyter-notebooks/variable-explorer.png){The Variable explorer tool}

![Screenshot: Variable explorer window](https://learn.microsoft.com/en-us/azure/machine-learning/media/how-to-run-jupyter-notebooks/variable-explorer-window.png){Every variable the kernel is holding — proof that state lives in the kernel}

![Screenshot: Table of contents in the notebook](https://learn.microsoft.com/en-us/azure/machine-learning/media/how-to-run-jupyter-notebooks/table-of-contents.png){Markdown headings become a table of contents}

![Toggle focus mode / standard view](https://learn.microsoft.com/en-us/azure/machine-learning/media/how-to-run-jupyter-notebooks/focusmode.gif){Focus mode hides the file explorer}

![Insert a code snippet](https://learn.microsoft.com/en-us/azure/machine-learning/media/how-to-run-jupyter-notebooks/insert-snippet.gif){Ctrl+Space inserts code snippets (preview)}

![Open snippet panel tool in the notebook toolbar](https://learn.microsoft.com/en-us/azure/machine-learning/media/how-to-run-jupyter-notebooks/open-snippet-panel.png){The snippet panel}

![Snippet panel allows you to propose a new snippet](https://learn.microsoft.com/en-us/azure/machine-learning/media/how-to-run-jupyter-notebooks/propose-new-snippet.png){Proposing a new snippet}

![Screenshot of notebook comments tool in the top toolbar.](https://learn.microsoft.com/en-us/azure/machine-learning/media/how-to-run-jupyter-notebooks/notebook-comments-tool.png){Notebook comments tool}

![Screenshot of add a comment to a code cell tool.](https://learn.microsoft.com/en-us/azure/machine-learning/media/how-to-run-jupyter-notebooks/comment-from-code.png){Commenting on code in a cell}

![Screenshot: select the Gather icon](https://learn.microsoft.com/en-us/azure/machine-learning/media/how-to-run-jupyter-notebooks/gather.png){Gather (preview): build a clean notebook from only the cells a result needs}

![Screenshot of save tool in notebook toolbar](https://learn.microsoft.com/en-us/azure/machine-learning/media/how-to-run-jupyter-notebooks/file-save.png){File > Save and checkpoint (notebooks also autosave every 30 seconds)}

![Export a notebook to your computer](https://learn.microsoft.com/en-us/azure/machine-learning/media/how-to-run-jupyter-notebooks/export-notebook.png){Export As Python, HTML or LaTeX}

DataFrames and results:

![Diagram of a Pandas dataframe.](https://learn.microsoft.com/en-us/training/modules/explore-analyze-data-with-python/media/2-pandas-df.png){A pandas DataFrame: rows, named columns, an index}

![Screenshot of a DataFrame generated in a notebook with log ingestion data retrieved from a Log Analytics workspace.](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/jupyter-notebook-ml-azure-monitor-logs/machine-learning-azure-monitor-logs-ingestion-all-tables-dataframe.png){A KQL query run from Python comes back as a DataFrame}

![A graph that shows the amount of data ingested into each of the tables in a Log Analytics workspace over seven days.](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/jupyter-notebook-ml-azure-monitor-logs/machine-learning-azure-monitor-logs-ingestion-all-tables.png){The same DataFrame drawn as a chart — something the portal can't do as freely}

![Screenshot that shows a query in Log Analytics on a custom table into which the analysis results from the notebook were ingested.](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/jupyter-notebook-ml-azure-monitor-logs/machine-learning-anomalies-in-azure-monitor-log-analytics-workspace.png){Optional last step: write the notebook's results back into a custom Log Analytics table}

## What the exam assumes you know

- A notebook = **cells** + a **kernel**. ==!Skipping cells or running them out of order causes errors.==
- Sentinel notebooks (Azure portal or Defender portal) open in ==+Azure Machine Learning==, not in Log Analytics and not in Logic Apps.
- ==+Data lake notebooks run in VS Code with the Microsoft Sentinel extension==, on Spark.
- **MSTICPy** is the Python security toolkit behind Sentinel notebooks; its results are pandas DataFrames.
- Saving and launching notebooks from Sentinel needs **Microsoft Sentinel Contributor** plus access to the AML workspace.

## Skip list

- **Skip** the full AML keyboard-shortcut tables (command mode and edit mode). Know Shift+Enter and restart kernel.
- **Skip** focus mode, snippets, comments, gather, checkpoints and export. Editor comfort features; never tested.
- **Skip** the private-endpoint AML setup (jump box, Bastion, private DNS zone links). Network design, not SOC work.
- **Skip** adding kernels and conda environments, and the `kernel.json` / `nbuser_settings.py` MSTICPy configuration. Admin setup.
- **Skip** NumPy, Matplotlib and statistics from the data-science module. Know what a DataFrame is.
- **Skip** writing results back with the Logs Ingestion API (DCR, data collection endpoint, app registration). Shown above for completeness only.
- **Skip** learning Python syntax beyond reading the snippet above. SC-200 tests where notebooks run and why, not coding.
