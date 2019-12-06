import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Remote(
    command_executor='http://hub:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME)

driver.implicitly_wait(5)

MLB = ['MIL']

year_list = ['1995', '1996', '1997', '1998', '1999',
            '2000', '2001', '2002', '2003', '2004',
			'2005', '2006', '2007', '2008', '2009',
    		'2010', '2011', '2012', '2013', '2014',
            '2015', '2016', '2017', '2018', '2019']

for team in MLB:
    club = []
    print(team)
    count = 0
    for year in year_list:
        url = f'https://www.baseball-reference.com/teams/{team}/{year}-schedule-scores.shtml'
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        season= []
        count += 1
        for row in soup.find('div', {'id':'all_team_schedule'}).find('tbody').find_all('tr'):
            boxscore = []
            game = {}
            try:
                game['game#'] = row.find('th', {'data-stat':'team_game'}).text
                boxscore.append(row.find('td', {'data-stat':'boxscore'}).find('a')['href'])
                game['day'] = (row.find('td', {'data-stat':'date_game'}).text).split()[0].strip(',')
                game['date'] = row.find('td').attrs['csk']
                game['team'] = row.find('td', {'data-stat':'team_ID'}).text
                game['home_away'] = row.find('td', {'data-stat':'homeORvis'}).text
                game['opp'] = row.find('td', {'data-stat':'opp_ID'}).text
                game['win_loss'] = row.find('td', {'data-stat':'win_loss_result'}).text
                game['r'] = row.find('td', {'data-stat':'R'}).text
                game['ra'] = row.find('td', {'data-stat':'RA'}).text
                game['innings'] = row.find('td', {'data-stat':'extra_innings'}).text
                game['record'] = row.find('td', {'data-stat':'win_loss_record'}).text
                game['divison_rank'] = row.find('td', {'data-stat':'rank'}).text
                game['games_back'] = row.find('td', {'data-stat':'games_back'}).text
                game['winning_pitcher'] = row.find('td', {'data-stat':'winning_pitcher'}).find('a').attrs['title'].replace('\xa0', ' ')
                game['losing_pitcher'] = row.find('td', {'data-stat':'losing_pitcher'}).find('a').attrs['title'].replace('\xa0', ' ')
                game['game_duration'] = row.find('td', {'data-stat':'time_of_game'}).text
                game['day_night'] = row.find('td', {'data-stat':'day_or_night'}).text
                game['attendance'] = row.find('td', {'data-stat':'attendance'}).text
                game['streak'] = row.find('td', {'data-stat':'win_loss_streak'}).text
                game['saving_pitcher'] = row.find('td', {'data-stat':'saving_pitcher'}).find('a').attrs['title'].replace('\xa0', ' ')
            except:
                pass
            sleep(3)

            for n in boxscore:
                boxscore_url = f'https://www.baseball-reference.com{boxscore[0]}'
                driver.get(boxscore_url)
                soup_2 = BeautifulSoup(driver.page_source,'lxml')

                for row2 in soup_2.find('div', {'id':'all_MilwaukeeBrewersbatting'}).find_all('tfoot'):
                    try:
                        game['bat_hits'] = row2.find('td', {'data-stat':'H'}).text
                        game['bat_rbi'] = row2.find('td', {'data-stat':'RBI'}).text
                        game['bat_walks'] = row2.find('td', {'data-stat':'BB'}).text
                        game['bat_strike_outs'] = row2.find('td', {'data-stat':'SO'}).text
                        game['hou_plate_app'] = row2.find('td', {'data-stat':'PA'}).text
                        game['bat_batting_avg'] = row2.find('td', {'data-stat':'batting_avg'}).text
                        game['bat_obp'] = row2.find('td', {'data-stat':'onbase_perc'}).text
                        game['bat_slg'] = row2.find('td', {'data-stat':'slugging_perc'}).text
                        game['bat_ops'] = row2.find('td', {'data-stat':'onbase_plus_slugging'}).text
                    except:
                        pass


                for row3 in soup_2.find('div', {'id':'all_MilwaukeeBrewerspitching'}).find_all('tfoot'):
                    try:
                        game['pitch_opp_hits'] = row3.find('td', {'data-stat':'H'}).text
                        game['pitch_walks'] = row3.find('td', {'data-stat':'BB'}).text
                        game['pitch_strike_outs'] = row3.find('td', {'data-stat':'SO'}).text
                        game['pitch_opp_hr'] = row3.find('td', {'data-stat':'HR'}).text
                        game['pitch_era'] = row3.find('td', {'data-stat':'earned_run_avg'}).text
                        game['pitch_batters_faced'] = row3.find('td', {'data-stat':'batters_faced'}).text
                        game['pitch_total_pitches'] = row3.find('td', {'data-stat':'pitches'}).text
                        game['pitch_combined_strikes'] = row3.find('td', {'data-stat':'strikes_total'}).text
                        game['pitch_strikes_contacted'] = row3.find('td', {'data-stat':'strikes_contact'}).text
                        game['pitch_strikes_swinging'] = row3.find('td', {'data-stat':'strikes_swinging'}).text
                        game['pitch_strikes_looking'] = row3.find('td', {'data-stat':'strikes_looking'}).text
                        game['pitch_wpa'] = row3.find('td', {'data-stat':'wpa_def'}).text
                    except:
                        pass
                sleep(3)
            if game['game#'] != 'Gm#':
                season.append(game)
            else:
                pass

        club.append(pd.DataFrame(season))
        sleep(3)
        if len(club) % 5 == 0:
            df = pd.concat(club, sort=False)
            df.to_csv(f'./data_scrape/{team}_{count}.csv', index=False)
        else:
            pass


#     df = pd.concat(club)
#     df.to_csv(f'../data/{team}_data.csv', index = False)
        print(f'{year} done!')


driver.close()
