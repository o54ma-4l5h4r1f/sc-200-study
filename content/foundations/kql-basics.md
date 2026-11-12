+++
slug = "kql-basics"
title = "KQL basics"
summary = "Kusto Query Language from zero: the table-then-pipe pattern, the dozen operators that cover most SOC queries (where, project, extend, summarize, bin, sort, top, take, let, join, union, render), time filtering, the has / contains / equals difference, and where to practise for free."
order = 12
ms_learn_urls = [
  "https://learn.microsoft.com/en-us/kusto/query/",
  "https://learn.microsoft.com/en-us/kusto/query/tutorials/learn-common-operators",
  "https://learn.microsoft.com/en-us/kusto/query/datatypes-string-operators",
  "https://learn.microsoft.com/en-us/kusto/query/join-operator",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-tutorial",
  "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/get-started-queries",
  "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-query-language",
]
captured = 2026-11-12
related_objectives = []
+++

## In one sentence

**KQL (Kusto Query Language)** is the read-only language you type to ask questions of log tables: you name a **table**, then pass its rows through a chain of **operators** joined by the pipe symbol `|`, and each step filters, reshapes or counts what the previous step handed it.

## Why it exists

A Log Analytics workspace (see the workspace primer) can hold billions of rows. You cannot scroll through that. You need to *ask*: "Which accounts failed to sign in more than 20 times in the last hour?" KQL is how you ask.

Think of a **sorting line in a post office**. A sack of letters (the table) is tipped onto a conveyor belt. Station one throws out everything not addressed to London (`where`). Station two tears off the parts of each envelope you do not need (`project`). Station three counts the letters per street (`summarize`). Each station only sees what the station before it passed along. That is the pipe.

KQL is the same language in Microsoft Sentinel, the Defender portal's **Advanced hunting**, Log Analytics and Azure Data Explorer. Learn it once. A KQL query **cannot change or delete data**. It only reads.

## Mental model

```svg
<svg viewBox="0 0 780 200" role="img" aria-label="A KQL query is a pipeline: a table feeds rows into where, then project, then summarize, each step passing a smaller table to the next">
  <defs>
    <marker id="kqb-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="line-accent"/>
    </marker>
  </defs>
  <rect class="box-accent" x="10" y="50" width="160" height="80" rx="8"/>
  <text x="90" y="80" text-anchor="middle" class="label-accent">SigninLogs</text>
  <text x="90" y="104" text-anchor="middle" class="muted">1,000,000 rows</text>
  <line x1="170" y1="90" x2="208" y2="90" class="line-accent" marker-end="url(#kqb-arrow)"/>
  <rect class="box" x="210" y="50" width="170" height="80" rx="8"/>
  <text x="295" y="80" text-anchor="middle">| where</text>
  <text x="295" y="104" text-anchor="middle" class="muted">keep failed, last 1h</text>
  <line x1="380" y1="90" x2="418" y2="90" class="line-accent" marker-end="url(#kqb-arrow)"/>
  <rect class="box" x="420" y="50" width="160" height="80" rx="8"/>
  <text x="500" y="80" text-anchor="middle">| summarize</text>
  <text x="500" y="104" text-anchor="middle" class="muted">count() by user</text>
  <line x1="580" y1="90" x2="618" y2="90" class="line-accent" marker-end="url(#kqb-arrow)"/>
  <rect class="box-ok" x="620" y="50" width="150" height="80" rx="8"/>
  <text x="695" y="80" text-anchor="middle">| top 10</text>
  <text x="695" y="104" text-anchor="middle" class="muted">10 rows out</text>
  <text x="390" y="170" text-anchor="middle">Every step takes a table in and hands a (usually smaller) table out.</text>
</svg>
```

```kql
SigninLogs
| where TimeGenerated > ago(1h)
| where ResultType != "0"
| summarize FailedCount = count() by UserPrincipalName
| top 10 by FailedCount
```

Read it out loud: *from SigninLogs, keep the last hour, keep the failures, count them per user, show the top ten.* `ResultType` is the sign-in result code; `"0"` means success.

