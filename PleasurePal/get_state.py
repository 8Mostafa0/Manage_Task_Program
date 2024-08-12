import sqlite3
import json

def save_state_to_json(state, json_file):
    try:
        with open(json_file, 'w') as f:
            json.dump(state, f, indent=4)

    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")

def generate_state_json(json_file):
    state = {
        'count':0
    }
    save_state_to_json(state,json_file)
    
