import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import os

downloads_folder = os.path.expanduser("~/Downloads")
csv_filename = os.path.join(downloads_folder, 'players_data.csv')

base_url = "https://www.pro-football-reference.com/players/"

alphabet = "IJKLMNOPQ"

players_data = pd.DataFrame(columns=['Name', 'Birthday'])

for letter in alphabet:
    url = f"{base_url}{letter}/"
    csv_filename = f'players_data_{alphabet}.csv'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    body = soup.find("body")

    if body:
        wrap = body.find("div", id="wrap")
        if wrap:
            content = wrap.find("div", id="content")
            if content:
                section_wrapper = content.find("div", id="all_players")
                if section_wrapper:
                    section_content = section_wrapper.find("div", id="div_players")
                    if section_content:
                        player_links = section_content.find_all("a")

                        player_count = 0

                        for player_link in player_links:
                            player_name = player_link.get_text(strip=True)
                            player_url = player_link['href']

                            full_player_url = f"https://www.pro-football-reference.com{player_url}"

                            if response.status_code == 200:
                                response = requests.get(full_player_url)
                                playersoup = BeautifulSoup(response.content, "html.parser")

                                script_tag = playersoup.find("script", type="application/ld+json")

                                if script_tag:
                                    script_content = script_tag.string

                                    player_data = json.loads(script_content)

                                    player_name = player_data.get("name")
                                    player_birthday = player_data.get("birthDate")

                                    print(f"{player_name} {player_birthday}")
                                    # players_data = players_data.append({'Name': player_name, 'Birthday': player_birthday}, ignore_index = True)

                                    new_data = pd.DataFrame({'Name': [player_name], 'Birthday': [player_birthday]})
                                    players_data = pd.concat([players_data, new_data], ignore_index=True)

                                    time.sleep(3)
                                else:
                                    print(
                                        f"Failed to retrieve data from {player_url}. Status code: {response.status_code}")

players_data.to_csv(csv_filename, index=False)

print(f"CSV file {csv_filename} saved to this projects folder in PycharmProjects.")
