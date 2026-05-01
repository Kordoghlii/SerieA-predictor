
from schemas.match import TeamStats

REQUIRED_FIELDS = {
    "team",
    "shots_for",
    "shots_against",
    "shots_on_target_pct",
    "matches_played",
    "avg_possession_pct",
}
def normalize_home_away_index(value: float) -> float:
        MIN_IDX = 5.0
        MAX_IDX = 20.0

        value = max(MIN_IDX, min(value, MAX_IDX))  # clamp
        return (value - MIN_IDX) / (MAX_IDX - MIN_IDX)
def map_team_row(row: dict) -> TeamStats:
    missing = REQUIRED_FIELDS - row.keys()
    if missing:
        raise ValueError(f"Missing fields in team data: {missing}")
    
    return TeamStats(
        team_name=row["team"],
        shots_for=float(row["shots_for"]),
        shots_against=float(row["shots_against"]),
        shots_on_target_pct=float(row["shots_on_target_pct"]),
        penalties_for=float(row["penalties_for"]),
        penalties_converted=float(row["penalties_converted"]),
        penalties_against=float(row["penalties_against"]),
        penalties_conceded=float(row["penalties_conceded"]),
        saves_pct=float(row["saves_pct"]),
        matches_played=int(row["matches_played"]),
        avg_possession_pct=float(row["avg_possession_pct"]),
        home_advantage_index= normalize_home_away_index(float(row["home_advantage_index"])),
        away_advantage_index= normalize_home_away_index(float(row["away_advantage_index"])),
    )
