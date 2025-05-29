from openai import OpenAI  # For interacting with OpenAI's API
from sentence_transformers import SentenceTransformer  # For embedding generation
import chromadb  # For managing persistent memory storage

# Initialize OpenAI client
client = OpenAI(api_key="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")  # Replace with your actual key

# Initialize SentenceTransformer for embeddings
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize ChromaDB client for persistent memory
chroma_client = chromadb.PersistentClient(path='rag_memory')
memory_collection = chroma_client.get_or_create_collection('conversation_memory')

def store_memory(text, metadata=None):
    """
    Stores a memory in the ChromaDB collection.

    Args:
        text (str): The text to store.
        metadata (dict): Additional metadata to associate with the memory.
    """
    if metadata is None:
        metadata = {}
    embedding = sentence_model.encode(text).tolist()
    memory_collection.add(
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata],
        ids=[str(hash(text))]
    )

def retrieve_memories(query, top_k=3):
    """
    Retrieves the most relevant memories for a given query.

    Args:
        query (str): The query text.
        top_k (int): The number of top results to retrieve.

    Returns:
        list: A list of the most relevant documents.
    """
    index_size = memory_collection.count()
    if index_size == 0:
        return []
    k = min(top_k, index_size)
    embedding = sentence_model.encode(query).tolist()
    results = memory_collection.query(query_embeddings=[embedding], n_results=top_k)
    return results['documents'][0]

def summarize_history(conversation_turns):
    """
    Summarizes the conversation history using OpenAI's GPT model.

    Args:
        conversation_turns (list): A list of conversation turns.

    Returns:
        str: A brief summary of the conversation.
    """
    summary_prompt = [{"role": "system", "content": "Summarize this conversation briefly:"}] + conversation_turns
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=summary_prompt,
        temperature=0
    )
    return response.choices[0].message.content.strip()
def clear_memory_collection():
    """
    Deletes all documents in the conversation_memory collection.
    """
    try:
        all_docs = memory_collection.get()
        ids = all_docs['ids']
        if ids:
            memory_collection.delete(ids=ids)
            print("[INFO] Cleared all documents in conversation_memory.")
        else:
            print("[INFO] No documents to delete in conversation_memory.")
    except Exception as e:
        print("[ERROR] Failed to clear ChromaDB collection:", e)
