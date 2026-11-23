from google.adk.agents.llm_agent import Agent
from google import LiteLlm
from google.genai import types

root_agent = Agent(
    model=LiteLlm(model_name="openai/gpt-oss-120b"),
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    
    generate_content_config=types.GenerateContentConfig(
            max_output_tokens=200,
            temperature=0.3,
            top_p=0.9,
            stop_sequences=["\n"],
        ),
)