## What actually matters

### The operators you will use every day

| Operator | What it does | Example |
|---|---|---|
| `where` | Keep only rows that match a condition | `where EventID == 4625` |
| `project` | Keep only the columns you name (and rename them) | `project TimeGenerated, Account, Computer` |
| `extend` | Add a calculated column, keep all the others | `extend Hour = bin(TimeGenerated, 1h)` |
| `summarize … by` | Group rows and aggregate them | `summarize count() by Computer` |
| `bin()` | Round a value (usually a time) into buckets | `bin(TimeGenerated, 1h)` |
| `sort by` | Order rows. Default is **descending** | `sort by TimeGenerated desc` |
| `top N by` | Sort and keep the first N rows | `top 10 by FailedCount` |
| `take N` | Return N **arbitrary** rows — for a quick look only | `take 10` |
| `count` | Return just the number of rows | one row, one column |
| `ago()` | A time relative to now | `ago(7d)`, `ago(1h)`, `ago(30m)` |
| `let` | Give a name to a value or a sub-query | `let lookback = 1d;` |
| `union` | Stack rows from several tables | `union DeviceProcessEvents, DeviceNetworkEvents` |
| `join` | Match rows from two tables on a shared column | `join kind=inner (…) on Account` |
| `render` | Draw the result as a chart | `render timechart` |

Lines starting with `//` are **comments** — notes for humans that KQL ignores.

### Time first, always

Every log table has a time column. In Sentinel and Log Analytics it is `TimeGenerated`. In Defender XDR advanced hunting tables it is usually `Timestamp`. Filter on it **first**. It makes queries fast and keeps results manageable. Kusto times are in **UTC**.

In Log Analytics, the **time picker** next to **Run** defaults to the **last 24 hours**. If your query has its own time filter, the picker changes to **Set in query**.

```kql
// Failed Windows logons per hour for the last day, as a chart
SecurityEvent
| where TimeGenerated > ago(1d)
| where EventID == 4625
| summarize Failures = count() by bin(TimeGenerated, 1h)
| render timechart
```

### Matching text: `has` vs `contains` vs equals

This is the most-tested beginner trap.

| Operator | Matches when… | Case | Speed |
|---|---|---|---|
| `==` | the whole value is exactly equal | case-**sensitive** | fast |
| `=~` | the whole value is equal, ignoring case | case-insensitive | fast |
| `has` | the right side is a **whole term** in the value | case-insensitive | fast (uses the term index) |
| `contains` | the right side appears **anywhere**, even mid-word | case-insensitive | slower (scans every value) |
| `in` / `in~` | the value is one of a list | sensitive / insensitive | fast |
| `has_any` | any of a list of terms is present | case-insensitive | fast |

A **term** is a run of letters and digits, split at spaces and punctuation. So `"KustoExplorerQueryRun" has "Explorer"` is **false**, but `"KustoExplorerQueryRun" contains "Explorer"` is **true**. Kusto only indexes terms of **three or more characters**. Prefer `has` when you are searching for a whole word. Add `_cs` (for example `has_cs`) for a case-sensitive version. Put `!` in front to negate: `!has`, `!contains`, `!=`.

KQL itself — table names, column names, operators — **is case-sensitive**. `securityevent` is not `SecurityEvent`.

### `let`, `union` and `join`

```kql
let suspicious = dynamic(["powershell.exe", "cmd.exe"]);
DeviceProcessEvents
| where Timestamp > ago(7d)
| where FileName in~ (suspicious)
| project Timestamp, DeviceName, AccountName, ProcessCommandLine
```

`union` stacks tables that hold similar events. `join` lines up two tables side by side on a shared column. The default join kind is `innerunique`. Name the kind you want.

| Join kind | Keeps |
|---|---|
| `innerunique` (default) | Matching rows; left side de-duplicated first |
| `inner` | Every matching pair |
| `leftouter` | All left rows, plus matches from the right (blanks if none) |
| `rightouter` / `fullouter` | All right rows / all rows from both |
| `leftsemi` | Left rows that *have* a match (no right columns) |
| `leftanti` | Left rows with ==!no== match — great for "what is missing" |
| `rightsemi` / `rightanti` | The same, from the right side |

