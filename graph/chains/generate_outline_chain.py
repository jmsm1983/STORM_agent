
from dotenv import load_dotenv
load_dotenv(override=True)
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from graph.state import  Outline
from langchain_openai import ChatOpenAI

import os
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o", api_key=api_key)

direct_gen_outline_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a Wikipedia writer. Write an outline for a Wikipedia page about a user-provided topic. Be comprehensive and specific.",
        ),
        ("user", "{topic}"),
    ]
)

generate_outline_direct = direct_gen_outline_prompt | llm .with_structured_output(Outline)

