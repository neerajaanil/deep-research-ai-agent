"""Research manager orchestrating the research process."""

import asyncio
import logging
from agents import Runner, trace, gen_trace_id

from .agents import (
    planner_agent, search_agent, writer_agent, email_agent,
    WebSearchPlan, WebSearchItem, ReportData
)

logger = logging.getLogger(__name__)


class ResearchManager:
    """Manages the deep research workflow."""

    async def run(self, query: str):
        """Run the deep research process, yielding status updates and the final report."""
        if not query or not query.strip():
            logger.warning("Received empty query")
            yield "Error: Query cannot be empty."
            return

        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            trace_url = f"https://platform.openai.com/traces/trace?trace_id={trace_id}"
            logger.info(f"Starting research. View trace: {trace_url}")
            yield f"View trace: {trace_url}"
            
            try:
                yield "Starting research..."
                search_plan = await self.plan_searches(query)
                yield f"Searches planned ({len(search_plan.searches)} searches), starting to search..."

                search_results = await self.perform_searches(search_plan)
                if not search_results:
                    logger.warning("No search results were returned; continuing to write report with empty results")
                yield f"Searches complete ({len(search_results)} results), writing report..."

                report = await self.write_report(query, search_results)
                yield "Report written, sending email..."

                await self.send_email(report)
                yield "Email sent, research complete"
                yield report.markdown_report
            except Exception as e:
                logger.error(f"Research run failed: {e}")
                yield f"Error: Research failed with error: {e}"

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """Plan the searches to perform for the query."""
        logger.info("Planning searches...")
        result = await Runner.run(planner_agent, f"Query: {query}")
        plan = result.final_output_as(WebSearchPlan)
        logger.info(f"Planned {len(plan.searches)} searches")
        return plan

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """Perform the searches in the plan."""
        logger.info("Performing searches...")
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []
        
        for task in asyncio.as_completed(tasks):
            try:
                result = await task
                if result:
                    results.append(result)
            except Exception as e:
                logger.error(f"Search failed: {e}")
        
        logger.info(f"Completed {len(results)}/{len(tasks)} searches")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """Perform a single search."""
        input_text = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(search_agent, input_text)
            return str(result.final_output)
        except Exception as e:
            logger.error(f"Search error for '{item.query}': {e}")
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """Write the research report."""
        logger.info("Writing report...")
        input_text = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(writer_agent, input_text)
        report = result.final_output_as(ReportData)
        logger.info("Report written successfully")
        return report

    async def send_email(self, report: ReportData) -> None:
        """Send the report via email."""
        logger.info("Sending email...")
        try:
            await Runner.run(email_agent, report.markdown_report)
            logger.info("Email sent successfully")
        except Exception as e:
            logger.error(f"Email sending failed: {e}")
