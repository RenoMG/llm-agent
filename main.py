import os
from dotenv import load_dotenv
from google import genai

def main():

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

    get_response = response

    if get_response.usage_metadata == None:
        raise RuntimeError("Failed API Request")

    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {get_response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {get_response.usage_metadata.candidates_token_count}")
    print(f"Response:\n{get_response.text}")


if __name__ == "__main__":
    main()
