
from dotenv import load_dotenv
load_dotenv(override=True)
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from graph.state import RelatedSubjects
import os
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o", api_key=api_key)


gen_related_topics_prompt = ChatPromptTemplate.from_template(
    """I'm writing a Wikipedia page for a topic mentioned below. 
    Please identify and recommend some Wikipedia pages on closely related subjects. 
    I'm looking for examples that provide insights into interesting aspects commonly associated with this topic, or examples that help me understand the typical content and structure included in Wikipedia pages for similar topics.

Please list the as many subjects and urls as you can.

Topic of interest: {topic}
"""
)

expand_chain = gen_related_topics_prompt | llm.with_structured_output(
    RelatedSubjects
)

