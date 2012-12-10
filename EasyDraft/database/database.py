from flask.ext.mysql import MySQL
from EasyDraft.models import User, Player, Team, League

class Database():

    def __init__(self, app):
        self.mysql = MySQL()
        self.mysql.init_app(app)

    def get_all_users(self):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT username, email, password FROM Users WHERE is_active = True"""
        cursor.execute(query)
        rows = cursor.fetchall()
        users = []
        for row in rows:
            users.append(User(row[0], row[1], row[2]))
        #self.mysql.get_db().close()
        return users


    def get_user(self, username=None, email=None, password=None):
        if email is None and username is None:
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        first = True
        query = """SELECT username, email, password, is_active FROM Users WHERE """
        if username:
            query += """username = '%s'""" % (username)
            first = False
        if email:
            if not first:
                query += """ AND """
            query += """email = '%s'""" % (email)
            first = False
        if password:
            if not first:
                query += """ AND """
            query += """password = '%s'""" % (password)
        cursor.execute(query)
        u = cursor.fetchone()
        cursor.close()
        #self.mysql.get_db().close()
        if not u:
            return None
        return User(u[0], u[1], u[2], u[3])

    def insert_user(self, username, email, password):
        if (not (username and email and password)):
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        statement = """INSERT INTO Users (username, email, password) VALUES ('%s', '%s', '%s')""" % (username, email, password)
        cursor.execute(statement)
        self.mysql.get_db().commit()
        cursor.close()
        #self.mysql.get_db().close()
        return User(username, email, password)

    def update_user(self, username, email=None, password=None, is_active=True):
        if (not (username) or not (email or password)):
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        statement = """UPDATE Users SET is_active = %s""" % (str(is_active))
        if email:
            statement += """, email = '%s'""" % email
        if password:
            statement += """, password = '%s'""" % password
        statement += """ WHERE username = '%s'""" % username
        cursor.execute(statement)
        self.mysql.get_db().commit()
        cursor.close()
        #self.mysql.get_db().close()
        return User(username, email, password)


    def get_all_players(self):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT player_id, first_name, last_name, nfl_team FROM Players"""
        cursor.execute(query)
        rows = cursor.fetchall()
        players = []
        for row in rows:
            players.append(Player(row[0], row[1], row[2], row[3]))
        #self.mysql.get_db().close()
        return players


    def get_player(self, player_id=None, first_name=None, last_name=None, nfl_team=None):
        if player_id is None and first_name is None and last_name is None and nfl_team is None:
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        first = True
        query = """SELECT player_id, first_name, last_name, nfl_team FROM Players WHERE """
        if player_id:
            query += """player_id = '%s'""" % (player_id)
            first = False
        if first_name:
            if not first:
                query += """ AND """
            query += """first_name = '%s'""" % (first_name)
            first = False
        if last_name:
            if not first:
                query += """ AND """
            query += """last_name = '%s'""" % (last_name)
            first = False
        if nfl_team:
            if not first:
                query += """ AND """
            query += """nfl_team = '%s'""" % (nfl_team)
            first = False
        cursor.execute(query)
        p = cursor.fetchone()
        cursor.close()
        #self.mysql.get_db().close()
        if not p:
            return None
        return Player(p[0], p[1], p[2], p[3])

    def insert_player(self, player_id, first_name, last_name, nfl_team):
        if (not (player_id and first_name and last_name and nfl_team)):
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        statement = """INSERT INTO Players (player_id, first_name, last_name, nfl_team) VALUES ('%s', '%s', '%s', '%s')""" % \
                        (player_id, first_name, last_name, nfl_team)
        try:
            cursor.execute(statement)
            self.mysql.get_db().commit()
        except:
            pass
        cursor.close()
        #self.mysql.get_db().close()
        return Player(player_id, first_name, last_name, nfl_team)

    def update_player(self, player_id, first_name=None, last_name=None, nfl_team=None):
        if (not (player_id) or not (first_name or last_name or nfl_team)):
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        statement = """UPDATE Players SET """
        first = True
        if first_name:
            statement += """first_name = '%s'""" % first_name
            first = False
        if last_name:
            if not first:
                statement += """, """
            statement += """last_name = '%s'""" % last_name
        if nfl_team:
            if not first:
                statement += """, """
            statement += """nfl_team = '%s'""" % nfl_team
        statement += """ WHERE player_id = '%s'""" % player_id
        print statement
        cursor.execute(statement)
        self.mysql.get_db().commit()
        cursor.close()
        #self.mysql.get_db().close()
        return Player(player_id, first_name, last_name, nfl_team)

    def insert_position(self, player_id, position_name):
        if (not position_name or not player_id):
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        statement = """INSERT INTO Positions (position_name) VALUES ('%s')""" % (position_name)
        try:
            cursor.execute(statement)
            self.mysql.get_db().commit()
        except Exception, e:
            pass
        statement = """INSERT INTO Play (player_id, position_name) VALUES ('%s', '%s')""" % (player_id, position_name)
        try:
            cursor.execute(statement)
            self.mysql.get_db().commit()
        except Exception, e:
            pass
        cursor.close()
        #self.mysql.get_db().close()
        return position_name

    def insert_stat(self, stat_id, player_id, stat_value, stat_name, season=2012):
        if (not player_id or not stat_id or not stat_name):
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        statement = """INSERT INTO Stats (stat_id, player_id, stat_value, stat_name, season) VALUES ('%s', '%s', '%s', '%s', '%s')""" \
                            % (stat_id, player_id, stat_value, stat_name, season)
        try:
            cursor.execute(statement)
            self.mysql.get_db().commit()
        except Exception, e:
            pass
        cursor.close()
        #self.mysql.get_db().close()
        return (stat_id, player_id, stat_value, stat_name, season)
        
    def insert_league(self, league_name, yahoo_league_id, stat_value, stat_name, season=2012):
        if (not player_id or not stat_id or not stat_name):
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        statement = """INSERT INTO Stats (stat_id, player_id, stat_value, stat_name, season) VALUES ('%s', '%s', '%s', '%s', '%s')""" \
                            % (stat_id, player_id, stat_value, stat_name, season)
        try:
            cursor.execute(statement)
            self.mysql.get_db().commit()
        except Exception, e:
            pass
        cursor.close()
        #self.mysql.get_db().close()
        return (stat_id, player_id, stat_value, stat_name, season)
