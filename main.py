import sys
import httpx
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# ------------------------------------------------------------------
# 1️⃣  Discover the Ollama host
# ------------------------------------------------------------------
OLLAMA_PORT = 11434
CANDIDATES = [
    f"http://host.docker.internal:{OLLAMA_PORT}",
    f"http://localhost:{OLLAMA_PORT}",
]


def _is_ollama_up(url: str) -> bool:
    """
    Ping the Ollama server.  Ollama exposes a simple `/api/tags` endpoint
    that returns a JSON list of available models.  If the request succeeds
    (status 200) we consider the host reachable.
    """
    try:
        with httpx.Client(timeout=2.0) as client:
            resp = client.get(f"{url}/api/tags")
            return resp.status_code == 200
    except Exception:
        return False


def discover_ollama() -> str:
    """
    Return the first URL from CANDIDATES that responds to /api/tags.
    Raise RuntimeError if none are reachable.
    """
    for url in CANDIDATES:
        if _is_ollama_up(url):
            return url
    raise RuntimeError(
        "Could not reach an Ollama daemon on any of the following URLs:\n"
        + "\n".join(f"  - {u}" for u in CANDIDATES)
        + "\n\nMake sure the Ollama server is running and reachable."
    )


# ------------------------------------------------------------------
# 2️⃣  Initialise the LLM client with the discovered URL
# ------------------------------------------------------------------
try:
    ollama_url = discover_ollama()
except RuntimeError as exc:
    print(f"❌ {exc}", file=sys.stderr)
    sys.exit(1)

try:
    model = OllamaLLM(model="gpt-oss", base_url=ollama_url)
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
        result = chain.invoke(
            {"reviews": [], "question": "What is the best pizza place in town?"})
        print(result)
    except Exception as e:
        print(
            f"❌ Failed to connect to the Ollama server at {ollama_url}.",
            file=sys.stderr,
        )
        print(
            "   Make sure the Ollama daemon is running and reachable from the container.",
            file=sys.stderr,
        )
        print(f"   Error details: {e}", file=sys.stderr)
        sys.exit(1)
