from dotenv import load_dotenv
import weaviate
import weaviate.classes as wvc
from weaviate.classes.query import MetadataQuery
import os
import requests
import json
from tqdm import tqdm

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
    # コレクションが既に存在するかチェック
    try:
        questions = client.collections.get("Question")
        print("Collection 'Question' already exists.")
    except weaviate.exceptions.UnexpectedStatusCodeException:
        questions = client.collections.create(
            name="Question",
            vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
            generative_config=wvc.config.Configure.Generative.openai(),
        )
        print("Collection 'Question' created successfully.")

    # コレクションにデータがあるかチェック
    response = questions.query.fetch_objects(limit=1)

    if len(response.objects) == 0:
        # データの取得と登録
        resp = requests.get(
            "https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json"
        )
        data = json.loads(resp.text)  # Load data

        question_objects = [
            {
                "answer": d["Answer"],
                "question": d["Question"],
                "category": d["Category"],
            }
            for d in data
        ]

        questions.data.insert_many(question_objects)
        print(
            f"Data insertion completed. {len(question_objects)} questions added to the collection."
        )
    else:
        print("Collection already contains data. No new data inserted.")

    # ベクトル検索の実行
    search_query = "biology"
    response = questions.query.near_text(
        query=search_query,
        limit=2
    )

    print(f"\nSearch results for '{search_query}':")
    for obj in response.objects:
        print(f"Question: {obj.properties['question']}")
        print(f"Answer: {obj.properties['answer']}")
        print(f"Category: {obj.properties['category']}")
        print("---")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client.close()  # Close client gracefully
