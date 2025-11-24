import sys

import pandas as pd
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from discover_ollama import discover_ollama

df = pd. read_csv("realistic_restaurant_reviews.csv")
embeddings = OllamaEmbeddings(
    model="mxbai-embed-large", base_url=discover_ollama())

db_location = "./chrome_langchain_db"
add_documents = True
# not os.path.exists(db_location)

if add_documents:
    print(
        ".. loading documents ..", file=sys.stderr)

    documents = []
    ids = []
    for i, row in df.iterrows():
        document = Document(
            page_content=row["Title"] + " " + row["Review"],
            metadata={"rating": row["Rating"], "date": row["Date"]},
            id=str(i)
        )
        ids.append(str(i))
        documents.append(document)
        print(f"new document appended: {document}", file=sys.stderr)

vector_store = Chroma(
    collection_name="restaurant_reviews",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)
