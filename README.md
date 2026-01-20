# Nestora Mumbai 🏠

**A Real Estate Listing Platform for Mumbai**  

Nestora Mumbai is a web application built with **Flask** that allows users to browse, create, and manage property listings. Admins can verify or reject properties, and users can manage profiles, reset passwords securely, and upload property images via **Cloudinary**.

---

## Table of Contents

- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Prerequisites](#prerequisites)  
- [Installation Guide](#installation-guide)  
- [Environment Variables](#environment-variables)  
- [Database Setup](#database-setup)  
- [Running the Application](#running-the-application)  
- [Usage](#usage)  
- [Admin Panel](#admin-panel)    
- [Image Preview](#image-preview)
---

## Features

- User signup, login, and logout  
- Profile management  
- Password reset with secure token  
- Browse properties with filters (area, property type, price)  
- Create, edit, and delete properties with images  
- Admin verification/rejection of properties  
- CSRF protection and form validation  
- Cloud-hosted property images with **Cloudinary**

---

## Tech Stack

- **Frontend:** HTML, CSS, Bootstrap, JavaScript, Jinja2 templates  
- **Backend:** Python, Flask, Flask-WTF  
- **Database:** MySQL (`mysql-connector-python`)  
- **Cloud:** Cloudinary for images  
- **Authentication & Security:** Sessions, bcrypt, CSRF protection  

---

## Prerequisites

Before setup, make sure the following are installed:

1. **Python 3.11+**  
   [Download here](https://www.python.org/downloads/)

   (Make sure `pip` is installed along with Python.)

3. **MySQL Server**  
   - Windows: [Installer](https://dev.mysql.com/downloads/installer/)  
   - macOS/Linux: Use your package manager (`brew install mysql`, `sudo apt install mysql-server`, etc.)

4. **Cloudinary Account**  
   Free signup: [https://cloudinary.com/](https://cloudinary.com/)

---

## Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/JainishaPatel/Nestora_Mumbai.git
cd Nestora_Mumbai
```

### 2️⃣ Create & Activate Virtual Environment

**Windows**
```bash
python -m venv my_env
my_env\Scripts\activate
```
**macOS / Linux**
```bash
python3 -m venv my_env
source my_env/bin/activate
```
### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

### Create a `.env` file in the root of your project with the following placeholders:
```bash
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=your_db_name
SECRET_KEY=your_secret_key
CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret
ADMIN_NAME=your_admin_name
ADMIN_EMAIL=your_admin_email
ADMIN_PASSWORD=your_admin_password
ADMIN_PHONE=your_admin_phone
```

⚠️ **Important**

- **Do NOT commit** the `.env` file to GitHub.
- Add `.env` to `.gitignore` to keep credentials safe.
- Replace all `your_*` placeholders with your actual credentials before running the project.

---

## Database Setup

### 1️⃣ Start MySQL server
- Make sure your MySQL service is running.

### 2️⃣ Create the database
```bash
CREATE DATABASE nestora;
```

### 3️⃣ Update environment variables
- Add your database credentials in the .env file.

### 4️⃣ Initialize database tables
- Run the database setup script to create all required tables:
``` bash
python models/database.py
```
( This command will automatically create all the required tables. )

### 5️⃣ Upload default/sample images (optional)
- Upload placeholder or sample images to Cloudinary:
``` bash
python -m utils.upload_defaults_to_cloudinary
```

### 6️⃣ Preload Dummy Data (Optional)
- If you want to add sample properties and users to your database for testing:
``` bash
python run.py
```
(This script will insert dummy/sample data into your database.
Make sure your `.env` file is configured and the database is initialized before running this.)

---

## Running the Application

### 1️⃣ Start the Flask server:
```bash
python app.py
```

### 2️⃣ Open your browser and visit:
``` bash
http://127.0.0.1:5000
```

---

## Usage

## User
- Register and log in
- Browse property listings
- Add new property listings with images
- Edit or delete your own properties
- Update profile information
- Reset password securely

## Guest
- View verified property listings
- Browse by area and property type

---

## Admin Panel

### Admins can:
- View all pending property listings
- Verify or reject properties
- Maintain listing quality and authenticity
  
(Admin credentials are configured via the `.env` file.)

---

## Image Preview

<img width="1763" height="930" alt="Nestora_Mumbai_Image_1" src="https://github.com/user-attachments/assets/1d05bbe1-8bd9-44d4-96d3-a867ff7fa72d" />

<img width="1771" height="872" alt="Nestora_Mumbai_Image_2" src="https://github.com/user-attachments/assets/c3074037-930b-4b70-adc9-73122e5431af" />

<img width="1765" height="1017" alt="Nestora_Mumbai_Image_3" src="https://github.com/user-attachments/assets/aac0e4f1-b212-4f28-87f3-9148934c7a87" />

<img width="1808" height="1020" alt="Nestora_Mumbai_Image_4" src="https://github.com/user-attachments/assets/ebafe03c-a825-4435-b94a-4ca816b71362" />

<img width="1885" height="1018" alt="Nestora_Mumbai_Image_5" src="https://github.com/user-attachments/assets/a91bc119-d095-421e-b6b7-8b1286ce3639" />














