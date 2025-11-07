import os
from dotenv import load_dotenv
from google import genai
import sys

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")





def main():
    print("Hello from bootdev-ai-agent!")
    if sys.argv[1]:
        user_prompt = sys.argv[1]

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=user_prompt,
        )
        print(response.text)
    else:
        print("No prompt provided.")
        exit(1)

if __name__ == "__main__":
    main()
