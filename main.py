import time
import pandas
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options

seasons = [
    {"season": "1992-1993", "url": "https://www.premierleague.com/results?co=1&se=1&cl=-1", "active": True},
    {"season": "1993-1994", "url": "https://www.premierleague.com/results?co=1&se=2&cl=-1", "active": True},
    {"season": "1994-1995", "url": "https://www.premierleague.com/results?co=1&se=3&cl=-1", "active": True},
    {"season": "1995-1996", "url": "https://www.premierleague.com/results?co=1&se=4&cl=-1", "active": True},
    {"season": "1996-1997", "url": "https://www.premierleague.com/results?co=1&se=5&cl=-1", "active": True},
    {"season": "1997-1998", "url": "https://www.premierleague.com/results?co=1&se=6&cl=-1", "active": True},
    {"season": "1998-1999", "url": "https://www.premierleague.com/results?co=1&se=7&cl=-1", "active": True},
    {"season": "1999-2000", "url": "https://www.premierleague.com/results?co=1&se=8&cl=-1", "active": True},
    {"season": "2000-2001", "url": "https://www.premierleague.com/results?co=1&se=9&cl=-1", "active": True},
    {"season": "2001-2002", "url": "https://www.premierleague.com/results?co=1&se=10&cl=-1", "active": True},
    {"season": "2002-2003", "url": "https://www.premierleague.com/results?co=1&se=11&cl=-1", "active": True},
    {"season": "2003-2004", "url": "https://www.premierleague.com/results?co=1&se=12&cl=-1", "active": True},
    {"season": "2004-2005", "url": "https://www.premierleague.com/results?co=1&se=13&cl=-1", "active": True},
    {"season": "2005-2006", "url": "https://www.premierleague.com/results?co=1&se=14&cl=-1", "active": True},
    {"season": "2006-2007", "url": "https://www.premierleague.com/results?co=1&se=15&cl=-1", "active": True},
    {"season": "2007-2008", "url": "https://www.premierleague.com/results?co=1&se=16&cl=-1", "active": True},
    {"season": "2008-2009", "url": "https://www.premierleague.com/results?co=1&se=17&cl=-1", "active": True},
    {"season": "2009-2010", "url": "https://www.premierleague.com/results?co=1&se=18&cl=-1", "active": True},
    {"season": "2010-2011", "url": "https://www.premierleague.com/results?co=1&se=19&cl=-1", "active": True},
    {"season": "2011-2012", "url": "https://www.premierleague.com/results?co=1&se=20&cl=-1", "active": True},
    {"season": "2012-2013", "url": "https://www.premierleague.com/results?co=1&se=21&cl=-1", "active": True},
    {"season": "2013-2014", "url": "https://www.premierleague.com/results?co=1&se=22&cl=-1", "active": True},
    {"season": "2014-2015", "url": "https://www.premierleague.com/results?co=1&se=27&cl=-1", "active": True},
    {"season": "2015-2016", "url": "https://www.premierleague.com/results?co=1&se=42&cl=-1", "active": True},
    {"season": "2016-2017", "url": "https://www.premierleague.com/results?co=1&se=54&cl=-1", "active": True},
    {"season": "2017-2018", "url": "https://www.premierleague.com/results?co=1&se=79&cl=-1", "active": True},
    {"season": "2018-2019", "url": "https://www.premierleague.com/results?co=1&se=210&cl=-1", "active": True},
    {"season": "2019-2020", "url": "https://www.premierleague.com/results?co=1&se=274&cl=-1", "active": True},
    {"season": "2020-2021", "url": "https://www.premierleague.com/results?co=1&se=363&cl=-1", "active": True},
    {"season": "2021-2022", "url": "https://www.premierleague.com/results?co=1&se=418&cl=-1", "active": True},
    {"season": "2022-2023", "url": "https://www.premierleague.com/results?co=1&se=489&cl=-1", "active": True},
    {"season": "2023-2024", "url": "https://www.premierleague.com/results?co=1&se=578&cl=-1", "active": True},
    {"season": "2024-2025", "url": "https://www.premierleague.com/results?co=1&se=719&cl=-1", "active": True}]

date_stamp = datetime.now().strftime("%Y%m%d")

options = Options()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)

premier_league_results = []

for season in seasons:
     if season["active"]:
        print(f"Waiting for {season['season']} page to load.")
        browser.get(season["url"])
        time.sleep(12)
        max_scroll_height = browser.execute_script("return document.body.scrollHeight")
        browser.execute_script(f"window.scrollTo(0, {max_scroll_height})")
        WebDriverWait(browser, 30).until(expected_conditions.invisibility_of_element_located((By.XPATH, "//*[@data-scroll-loader]")))
        print("Page loaded, scraping data.")
        fixtures_matches_list = browser.find_elements(by=By.CLASS_NAME, value="fixtures__matches-list")
        for matches in fixtures_matches_list:
            match_date = matches.get_attribute("data-competition-matches-list")
            match_list = matches.find_elements(by=By.CLASS_NAME, value="matchList")
            for match_list_item in match_list:
                match_fixtures = match_list_item.find_elements(by=By.CLASS_NAME, value="match-fixture")
                for match in match_fixtures:
                    home_team = match.get_attribute("data-home")
                    away_team = match.get_attribute("data-away")
                    competition = match.get_attribute("data-competition")
                    venue = match.get_attribute("data-venue")
                    score = match.find_element(by=By.CLASS_NAME, value="match-fixture__score").text.split("\n")
                    home_score = score[0]
                    away_score = score[2]
                    premier_league_results.append({
                        "season": season["season"],
                        "match_date": match_date, 
                        "home_team": home_team, 
                        "away_team": away_team, 
                        "competition": competition, 
                        "venue": venue, 
                        "home_score": home_score, 
                        "away_score": away_score})           
        print(f"Finished scraping season: {season['season']}.")


