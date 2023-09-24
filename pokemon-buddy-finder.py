# IMPORT NECESSARY MODULES

# The 'random' module provides functions for generating random numbers and performing random selection.
# I used this code to randomly select Pokémon from the retrieved data.
import random

# This module allows to make HTTP requests to APIs
# I used this code to send HTTP GET requests to the PokéAPI web service to retrieve Pokémon data based on the user's preferences
# To install this module: write 'pip install requests' in Terminal
import requests

# This module provides a way to interact with the operating system on which Python is running.
# I used this code to check for the existence of a CSV file and create one if it doesn't exist.
import os

# The 'csv' module provides functionality for working with CSV (Comma Separated Values) files.
# I used this to log user data, including timestamps, names, Pokémon types, IDs, names and colors to keep track of user's Pokémon buddy choices.
import csv

# Used time module to import the 'sleep(secs)' function, which suspends execution of the thread being called for the
# given number of seconds
import time

# This module provides classes for working with dates and times.
# I used this to generate a timestamps when logging user data to the CSV file.
from datetime import datetime


# Define a function to display a welcome header using an ASCII art from 'https://www.asciiart.eu/text-to-ascii-art'
def header():
    print("#####################################################################" + '\n')
    print("\t Welcome to the")
    print("                                  ,'\ ")
    print("    _.----.        ____         ,'  _\   ___    ___     ____")
    print("_,-'       `.     |    |  /`.   \,-'    |   \  /   |   |    \  |`. ")
    print("\      __    \    '-.  | /   `.  ___    |    \/    |   '-.   \ |  | ")
    print(" \.    \ \   |  __  |  |/    ,','_  `.  |          | __  |    \|  | ")
    print("   \    \/   /,' _`.|      ,' / / / /   |          ,' _`.|     |  | ")
    print("    \     ,-'/  /   \    ,'   | \/ / ,`.|         /  /   \  |     | ")
    print("     \    \ |   \_/  |   `-.  \    `'  /|  |    ||   \_/  | |\    | ")
    print("      \    \ \      /       `-.`.___,-' |  |\  /| \      /  | |   | ")
    print("       \    \ `.__,'|  |`-._    `|      |__| \/ |  `.__,'|  | |   | ")
    print("        \_.-'       |__|    `-._ |              '-.|     '-.| |   | ")
    print("                                `'                            '-._| ")
    print("\n\t                    ♥♥︎ BUDDY FINDER ♥︎♥" + '\n')
    print("#####################################################################" + '\n')

    # Wait for 2 seconds
    time.sleep(2)


# Calls the header() function to display the welcome header
header()

# Created a variable 'name' to get the user's name and follows with a greeting
name = input("What is your name? ").capitalize()
print(f"Hi there, {name}! Let's help you find your Pokémon buddy!" + '\n')


# A function to retrieve Pokémon by type from the PokéAPI
def get_pokemon_by_type(pokemon_type, limit=3):
    # Use the PokeAPI to get a list of Pokémon of the specified type
    # Make a GET request to the PokeAPI endpoint
    url = f"https://pokeapi.co/api/v2/type/{pokemon_type.lower()}/"
    response = requests.get(url)

    # If the response is successful (status code 200), parse JSON data and return a list of Pokémon
    if response.status_code == 200:
        data = response.json()

        # Extract the list of Pokémon names
        pokemon_entries = data.get('pokemon', [])[:limit]

        # Create a list comprehension to extract Pokémon names
        pokemon_list = [entry['pokemon']['name'] for entry in pokemon_entries]

        return pokemon_list

    else:
        # If GET request is not successful, main() function will be called
        print("Failed to retrieve Pokemon data.")
        return main()


def get_pokemon_by_color(pokemon_color, limit=3):
    url = f"https://pokeapi.co/api/v2/pokemon-color/{pokemon_color.lower()}/"
    response = requests.get(url)

    if response.status_code == 200:
        color_data = response.json()

        pokemon_entries = color_data.get('pokemon_species', [])

        pokemon_color_list = []
        count = 0  # Initialize a count variable to keep track of the number of Pokémon added

        for entry in pokemon_entries:
            if count >= limit:
                break  # Exit the loop if the limit has been reached

            pokemon_name = entry.get('name', '')
            if pokemon_name:
                pokemon_color_list.append(pokemon_name)
                count += 1  # Increment the count

        return pokemon_color_list

    else:
        print('Failed to retrieve Pokémon data by color.')
        return []


