# CAP776
 NASA API Integration
Project Overview
This project is a Python-based user management system that allows users to register, log in, and reset passwords securely. It integrates with NASA's APIs to fetch information about Near-Earth Objects (NEOs) and other solar system bodies. The system includes features for password hashing, user data validation, and logging activities.

Features
User registration and login
Password reset functionality
Data fetching from NASA APIs:
Near-Earth Objects (NEOs)
Solar System Objects
Input validation for emails and passwords
Logging user activities and errors to a log file
Requirements
Before running the project, ensure you have the following installed:

Python 3.6 or higher
pip (Python package installer)
Required Python Packages
The following packages need to be installed to run the project:

requests: For making API calls.
bcrypt (if using the improved password hashing approach): For secure password hashing.
You can install these packages using the following command:

bash
Copy code
pip install requests bcrypt
Installation
Clone the Repository: Download the project files or clone the repository from GitHub (if hosted).

bash
Copy code
git clone <repository-url>
Navigate to the Project Directory: Change your current directory to the project folder.

bash
Copy code
cd <project-directory>
Install Required Packages: Run the pip install command mentioned above.

Configuration
Set Up CSV File: Create a CSV file named regno.csv in the project directory. The file should initially be empty or contain the header:

csv
Copy code
email,password,security_question,security_answer
API Key: Obtain a NASA API key by signing up at NASA API and replace the placeholder in the code:

python
Copy code
API_KEY = 'YOUR_NASA_API_KEY'
Usage
Run the Application: Execute the Python script using the following command:

bash
Copy code
python <script-name>.py
User Interaction: Follow the prompts to register, log in, or reset your password. Upon successful login, choose between fetching data from NEO Feed or Solar System Data.

Logging
All activities, including errors and warnings, will be logged in the app.log file in the project directory.

Notes
Ensure you have an active internet connection to fetch data from the NASA APIs.
Passwords must meet specified security criteria (at least 8 characters long, one uppercase letter, and one special character).
