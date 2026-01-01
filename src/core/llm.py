from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from src.config import LLM_BASE_URL, LLM_API_KEY, EMBEDDING_MODEL_NAME

def get_llm():
    """Returns the Chat Model (LLM) connected to LM Studio."""
    return ChatOpenAI(
        base_url="http://127.0.0.1:1234/v1",
        api_key="not-needed",
        temperature=0.3,  # Lower temperature for accurate factual answers
        model="google/gemma-3-4b" 
    )

def get_embedding_model():
    """Returns the Nomic Embedding Model as configured in your original script."""
    return OpenAIEmbeddings(
        model=EMBEDDING_MODEL_NAME,
        openai_api_base=LLM_BASE_URL,
        openai_api_key=LLM_API_KEY,
        check_embedding_ctx_length=False
    )