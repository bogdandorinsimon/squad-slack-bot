import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("eval_slack_bot")
logging.getLogger("slack_bolt").setLevel(logging.WARNING)
logger.info("Custom logger is working!")

# Load environment variables from .env file
load_dotenv()
logger.info("Environment variables loaded.")

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not SLACK_BOT_TOKEN or not SLACK_APP_TOKEN or not OPENAI_API_KEY:
    logger.error("Missing one or more required environment variables.")
    raise ValueError("SLACK_BOT_TOKEN, SLACK_APP_TOKEN, and OPENAI_API_KEY must be set.")

class 
class DummySearchTool:
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(
            openai_api_key=openai_api_key,
            temperature=0,  
        )

    def run(self, query: str) -> str:
        logger.info(f"Running DummySearchTool with query: {query}")
        try:
            response = self.llm(query)
            logger.info(f"ChatGPT response: {response}")
            if hasattr(response, "content"):
                return response.content
            else:
                return str(response)
        except Exception as e:
            logger.error(f"Error while querying ChatGPT: {str(e)}", exc_info=True)
            return "An error occurred while processing your request."

# Initialize the Slack Bolt App
app = App(token=SLACK_BOT_TOKEN)
logger.info("Slack Bolt App initialized.")

# Instantiate the DummySearchTool
dummy_tool = DummySearchTool(openai_api_key=OPENAI_API_KEY)

# Set Up an Event Listener for Mentions in Slack
@app.event("app_mention")
def mention_handler(body, say):
    logger.info("Received a mention event: %s", body)

    # Extract the text of the message
    user_query = body["event"]["text"]
    user_id = body["event"]["user"]
    say(f"Hey <@{user_id}>! I'm processing your request...")

    try:
        # Call the DummySearchTool to process the query
        response = dummy_tool.run(user_query)
        logger.info("DummySearchTool response: %s", response)
        say(response)
    except Exception as e:
        logger.error("An error occurred while processing the query: %s", str(e), exc_info=True)
        say("An error occurred: {}".format(str(e)))

# Start the Socket Mode Handler
if __name__ == "__main__":
    logger.info("Starting the Socket Mode Handler.")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()