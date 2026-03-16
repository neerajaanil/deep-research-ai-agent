"""Email agent for sending research reports."""

import os
from typing import Dict
import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool

from ..config import Config


@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send an email with the given subject and HTML body."""
    if not Config.SENDGRID_API_KEY:
        return {"error": "SendGrid API key not configured"}
    
    if not Config.EMAIL_FROM or not Config.EMAIL_TO:
        return {"error": "Email addresses not configured"}
    
    try:
        sg = sendgrid.SendGridAPIClient(api_key=Config.SENDGRID_API_KEY)
        from_email = Email(Config.EMAIL_FROM)
        to_email = To(Config.EMAIL_TO)
        content = Content("text/html", html_body)
        mail = Mail(from_email, to_email, subject, content).get()
        response = sg.client.mail.send.post(request_body=mail)
        return {"status": "success", "status_code": response.status_code}
    except Exception as e:
        return {"error": str(e)}


INSTRUCTIONS = (
    "You are able to send a nicely formatted HTML email based on a detailed report. "
    "You will be provided with a detailed report. You should use your tool to send one email, "
    "providing the report converted into clean, well presented HTML with an appropriate subject line."
)

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model=Config.OPENAI_MODEL,
)
