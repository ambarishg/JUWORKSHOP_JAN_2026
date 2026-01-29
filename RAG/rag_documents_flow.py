import json
import os

import azure.identity
import openai
from dotenv import load_dotenv
from lunr import lunr
from get_model import *

# Index the data from the JSON - each object has id, text, and embedding
with open("rag_ingested_chunks.json") as file:
    documents = json.load(file)
    documents_by_id = {doc["id"]: doc for doc in documents}
index = lunr(ref="id", fields=["text"], documents=documents)

# Get the user question
user_question = "where do digger bees live?"

# Search the index for the user question
results = index.search(user_question)
retrieved_documents = [documents_by_id[result["ref"]] for result in results]
print(f"Retrieved {len(retrieved_documents)} matching documents, only sending the first 5.")
context = "\n".join([f"{doc['id']}: {doc['text']}" for doc in retrieved_documents[0:5]])

# Now we can use the matches to generate a response
SYSTEM_MESSAGE = """
You are a helpful assistant that answers questions about insects.
You must use the data set to answer the questions,
you should not provide any info that is not in the provided sources.
Cite the sources you used to answer the question inside square brackets.
The sources are in the format: <id>: <text>.
"""

response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.3,
    messages=[
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": f"{user_question}\nSources: {context}"},
    ],
)

print(f"\nResponse from {MODEL_NAME} on : \n")
print(response.choices[0].message.content)