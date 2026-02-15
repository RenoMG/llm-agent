import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import SYSTEM_PROMPT
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

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
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    #Create client with api key and store conversation list
    client = genai.Client(api_key=api_key)
    message_history = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    #Available function calls
    available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file],
    )

    #Choose model and provide prompt
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=message_history,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT, 
            temperature=0)   
    )

    #Get the response and then print the output
    get_response = response
    if get_response.usage_metadata == None:
        raise RuntimeError("Failed API Request")
    
    #Call function
    def call_function(function_call, verbose=False):
        if verbose:
            print(f"Calling function: {function_call.name}({function_call.args})")
        else:
            print(f"Calling function: {function_call.name}")

        function_map = {
        "get_file_content": get_file_content,
        "write_file" : write_file,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        }

        function_name = function_call.name or ""

        if function_name not in function_map:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )          
        
        args = dict(function_call.args) if function_call.args else {}

        args["working_directory"] = "./calculator"

        function_result = function_map[function_name](**args)

        return types.Content(
        role="tool",
        parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
                )
            ],
        )
          
    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {get_response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {get_response.usage_metadata.candidates_token_count}")
        if get_response.function_calls != None:
            function_call_result = ""
            for call in get_response.function_calls:
                function_call_result = call_function(call, True)
            if len(function_call_result.parts) == 0:
                raise Exception("Empty .parts list!")
            if function_call_result.parts[0] == None:
                raise Exception(".parts[0] is none!")
            if function_call_result.parts[0].function_response.response == None:
                raise Exception("Response is none!")
            function_call_result.parts[0].function_response.response
            print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(f"Response:\n{get_response.text}")
    else:
        if get_response.function_calls != None:
            function_call_result = ""
            for call in get_response.function_calls:
                function_call_result = call_function(call, False)
            if len(function_call_result.parts) == 0:
                raise Exception("Empty .parts list!")
            if function_call_result.parts[0] == None:
                raise Exception(".parts[0] is none!")
            if function_call_result.parts[0].function_response.response == None:
                raise Exception("Response is none!")
            function_call_result.parts[0].function_response.response
        else:
            print(f"Response:\n{get_response.text}")


if __name__ == "__main__":
    main()
