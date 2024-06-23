import pandas as pd
import random
import os

df = pd.read_excel("dungeonsdragons.xlsx")

print("Column names in the Excel file:")
print(df.columns)
classes = df["Class"].tolist()
races = df["Race"].tolist()
backgrounds = df["Background"].tolist()
alignments = df["Alignment"].tolist()
names = df["Name"].dropna().tolist()
class_priority = {
    "Artificer": "Intelligence",
    "Wizard": "Intelligence",
    "Warlock": "Charisma",
    "Bard": "Charisma",
    "Barbarian": "Strength",
    "Cleric": "Wisdom",
    "Druid": "Wisdom",
    "Paladin": "Wisdom",
    "Fighter": "Constitution",
    "Sorcerer": "Constitution",
    "Monk": "Dexterity",
    "Ranger": "Dexterity",
    "Blood Hunter": "Dexterity",
}
def choose_option(options, message):
    non_empty_options = [option for option in options if isinstance(option, str)]
    print("\n".join([f"{i+1}. {option}" for i, option in enumerate(non_empty_options)]))
    choice = input(message)
    while not choice.isdigit() or int(choice) not in range(1, len(non_empty_options) + 1):
        print("Invalid choice. Please enter a valid number.")
        choice = input(message)
    return non_empty_options[int(choice) - 1]
def generate_ability_scores():
    scores = []
    for _ in range(6):
        rolls = sorted([random.randint(1, 6) for _ in range(4)])
        scores.append(sum(rolls[1:]))
    return scores
def calculate_modifier(score):
    return (score - 10) // 2

def assign_scores_by_priority(scores, priority_stat):
    """Assigns scores to stats with priority given to the priority_stat."""
    stats = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
    scores.sort(reverse=True) 
    priority_index = stats.index(priority_stat)
    assigned_scores = {stat: 0 for stat in stats}

    assigned_scores[priority_stat] = scores.pop(0)
    for stat in stats:
        if stat != priority_stat:
            assigned_scores[stat] = scores.pop(0)

    return assigned_scores

def calculate_hp(character_class, constitution_modifier, level):
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
    base_hp = hit_dice[character_class] + constitution_modifier
    additional_hp = sum([random.randint(1, hit_dice[character_class]) + constitution_modifier for _ in range(1, level)])
    return base_hp + additional_hp

def calculate_armor_class(dexterity_modifier, armor_type=None):
    if armor_type is None:
        return 10 + dexterity_modifier
    else:
        armor_class = {
            "light": 11 + dexterity_modifier,
            "medium": 12 + min(dexterity_modifier, 2),
            "heavy": 16
        }
        return armor_class.get(armor_type.lower(), 10 + dexterity_modifier)

def generate_character():
    character = {}
    character["Class"] = choose_option(classes, "Choose a class (enter the corresponding number): ")
    character["Race"] = choose_option(races, "Choose a race (enter the corresponding number): ")
    character["Background"] = choose_option(backgrounds, "Choose a background (enter the corresponding number): ")
    character["Alignment"] = choose_option(alignments, "Choose an alignment (enter the corresponding number): ")   
    name_choice = input("Do you want to enter your character's name or have it generated? (enter/generated): ").lower()
    if name_choice == "enter":
        character["Name"] = input("Enter your character's name: ")
    else:
        character["Name"] = generate_name()
   
    character["Level"] = int(input("Enter your character's level: "))
    ability_scores = generate_ability_scores()
    priority_stat = class_priority[character["Class"]]
    assigned_scores = assign_scores_by_priority(ability_scores, priority_stat)
    for stat, score in assigned_scores.items():
        character[stat] = score
        character[f"{stat} Modifier"] = calculate_modifier(score)
    character["HP"] = calculate_hp(character["Class"], character["Constitution Modifier"], character["Level"])
    character["AC"] = calculate_armor_class(character["Dexterity Modifier"])

    return character
def generate_name():
    return random.choice(names)

def display_character_sheet(character):
    print("\nCharacter Sheet:")
    for key, value in character.items():
        print(f"{key}: {value}")
def get_next_filename(base_filename="character_sheet"):
    """Generates a new filename with an incremented number if the base filename exists."""
    i = 1
    filename = f"{base_filename}.txt"
    while os.path.exists(filename):
        i += 1
        filename = f"{base_filename} ({i}).txt"
    return filename
def save_character_sheet(character):
    filename = get_next_filename()
    with open(filename, "w") as file:
        file.write("Character Sheet:\n")
        for key, value in character.items():
            file.write(f"{key}: {value}\n")
    return filename

while True:
    print("Welcome to Dungeons and Dragons Character Creation!")
    new_character = generate_character()
    display_character_sheet(new_character)
    saved_filename = save_character_sheet(new_character)
    print(f"Character sheet saved as '{saved_filename}'")
    create_new_character = input("Do you want to create a new character? (yes/no): ").lower()
    if create_new_character not in ("yes", "y"):
        break
