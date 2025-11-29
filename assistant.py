import os
import json
import hashlib
import datetime
import requests
import webbrowser
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTES_FILE = os.path.join(BASE_DIR, "notes.txt")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

# ---------------------
# PASSWORD SYSTEM
# ---------------------

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def setup_password():
    print("No password found. Let's create one.")
    while True:
        pwd1 = input("Create a new password: ")
        pwd2 = input("Confirm password: ")

        if pwd1 == pwd2:
            hashed = hash_password(pwd1)
            save_config({"password": hashed})
            print("Password created successfully!\n")
            break
        else:
            print("Passwords do not match. Try again.\n")

def login():
    config = load_config()

    if "password" not in config:
        setup_password()
        config = load_config()

    stored_hash = config["password"]

    print("==== LOGIN REQUIRED ====")
    attempts = 3

    while attempts > 0:
        pwd = input("Enter password: ")
        if hash_password(pwd) == stored_hash:
            print("Login successful!\n")
            return True
        else:
            attempts -= 1
            print(f"Incorrect password. Attempts left: {attempts}")

    print("Too many failed attempts. Exiting.")
    exit()

# ---------------------
# MAIN ASSISTANT FEATURES
# ---------------------

def show_menu():
    print("\n===== PERSONAL ASSISTANT =====")
    print("1. Add Note")
    print("2. View Notes")
    print("3. Delete Notes")
    print("4. Weather Info")
    print("5. Random Joke")
    print("6. Open Google")
    print("7. Show Date & Time")
    print("8. Exit")

def add_note():
    try:
        note = input("Enter your note: ").strip()
        if not note:
            print("No text entered.")
            return
        with open(NOTES_FILE, "a", encoding="utf-8") as f:
            f.write(note + "\n")
        print("Note saved!")
    except Exception:
        print(traceback.format_exc())

def view_notes():
    if not os.path.exists(NOTES_FILE):
        print("No notes found.")
        return
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        print("\n===== Notes =====")
        print(f.read())

def delete_notes():
    if os.path.exists(NOTES_FILE):
        os.remove(NOTES_FILE)
        print("Notes deleted!")
    else:
        print("No notes file.")

def get_weather():
    city = input("Enter city: ").strip()
    try:
        url = f"https://wttr.in/{city}?format=3"
        resp = requests.get(url, timeout=5)
        print("Weather:", resp.text)
    except:
        print("Error getting weather.")

def get_joke():
    try:
        url = "https://official-joke-api.appspot.com/random_joke"
        resp = requests.get(url, timeout=5).json()
        print(resp["setup"])
        print(resp["punchline"])
    except:
        print("Joke API failed.")

def open_google():
    print("Opening Google...")
    webbrowser.open("https://google.com")

def show_datetime():
    now = datetime.datetime.now()
    print("Current Date & Time:", now.strftime("%Y-%m-%d %H:%M:%S"))

def main():
    login()  # <-- PASSWORD LOGIN REQUIRED BEFORE START

    while True:
        show_menu()
        choice = input("Choose: ").strip()

        if choice == "1":
            add_note()
        elif choice == "2":
            view_notes()
        elif choice == "3":
            delete_notes()
        elif choice == "4":
            get_weather()
        elif choice == "5":
            get_joke()
        elif choice == "6":
            open_google()
        elif choice == "7":
            show_datetime()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
