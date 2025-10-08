from json import load
from openai import AzureOpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid
import os
from dotenv import load_dotenv
load_dotenv()

# Azure OpenAI client   
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_EMBEDDING_API_KEY"),
    api_version=os.getenv("OPENAI_EMBEDDING_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT")
)

EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL_NAME")
VECTOR_DIM = 1536  # for text-embedding-3-small
COLLECTION_NAME = "compass_group_knowledge"

# Qdrant client (local or cloud)
qdrant = QdrantClient(
    host="localhost",  # change to cloud Qdrant URL if needed
    port=6333
)


def ensure_collection():
    """Create Qdrant collection if it doesn’t exist."""
    if COLLECTION_NAME not in [c.name for c in qdrant.get_collections().collections]:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE)
        )


def paragraph_chunks(text: str) -> list[str]:
    """
    Split story text into paragraphs.
    Paragraphs are separated by two newlines.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    return paragraphs


def create_embeddings(chunks: list[str]) -> list[list[float]]:
    """Generate embeddings from Azure OpenAI."""
    response = client.embeddings.create(
        model=EMBEDDING_DEPLOYMENT,
        input=chunks
    )
    return [data.embedding for data in response.data]


def store_in_qdrant(chunks: list[str], embeddings: list[list[float]]):
    """Store text chunks with embeddings in Qdrant."""
    points = []
    for chunk, embedding in zip(chunks, embeddings):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={"text": chunk}
            )
        )
    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    print(f"✅ Stored {len(points)} paragraphs in Qdrant collection '{COLLECTION_NAME}'")

def embed_text(text: str):
    emb = client.embeddings.create(
        model=EMBEDDING_DEPLOYMENT,
        input=text
    )
    return emb.data[0].embedding

def search_qdrant(query: str, top_k=5):
    vector = embed_text(query)
    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=top_k,
    )
    return [
        {
            "text": hit.payload.get("text", ""),
            "score": hit.score
        }
        for hit in results
    ]

def process_story_to_qdrant(story_text: str):
    ensure_collection()

    # Load the story text produced by the LLM
    # with open("knowledge_base.txt", "r", encoding="utf-8") as f:
    #     story_text = f.read()

    chunks = paragraph_chunks(story_text)
    embeddings = create_embeddings(chunks)
    store_in_qdrant(chunks, embeddings)

if __name__ == "__main__":
    with open("story_output_batched.txt", "r", encoding="utf-8") as f:
        story_text = f.read()
    process_story_to_qdrant(story_text)
