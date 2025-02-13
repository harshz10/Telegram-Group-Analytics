 # Screenshots
 ![Image Alt](https://github.com/harshz10/Data-Analyst/blob/df9c70045ad93d541b1b17e9037fdcbc0165be91/store/home.png)
 ![Image Alt](https://github.com/harshz10/Data-Analyst/blob/8691df90a89a97fa80d70daa8670bd41e1fe6a86/store/analytics%20proposal.png).
 ![Image Alt](https://github.com/harshz10/Data-Analyst/blob/0df57ddc0bbec2e3e0900c613fdf8fce721a05df/store/admin%20dashboard.png)

 https://github.com/user-attachments/assets/79c5036f-bffc-4eae-909e-a3a0b744fdf1



# Telegram Group Analytics & Admin Dashboard

## Problem Statement
This project addresses two technical challenges for a Data Analyst role:
1. **Technical Round 1**: Propose 20 analytics metrics based on schema data from Telegram groups (Group Info, Member Info, Message Info).
2. **Technical Round 2**: Design an Admin Dashboard with 30 analytics/visualizations to help admins manage group engagement, growth, and content..

## Solution Overview
- **Analytics Proposal**: 20 metrics (e.g., Group Activity Score, Message Sentiment Analysis) derived from schema fields like `member_count`, `message_type`, and `timestamp`.
- **Admin Dashboard**: 30 visualizations (e.g., Daily Active Users, Spam Detection) to monitor group health, trends, and moderation efficiency.
- **Implementation**: A Flask app containerized using Docker, with logging, configuration, and dummy endpoints for demonstration.

## Folder Structure
├── logs/ # Log files for app processes and errors
│ ├── app.log
│ └── error.log
├── app.py # Flask application with analytics endpoints
├── config.py # Configuration for database and constants.
├── code_file.py # Core logic for calculating analytics
├── Dockerfile # Instructions to build the Docker image.
├── README.md # Project documentation (this file)
├── requirements.txt # Python dependencies (Flask, pandas, etc.)
└── analytics.docx # Detailed documentation of 20 + 30 analytics

# How to Run the Project

## Prerequisites
Before running the project, ensure you have the following installed:
1. **Docker** (for containerization) - [Download Docker](https://www.docker.com/get-started)
2. **Git** (optional, for cloning the repository) - [Download Git](https://git-scm.com/)
3. **Python 3.9+** (if running locally without Docker)
4. **Repository Access**: Clone or download the GitHub repository provided.

---

## Step-by-Step Instructions

### Method 1: Using Docker (Recommended)
1. **Clone the Repository**:
   ```bash
   git clone [your-github-repository-link]
   cd [repository-folder-name]
Build the Docker Image:

bash

docker build -t telegram-analytics 
Run the Docker Container:

bash

docker run -p 5000:5000 telegram-analytics
Verify the Application:

The Flask app will run on http://localhost:5000.

Check the logs for success messages:

bash

docker logs [container-id]  # Replace with your container ID
Method 2: Running Locally (Without Docker)
Clone the Repository:

bash

git clone [your-github-repository-link]
cd [repository-folder-name]
Create a Virtual Environment (optional but recommended):

bash

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Install Dependencies:

bash

pip install -r requirements.txt
Run the Flask Application:

bash

python app.py
Access Endpoints:

The app will be available at http://localhost:5000.

Example endpoints (modify in app.py for actual logic):

GET /daily_messages: Returns dummy daily message counts.

GET /active_users: Lists placeholder active users.



## Installation & Usage

### Prerequisites
- Docker installed on your machine.
- Git (optional, for cloning the repository).

### Steps to Run
1. **Clone the Repository**:
   ```bash
   git clone [your-repository-link]
   cd [repository-name]
Build and Run the Docker Container:

bash

docker build -t telegram-analytics .
docker run -p 5000:5000 telegram-analytics
Access Endpoints:

The Flask app runs on http://localhost:5000.

Example endpoints (modify in app.py as needed):

/daily_messages: Returns daily message counts.

/active_users: Lists daily active users.

Input/Output
Input: Data structured as per the schema (Group Info, Member Info, Message Info).

Output: Analytics results logged in app.log or returned via Flask endpoints.

Analytics Documentation
Detailed metrics for Round 1 and Round 2 are explained in analytics.docx.

Includes descriptions, purposes, and schema fields used for each analytic.

Dependencies
Python libraries listed in requirements.txt:

text

Flask==2.0.3
pandas==1.3.5
matplotlib==3.5.1

License
MIT License See LICENSE for details




