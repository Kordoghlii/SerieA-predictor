# data/fbref/repository.py

from data.fbref.loader import load_fbref_csv
from data.fbref.mapper import map_team_row


def normalize_team_name(name: str) -> str:
    return (
        name.lower()
        .replace(" fc", "")
        .replace(" calcio", "")
        .replace(".", "")
        .strip()
    )


class FBrefRepository:
    def __init__(self, csv_path: str):
        # 1. Load raw CSV rows
        raw_rows = load_fbref_csv(csv_path)

        # 2. Map rows to TeamStats ONCE
        self.teams = [
            map_team_row(row) for row in raw_rows
        ]

        # 3. Build name index (TeamStats)
        self.index = {
            normalize_team_name(team.team_name): team
            for team in self.teams
        }

        # 4. Compute league-wide defensive bounds
        self.min_shots_against = min(
            team.shots_against for team in self.teams
        )
        self.max_shots_against = max(
            team.shots_against for team in self.teams
        )

    # ---------- Public API ----------

    def get_team_stats(self, team_name: str):
        key = normalize_team_name(team_name)

        if key not in self.index:
            raise ValueError(f"Team '{team_name}' not found in FBref data")

        return self.index[key]

    def get_defensive_bounds(self):
        return self.min_shots_against, self.max_shots_against
