from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.recommendation import ScenarioInput, ScenarioResult
from app.services.outcome_simulator.simulator_engine import run_simulation
from app.services.outcome_simulator.scenario_builder import get_predefined_scenarios

router = APIRouter(prefix="/simulator", tags=["Simulator"])

@router.post("/simulate", response_model=ScenarioResult, status_code=status.HTTP_200_OK)
def simulate_scenario(
    request: ScenarioInput,
    db: Session = Depends(get_db)
):
    """
    Simulates changes to alternative cashflow and repayment variables,
    returning a projected score, grade, and outcome recommendation.
    """
    try:
        result = run_simulation(
            db=db,
            gstin=request.gstin,
            adjustments=request.adjustments
        )
        return ScenarioResult(
            projected_score=result["projected_score"],
            projected_grade=result["projected_grade"],
            projected_outcome=result["projected_outcome"],
            delta_score=result["delta_score"],
            improvements=result["improvements"]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Simulation calculation error: {str(e)}"
        )

@router.get("/scenarios", response_model=List[Dict[str, Any]])
def list_scenarios():
    """
    Lists predefined credit scoring improvement scenarios for borrowers.
    """
    return get_predefined_scenarios()
