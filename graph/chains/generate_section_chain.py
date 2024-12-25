
from dotenv import load_dotenv
load_dotenv(override=True)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from qdrant_client.http.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models
from graph.state import WikiSection
from graph.nodes.index_references_node import vectorstore
import os

api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o", api_key=api_key)
retriever = vectorstore.as_retriever(k=3)  # Top 3 relevant documents


async def retrieve(inputs: dict):
    docs = await retriever.ainvoke(inputs["topic"] + ": " + inputs["section"])
    formatted = "\n".join(
        [
            f'<Document href="{doc.metadata["source"]}"/>\n{doc.page_content}\n</Document>'
            for doc in docs
        ]
    )
    return {"docs": formatted, **inputs}




section_writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert Wikipedia writer. "
            "Complete your assigned WikiSection from the following outline:\n\n"
            "Minimun number of words per section or subsection is 1000"
            "Section must provide comprehensive, in-depth knowledge with nuanced insights and thorough explanations, ensuring clarity and expert-level detail"
            "Develop a thorough and nuanced analysis of the topic at hand. The section should incorporate historical context, current trends, and future implications. Break down the subject into key subtopics, providing detailed insights, data (where applicable), and examples or case studies. Address challenges, opposing viewpoints, and potential solutions. Ensure the content is structured logically and reflects expert-level understanding"
            "{outline}\n\nCite your sources, using the following references:\n\n<Documents>\n{docs}\n<Documents>",
        ),
        ("user", "Write the full WikiSection for the {section} section."),
    ]
)

section_writer = (retrieve | section_writer_prompt
    | llm.with_structured_output(WikiSection))
