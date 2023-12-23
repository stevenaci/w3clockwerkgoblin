from w3c.w3c_service import W3CApi
from w3c.w3c_interface import Match, PlayerStats
import traceback

class Player():

    name: str

    def __init__(self, channel, bnet: str):
        self.bnet = bnet
        self.channel = channel
        self.name, self.id = [s for s in bnet.split("#")[0:2]]
        assert self.name and self.id

    @property
    def w3c_url(self)-> str:
        return f"{self.name}%23{self.id}"

    def get_current_match(self) -> Match:
        try:
            return W3CApi().get_current_match(self.w3c_url)
        except:
            return None

    def describe_current_match(self) -> str:
        match: Match = self.get_current_match(self)
        if match:
            match.describe_teams(self.bnet)
        else:
            raise Exception() 

    def get_stats(self) -> PlayerStats:
        try:
            return W3CApi().get_player_stats(self.w3c_url)
        except Exception:
            print(traceback.print_exc())
            return None

