import requests as re
from w3c.w3c_interface import Match, PlayerStats


class Endpoints:
    PLAYERS = "players/"
    MATCHES_ONGOING = "matches/ongoing/"


class W3CServer:

    live_prefix = "https://"
    mock_prefix = "mock://"
    base_url = "statistic-service.w3champions.com/api/"

    def full_url(self, end_point: str, mock: bool = False):
        prefix = self.mock_prefix if mock else self.live_prefix 
        return prefix + self.base_url + end_point
    
    def __init__(self) -> None:
        pass
        # self.mocker = Mocker()
        # self.mocker.get(self.mock_prefix + self.full_url(Endpoints.PLAYERS) , json=test_player_stats)
        # self.mocker.get(self.mock_prefix + self.full_url(Endpoints.MATCHES_ONGOING), json=test_match)


class W3CApi():

    server = W3CServer()
  
    def get_json(self, endpoint: str, player: str):
        try:
            res = re.get(self.server.full_url(endpoint + player))
            return res.json()
        except:
            return {}

    def get_player_stats(self, player_url: str):
        res = self.get_json(Endpoints.PLAYERS, player_url)
        return PlayerStats(**res)

    def get_current_match(self, player_url: str):
        return  Match(**self.get_json(Endpoints.MATCHES_ONGOING, player_url))
