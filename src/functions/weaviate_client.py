import os
import weaviate
from weaviate.classes.init import Auth
from dotenv import load_dotenv


def get_weaviate_client():
    wcd_url = os.getenv("WCD_URL")
    wcd_api_key = os.getenv("WCD_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    client = weaviate.connect_to_weaviate_cloud(
		cluster_url=wcd_url,
        auth_credentials=Auth.api_key(wcd_api_key),
        headers={"X-OpenAI-Api-Key": openai_api_key } 
  	)
    
    return client