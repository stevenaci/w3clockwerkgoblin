import pytest
from w3c.players import Players
from w3c.player import Player
from w3c.w3c_service import W3CApi, Endpoints, PlayerStats, re

@pytest.fixture
def players():
    return Players()

@pytest.mark.asyncio
async def test_add_remove_user(players: Players):
    twitch = "protectionfromblue"
    bnet = "NWILLIAMS28#1797"
    await players.add_player(twitch, bnet)
    assert players[twitch]
    # remove based on channel name
    players.remove_player(twitch)
    # Second time should not work, already been removed
    assert not players.get(twitch)
