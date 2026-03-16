"""Gradio application for deep research agent."""

import logging
import gradio as gr

from .config import Config
from .manager import ResearchManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app() -> gr.Blocks:
    """Create and configure the Gradio interface."""
    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise
    
    async def run(query: str):
        """Run research and yield updates."""
        manager = ResearchManager()
        async for chunk in manager.run(query):
            yield chunk
    
    with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
        gr.Markdown("# Deep Research Agent")
        gr.Markdown("Enter a research query to generate a comprehensive report.")
        query_textbox = gr.Textbox(
            label="Research Query",
            placeholder="What topic would you like to research?",
            lines=3
        )
        run_button = gr.Button("Run Research", variant="primary")
        report = gr.Markdown(label="Report", value="")
        
        run_button.click(fn=run, inputs=query_textbox, outputs=report)
        query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)
    
    return ui


def main():
    """Main entry point."""
    try:
        ui = create_app()
        ui.launch(
            server_name=Config.SERVER_HOST,
            server_port=Config.SERVER_PORT,
            share=Config.SHARE,
            show_error=True
        )
    except Exception as e:
        logger.error(f"Failed to launch application: {e}")
        raise


if __name__ == "__main__":
    main()
