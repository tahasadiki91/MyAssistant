import json
import threading
import time
from datetime import datetime

# === FICHIERS ===
TASKS_FILE = "tasks.json"
NOTES_FILE = "notes.json"
LOG_FILE = "activity_log.json"

# === CHARGEMENT & SAUVEGARDE ===
def load_json_file(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_json_file(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# === JOURNAL D'ACTIVITÉS ===
def log_action(action):
    log = load_json_file(LOG_FILE)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.append({"timestamp": timestamp, "action": action})
    save_json_file(log, LOG_FILE)

def show_log():
    log = load_json_file(LOG_FILE)
    for entry in log:
        print(f"{entry['timestamp']} - {entry['action']}")

def search_log():
    keyword = input("Mot-clé : ").strip().lower()
    log = load_json_file(LOG_FILE)
    results = [e for e in log if keyword in e["action"].lower()]
    for entry in results:
        print(f"{entry['timestamp']} - {entry['action']}")

# === PLANIFICATEUR DE TÂCHES ===
def add_task(tasks):
    title = input("Titre tâche : ")
    priority = input("Priorité (haute, moyenne, basse) : ").lower()
    if priority not in ["haute", "moyenne", "basse"]:
        priority = "moyenne"
    tasks.append({"title": title, "priority": priority, "done": False})
    log_action(f"Ajout tâche : {title}")

def mark_done(tasks):
    show_tasks(tasks)
    idx = int(input("Num tâche à terminer : ")) - 1
    if 0 <= idx < len(tasks):
        tasks[idx]["done"] = True
        log_action(f"Tâche terminée : {tasks[idx]['title']}")

def show_tasks(tasks):
    if not tasks:
        print("Aucune tâche.")
        return
    priority_order = {"haute": 0, "moyenne": 1, "basse": 2}
    tasks_sorted = sorted(tasks, key=lambda x: (x["done"], priority_order[x["priority"]]))
    for i, t in enumerate(tasks_sorted, 1):
        status = "✔️" if t["done"] else "❌"
        print(f"{i}. [{status}] ({t['priority']}) {t['title']}")

def tasks_menu():
    tasks = load_json_file(TASKS_FILE)
    while True:
        print("\n--- Planificateur de Tâches ---")
        print("1. Ajouter  2. Terminer  3. Afficher  4. Retour")
        c = input("Choix : ")
        if c == "1": add_task(tasks)
        elif c == "2": mark_done(tasks)
        elif c == "3": show_tasks(tasks)
        elif c == "4": break
        save_json_file(tasks, TASKS_FILE)

# === GESTION DES NOTES ===
def add_note(notes):
    title = input("Titre : ")
    content = input("Contenu : ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notes.append({"title": title, "content": content, "date": date})
    log_action(f"Ajout note : {title}")

def show_notes(notes):
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note['title']} ({note['date']})")

def search_notes(notes):
    k = input("Mot-clé : ").lower()
    for note in notes:
        if k in note['title'].lower() or k in note['content'].lower():
            print(f"- {note['title']} ({note['date']})")

def notes_menu():
    notes = load_json_file(NOTES_FILE)
    while True:
        print("\n--- Notes ---")
        print("1. Ajouter  2. Afficher  3. Rechercher  4. Retour")
        c = input("Choix : ")
        if c == "1": add_note(notes)
        elif c == "2": show_notes(notes)
        elif c == "3": search_notes(notes)
        elif c == "4": break
        save_json_file(notes, NOTES_FILE)

# === RAPPELS PROGRAMMÉS ===
reminders = []

def reminder_thread(time_str, msg):
    r_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    while datetime.now() < r_time:
        time.sleep(1)
    print(f"\n🔔 Rappel : {msg}")
    log_action(f"Rappel déclenché : {msg}")

def add_reminder():
    time_str = input("Heure (YYYY-MM-DD HH:MM) : ")
    msg = input("Message : ")
    t = threading.Thread(target=reminder_thread, args=(time_str, msg), daemon=True)
    t.start()
    reminders.append((time_str, msg))
    log_action(f"Rappel ajouté : {msg} à {time_str}")

def list_reminders():
    for i, (t, m) in enumerate(reminders, 1):
        print(f"{i}. {t} - {m}")

def reminders_menu():
    while True:
        print("\n--- Rappels ---")
        print("1. Ajouter  2. Lister  3. Retour")
        c = input("Choix : ")
        if c == "1": add_reminder()
        elif c == "2": list_reminders()
        elif c == "3": break

# === JOURNAL MENU ===
def log_menu():
    while True:
        print("\n--- Journal ---")
        print("1. Afficher  2. Rechercher  3. Retour")
        c = input("Choix : ")
        if c == "1": show_log()
        elif c == "2": search_log()
        elif c == "3": break

# === MENU PRINCIPAL ===
def main_menu():
    while True:
        print("\n=== Assistant Personnel ===")
        print("1. Tâches  2. Notes  3. Rappels  4. Journal  5. Quitter")
        c = input("Choix : ")
        if c == "1": tasks_menu()
        elif c == "2": notes_menu()
        elif c == "3": reminders_menu()
        elif c == "4": log_menu()
        elif c == "5": print("À bientôt !"); break

if __name__ == "__main__":
    main_menu()
