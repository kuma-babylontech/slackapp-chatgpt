import os
import re

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

app = App(token=os.getenv("SLACK_BOT_TOKEN"))

@app.event("app_mention")
def handle_mention(event, say):
    thread_ts = event["ts"]
    message = re.sub(r"<@.*>", "", event["text"])

    llm = ChatOpenAI(
        model_name=os.getenv("OPENAI_API_MODEL"),
        temperature=os.getenv("OPENAI_API_TEMPERATURE"),
    )

    response = llm.predict(message)
    say(text=response, thread_ts=thread_ts)

if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()
