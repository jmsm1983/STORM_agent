
from graph.state import ResearchState
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

# Initialize embeddings and vectorstore globally
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = InMemoryVectorStore(embedding=embeddings)  # Shared vectorstore


async def index_references(state: ResearchState):

    # Collect all reference documents
    all_docs = []

    for interview_state in state["interview_results"]:
        reference_docs = [
            Document(page_content=v, metadata={"source": k})
            for k, v in interview_state["references"].items()
        ]
        all_docs.extend(reference_docs)


    # Asynchronously add all documents to the vector store
    await vectorstore.aadd_documents(all_docs)

    print(f"Indexed {len(all_docs)} documents in memory (asynchronously).")

    return state