# Function to retrieve Pokémon info from the API
def retrieve_pokemon_info():
    pokemon_id = input('\n' + 'Enter the name of the Pokémon that you would like to buddy up: ')
    url = f'https://pokeapi.co/api/v2/pokemon-species/{pokemon_id.lower()}'
    response = requests.get(url)
    pokemon = response.json()

    if response.status_code == 200:
        # Initialize a variable to store the favorite text in English
        favorite_text_en = []

        # Loop through the flavor text entries to find the one in English
        for entry in pokemon['flavor_text_entries']:
            if entry['language']['name'] == 'en':
                favorite_text_en.append(entry['flavor_text'])
                break  # Exit the loop once you find the English entry

        info_str = " ".join(favorite_text_en)

        return {
            'name': pokemon['name'][:10],  # Used string slicing to limit the name to the first 10 characters
            'info': info_str,  # Use the found English flavor text
            'id': pokemon['id'],
            'color': pokemon['color']['name']
        }

    else:
        print("There is no information about this Pokémon.")
        return []


# Function to log user data to a CSV file
def log_to_csv(user_name, pokemon_name, pokemon_type, pokemon_id, pokemon_color):
    # Import the 'datetime' module to work with timestamps
    # Get the current timestamp in the format "dd-mm-yyyy HH:MM"
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")

    # Check whether a file named "poke-buddy_records.csv" exists in the current directory
    # 'os.path.isfile()' returns True if file already exists, and 'not' is used to negate it.
    # If the value returns True, then a new file will be created as the file does not currently exist
    is_new_file = not os.path.isfile("poke-buddy_records.csv")

    # Open the CSV file in "append" mode.
    # If the file is new, a header row with column names will be created
    with open("poke-buddy_records.csv", "a", newline="") as file:
        writer = csv.writer(file)

        if is_new_file:
            # Write the header row if it's a new file
            writer.writerow(
                ["Timestamp",
                 "User's Name",
                 "Pokémon Name",
                 "Pokémon Type",
                 "Pokémon ID",
                 "Pokémon Color"]
            )

        # Write a new row of data with timestamp, user's name, Pokémon type, ID, name and color.
        writer.writerow(
            [timestamp, user_name, pokemon_name, pokemon_type, pokemon_id, pokemon_color]
        )


# Function to display a numbered list
def display_numbered_list(items):
    for i, item in enumerate(items, 1):
        print(f"{i}. {item.capitalize()}")


# Main function to deploy the app
def main():
    # Use the user's preferences to find a matching Pokémon type (e.g., fire)
    pokemon_type = input("Which Pokémon type (e.g. water, grass, normal, etc.) do you prefer? ")
    favorite_color = input("Enter your favorite Pokémon color: ")

    # Get a list of Pokémon that match the user's type preference
    matching_pokemon_type = get_pokemon_by_type(pokemon_type, limit=3)
    matching_pokemon_color = get_pokemon_by_color(favorite_color, limit=3)

    # Combine the two lists into a single list
    matching_pokemon = matching_pokemon_type + matching_pokemon_color

    # Shuffle the combined list to randomize the order
    random.shuffle(matching_pokemon)

    # If type is found in the database, this will generate random Pokémon's name and their corresponding ID
    if matching_pokemon:
        print(f"Here are some random Pokémons for you to pick: " + '\n')
        display_numbered_list(matching_pokemon)

    else:
        return None

    # Retrieve information about the chosen Pokémon
    chosen_pokemon = retrieve_pokemon_info()

    # Display information about the chosen Pokémon
    print(f"You chose... '{chosen_pokemon['name'].capitalize()}'.")
    print(f"Here are some fun facts about {chosen_pokemon['name'].capitalize()}:")
    print(f"{str(chosen_pokemon['info'])}")

    # Log user data to a CSV file
    log_to_csv(name, chosen_pokemon['name'].upper(), pokemon_type.upper(), chosen_pokemon['id'], chosen_pokemon[
        'color'].upper())


# Check if the main function is being called
if main:
    main()
