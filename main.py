from dotenv import load_dotenv
import weaviate
import weaviate.classes as wvc
import os
import requests
import json

load_dotenv()

# Best practice: store your credentials in environment variables
wcd_url = os.getenv("WCD_URL")
wcd_api_key = os.getenv("WCD_KEY")
openai_api_key = os.getenv("OPENAI_KEY")

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,  # Replace with your Weaviate Cloud URL
    auth_credentials=wvc.init.Auth.api_key(
        wcd_api_key
    ),  # Replace with your Weaviate Cloud key
    headers={
        "X-OpenAI-Api-Key": openai_api_key
    },  # Replace with appropriate header key/value pair for the required API
)

try:
    pass  # Replace with your code. Close client gracefully in the finally block.

finally:
    client.close()  # Close client gracefully
