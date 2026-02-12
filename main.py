import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():

    #Load env variable
    try:
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
    except Exception as err:
        RuntimeError(f"Something went wrong {err}")

    #Get args from user for custom prompt
    parser = argparse.ArgumentParser(description="Mini Reno")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    args = parser.parse_args()

    #Create client with api key and store conversation list
    client = genai.Client(api_key=api_key)


    #Choose model and provide prompt
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=args.user_prompt
    )

    #Get the response and then print the output
    get_response = response
    if get_response.usage_metadata == None:
        raise RuntimeError("Failed API Request")

    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {get_response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {get_response.usage_metadata.candidates_token_count}")
    print(f"Response:\n{get_response.text}")


if __name__ == "__main__":
    main()
