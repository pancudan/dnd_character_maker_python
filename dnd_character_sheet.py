import pandas as pd
import random


df = pd.read_excel("dungeonsdragons.xlsx")

print("Column names in the Excel file:")
print(df.columns)


classes = df["Class"].tolist()
races = df["Race"].tolist()
backgrounds = df["Background"].tolist()
alignments = df["Alignment"].tolist()


def choose_option(options, message):
    print("\n".join([f"{i+1}. {option}" for i, option in enumerate(options)]))
    choice = input(message)
    while not choice.isdigit() or int(choice) not in range(1, len(options) + 1):
        print("Invalid choice. Please enter a valid number.")
        choice = input(message)
    return options[int(choice) - 1]

def generate_ability_scores():
    return {
        "Strength": random.randint(8, 18),
        "Dexterity": random.randint(8, 18),
        "Constitution": random.randint(8, 18),
        "Intelligence": random.randint(8, 18),
        "Wisdom": random.randint(8, 18),
        "Charisma": random.randint(8, 18)
    }

def calculate_hp(character_class, constitution_modifier):
    hit_dice = {
        "Artificer": 8,
        "Barbarian": 12,
        "Bard": 8,
        "Cleric": 8,
        "Druid": 8,
        "Fighter": 10,
        "Monk": 8,
        "Paladin": 10,
        "Ranger": 10,
        "Rogue": 8,
        "Sorcerer": 6,
        "Warlock": 8,
        "Wizard": 6,
        "Blood Hunter": 10
    }
    return hit_dice[character_class] + constitution_modifier

def calculate_armor_class(dexterity_modifier, armor_type=None):
    if armor_type is None:
        return 10 + dexterity_modifier
    else:
        pass

def generate_character():
    character = {}
    character["Class"] = choose_option(classes, "Choose a class (enter the corresponding number): ")
    character["Race"] = choose_option(races, "Choose a race (enter the corresponding number): ")
    character["Background"] = choose_option(backgrounds, "Choose a background (enter the corresponding number): ")
    character["Alignment"] = choose_option(alignments, "Choose an alignment (enter the corresponding number): ")
    character["Name"] = input("Enter your character's name: ")
    character.update(generate_ability_scores())
    character["HP"] = calculate_hp(character["Class"], (character["Constitution"] - 10) // 2)
    character["AC"] = calculate_armor_class((character["Dexterity"] - 10) // 2) 
    return character

def display_character_sheet(character):
    print("\nCharacter Sheet:")
    for key, value in character.items():
        print(f"{key}: {value}")

def save_character_sheet(character):
    with open("character_sheet.txt", "w") as file:
        file.write("Character Sheet:\n")
        for key, value in character.items():
            file.write(f"{key}: {value}\n")

while True:
    print("Welcome to Dungeons and Dragons Character Creation!")
    new_character = generate_character()
    display_character_sheet(new_character)
    save_character_sheet(new_character)
    print("Character sheet saved as 'character_sheet.txt'")
    create_new_character = input("Do you want to create a new character? (yes/no): ").lower()
    if create_new_character != "yes":
        break