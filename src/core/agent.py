# src/core/agent.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.core.vector_db import SunbeamKnowledgeBase
from src.core.llm import get_llm

def initialize_agent():
    """
    Creates a Direct RAG Chain that mimics the AgentExecutor interface.
    This is much more stable for Local LLMs than a ReAct Agent.
    """
    
    # 1. Setup Resources
    kb = SunbeamKnowledgeBase()
    retriever = kb.get_retriever(k=4) # Retrieve top 4 chunks
    llm = get_llm()

    # 2. Define the Prompt
    # We explicitly ask the model to act as SIA and use the context.
    system_template = """You are SIA, the official AI assistant for Sunbeam Infotech.
    
    Use the following pieces of retrieved context to answer the student's question.
    If the answer is not in the context, politely say you don't know and advise them to contact admission@sunbeaminfo.com.
    
    CONTEXT:
    {context}
    
    CHAT HISTORY:
    {chat_history}
    
    STUDENT QUESTION:
    {question}
    
    ANSWER (Be professional, concise, and use bullet points if needed):
    """
    
    prompt = ChatPromptTemplate.from_template(system_template)

    # 3. Helper to format documents
    def format_docs(docs):
        return "\n\n".join([d.page_content for d in docs])

    # 4. Define the Chain (Retrieve -> Prompt -> LLM)
    rag_chain = (
        {
            "context": lambda x: format_docs(retriever.invoke(x["question"])),
            "question": lambda x: x["question"],
            "chat_history": lambda x: x["chat_history"]
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    # 5. Wrapper Class
    # This ensures your existing app.py code (which expects .invoke() and ['output']) continues to work.
    class RAGEngineWrapper:
        def invoke(self, input_dict):
            # Extract query and history from the app.py input
            query = input_dict.get("input", "")
            
            # Simple formatter for chat history (convert list of dicts to string)
            history_list = input_dict.get("chat_history", [])
            history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history_list[-5:]]) # Keep last 5 msgs
            
            # Run the chain
            response_text = rag_chain.invoke({
                "question": query,
                "chat_history": history_str
            })
            
            # Return in the format app.py expects
            return {"output": response_text}

    return RAGEngineWrapper()