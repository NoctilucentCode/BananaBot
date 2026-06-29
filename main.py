### Bananabot - A simple chatbot using Gemini API ###

### Import Libraries ###
from pyexpat.errors import messages
import sys
import argparse
import os
from urllib import response
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function

### Global Variables ###
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
    for _ in range(20):
        result = generate_content(client, messages, verbose=args.verbose)
        if result is not None:
            print("Final response:")
            print(result)
            return
        else: 
            pass  # Continue to the next iteration if result is None

    print("Maximum number of iterations reached. Exiting.")
    sys.exit(1)

    
### Generate Response from Gemini API ###
def generate_content(client: genai.Client, messages: list[types.Content], verbose: bool) -> str | None:
    response = client.models.generate_content(model=model_name, contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt,  temperature = 0, tools=[available_functions]))
    function_responses: list[types.Part] = []
    
    
### Check if the response has text and return it ###
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)
        
    if not response.function_calls:
        return response.text
    
    
    for call in response.function_calls:
        function_call_result = call_function(call, verbose=verbose)
        if function_call_result is None:
            raise RuntimeError(f"Function call {call.name} returned None.")
        if len(function_call_result.parts) == 0 or function_call_result.parts[0] is None:
            raise RuntimeError(f"Function call {call.name} returned no parts.")
        if function_call_result.parts[0].function_response is None:
            raise RuntimeError(f"Function call {call.name} returned no function response.")
        if function_call_result.parts[0].function_response.response is None:
            raise RuntimeError(f"Function call {call.name} returned no response.")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])
    messages.append(types.Content(role="user", parts=function_responses))
    
    
    return None


if __name__ == "__main__":
    main()