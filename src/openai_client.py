import os
from openai import OpenAI
from prompt_chains import SYSTEM_PROMPT, build_user_prompt, SplunkTAConfig

def generate_ta_code(api_spec: str) -> SplunkTAConfig:
    """Calls OpenAI API using Structured Outputs to guarantee the response schema."""
    # The client automatically picks up OPENAI_API_KEY from the environment
    client = OpenAI() 
    
    try:
        response = client.beta.chat.completions.parse(
            model="gpt-4o", # Using the latest flagship model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(api_spec)}
            ],
            response_format=SplunkTAConfig,
            temperature=0.2 # Low temperature for deterministic code generation
        )
        return response.choices[0].message.parsed
    except Exception as e:
        print(f"Error communicating with OpenAI API: {e}")
        raise
