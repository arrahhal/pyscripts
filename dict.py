#!/usr/bin/env python
import requests
import argparse
import subprocess

def read_primary_clipboard():
    try:
        result = subprocess.run(['wl-paste', '-p'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print("Failed to read from primary clipboard.")
            return ""
    except FileNotFoundError:
        print("wl-paste is not installed.")
        return ""

def dmenu(prompt, items):
    try:
        result = subprocess.run(["bemenu",'-p', f"{prompt}:"], input=items, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return None
    except FileNotFoundError:
        print("bemenu is not installed.")
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("word", nargs='?')
    args = parser.parse_args()

    api = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    req_url = api
    if (args.word):
         req_url += args.word
    else:
         req_url += read_primary_clipboard()
    response = requests.get(req_url)

    if response.status_code != 200:
        print("Failed to fetch definition. Status code:", response.status_code)
        return 1

    data = response.json()
    if data:
        first_entry = data[0]
        word = first_entry.get("word", "")
        phonetic = first_entry.get("phonetic", "")
        prompt = f"{word}-{phonetic}"
        print(prompt)

        defs = ""
        meanings = first_entry.get("meanings", "")

        for meaning in meanings:
            for index, definition in enumerate(meaning.get("definitions", "")):
                if index < 3:
                    defs += definition.get('definition', '') + '\n'
                else:
                    break;

        print(dmenu(prompt, defs))
    else:
        print("No definition found for the word:", args.word)
        return 1

    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)

