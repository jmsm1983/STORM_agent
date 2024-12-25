
from dotenv import load_dotenv
load_dotenv(override=True)
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from graph.state import Perspectives

import os
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o", api_key=api_key)
gen_perspectives_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You need to select a diverse (and distinct) group of editors who will work together to create a comprehensive article on the topic. 
            Each of them represents a different perspective, role, or affiliation related to this topic.\
            You can use other Wikipedia pages of related topics for inspiration. For each editor, add a description of what they will focus on.
        
            Wiki page outlines of related topics for inspiration:
            {examples}""",
                ),
                ("user", "Topic of interest: {topic}"),
            ]
        )

gen_perspectives_chain = gen_perspectives_prompt | llm.with_structured_output(Perspectives)