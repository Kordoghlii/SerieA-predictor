from fastapi import APIRouter, HTTPException
from agent.orchestrator import analyze_match
from schemas.match import MatchContext
from data.fbref.repository import FBrefRepository

router = APIRouter()

fbref_repo = FBrefRepository(csv_path="data/samples/serie_a_teams.csv")

@router.post("/analyze-match", response_model=None)
def analyze_match_route(payload: dict):
    try:
        home_team = payload["home_team"]
        away_team = payload["away_team"]
        competition = payload["competition"]
        match_date = payload["match_date"]

        home_stats = fbref_repo.get_team_stats(home_team)
        away_stats = fbref_repo.get_team_stats(away_team)

        context = MatchContext(
            home_team=home_team,
            away_team=away_team,
            competition=competition,
            match_date=match_date,
            home_stats=home_stats,
            away_stats=away_stats,
        )
        result = analyze_match(context)

        # IMPORTANT: return ONLY a dict
        return result.to_dict()
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing field in payload: {e}")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
