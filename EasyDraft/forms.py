from flask.ext.wtf import (Form, BooleanField, TextField, PasswordField, IntegerField, 
                            SelectField, validators)
from EasyDraft import database

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=6, max=35)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.Length(min=6, max=35), validators.Required(), 
                                            validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

class ChangePassForm(Form):
    old_password = PasswordField('Password', [validators.Required()])
    password = PasswordField('Password', [validators.Length(min=6, max=35), validators.Required(), 
                                            validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.Required()])

def use_yahoo(form, field):
    if form.pull_from_yahoo.data:
        if len(field.data) < 2:
            raise validators.ValidationError('Please Enter League ID #')

class NewLeagueForm(Form):
    league_name = TextField('League Name', [validators.Length(min=3, max=20)])
    pull_from_yahoo = BooleanField('Pull Yahoo League Info:')
    yahoo_league_id = TextField('Yahoo League ID', [use_yahoo])
    
def get_choices(min_num, max_num):
    if max_num < min_num:
        return None
    i = min_num
    l=list()
    while (i <= max_num):
        l.append((str(i),str(i)))
        i = i+1
    return l

def validate_team(form, field):
    if (int(form.num_teams.data) >= int(field.label.text.split()[-1]) and not field.data):
        raise validators.ValidationError('Please Enter a Team Name')

def validate_user(form, field):
    if (field.data and not database.get_user(field.data)):
        raise validators.ValidationError('No such Username Exists')

class LeagueRequirementsForm(Form):
    roster_size = SelectField('Total Roster Size', choices=get_choices(1,25))
    num_teams = SelectField('Number of Teams', choices=get_choices(2, 16))
    num_qb = SelectField(choices=get_choices(0,3))
    start_qb = SelectField('QB', choices=get_choices(0,2))
    num_rb = SelectField(choices=get_choices(0,5))
    start_rb = SelectField('RB', choices=get_choices(0,3))
    num_wr = SelectField(choices=get_choices(0,7))
    start_wr = SelectField('WR', choices=get_choices(0,4))
    num_te = SelectField(choices=get_choices(0,4))
    start_te = SelectField('TE', choices=get_choices(0,2))
    num_k = SelectField(choices=get_choices(0,3))
    start_k = SelectField('TE', choices=get_choices(0,2))
    num_def = SelectField(choices=get_choices(0,3))
    start_def = SelectField('DEF', choices=get_choices(0,2))
    team_1 = TextField('Team 1', [validate_team])
    team_2 = TextField('Team 2', [validate_team])
    team_3 = TextField('Team 3', [validate_team])
    team_4 = TextField('Team 4', [validate_team])
    team_5 = TextField('Team 5', [validate_team])
    team_6 = TextField('Team 6', [validate_team])
    team_7 = TextField('Team 7', [validate_team])
    team_8 = TextField('Team 8', [validate_team])
    team_9 = TextField('Team 9', [validate_team])
    team_10 = TextField('Team 10', [validate_team])
    team_11 = TextField('Team 11', [validate_team])
    team_12 = TextField('Team 12', [validate_team])
    team_13 = TextField('Team 13', [validate_team])
    team_14 = TextField('Team 14', [validate_team])
    team_15 = TextField('Team 15', [validate_team])
    team_16 = TextField('Team 16', [validate_team])
    team_1_user = TextField(validators=[validate_user])
    team_2_user = TextField(validators=[validate_user])
    team_3_user = TextField(validators=[validate_user])
    team_4_user = TextField(validators=[validate_user])
    team_5_user = TextField(validators=[validate_user])
    team_6_user = TextField(validators=[validate_user])
    team_7_user = TextField(validators=[validate_user])
    team_8_user = TextField(validators=[validate_user])
    team_9_user = TextField(validators=[validate_user])
    team_10_user = TextField(validators=[validate_user])
    team_11_user = TextField(validators=[validate_user])
    team_12_user = TextField(validators=[validate_user])
    team_13_user = TextField(validators=[validate_user])
    team_14_user = TextField(validators=[validate_user])
    team_15_user = TextField(validators=[validate_user])
    team_16_user = TextField(validators=[validate_user])
