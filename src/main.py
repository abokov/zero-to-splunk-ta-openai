import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

# Import our custom modules
from openai_client import generate_ta_code

# Import the new helper at the top of main.py
from token_helper import count_tokens, estimate_cost


def main():
    parser = argparse.ArgumentParser(description="Zero to Splunk TA: AI Deployment Framework")
    parser.add_argument("--spec", required=True, help="Path to the API documentation or spec file")
    parser.add_argument("--output", default="./build/Custom_Splunk_TA", help="Output directory")
    args = parser.parse_args()

    # Load environment variables (.env)
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set. Please add it to your .env file.")
        return

    # 1. Read API Spec
    try:
        with open(args.spec, "r") as f:
            api_spec_content = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find file {args.spec}")
        return

    # Log token usage before the API call!
    input_tokens = count_tokens(api_spec_content)
    est_cost = estimate_cost(input_tokens)
    print(f"📊 Analyzing API Spec: {input_tokens:,} tokens (Est. Input Cost: ${est_cost:.5f})")
    
    print("🚀 Calling OpenAI API...")

    ta_config = generate_ta_code(api_spec_content)
    
    # 3. Setup Output Directory
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "default").mkdir(exist_ok=True)
    (out_dir / "bin").mkdir(exist_ok=True)

    # 4. Render Templates
    print("📝 Rendering Splunk .conf files...")
    # Assumes you run the script from the root of the repository
    env = Environment(loader=FileSystemLoader('templates'))
    
    props_template = env.get_template('props.conf.template')
    with open(out_dir / "default" / "props.conf", "w") as f:
        f.write(props_template.render(sourcetype=ta_config.sourcetype))

    inputs_template = env.get_template('inputs.conf.template')
    with open(out_dir / "default" / "inputs.conf", "w") as f:
        f.write(inputs_template.render(
            input_name=ta_config.input_name, 
            interval=ta_config.interval, 
            sourcetype=ta_config.sourcetype
        ))

    # 5. Write Python Logic
    print("🐍 Writing Python collection script...")
    with open(out_dir / "bin" / f"{ta_config.input_name}.py", "w") as f:
        f.write(ta_config.python_logic)

    print(f"✅ Success! Splunk TA generated at: {out_dir.absolute()}")

if __name__ == "__main__":
    main()
