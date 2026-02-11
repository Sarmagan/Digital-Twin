from openai import OpenAI
from pypdf import PdfReader
import gradio as gr
import json
import requests
import os 
# inspired by Ed Donner's Agentic AI course in Udemy

openai = OpenAI()
MODEL_NAME = "gpt-5-nano"

MAX_ITERATIONS = 10 # Safety limit to prevent infinite loops

reader = PdfReader("linkedin_profile.pdf")
linkedin = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text

with open("summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

name = "Suleyman Armagan Er"

system_prompt = f"You are acting as {name}. You are questions related to {name}'s career, background, \
skills and experience. Your responsibility is to represent {name} as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a future employer who came across the website. \
If you don't know the answer, say so."

system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."

# print(system_prompt)

def record_user_details(email, name="Name not provided", notes="not provided"):
    # records user details and sends a DM on Slack to Armagan 

    print(f"Recording interest from {name} with email {email} and notes {notes}")

    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("The SLACK_WEBHOOK_URL environment variable is not set.")

    payload = {"text": f"Recording interest from {name} with email {email} and notes {notes}"}
    requests.post(webhook_url, data=json.dumps(payload))
    return "Notification sent to Slack."
    
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json}]

def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
    return results

def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    
    for _ in range(MAX_ITERATIONS):
  
        response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    
        finish_reason = response.choices[0].finish_reason    

        if finish_reason=="tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            results = handle_tool_calls(tool_calls)
            messages.append(message)
            messages.extend(results)
            continue
        else:
            return response.choices[0].message.content

    return "I'm sorry, the request required too many steps to process."

if __name__ == "__main__":
    gr.ChatInterface(chat, type="messages").launch()