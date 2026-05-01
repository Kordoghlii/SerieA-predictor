# agent/scoring.py

from schemas.match import TeamStats
from data.fbref.repository import FBrefRepository


# ============================================================
# Normalization utilities
# ============================================================
min_shots_against = FBrefRepository("data/samples/serie_a_teams.csv").min_shots_against
max_shots_against = FBrefRepository("data/samples/serie_a_teams.csv").max_shots_against


def normalize_min_max(value: float, min_val: float, max_val: float) -> float:
    """
    Generic min-max normalization to [0, 1].
    """
    if max_val == min_val:
        return 0.5  # neutral fallback
    return (value - min_val) / (max_val - min_val)


def defensive_quality(
    shots_against: float,
    min_shots_against: float,
    max_shots_against: float
) -> float:
    """
    Defensive quality derived from shots against.
    Lower shots against => higher defensive quality.
    """
    normalized = normalize_min_max(
        shots_against,
        min_shots_against,
        max_shots_against
    )
    return 1.0 - normalized


# ============================================================
# Main scoring logic
# ============================================================

def compute_team_score(
    stats: TeamStats,
    is_home: bool,
    min_shots_against: float,
    max_shots_against: float
) -> float:
    """
    Computes the final dominance score for a team.

    Pipeline:
    - Attack / Defense / Control (objective)
    - Base score
    - Venue-specific adjustment (home / away index)
    """

    # ----------------------------
    # ATTACK COMPONENT
    # ----------------------------

    shot_pressure = stats.shots_for - stats.shots_against
    shot_quality = stats.shots_on_target_pct * 10

    penalties_conversion_rate = (
        stats.penalties_converted / stats.penalties_for
        if stats.penalties_for > 0 else 0.0
    )

    attack = (
        shot_pressure * 0.40 +
        shot_quality * 0.30 +
        penalties_conversion_rate * 0.30
    )

    # ----------------------------
    # DEFENSE COMPONENT
    # ----------------------------

    penalties_conceded_rate = (
        stats.penalties_conceded / stats.penalties_against
        if stats.penalties_against > 0 else 0.0
    )

    saves_pct = stats.saves_pct / 100.0

    defense_quality = defensive_quality(
        stats.shots_against,
        min_shots_against,
        max_shots_against
    )

    defense = (
        (1.0 - penalties_conceded_rate) * 0.40 +
        defense_quality * 0.30 +
        saves_pct * 0.30
    )

    # ----------------------------
    # CONTROL COMPONENT
    # ----------------------------

    possession_factor = stats.avg_possession_pct / 100.0

    control = possession_factor

    # ----------------------------
    # BASE SCORE (venue-agnostic)
    # ----------------------------

    base_score = (
        attack * 0.50 +
        defense * 0.30 +
        control * 0.20
    )

    # ----------------------------
    # VENUE CONTEXT ADJUSTMENT
    # ----------------------------

    venue_boost = (
        stats.home_advantage_index
        if is_home
        else stats.away_advantage_index
    )

    final_score = base_score + venue_boost

    return round(final_score, 2)


# ============================================================
# Advantage & confidence decision
# ============================================================

def determine_advantage(home_score: float, away_score: float):
    """
    Determines match advantage and calibrated confidence.
    """

    diff = home_score - away_score

    if abs(diff) < 1.0:
        return "NONE", 0.50

    if diff > 0:
        confidence = min(0.50 + diff / 10.0, 0.90)
        return "HOME", round(confidence, 2)

    confidence = min(0.50 + abs(diff) / 10.0, 0.90)
    return "AWAY", round(confidence, 2)
