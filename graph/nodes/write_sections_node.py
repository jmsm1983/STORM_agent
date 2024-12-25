

from graph.state import ResearchState
from graph.chains.generate_section_chain import section_writer

async def write_sections(state: ResearchState):
    refined_outline = state["outline"]

    sections = await section_writer.abatch(
        [
            {
                "outline": refined_outline.as_str,
                "section": section.section_title,
                "topic": state["topic"],
            }
            for section in refined_outline.sections
        ]
    )
    return {
        **state,
        "sections": sections,
    }
