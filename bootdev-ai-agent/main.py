import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.services import FunctionCaller, FunctionMapper

class ContentGenerator():
    def __init__(self):
        pass


    def generate_content(self, client, messages, verbose=False):
        function_mapper = FunctionMapper()
        available_tools = types.Tool(
            function_declarations=function_mapper.get_available_function_schemas()
        )
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_tools],
                system_instruction=system_prompt,
            ),
        )
        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        
        # If there's no function call, return the text response
        if not response.function_calls:
            return response.text

        # Process function calls
        function_caller = FunctionCaller(verbose=verbose)
        function_responses = []
        print("Function responses: ")
        for function_call_part in response.function_calls:
            function_call_result = function_caller.call_function(function_call_part)

            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("empty function call result")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            
            messages.append(
                types.Content(
                    role="user",
                    parts=[function_call_result.parts[0]]
                )
            )
            function_responses.append(function_call_result.parts[0])

        if not function_responses:
            raise Exception("no function responses generated, exiting.")


def main():
    load_dotenv() 
    
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("Welcome to the Code Assistant!")
        print("We are using Gemini 2.0 Flash model to assist you with your coding needs.")
        print("")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
        
    user_prompt = " ".join(args)
    
    if verbose:
        print(f"User prompt:, {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    content_service = ContentGenerator()
    for iteration in range(20):
        try:
            result = content_service.generate_content(client, messages, verbose=verbose)
            if result:
                print("\nFinal response from AI:")
                print(result)
                break
        except Exception as e:
            print(f"Error during content generation: {e}")
            break

if __name__ == "__main__":
    main()
