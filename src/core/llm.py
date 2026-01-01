from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from src.config import LLM_BASE_URL, LLM_API_KEY, EMBEDDING_MODEL_NAME

def get_llm():
    """Returns the Chat Model (LLM) connected to LM Studio."""
    return ChatOpenAI(
        base_url=LLM_BASE_URL,
        api_key=LLM_API_KEY,
        temperature=0.3,  # Lower temperature for accurate factual answers
        model="local-model" 
    )

def get_embedding_model():
    """Returns the Nomic Embedding Model as configured in your original script."""
    return OpenAIEmbeddings(
        model=EMBEDDING_MODEL_NAME,
        openai_api_base=LLM_BASE_URL,
        openai_api_key=LLM_API_KEY,
        check_embedding_ctx_length=False
    )