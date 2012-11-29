CREATE DATABASE IF NOT EXISTS EasyDraft;

USE EasyDraft;


CREATE TABLE IF NOT EXISTS Users ( email CHAR(50),
                     password CHAR(30) NOT NULL,
                     PRIMARY KEY (email) );

CREATE TABLE IF NOT EXISTS Leagues (  league_id INTEGER,
                        league_name CHAR(20) NOT NULL DEFAULT 'My League',
                        yahoo_league_key CHAR(30),
                        yahoo_league_id CHAR(30),
                        roster_size INTEGER NOT NULL,
                        PRIMARY KEY (league_id) );

CREATE TABLE IF NOT EXISTS Teams ( team_id INTEGER,
                     team_name CHAR(20),
                     PRIMARY KEY (team_id) );

CREATE TABLE IF NOT EXISTS Commissioners ( user_email CHAR(50),
                             league_id INTEGER,
                             PRIMARY KEY (user_email, league_id),
                             FOREIGN KEY (user_email) REFERENCES Users(email),
                             FOREIGN KEY (league_id) REFERENCES Leagues(league_id) );

CREATE TABLE IF NOT EXISTS Plays_with_in ( user_email CHAR(50),
                             league_id INTEGER,
                             team_id INTEGER,
                             PRIMARY KEY (user_email, league_id, team_id),
                             FOREIGN KEY (user_email) REFERENCES Users(email),
                             FOREIGN KEY (league_id) REFERENCES Leagues(league_id),
                             FOREIGN KEY (team_id) REFERENCES Teams(team_id) );

CREATE TABLE IF NOT EXISTS Players ( player_id INTEGER,
                       full_name CHAR(30) NOT NULL,
                       nfl_team CHAR(20) NOT NULL,
                       PRIMARY KEY (player_id) );

CREATE TABLE IF NOT EXISTS Roster_of ( team_id INTEGER,
                         player_id INTEGER,
                         PRIMARY KEY (team_id, player_id),
                         FOREIGN KEY (team_id) REFERENCES Teams(team_id),
                         FOREIGN KEY (player_id) REFERENCES Players(player_id) );

CREATE TABLE IF NOT EXISTS Positions ( position_id INTEGER,
                         position_name CHAR(20) NOT NULL,
                         PRIMARY KEY (position_id) );

CREATE TABLE IF NOT EXISTS Requires ( league_id INTEGER,
                       position_id INTEGER,
                       minimum INTEGER,
                       maximum INTEGER,
                       starters INTEGER,
                       PRIMARY KEY (league_id, position_id),
                       FOREIGN KEY (league_id) REFERENCES Leagues(league_id),
                       FOREIGN KEY (position_id) REFERENCES Positions(position_id) );

CREATE TABLE IF NOT EXISTS Play ( player_id INTEGER,
                    position_id INTEGER,
                    PRIMARY KEY (player_id, position_id),
                    FOREIGN KEY (player_id) REFERENCES Players(player_id),
                    FOREIGN KEY (position_id) REFERENCES Positions(position_id) );

CREATE TABLE IF NOT EXISTS Stats ( stat_id INTEGER,
                     yahoo_stat_id INTEGER,
                     stat_value REAL,
                     stat_name CHAR(20) NOT NULL,
                     season INTEGER NOT NULL,
                     PRIMARY KEY (stat_id) );

CREATE TABLE IF NOT EXISTS Have ( player_id INTEGER,
                    stat_id INTEGER,
                    PRIMARY KEY (player_id, stat_id),
                    FOREIGN KEY (player_id) REFERENCES Players(player_id),
                    FOREIGN KEY (stat_id) REFERENCES Stats(stat_id) );
