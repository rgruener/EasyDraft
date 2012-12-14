from flask.ext.login import UserMixin

class User(UserMixin):

    def __init__(self, username, email, password, active=True):
        self.username = username
        self.email = email
        self.password = password
        self.active = active

    def is_active(self):
        return self.active

    def get_id(self):
        return str(self.username)

class League():

    def __init__(self, league_id, name, roster_size, yahoo_league_key, yahoo_league_id):
        self.league_id = league_id
        self.name = name
        self.roster_size = roster_size
        self.yahoo_league_key = yahoo_league_key
        self.yahoo_league_id = yahoo_league_id

class Team():

    def __init__(self, league_id, name, roster_size, yahoo_league_key, yahoo_league_id):
        self.league_id = league_id
        self.name = name
        self.roster_size = roster_size
        self.yahoo_league_key = yahoo_league_key
        self.yahoo_league_id = yahoo_league_id

class Player():

    def __init__(self, player_id, first_name, last_name, nfl_team, position=None):
        self.player_id = player_id
        self.first_name = first_name
        self.last_name = last_name
        self.nfl_team = nfl_team
        self.position = position
