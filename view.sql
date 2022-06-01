
CREATE VIEW public.country_leagues as
SELECT
    match.id,
    country.name as country_name,
    league.name as league_name,
    match.season,
    match.date,
    ht.team_long_name as home_team,
    at.team_long_name AS away_team,
    match.home_team_goal,
    match.away_team_goal
FROM
    match
    JOIN country ON country.id = match.country_id
    JOIN league ON league.id = match.league_id
    LEFT JOIN team ht ON ht.team_api_id = match.home_team_api_id
    LEFT JOIN team at ON at.team_api_id = match.away_team_api_id
ORDER BY
    match.date;