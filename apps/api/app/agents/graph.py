from langgraph.graph import END, START, StateGraph

from app.agents.state import AgentState
from app.retrieval.base import RetrievalScope, Retriever
from app.services.generator import compose_grounded_answer


def build_graph(retriever: Retriever):
    async def retrieve(state: AgentState) -> AgentState:
        chunks = await retriever.search(
            state["message"],
            RetrievalScope(tenant_id=state["tenant_id"], user_id=state["user_id"]),
            limit=5,
        )
        return {"chunks": chunks}

    async def compose(state: AgentState) -> AgentState:
        answer, citations, unsupported = compose_grounded_answer(state.get("chunks", []))
        return {
            "answer": answer,
            "citations": citations,
            "unsupported": unsupported,
        }

    builder = StateGraph(AgentState)
    builder.add_node("retrieve", retrieve)
    builder.add_node("compose", compose)
    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "compose")
    builder.add_edge("compose", END)
    return builder.compile()
