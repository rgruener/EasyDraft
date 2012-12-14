CREATE DATABASE IF NOT EXISTS EasyDraft;

USE EasyDraft;


CREATE TABLE IF NOT EXISTS Users ( username CHAR(20),
                     email CHAR(50),
                     password CHAR(50) NOT NULL,
                     is_active BOOLEAN DEFAULT True,
                     PRIMARY KEY (username) );

CREATE TABLE IF NOT EXISTS Leagues (  league_id INTEGER AUTO_INCREMENT,
                        league_name CHAR(20) NOT NULL DEFAULT 'My League',
                        yahoo_league_id CHAR(30),
                        roster_size INTEGER NOT NULL,
                        drafted BOOLEAN DEFAULT False,
                        PRIMARY KEY (league_id) );

CREATE TABLE IF NOT EXISTS Teams ( team_id INTEGER AUTO_INCREMENT,
                     team_name CHAR(20),
                     PRIMARY KEY (team_id) );

CREATE TABLE IF NOT EXISTS Commissioners ( username CHAR(50),
                             league_id INTEGER,
                             PRIMARY KEY (username, league_id),
                             FOREIGN KEY (username) REFERENCES Users(username),
                             FOREIGN KEY (league_id) REFERENCES Leagues(league_id) );

CREATE TABLE IF NOT EXISTS Plays_with_in ( username CHAR(50),
                             league_id INTEGER,
                             team_id INTEGER,
                             PRIMARY KEY (username, league_id, team_id),
                             FOREIGN KEY (username) REFERENCES Users(username),
                             FOREIGN KEY (league_id) REFERENCES Leagues(league_id),
                             FOREIGN KEY (team_id) REFERENCES Teams(team_id) );

CREATE TABLE IF NOT EXISTS Players ( player_id INTEGER,
                       first_name CHAR(30) NOT NULL,
                       last_name CHAR(30) NOT NULL,
                       nfl_team CHAR(20) NOT NULL,
                       PRIMARY KEY (player_id) );

CREATE TABLE IF NOT EXISTS Roster_of ( team_id INTEGER,
                         player_id INTEGER,
                         PRIMARY KEY (team_id, player_id),
                         FOREIGN KEY (team_id) REFERENCES Teams(team_id),
                         FOREIGN KEY (player_id) REFERENCES Players(player_id) );

CREATE TABLE IF NOT EXISTS Positions ( position_name CHAR(20) NOT NULL,
                         PRIMARY KEY (position_name) );

CREATE TABLE IF NOT EXISTS Requires ( league_id INTEGER,
                       position_name CHAR(20),
                       maximum INTEGER,
                       starters INTEGER,
                       PRIMARY KEY (league_id, position_name),
                       FOREIGN KEY (league_id) REFERENCES Leagues(league_id),
                       FOREIGN KEY (position_name) REFERENCES Positions(position_name) );

CREATE TABLE IF NOT EXISTS Play ( player_id INTEGER,
                    position_name CHAR(20),
                    PRIMARY KEY (player_id, position_name),
                    FOREIGN KEY (player_id) REFERENCES Players(player_id),
                    FOREIGN KEY (position_name) REFERENCES Positions(position_name) );

CREATE TABLE IF NOT EXISTS Stats ( stat_id INTEGER,
                     player_id INTEGER,
                     stat_value REAL,
                     stat_name CHAR(20) NOT NULL,
                     season INTEGER,
                     PRIMARY KEY (stat_id, player_id, season),
                     FOREIGN KEY (player_id) REFERENCES Players(player_id) );
