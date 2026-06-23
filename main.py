### Bananabot - A simple chatbot using Gemini API ###

### Import Libraries ###
import sys
import argparse
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions
model_name = "gemini-2.5-flash"

### Parse Command Line Arguments ###
parser = argparse.ArgumentParser(description="Bananabot - A simple chatbot using Gemini API")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
parser.add_argument("user_prompt", type=str, help="The question to ask Bananabot")
args = parser.parse_args()


### Main Function ###
def main():
    ###Load Environment Variables ###
    load_dotenv()
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not found. Please set it in APIKey.env file.")
    
    ### Initialize Gemini API Client ###
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    ### message types for Gemini API ###
    messages: list[types.Content] = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    ### runs helper function to generate response from Gemini API ###
    generate_content(client, messages)
    
### Generate Response from Gemini API ###
def generate_content(client: genai.Client, messages: list[types.Content]) -> None:
    response = client.models.generate_content(model=model_name, contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt,  temperature = 0, tools=[available_functions]))
    ### Checking Metadata ###
    if args.verbose:
        if response.usage_metadata is not None:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        else: 
            raise RuntimeError("No metadata available.")
    ### Print the Response ###
    if response.function_calls:
        for call in response.function_calls:
            print(f"Calling function: {call.name} with {call.args}")
    else:
        print("Response:")
        print(response.text)


if __name__ == "__main__":
    main()
