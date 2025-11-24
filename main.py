import sys

import httpx
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

from discover_ollama import discover_ollama
from vector import retriever

# ------------------------------------------------------------------
# 2️⃣  Initialise the LLM client with the discovered URL
# ------------------------------------------------------------------
try:
    ollama_url = discover_ollama()
except RuntimeError as exc:
    print(f"❌ {exc}", file=sys.stderr)
    sys.exit(1)

try:
    model = OllamaLLM(model="llama3.2", base_url=discover_ollama())
except Exception as e:
    print(
        f"❌ Failed to initialise Ollama client at {ollama_url}.",
        file=sys.stderr,
    )
    print(f"   Error details: {e}", file=sys.stderr)
    sys.exit(1)

# ------------------------------------------------------------------
# 3️⃣  Build the prompt chain
# ------------------------------------------------------------------
template = """

You are an expert in answerting questions about a pizza restaurant.
Here are some relevant reviews: {reviews}
Here is the question to answer: {question}

"""


prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("\n\n------------------")
    question = input("Ask your question (q to quit) :")
    print("\n\n")
    if question == "q":
        break

    # ------------------------------------------------------------------
    # 4️⃣  Invoke the chain and handle errors
    # ------------------------------------------------------------------

    try:
        reviews = retriever.invoke(question)
        result = chain.invoke(
            {"reviews": [], "question": "What is the best pizza place in town?"})
        print(result)
    except Exception as e:
        print(f"   Error details: {e}", file=sys.stderr)
        sys.exit(1)
