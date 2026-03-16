## Agents Overview

This project uses a **multi‑agent architecture** to perform deep research. The agents are thin wrappers around `openai-agents` primitives and are orchestrated by `ResearchManager`.

- **Planner agent** (`agents/planner.py`)
  - **Purpose**: Turn a user’s free‑form research query into a structured web‑search plan.
  - **Model instructions**: Ask the model to break the query into multiple focused searches and explain *why* each search is needed.
  - **Tools / schema**:
    - Produces a `WebSearchPlan` (Pydantic model) containing a list of `WebSearchItem`s.
  - **Used by**:
    - `ResearchManager.plan_searches` to decide which web searches to execute.

- **Search agent** (`agents/search.py`)
  - **Purpose**: Execute a single web search and summarize the results.
  - **Model instructions**: Given a search term, call the web search tool and produce a concise 2–3 paragraph summary (≤ 300 words), focused on key points only.
  - **Tools**:
    - `WebSearchTool(search_context_size="low")` – provided by `openai-agents`, backed by OpenAI’s web search.
  - **Used by**:
    - `ResearchManager.search` / `ResearchManager.perform_searches` to run many searches concurrently based on the planner’s output.

- **Writer agent** (`agents/writer.py`)
  - **Purpose**: Synthesize all search summaries into a coherent research report.
  - **Model instructions**: Take the original query and the list of summarized search results, then write a structured markdown report with sections, a high‑level summary, and follow‑up questions.
  - **Outputs**:
    - A `ReportData` Pydantic model that includes `markdown_report` (the final report shown in the UI and emailed).
  - **Used by**:
    - `ResearchManager.write_report` to produce the final report content.

- **Email agent** (`agents/email.py`)
  - **Purpose**: Convert the markdown report into HTML and send it via email using SendGrid.
  - **Tools**:
    - `send_email` function tool, which wraps `sendgrid.SendGridAPIClient` and returns a small JSON status dict.
  - **Configuration**:
    - Requires `SENDGRID_API_KEY`, `EMAIL_FROM`, and `EMAIL_TO` in `.env`.
  - **Used by**:
    - `ResearchManager.send_email` after the report has been written.

## Orchestration Flow

The `ResearchManager` (`manager.py`) coordinates all agents inside a single OpenAI **trace**:

1. **Trace creation**
   - A trace ID is generated via `gen_trace_id`, and a `trace("Research trace", trace_id=...)` context is opened.
   - A trace URL is logged and yielded to the Gradio UI so you can inspect the run in the OpenAI dashboard.
2. **Planning**
   - `plan_searches(query)` → runs the **planner agent**, returns a `WebSearchPlan`.
3. **Searching**
   - `perform_searches(plan)` → runs the **search agent** once per `WebSearchItem`, concurrently, and collects text summaries.
4. **Writing**
   - `write_report(query, search_results)` → runs the **writer agent** to build a `ReportData` object containing `markdown_report`.
5. **Email (optional)**
   - `send_email(report)` → runs the **email agent**, which calls the `send_email` tool to send the HTML version of the report.

The Gradio app (`app.py`) exposes a single async `run(query)` function that instantiates `ResearchManager` and streams these status messages and the final `markdown_report` back to the UI.

