from dataclasses import dataclass
from openai import AsyncOpenAI


@dataclass
class AttackReport:
    agent_name: str
    god: str
    domain: str
    emoji: str
    findings: list[str]
    severity: str  # LOW / MEDIUM / HIGH / CRITICAL
    raw: str


def make_client() -> AsyncOpenAI:
    return AsyncOpenAI()
