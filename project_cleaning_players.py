# -*- coding: utf-8 -*-
"""Project_CLEANING_Players.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iecy5gv1oFMBgWBAc3JxxAFEMP3bOY1m
"""

import pandas as pd

from google.colab import files
uploaded=files.upload()

players_data = pd.read_csv('modified_players_data.csv')

players_data = pd.read_csv('players_age.csv')

# Input the player name you want to search for
search_name = 'Winston, Jameis'

# Search for Tom Brady and print True if found, else False
player_exists = search_name in players_data['Name'].values
print(player_exists)

# Convert the 'Birthday' column to datetime format with errors='coerce' to handle invalid dates
players_data['Birthday'] = pd.to_datetime(players_data['Birthday'], format='%m/%d/%Y', errors='coerce')

# Drop rows with NaT (Not a Time) values
players_data = players_data.dropna(subset=['Birthday'])

# Find the maximum date and corresponding player
max_date_player = players_data.loc[players_data['Birthday'].idxmax()]

# Print the maximum date and player name
print("Maximum Date:", max_date_player['Birthday'].strftime('%m/%d/%Y'))
print("Player Name:", max_date_player['Name'])

"""Dropping columns we won't need"""

# List of columns to drop
columns_to_drop = ['Birth Place', 'College', 'Current Status', 'Current Team', 'High School', 'High School Location', 'Number', 'Player Id']

# Drop the specified columns
players_data = players_data.drop(columns=columns_to_drop, errors='ignore')

# Display the modified DataFrame
print(players_data)

"""Finding null value count in all columns"""

for column in players_data.columns:
    null_count = players_data[column].isnull().sum()
    if null_count > 0:
        print(f"Column '{column}' has {null_count} null values.")

"""Dropping all columns with null birthdays"""

# Drop rows with null values in the 'Birthday' column
players_data = players_data.dropna(subset=['Birthday'])

# Print the modified DataFrame
print(players_data)

"""Change the format of the Name column to match our other database"""

# Rearrange 'Name' column to 'FirstName LastName'
players_data['Name'] = players_data['Name'].str.split(', ').str[1] + ' ' + players_data['Name'].str.split(', ').str[0]

# Print the modified DataFrame
print(players_data)

"""Switching the Birthday column from "MM/DD/YYYY" to "YYYY-MM-DD"
"""

# Convert 'Birthday' column to datetime with inferred format
players_data['Birthday'] = pd.to_datetime(players_data['Birthday'], infer_datetime_format=True, errors='coerce')

# Format 'Birthday' column as 'YYYY-MM-DD'
players_data['Birthday'] = players_data['Birthday'].dt.strftime('%Y-%m-%d')

# Print the modified DataFrame
print(players_data)

"""Double checking to see if there are any null values in Name or Birthday"""

# Check for null values in 'Name' and 'Birthday' columns
null_name = players_data['Name'].isnull().any()
null_birthday = players_data['Birthday'].isnull().any()

# Print the result
print(f"Null values in 'Name' column: {null_name}")
print(f"Null values in 'Birthday' column: {null_birthday}")

"""There are still 3 null values in Birthday, removing them now"""

# Drop rows with null values in the 'Birthday' column
players_data = players_data.dropna(subset=['Birthday'])

players_data.to_csv('modified_players_data.csv', index=False)

files.download('modified_players_data.csv')