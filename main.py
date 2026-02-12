import os
from dotenv import load_dotenv
from google import genai

try:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
except Exception as err:
    RuntimeError(f"Something went wrong {err}")

prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.5-flash', contents=prompt
)

print(response.text)

def main():
    print("Hello from llm-agent!")


if __name__ == "__main__":
    main()
