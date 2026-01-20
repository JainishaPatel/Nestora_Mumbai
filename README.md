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
- [Project Structure](#project-structure)  
- [Dependencies](#dependencies)  
- [Notes / Tips](#notes--tips)  

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

2. **MySQL Server**  
   - Windows: [Installer](https://dev.mysql.com/downloads/installer/)  
   - macOS/Linux: Use your package manager (`brew install mysql`, etc.)

3. **Cloudinary Account**  
   Free signup: [https://cloudinary.com/](https://cloudinary.com/)

---

## Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/JainishaPatel/Nestora_Mumbai.git
cd nestora_mumbai
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









