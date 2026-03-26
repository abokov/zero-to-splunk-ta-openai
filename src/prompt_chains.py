from pydantic import BaseModel, Field

# 1. Define the Pydantic Schema for Structured Output
class SplunkTAConfig(BaseModel):
    sourcetype: str = Field(description="The suggested Splunk sourcetype name, e.g., 'custom:api:data'")
    input_name: str = Field(description="The name of the modular input")
    interval: int = Field(description="Suggested polling interval in seconds (default 300)")
    python_logic: str = Field(description="The raw Python code for the data collection logic using the requests library. Do not include markdown formatting.")

# 2. Define the Prompts
SYSTEM_PROMPT = """You are an expert Splunk Architect and Python Developer. 
Your goal is to analyze API documentation and generate a production-ready Splunk Technology Add-on (TA) configuration.
Extract the required endpoints, authentication methods, and generate the Python requests logic to fetch the data."""

def build_user_prompt(api_spec_content: str) -> str:
    return f"""Analyze the following API documentation and generate the Splunk TA configuration and Python collection logic.

API Documentation:
{api_spec_content}
"""
