import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt


def main():
    load_dotenv()
    
    args = sys.argv[1:]

    verbose = True if "--verbose" in args else False

    if not args:
        print("Welcome to the Code Assistant!")
        print("We are using Gemini 2.0 Flash model to assist you with your coding needs.")
        print("")
        sys.exit(1)

    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
        
    user_prompt = args[0]
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    def generate_content(client, messages):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt)
        )
        if verbose:   
            print(f"User prompt: {user_prompt}")
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        print("Response:")
        print(response.text)

    generate_content(client, messages)


if __name__ == "__main__":
    main()
