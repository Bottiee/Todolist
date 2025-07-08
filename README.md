# To-Do List Application

A full-featured To-Do list web application built with Django. This project allows users to manage their daily tasks through a clean and interactive interface, with advanced features for both regular users and administrators.

---
## ✨ Key Features

* **User Authentication:** Secure user registration, login, and logout functionality.
* **Full CRUD Functionality:** Users can Create, Read, Update, and Delete their own tasks.
* **Data Isolation:** A user can only see and manage the tasks they have created.
* **Drag-and-Drop Priority:** Easily reorder tasks by dragging and dropping them to set their priority. The new order is saved automatically.
* **Superuser Dashboard:** A special administrative view where a superuser can see all registered users and view their respective tasks.
* **Dynamic Frontend:**
    * **Light/Dark Mode Toggle:** A theme switcher that saves the user's preference.
    * **Interactive UI:** Built with Bootstrap 5 for a responsive and modern look.
    * **Hover-to-Reveal Footer:** A dynamic footer that stays hidden at the bottom of the page until moused over.

---
## 🛠️ Technologies Used

* **Backend:** Django
* **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
* **Database:** SQLite (default, can be configured for others)
* **JavaScript Library:** SortableJS for drag-and-drop functionality.

---
## 🚀 Setup and Installation

To get this project running locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Bottiee/Todolist.git
    cd <project-directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For Windows
    python -m venv .venv
    .venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply the database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser to access the admin dashboard:**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create your admin account.

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000/`.

---
## ✍️ Author

This project was created by **Manfredas Šiaulys** as part of the CodeAcademy PTU30 course.
