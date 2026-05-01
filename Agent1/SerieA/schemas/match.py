# schemas/match.py
from typing import List, Dict, Any

class TeamStats:
    """
    Represents aggregated recent performance statistics of a team.
    All values must be provided explicitly by the caller.
    """
    def __init__(
        self,
        team_name: str,
        #shooting stats
        shots_for: int,  
        shots_against: int,
        shots_on_target_pct: float,
        #Set pieces
        penalties_for: float,
        penalties_converted: float,
        penalties_against: float,
        penalties_conceded: float,
        #Goalkeeping
        saves_pct: float,
        #General stats
        matches_played: int,
        avg_possession_pct: float,
        home_advantage_index: float,
        away_advantage_index: float
    ):
        if matches_played <= 0:
            raise ValueError("matches_played must be greater than 0")   
        self.team_name = team_name
        self.shots_for = shots_for
        self.shots_against = shots_against 
        self.shots_on_target_pct = shots_on_target_pct
        self.penalties_for = penalties_for
        self.penalties_converted = penalties_converted
        self.penalties_against = penalties_against
        self.penalties_conceded = penalties_conceded
        self.saves_pct = saves_pct
        self.matches_played = matches_played    
        self.avg_possession_pct = avg_possession_pct
        self.home_advantage_index = home_advantage_index
        self.away_advantage_index = away_advantage_index
    def to_dict(self) -> Dict[str, Any]:
        return {
            "team_name": self.team_name,
            "shots_for": self.shots_for,
            "shots_against": self.shots_against,
            "shots_on_target_pct": self.shots_on_target_pct,
            "penalties_for": self.penalties_for,
            "penalties_converted": self.penalties_converted,
            "penalties_against": self.penalties_against,
            "penalties_conceded": self.penalties_conceded,
            "saves_pct": self.saves_pct,
            "matches_played": self.matches_played,
            "avg_possession_pct": self.avg_possession_pct,
        }
class MatchContext:
    """
    Represents the full context of a football match before kickoff.
    """

    def __init__(
            self, 
            home_team: str,
            away_team: str,
            competition: str,
            match_date: str,
            home_stats: TeamStats, 
            away_stats: TeamStats,
    ):
        if home_team == away_team:
            raise ValueError("home_team and away_team must be different")
        self.home_team = home_team
        self.away_team = away_team  
        self.competition = competition
        self.match_date = match_date
        self.home_stats = home_stats
        self.away_stats = away_stats
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MatchContext":
        """
        Factory method used by external adapters (e.g. FastAPI) .
        """
        try:
            home_stats = TeamStats(**data["home_stats"])
            away_stats = TeamStats(**data["away_stats"])
            return cls(
                home_team=data["home_team"],
                away_team=data["away_team"],
                competition=data["competition"],
                match_date=data["match_date"],
                home_stats=home_stats,
                away_stats=away_stats,
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}") from e 
    def to_prompt_payload(self) -> Dict[str, Any]:
        """
        Returns a clean, LLM-ready representation.
        """
        return {
            "match": {
                "home_team": self.home_team,
                "away_team": self.away_team,
                "competition": self.competition,
                "match_date": self.match_date,
            },

            "home_team_stats": self.home_stats.to_dict(),
            "away_team_stats": self.away_stats.to_dict(),
        }
class AnalysisResult:
    """
    Represents the agent's final structured decision.
    """
    def __init__(
            self, 
            advantage: str,
            confidence: float,
            key_factors: List[str],
            risk_factors: List[str],
            summary: str,
    ):
        if advantage not in {"HOME", "AWAY", "NONE"}:
            raise ValueError("Advantage must be HOME, AWAY, or NONE")
        if not (0.0 <= confidence <= 1.0):
            raise ValueError("Confidence must be between 0.0 and 1.0")
        self.advantage = advantage
        self.confidence = confidence
        self.key_factors = key_factors
        self.risk_factors = risk_factors
        self.summary = summary
    def to_dict(self) -> Dict[str, Any]:
        return {
            "advantage": self.advantage,
            "confidence": self.confidence,
            "key_factors": self.key_factors,
            "risk_factors": self.risk_factors,
            "summary": self.summary,
        }