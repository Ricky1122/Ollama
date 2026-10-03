from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

print("🔄 Initializing local Ollama models...")
# 1. Configure Settings to use Ollama for both LLM and Embeddings
Settings.llm = Ollama(model="tinyllama", request_timeout=360.0)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

print("📄 Chunking and Indexing documents from ./data ...")
# 2. Automatically load documents, parse them, chunk them, and generate embeddings
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)

print("🚀 Creating the retrieval engine...")
# 3. Assemble the RAG query engine
query_engine = index.as_query_engine()

print("\n✅ System Ready! Ask a question based on your documents.")
# 4. Prompt your local data
while True:
    user_query = input("\nUser Query: ")
    if user_query.lower() in ['exit', 'quit']:
        break
        
    print("🤖 Searching local database and generating answer...")
    response = query_engine.query(user_query)
    print(f"\nAnswer:\n{response}")
