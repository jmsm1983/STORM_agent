
from dotenv import load_dotenv
load_dotenv(override=True)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from graph.subgraphs.interview_graph.chains.utils import swap_roles,tag_with_name

import os
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o", api_key=api_key)

gen_qn_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an experienced Wikipedia writer and want to edit a specific page. \
    Besides your identity as a Wikipedia writer, you have a specific focus when researching the topic. \
    Now, you are chatting with an expert to get information. Ask good questions to get more useful information.
    
    When you have no more questions to ask, say "Thank you so much for your help!" to end the conversation.\
    Please only ask one question at a time and don't ask what you have asked before.\
    Your questions should be related to the topic you want to write.
    Be comprehensive and curious, gaining as much unique insight from the expert as possible.\
    
    Stay true to your specific perspective:
    
    {persona}""",
            ),
            MessagesPlaceholder(variable_name="messages", optional=True),
        ]
    )

def build_gn_chain(editor):
    gn_chain = (
            RunnableLambda(swap_roles).bind(name=editor.name)
            | gen_qn_prompt.partial(persona=editor.persona)
            | llm
            | RunnableLambda(tag_with_name).bind(name=editor.name)
    )

    return gn_chain