```kql
// Accounts that signed in successfully after failing at least 5 times
let failures = SigninLogs
    | where TimeGenerated > ago(1d) and ResultType != "0"
    | summarize Fails = count() by UserPrincipalName
    | where Fails >= 5;
SigninLogs
| where TimeGenerated > ago(1d) and ResultType == "0"
| join kind=inner failures on UserPrincipalName
| project TimeGenerated, UserPrincipalName, Fails, IPAddress
```

### Reading the results

Results come back as a grid. Click a row's arrow to expand all its columns. You can sort by clicking a column header. A **Chart** tab draws the same data (that is what `render` does for you).

## Where it lives

| Where | Path | Time column |
|---|---|---|
| Log Analytics (Azure portal) | Your workspace > **Logs**, or **Monitor** > **Logs** | `TimeGenerated` |
| Microsoft Sentinel in the Defender portal | **Investigation & response** > **Hunting** > **Advanced hunting** | `TimeGenerated` for Sentinel tables, `Timestamp` for Defender tables |
| Microsoft Sentinel in the Azure portal | Microsoft Sentinel > **Logs** | `TimeGenerated` |
| **Free practice** | The **Log Analytics demo environment** — `https://portal.azure.com/#blade/Microsoft_Azure_Monitoring_Logs/DemoLogsBlade`. Sample data, ==+no Azure subscription required== | `TimeGenerated` |

Log Analytics has two editing modes. **KQL mode** is the text editor. **Simple mode** builds a query from menus. Use KQL mode — the exam shows KQL text.

### Log Analytics tutorial (the demo environment)

![Screenshot that shows the Log Analytics scope for the demo](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/log-analytics-tutorial/log-analytics-query-scope.png)

![Screenshot that shows preview data for the AppRequests table](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/log-analytics-tutorial/preview-data.png)

![Screenshot that shows the time range selector sin Log Analytics](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/log-analytics-tutorial/query-time-range.png)

![Screenshot that shows query results with multiple filters](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/log-analytics-tutorial/query-multiple-filters.png)

![Screenshot that shows query results being sorted by the TimeGenerated column and a record expanded](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/log-analytics-tutorial/sort-query-results.png)

![Screenshot that shows a record expanded in the search results](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/log-analytics-tutorial/expand-query-search-result.png)

![Screenshot that shows the search box at the top right of the result pane](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/log-analytics-tutorial/search-query-results.png)

![Screenshot that shows query results grouped by URL](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/log-analytics-tutorial/query-results-grouped.png)

![Screenshot that shows how to turn on Pivot Mode and configure a pivot table based on the URL and DurationMS values](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/log-analytics-tutorial/log-analytics-pivot-table.png)

![Screenshot that shows the query results chart](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/log-analytics-tutorial/example-query-output-chart.png)

### Get started with log queries (KQL mode and Simple mode)

![Screenshot shows the KQL mode ribbon](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/kql-mode-ribbon.png)

![Screenshot shows the Simple mode ribbon](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/simple-mode-ribbon.png)

![Screenshot shows the Add dropdown in simple mode with 'Search in table' highlighted](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/logs-simple-search-add.png)

![Screenshot shows the Search field in simple mode](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/logs-simple-search-select.png)

![Screenshot shows the Show dropdown in simple mode](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/logs-simple-limit.png)

![Screenshot shows the Add dropdown in simple mode with Sort highlighted](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/logs-simple-sort-add.png)

![Screenshot shows the Sort field in simple mode](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/logs-simple-sort-select.png)

![Screenshot that shows the top 10 records sorted in descending order](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/logs-kql-top.png)

![Screenshot that shows the Add filters menu that opens when you select Add in Log Analytics simple mode](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/logs-simple-filter-add.png)

