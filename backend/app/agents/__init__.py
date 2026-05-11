# BACKEND_AGENT | 2026-05-10 | Agent registry
from app.agents.planner_agent import PlannerAgent
from app.agents.researcher_agent import ResearcherAgent
from app.agents.frontend_agent import FrontendAgent
from app.agents.backend_agent import BackendAgent
from app.agents.database_agent import DatabaseAgent
from app.agents.devops_agent import DevOpsAgent
from app.agents.update_agent import UpdateAgent
from app.models.agent_task import AgentType

AGENT_REGISTRY: dict[AgentType, type] = {
    AgentType.PLANNER: PlannerAgent,
    AgentType.RESEARCHER: ResearcherAgent,
    AgentType.FRONTEND: FrontendAgent,
    AgentType.BACKEND: BackendAgent,
    AgentType.DATABASE: DatabaseAgent,
    AgentType.DEVOPS: DevOpsAgent,
    AgentType.UPDATE: UpdateAgent,
}

__all__ = [
    "PlannerAgent",
    "ResearcherAgent",
    "FrontendAgent",
    "BackendAgent",
    "DatabaseAgent",
    "DevOpsAgent",
    "UpdateAgent",
    "AGENT_REGISTRY",
]
