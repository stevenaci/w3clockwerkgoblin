from datetime import datetime
from typing import Optional
from pydantic import BaseModel
"""
https://statistic-service.w3champions.com/api/players/Minigun%2311620/winrate?season=2
"""
gateway_map = {10:'America', 20: 'Europe'}
gamemode_map = {1: '1v1', 2:'2v2', 3:'3v3', 4:'4v4'}
race_map = {
    1:"Hu",
    2:"Or",
    8:"Ud",
    4:"Ne",
    0:"Rd"
}
class WinLosses(BaseModel):
    race: int
    wins: int
    losses: int
    games: int
    winrate: float

class iPlayerAka(BaseModel):
    name: str
    main_race: str
    country: str
    liquipedia: str

class PlayerStats(BaseModel):
    battleTag: str
    name: str
    participatedInSeasons: list
    winLosses: list[WinLosses]

class MatchPlayer(BaseModel):
    race: Optional[int]
    oldMmr: Optional[int]
    currentMmr: int
    battleTag: str
    name: str
    mmrGain: int
    won: bool
    location: str
    country: Optional[str]
    def describe(self):
        return format(
            "Race: {} "\
            "Mmr: {} "\
            "Battletag:{} ",
            self.race, self.currentMmr, self.battleTag
        )

class MatchTeam(BaseModel):
    players: list[MatchPlayer]
    @property
    def describe(self):
        return [p.describe for p in self.players].join(" \n")

class Match(BaseModel):
    map: str
    id: str
    durationInSeconds: int
    startTime: datetime
    endTime: datetime
    gameMode: int
    teams: list[MatchTeam]
    gateWay: int
    season: int

    @property
    def game_mode(self):
        return gamemode_map.get(self.gameMode)
    
    @property
    def players(self):
        return sum([
            team.players for team in self.teams
        ], []) if self.teams else []

    def opponents(self, battletag: str) -> list[MatchPlayer]:
        # collect teams which doesn't have this player on it.
        # collect players
        opponent_teams = []
        for team in self.teams:
            if not any([p.battleTag == battletag for p in team.players]):
                opponent_teams.append(team)

        return sum([
            team.players for team in opponent_teams
        ], []) if opponent_teams else []


    def describe_game(self, user_bt: str):
        return (
            f"Map: {self.map} Time elapsed: {(self.startTime.replace(tzinfo=None) - datetime.now()).seconds} seconds",
            f"Oppo: { ', '.join(p.battleTag for p in self.players) }",
            f"Game M0de: {self.game_mode}"
        )
    
    @property
    def describe_teams(self):
        s = ""
        for i, team in enumerate(self.teams):
            s += "Team " + i + "\n" + team.describe