![Screenshot that shows filter values for the OperationId column in Log Analytics simple mode](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/logs-simple-filter-select.png)

![Screenshot that shows the time picker and its list of time-range commands in KQL mode](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/logs-kql-time.png)

![Screenshot that shows the time picker and its list of time-range commands in simple mode](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/logs-simple-time.png)

![Screenshot that shows the query 'project' results list](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/logs-kql-project.png)

![Screenshot shows the Add dropdown in simple mode with 'Show columns' highlighted](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/logs-simple-columns-add.png)

![Screenshot that shows the 'Show columns' selector](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/logs-simple-columns-select.png)

![Screenshot that shows the selected values for aggregations in simple mode](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/logs-simple-aggregate.png)

![Screenshot that shows the selected values for statistical calculations in simple mode](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/logs-simple-stat-calc.png)

![Screenshot that shows the values of a query memory over time in KQL mode](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/logs-kql-graph.png)

![Screenshot that shows the values of a query memory over time in simple mode](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/media/get-started-queries/logs-simple-graph.png)

### Join kinds

![Diagram showing query join kinds](https://learn.microsoft.com/en-us/kusto/query/media/joinoperator/join-kinds.png)

![join innerunique](https://learn.microsoft.com/en-us/kusto/query/media/joinoperator/join-innerunique.png)

![join inner](https://learn.microsoft.com/en-us/kusto/query/media/joinoperator/join-inner.png)

![join leftouter](https://learn.microsoft.com/en-us/kusto/query/media/joinoperator/join-leftouter.png)

![join rightouter](https://learn.microsoft.com/en-us/kusto/query/media/joinoperator/join-rightouter.png)

![join fullouter](https://learn.microsoft.com/en-us/kusto/query/media/joinoperator/join-fullouter.png)

![join leftsemi](https://learn.microsoft.com/en-us/kusto/query/media/joinoperator/join-leftsemi.png)

![join leftanti](https://learn.microsoft.com/en-us/kusto/query/media/joinoperator/join-leftanti.png)

![join rightsemi](https://learn.microsoft.com/en-us/kusto/query/media/joinoperator/join-rightsemi.png)

![join rightanti](https://learn.microsoft.com/en-us/kusto/query/media/joinoperator/join-rightanti.png)

### Advanced hunting in the Defender portal

![An example of multiple queries execution in the New query page in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/advanced-hunting-query-language/multiple-queries.png)

![Opening a new tab by selecting Create new in advanced hunting in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/advanced-hunting-query-language/multitab.png)

![Run different queries without ever leaving the advanced hunting page in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/advanced-hunting-query-language/multitab-examples.png)

![The Getting started section in the Advanced hunting page in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/media/advanced-hunting-query-language/get-started-section.png)

## What the exam assumes you know

- Read a 5-line query and say what it returns. Most SC-200 KQL questions are "complete the query" or "which operator".
- `project` drops columns; `extend` adds one. `summarize` collapses rows into groups.
- ==!`take` is not ordered.== Use `top` or `sort` when order matters.
- ==!`contains` is not the same as `has`.== `has` matches whole terms and is faster.
- ==+Filter on time first.==

## Skip list

- **Skip:** the help cluster and Azure Data Explorer setup in the KQL tutorial (`StormEvents` sample data). The demo workspace above uses security-shaped tables and needs nothing installed.
- **Skip:** the full list of string operators (`hasprefix`, `hassuffix`, `startswith`, `matches regex` and their `_cs` and `!` twins). Know `==`, `=~`, `has`, `contains`, `in`, `has_any`. Look the rest up in the exam's Learn pane.
- **Skip:** join hints (`hint.strategy=shuffle`, `broadcast`) and performance tuning. Not tested at this level.
- **Skip:** Simple mode menus. The screenshots are above because they are in the cited article; the exam is KQL text.
- **Skip:** pivot tables, saving queries and query packs in the Log Analytics tutorial. Tool features, not language.
- **Skip:** `parse`, `mv-expand`, `make-series` and time-series functions here. The KQL objective pages cover the ones SC-200 asks for.
