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
        cursor.close()
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
        cursor.execute(statement)
        self.mysql.get_db().commit()
        cursor.close()
        #self.mysql.get_db().close()
        return Player(player_id, first_name, last_name, nfl_team)

    def get_players_draft(self, league_id, order_by='last_name', position=None, nfl_team=None, last_name=None, limit=200):
        if not league_id:
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        first = True
        query = """SELECT P.player_id, P.first_name, P.last_name, P.nfl_team, Play.position_name FROM Players P, Play WHERE Play.player_id = P.player_id"""
        query += """ AND P.player_id NOT IN (SELECT P2.player_id FROM Plays_with_in Pl, Players P2, Teams T, Roster_of R WHERE \
                        Pl.league_id=%s and T.team_id=Pl.team_id and R.team_id=T.team_id and R.player_id=P2.player_id)""" % (league_id)
        if position:
            query += """ AND Play.position_name = '%s'""" % (position)
        if nfl_team:
            query += """ AND P.nfl_team LIKE """ + "'%" + str(nfl_team) + "%'"
            first = False
        if last_name:
            query += """ AND last_name LIKE """ + "'%" + str(last_name) + "%'"
            first = False
        query += """ ORDER BY %s LIMIT %s""" % (order_by,limit)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        players = []
        for row in rows:
            players.append(Player(row[0], row[1], row[2], row[3], row[4]))
        #self.mysql.get_db().close()
        return players

    def insert_pick(self, team_id, player_id):
        if (not team_id or not player_id):
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        statement = """INSERT INTO Roster_of (team_id, player_id) VALUES (%s, %s)""" \
                            % (team_id, player_id)
        try:
            cursor.execute(statement)
            ret_val = cursor.lastrowid
            self.mysql.get_db().commit()
        except Exception, e:
            print e
            ret_val=None
        cursor.close()
        #self.mysql.get_db().close()
        return ret_val

    def get_total_draft(self, league_id):
        if not league_id:
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT COUNT(P2.player_id) FROM Plays_with_in Pl, Players P2, Teams T, Roster_of R WHERE \
                Pl.league_id='%s' and T.team_id=Pl.team_id and R.team_id=T.team_id and R.player_id=P2.player_id""" % (league_id)
        cursor.execute(query)
        ans = cursor.fetchone()
        cursor.close()
        return ans

    def complete_draft(self, league_id):
        if not league_id:
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """UPDATE League SET drafted=True WHERE league_id=%s""" % (league_id)
        cursor.execute(query)
        cursor.close()
        self.mysql.get_db().commit()
        return True
    


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
        
    def insert_league(self, league_name, yahoo_league_id, roster_size):
        if (not league_name or not roster_size):
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        if yahoo_league_id:
            statement = """INSERT INTO Leagues (league_name, yahoo_league_id, roster_size) VALUES ('%s', '%s', %s)""" \
                                % (league_name, yahoo_league_id, roster_size)
        else:
            statement = """INSERT INTO Leagues (league_name, roster_size) VALUES ('%s', %s)""" \
                                % (league_name, roster_size)
        try:
            cursor.execute(statement)
            self.mysql.get_db().commit()
            league_id = cursor.lastrowid
        except Exception, e:
            pass
        cursor.close()
        #self.mysql.get_db().close()
        return league_id

    def my_leagues(self, username):
        if not username:
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT L.league_id, L.league_name, T.team_name, L.drafted, T.team_id from Plays_with_in P, Leagues L, Teams T \
                    WHERE P.username="%s" and P.league_id = L.league_id and P.team_id = T.team_id""" % (username)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        info = []
        for row in rows:
            info.append((row[0], row[1], row[2], row[3], row[4]))
        #self.mysql.get_db().close()
        return info

    def user_in_league(self, username, league_id):
        if not username or not league_id:
            return False
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """ SELECT * from Plays_with_in P WHERE P.username = '%s' AND P.league_id = %s""" % (username, league_id)
        cursor.execute(query)
        if not cursor.fetchone():
            cursor.close()
            return False
        cursor.close()
        return True

    def get_league(self, league_id):
        if not league_id:
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT league_id, league_name, roster_size, drafted FROM Leagues WHERE league_id = %s""" % (league_id)
        cursor.execute(query)
        league = cursor.fetchone()
        cursor.close()
        return league

    def get_league_teams(self, league_id):
        if not league_id:
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT T.team_id, T.team_name, P.username from Teams T, Plays_with_in P WHERE P.league_id=%s AND P.team_id=T.team_id;""" % (league_id)
        cursor.execute(query)
        teams = cursor.fetchall()
        cursor.close()
        return teams

    def get_league_team_ids(self, league_id):
        if not league_id:
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT T.team_id from Teams T, Plays_with_in P WHERE P.league_id=%s AND P.team_id=T.team_id;""" % (league_id)
        cursor.execute(query)
        teams = cursor.fetchall()
        cursor.close()
        return teams

    def get_team_players(self, team_id):
        if not team_id:
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT P.player_id, P.first_name, P.last_name, P.nfl_team, Play.position_name FROM Roster_of R, Players P, Play WHERE \
                            P.player_id=R.player_id AND R.team_id='%s' AND Play.player_id=P.player_id""" % (team_id)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        players = []
        for row in rows:
            players.append(Player(row[0], row[1], row[2], row[3], row[4]))
        #self.mysql.get_db().close()
        return players

    def insert_team(self, team_name, league_id, username="anonymous"):
        if (not team_name or not league_id):
            return None
        team_id = None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        statement = """INSERT INTO Teams (team_name) VALUES ('%s')""" \
                            % (team_name)
        try:
            cursor.execute(statement)
            self.mysql.get_db().commit()
            team_id = cursor.lastrowid
        except Exception, e:
            print e
        cursor.close()
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        statement = """INSERT INTO Plays_with_in (username, league_id, team_id) VALUES ('%s', %s, %s)""" \
                            % (username, league_id, team_id)
        try:
            cursor.execute(statement)
            self.mysql.get_db().commit()
        except Exception, e:
            print e
        cursor.close()
        #self.mysql.get_db().close()
        return team_id

    def insert_requirement(self, league_id, position_name, maximum, starters):
        if (not league_id or not position_name or not maximum or not starters):
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        statement = """INSERT INTO Requires (league_id, position_name, maximum, starters) VALUES (%s, '%s', %s, %s)""" \
                            % (league_id, position_name, maximum, starters)
        try:
            cursor.execute(statement)
            ret_val = cursor.lastrowid
            self.mysql.get_db().commit()
        except Exception, e:
            print e
        cursor.close()
        #self.mysql.get_db().close()
        return ret_val

