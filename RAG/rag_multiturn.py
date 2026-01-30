import csv
import os

import azure.identity
import openai
from dotenv import load_dotenv
from lunr import lunr
from get_model import *

# Index the data from the CSV
with open("hybrid.csv") as file:
    reader = csv.reader(file)
    rows = list(reader)
documents = [{"id": (i + 1), "body": " ".join(row)} for i, row in enumerate(rows[1:])]
index = lunr(ref="id", fields=["body"], documents=documents)

SYSTEM_MESSAGE = """
You are a helpful assistant that answers questions about cars based off a hybrid car data set.
You must use the data set to answer the questions, you should not provide any info that is not in the provided sources.
"""

messages = [{"role": "system", "content": SYSTEM_MESSAGE}]

def search(query):
    # Search the index for the user question
    query = query.lower().replace("?", "")
    results = index.search(query)
    matching_rows = [rows[int(result["ref"])] for result in results]

    # Format as a markdown table, since language models understand markdown
    matches_table = " | ".join(rows[0]) + "\n" + " | ".join(" --- " for _ in range(len(rows[0]))) + "\n"
    matches_table += "\n".join(" | ".join(row) for row in matching_rows)
    return matches_table

while True:
    question = input("\nYour question about electric cars: ")

    # Search the CSV for the question
    matches = search(question)
    print("Found matches:\n")
    print(matches)

    # Use the matches to generate a response
    messages.append({"role": "user", "content": f"{question}\nSources: {matches}"})
    response = client.chat.completions.create(
    model=AZURE_OPENAI_DEPLOYMENT_ID,
    temperature=0.3,
    messages=messages
)
    bot_response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": bot_response})

    print(f"\nResponse from {AZURE_OPENAI_DEPLOYMENT_ID}: \n")
    print(bot_response)
