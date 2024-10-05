import csv
import hashlib
import re
import requests
import logging

CSV_FILE = 'regno.csv'
LOG_FILE = 'app.log'
API_KEY = '9Y58k5zlXuf0J6aUMvbgsdYlqUwuZHnK3zTYOfEc'
MAX_LOGIN_ATTEMPTS = 5
LIMIT = 10

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_users():
    users = {}
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            if 'email' not in reader.fieldnames:
                logging.error("CSV file format is incorrect. Missing 'email' field.")
                return users
            for row in reader:
                users[row['email']] = row
    except FileNotFoundError:
        pass
    return users

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$", email) is not None

def is_strong_password(password):
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char in "!@#$%^&*()" for char in password):
        return False
    return True

def register(users):
    email = input("Enter your email: ")
    if email in users:
        print("Email already exists!")
        logging.warning(f"Attempted to register with existing email: {email}")
        return

    if not is_valid_email(email):
        print("Invalid email format!")
        logging.warning(f"Invalid email format: {email}")
        return

    password = input("Enter your password (min 8 chars, 1 uppercase letter, 1 special character): ")
    if not is_strong_password(password):
        print("Password must be at least 8 characters long, contain one uppercase letter, and a special character!")
        logging.warning(f"Weak password attempt for email: {email}")
        return


    security_answer = input("What is your favorite color? ")

    users[email] = {
        'email': email,
        'password': hash_password(password),
        'security_question': "What is your favorite color?",
        'security_answer': security_answer
    }
    save_users(users)
    print(f"Registration successful for {email}!")
    logging.info(f"New user registered: {email}")

def login(users):
    attempts = 0
    while attempts < MAX_LOGIN_ATTEMPTS:
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        if email in users and hash_password(password) == users[email]['password']:
            print("Login successful!")
            logging.info(f"User logged in: {email}")
            return users[email]
        else:
            attempts += 1
            print(f"Invalid credentials. {MAX_LOGIN_ATTEMPTS - attempts} attempts left.")
            logging.warning(f"Failed login attempt for email: {email}")
    
    print("Too many failed attempts.")
    logging.error(f"Max login attempts exceeded for email: {email}")
    return None

def save_users(users):
    with open(CSV_FILE, mode='w', newline='') as file:
        fieldnames = ['email', 'password', 'security_question', 'security_answer']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for user in users.values():
            writer.writerow(user)

def fetch_neo_data():
    url = f'https://api.nasa.gov/neo/rest/v1/feed?api_key={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("Near-Earth Objects (NEOs):")
        count = 0
        for date in data['near_earth_objects']:
            for item in data['near_earth_objects'][date]:
                if count >= LIMIT:
                    break
                print(f"Name: {item['name']}")
                print(f"Close Approach Date: {item['close_approach_data'][0]['close_approach_date']}")
                print(f"Velocity: {item['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']} km/h")
                print(f"Hazardous: {item['is_potentially_hazardous_asteroid']}\n")
                count += 1
            if count >= LIMIT:
                break
        logging.info(f"Fetched NEO data from NASA API")
    except Exception as e:
        logging.error(f"Error fetching NEO data: {e}")
        print(f"Error fetching NEO data: {e}")

def fetch_ssd_data():
    url = f'https://api.le-systeme-solaire.net/rest/bodies/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("Solar System Objects:")
        count = 0
        for obj in data['bodies']:
            if count >= LIMIT:
                break
            print(f"Name: {obj['englishName']}")
            print(f"Type: {obj['bodyType']}")
            print(f"Mass: {obj.get('mass', {}).get('massValue', 'N/A')} kg")
            print(f"Radius: {obj.get('meanRadius', 'N/A')} km")
            print(f"Discovered: {obj.get('discoveredBy', 'N/A')}")
            print("\n")
            count += 1
        logging.info(f"Fetched Solar System data from NASA API")
    except Exception as e:
        logging.error(f"Error fetching Solar System data: {e}")
        print(f"Error fetching Solar System data: {e}")

def reset_password(users):
    email = input("Enter your registered email: ")
    if email not in users:
        print("Email not found.")
        logging.warning(f"Password reset attempt with non-existing email: {email}")
        return

    print(f"Security Question: {users[email]['security_question']}")
    answer = input("Your answer: ")

    if answer.lower() == users[email]['security_answer'].lower():
        new_password = input("Enter a new password (min 8 chars, 1 uppercase letter, 1 special character): ")
        if is_strong_password(new_password):
            users[email]['password'] = hash_password(new_password)
            save_users(users)
            print("Password reset successful!")
            logging.info(f"Password reset for email: {email}")
        else:
            print("Password must be at least 8 characters long, contain one uppercase letter, and a special character!")
            logging.warning(f"Weak password attempt during reset for email: {email}")
    else:
        print("Incorrect answer to the security question.")
        logging.warning(f"Incorrect security answer during password reset for email: {email}")

def main():
    users = load_users()

    while True:
        choice = input("Choose an option:\n1. Login\n2. Register\n3. Quit\nEnter choice: ").strip()
        
        if choice == '1':
            user_info = login(users)
            if user_info:
                api_choice = input("Choose API:\n1. NEO Feed\n2. Solar System Data\nEnter 1 or 2: ").strip()
                if api_choice == '1':
                    fetch_neo_data()
                elif api_choice == '2':
                    fetch_ssd_data()
                else:
                    print("Invalid choice.")
            else:
                reset_choice = input("Would you like to reset your password? (yes/no): ").strip().lower()
                if reset_choice == 'yes':
                    reset_password(users)
                else:
                    print("Exiting the login process.")
            continue

        elif choice == '2':
            register(users)
        elif choice == '3':
            print("Exiting...")
            logging.info("Program exited.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
