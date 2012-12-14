from EasyDraft import database

def process_league_form(league_name, yahoo_league_id, form):
    league_id = database.insert_league(league_name, yahoo_league_id, form.roster_size.data)
    num_teams = int(form.num_teams.data)
    team_ids = list()
    if num_teams >= 2:
        team_ids.append(database.insert_team(form.team_1.data, league_id, form.team_1_user.data or 'anonymous'))
        team_ids.append(database.insert_team(form.team_2.data, league_id, form.team_2_user.data or 'anonymous'))
    if num_teams >= 3:
        team_ids.append(database.insert_team(form.team_3.data, league_id, form.team_3_user.data or 'anonymous'))
    if num_teams >= 4:
        team_ids.append(database.insert_team(form.team_4.data, league_id, form.team_4_user.data or 'anonymous'))
    if num_teams >= 5:
        team_ids.append(database.insert_team(form.team_5.data, league_id, form.team_5_user.data or 'anonymous'))
    if num_teams >= 6:
        team_ids.append(database.insert_team(form.team_6.data, league_id, form.team_6_user.data or 'anonymous'))
    if num_teams >= 7:
        team_ids.append(database.insert_team(form.team_7.data, league_id, form.team_7_user.data or 'anonymous'))
    if num_teams >= 8:
        team_ids.append(database.insert_team(form.team_8.data, league_id, form.team_8_user.data or 'anonymous'))
    if num_teams >= 9:
        team_ids.append(database.insert_team(form.team_9.data, league_id, form.team_9_user.data or 'anonymous'))
    if num_teams >= 10:
        team_ids.append(database.insert_team(form.team_10.data, league_id, form.team_10_user.data or 'anonymous'))
    if num_teams >= 11:
        team_ids.append(database.insert_team(form.team_11.data, league_id, form.team_11_user.data or 'anonymous'))
    if num_teams >= 12:
        team_ids.append(database.insert_team(form.team_12.data, league_id, form.team_12_user.data or 'anonymous'))
    if num_teams >= 13:
        team_ids.append(database.insert_team(form.team_13.data, league_id, form.team_13_user.data or 'anonymous'))
    if num_teams >= 14:
        team_ids.append(database.insert_team(form.team_14.data, league_id, form.team_14_user.data or 'anonymous'))
    if num_teams >= 15:
        team_ids.append(database.insert_team(form.team_15.data, league_id, form.team_15_user.data or 'anonymous'))
    if num_teams == 16:
        team_ids.append(database.insert_team(form.team_16.data, league_id, form.team_16_user.data or 'anonymous'))
    database.insert_requirement(league_id, 'QB', form.num_qb.data, form.start_qb.data)
    database.insert_requirement(league_id, 'RB', form.num_rb.data, form.start_rb.data)
    database.insert_requirement(league_id, 'WR', form.num_wr.data, form.start_wr.data)
    database.insert_requirement(league_id, 'TE', form.num_te.data, form.start_te.data)
    database.insert_requirement(league_id, 'K', form.num_k.data, form.start_k.data)
    database.insert_requirement(league_id, 'DEF', form.num_def.data, form.start_def.data)
    return league_id 
