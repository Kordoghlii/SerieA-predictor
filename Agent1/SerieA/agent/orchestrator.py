# agent/orchestrator.py

from schemas.match import MatchContext, AnalysisResult
from agent.reasoning import analyze_with_llm
from agent.scoring import compute_team_score, determine_advantage 
from data.fbref.repository import FBrefRepository as repo

def analyze_match(context: MatchContext) -> AnalysisResult:
    """
    Entry point for match analysis.

    Coordinates data preparation and reasoning.
    """
    min_sa, max_sa = repo("data/samples/serie_a_teams.csv").get_defensive_bounds()

    home_score = compute_team_score(
        context.home_stats,
        is_home=True,
        min_shots_against=min_sa,
        max_shots_against=max_sa
        )
    away_score = compute_team_score(
        context.away_stats,
        is_home=False,
        min_shots_against=min_sa,
        max_shots_against=max_sa
    )
    advantage, confidence = determine_advantage(home_score, away_score)


    # Prepare payload for reasoning engine
    prompt_payload = {
        "match_context":{
            "home_team": context.home_team,
            "away_team": context.away_team,
            "competition": context.competition,
            "match_date": context.match_date,
            "home_stats": context.home_stats.__dict__,
            "away_stats": context.away_stats.__dict__,
        },
        "scoring":{
            "home_score": home_score,
            "away_score": away_score,
            "advantage": advantage,
            "confidence": confidence,
        }   
    }

    # Delegate reasoning to LLM-based engine
    explanation = analyze_with_llm(prompt_payload)

    # Validate and construct domain result
    try:
        result = AnalysisResult(
            advantage=advantage,
            confidence=confidence,
            key_factors=explanation["key_factors"],
            risk_factors=explanation["risk_factors"],
            summary=explanation["summary"],
        )
    except KeyError as e:
        raise ValueError(f"Missing field in reasoning output: {e}")

    return result
