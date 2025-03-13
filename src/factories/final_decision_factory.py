from typing import Dict, Any

from src.models.final_decision import FinalDecision


class FinalDecisionFactory:
    @staticmethod
    def create_final_decision(decision_data: Dict[str, Any]) -> FinalDecision:
        blocks_data = decision_data.get("blocks", [])
        return FinalDecision()