premier_league_results_file_name = f"files/premier_league_results_{date_time_stamp}.csv"
pandas.DataFrame(premier_league_results).to_csv(f"{premier_league_results_file_name}", index=False)
browser.quit()
print("Premier League results scraped and saved to file.")

def calculate_points(ndarray):
    points = 0
    for value in ndarray:
        if value[0] > value[1]: points += 3
        elif value[0] == value[1]: points += 1
        else: points += 0
    return points

def calculate_results(ndarray):
    results = {"wins": 0, "draws": 0, "losses": 0}
    for value in ndarray:
        if value[0] > value[1]: results["wins"] += 1
        elif value[0] == value[1]: results["draws"] += 1
        else: results["losses"] += 1
    return results

def calculate_season_form(ndarray, team):
    form = []
    for index, value in enumerate(ndarray):
        if (value[0] == team and value[2] > value[3]) or (value[1] == team and value[3] > value[2]): form.append("W")
        elif value[0] == team and value[2] < value[3] or value[1] == team and value[3] < value[2]: form.append("L")
        else: form.append("D")
    return ",".join(form)

def calculate_home_away_form(ndarray):
    form = []
    for index, value in enumerate(ndarray):
        if value[0] > value[1]: form.append("W")
        elif value[0] < value[1]: form.append("L")
        else: form.append("D")
    return ",".join(form)

def calculate_position(datas):
    for data in datas:
        position = 1
        team = data["team"]
        points = data["points"]
        gd = data["goal_difference"]
        goals_for = data["goals_for"]
        for sub_item in datas:
            if sub_item["team"] != team and sub_item["points"] > points: position += 1
            elif sub_item["team"] != team and sub_item["points"] == points:
                if sub_item["goal_difference"] > gd: position += 1
                elif sub_item["goal_difference"] == gd:
                    if sub_item["goals_for"] > goals_for: position += 1
        data["position"] = position

season_groups = pandas.read_csv(f"files/premier_league_results_{date_stamp}.csv").groupby("season")

premier_league_season_insights = []

for season_name, season_data in season_groups:

    premier_league_season_datas = []

    print(f"Starting table calculations for season: {season_name}.")

    teams = pandas.unique(season_data["home_team"].sort_values(ascending=True))

    for team in teams:

        all_games = season_data[(season_data["home_team"] == team) | (season_data["away_team"] == team)]
        home_games = all_games[all_games["home_team"] == team]
        away_games = all_games[all_games["away_team"] == team]
        home_points = calculate_points(home_games[["home_score", "away_score"]].values)
        away_points = calculate_points(away_games[["away_score", "home_score"]].values)
        home_results = calculate_results(home_games[["home_score", "away_score"]].values)
        away_results = calculate_results(away_games[["away_score", "home_score"]].values)
        home_goals_for = int(home_games["home_score"].sum())
        home_goals_against = int(home_games["away_score"].sum())
        away_goals_for = int(away_games["away_score"].sum())
        away_goals_against = int(away_games["home_score"].sum())
        season_form = calculate_season_form(all_games[["home_team", "away_team", "home_score", "away_score"]].values, team)
        home_form = calculate_home_away_form(home_games[["home_score", "away_score"]].values)
        away_form = calculate_home_away_form(away_games[["away_score", "home_score"]].values)

        premier_league_season_datas.append({
            "season": season_name,
            "position": 0,
            "team": team,
            "played": len(home_games) + len(away_games),
            "won": home_results["wins"] + away_results["wins"],
            "draw": home_results["draws"] + away_results["draws"],
            "lost": home_results["losses"] + away_results["losses"],
            "goals_for": home_goals_for + away_goals_for,
            "goals_against": home_goals_against + away_goals_against,
            "goal_difference": (home_goals_for + away_goals_for) - (home_goals_against + away_goals_against),
            "points": home_points + away_points,
            "home_games_played": len(home_games),
            "away_games_played": len(away_games),
            "home_goals_for": home_goals_for,
            "home_goals_against": home_goals_against,
            "away_goals_for": away_goals_for,
            "away_goals_against": away_goals_against,
            "home_wins": home_results["wins"],
            "home_draws": home_results["draws"],
            "home_losses": home_results["losses"],
            "away_wins": away_results["wins"],
            "away_draws": away_results["draws"],
            "away_losses": away_results["losses"],
            "season_form": season_form,
            "home_form": home_form,
            "away_form": away_form
        })

    calculate_position(premier_league_season_datas)
    premier_league_season_insights.extend(premier_league_season_datas)

print(f"Finished table calculations for season: {season_name}")

pandas.DataFrame(premier_league_season_insights).sort_values(["season", "position"], ascending=[True, True]).to_csv(f"files/premier_league_season_insights_{date_stamp}.csv", index=False)
print("Premier League tables calculated and saved to file.")