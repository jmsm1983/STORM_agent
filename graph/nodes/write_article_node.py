
from graph.state import ResearchState
from graph.chains.generate_article_chain import writer
from graph.tools.visualizer import generate_image
from graph.tools.pdf import markdown_to_pdf_file,generate_html_text

async def write_article(state: ResearchState):
    topic = state["topic"]
    sections = state["sections"]
    draft = "\n\n".join([section.as_str for section in sections])
    article = await writer.ainvoke({"topic": topic, "draft": draft})

    image_description=f"""
    Abstract digital art in a minimalistic style, representing the concept of {topic} without any text. 
    The artwork features sleek lines, clean geometric shapes, and a subtle color palette on a white background, emphasizing a modern and innovative theme. 
    The design captures the essence of contemporary innovation in legal documentation, focusing on simplicity and elegance. 
    """

    generate_image(image_description)
    markdown_text=generate_html_text(article)
    markdown_to_pdf_file(markdown_text)


    return {
        **state,
        "article": article,
    }