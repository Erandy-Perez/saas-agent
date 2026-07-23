import os
from dotenv import load_dotenv
from transformers import AutoTokenizer
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def inicializar_motor():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    loader = PyPDFLoader("directorio/Manual_ApexCore.pdf")
    docs = loader.load()

    tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-m3")
    splitter = CharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer=tokenizer,
        chunk_size=1200,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )

    vector_db = FAISS.from_documents(chunks, embeddings)
    retriever = vector_db.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 20, "lambda_mult": 0.7}
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0
    )

    prompt_base = ChatPromptTemplate.from_template('''
    Eres el agente de soporte técnico de ApexCore.
    Responde de manera formal y profesional utilizando exclusivamente la información del siguiente contexto.
    Si la respuesta no está en el contexto, responde textualmente: "La información solicitada no se encuentra en el manual técnico actual."
    
    Contexto:
    {contexto}

    Consulta:
    {query}

    Respuesta:''')

    cadena_principal = (
        {"contexto": retriever, "query": RunnablePassthrough()}
        | prompt_base
        | llm
        | StrOutputParser()
    )

    prompt_optimizacion = PromptTemplate.from_template('''
    Genera cinco variaciones de la siguiente pregunta técnica.
    Devuelve únicamente las preguntas separadas por saltos de línea.
    Pregunta: {question}''')
    
    cadena_optimizacion = prompt_optimizacion | llm | StrOutputParser()

    return cadena_principal, cadena_optimizacion
