from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
from IPython.display import display

##
# Parameters: GOL (game of legends) tournament match game statistic URL, Pro-Sports
# Returns: pandas dataframe (likely with 10 rows, since there are 10 players in each game
# Purpose: Scrapes GOL game statistic URL for specific statistics such as player name, role, level, etc.
# NOTE: as long as the URL is of the match game (i.e. game_1, game_2) statistics, it can be on any sub-page (summary, allstats)
##
def scrape_all_stats_and_summary(url, Match_name):
    driver = webdriver.Firefox()
    driver.get(url)
    driver.maximize_window()
    WebDriverWait(driver, 2)

    try:
        # required columns to satisfy our ERD
        desired_cols = ["Player", "Role", "Level", "Kills", "Deaths", "Assists", "CS", "Golds", 'GPM']
        additional_cols = ["Tournament_name", "Match_name", "Players_team", "Opponents_team", "Winning_Team"]

        #ensure we are looking at 'all stats' section
        allStats_button = driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div/div[2]/div/nav[2]/div/ul/li[2]/a')
        allStats_button.click()

        # find the main table. (the path is consistent across different GOL game statistics)
        tbody = driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div/div[3]/div/div/div/table/tbody')

        # create pandas dataframe (df)
        df = None

        ## Scrape Relevant Information (i.e. the 'desired_cols') from GOL Table
        # for each row in the table's body
        for tr in tbody.find_elements(By.XPATH, '//tr'):

            # find the column name, if it's a desired one, extract the row's data.
            GOL_row = tr.find_elements(By.XPATH, './/td')
            if len(GOL_row) > 0:
                if GOL_row[0].text.strip() in desired_cols:

                    ## Add GOL_rows as cols into df
                    # get name and values from GOL_row
                    data_col_name = GOL_row[0].text.strip()
                    data_col_vals = [GOL_row[i].text.strip() for i in range(1, len(GOL_row))]

                    # add column if df exists, create df otherwise
                    if df is not None:
                        new_column_df = pd.DataFrame({data_col_name: data_col_vals})
                        df = pd.concat([df, new_column_df], axis="columns")
                    else:
                        df = pd.DataFrame({data_col_name: data_col_vals})

        additional_cols = ["Tournament_name", "Match_name", "Player's_team", "Opponent's_team", "Winning_team"]
        num_rows = df.shape[0]

        ## Scrape data for Additional Columns
        #get tournament_name, add it to each row
        Tournament_name = driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div/div[1]/div[1]/a').text
        new_column_df = pd.DataFrame({"Tournament_name": [Tournament_name for i in range(num_rows)]})
        df = pd.concat([df, new_column_df], axis="columns")

        # Match_name
        new_column_df = pd.DataFrame({"Match_name": [Match_name for i in range(num_rows)]})
        df = pd.concat([df, new_column_df], axis="columns")

        Team_1 = driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div/h1').text.split("vs")[0].strip()
        Team_2 = driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div/h1').text.split("vs")[1].strip()

        # Players_team
        # first half of players are in Team_1, second half in Team_2
        new_column_df = pd.DataFrame({"Players_team": [Team_1 for i in range(num_rows//2)] + [Team_2 for i in range(num_rows//2)]})
        df = pd.concat([df, new_column_df], axis="columns")

        # Opponents_team
        # first half of players play against Team_2, second half against Team_1
        new_column_df = pd.DataFrame({"Opponents_team": [Team_2 for i in range(num_rows // 2)] + [Team_1 for i in range(num_rows//2)]})
        df = pd.concat([df, new_column_df], axis="columns")

        # Winning Team
        # go to summary page, look if first team won or lost
        summary_button = driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div/div[2]/div/nav[2]/div/ul/li[1]/a')
        summary_button.click()

        winLoss = driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div/div[3]/div/div/div/div[1]/div/div/div[2]/div[1]/div[1]/div').text.split("-")[1].strip().lower()
        if winLoss == "win":
            Winning_team = Team_1
        else:
            Winning_team = Team_2

        new_column_df = pd.DataFrame({"Winning_team": [Winning_team for i in range(num_rows)]})
        df = pd.concat([df, new_column_df], axis="columns")

        return df
    except OSError:
        return None
    finally:
        driver.quit()


##
# Parameters: GOL (game of legends) tournament game statistic URL
# Returns: pandas dataframe
# Purpose: A GOL tournament consists of multiple matches. This tool scrapes and compiles all matches from that one tournanment
##
def scrape_tournament(url):
    driver = webdriver.Firefox()
    driver.get(url)
    driver.maximize_window()

    try:
        # look at "preview, game_1, ..., summary" bar
        GameMenuToggler = driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div/div[2]/div/nav[1]/div/ul')

        ## Get all paths to Game buttons
        df = None

        for ls in GameMenuToggler.find_elements(By.XPATH, './/li'):

            # get the individual button, click if its a Game button
            button = ls.find_element(By.XPATH, './/a')
            if button.text.lower() not in ['preview', 'summary']:

                game_url = button.get_attribute("href")

                if df is not None:
                    new_df = scrape_all_stats_and_summary(game_url, button.text.lower().replace(" ", "_"))
                    WebDriverWait(driver, 2)

                    df = pd.concat([df, new_df])
                else:
                    df = scrape_all_stats_and_summary(game_url, button.text.lower().replace(" ", "_"))
                    WebDriverWait(driver, 2)

        df.to_csv('EMEA Masters Summer 2023 data.csv', index=False)

    finally:
        driver.quit()

# set up driver and URL to scrape
url = "https://gol.gg/game/stats/53315/page-fullstats/" #"https://gol.gg/game/stats/53293/page-fullstats/"
scrape_tournament(url)

