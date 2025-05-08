# 🔴 Pokepy
---

This is a simple, yet complete, full-stack web application built in **Flask/Python** that demonstrates all the **CRUD** (Create, Read, Update, Delete) operations, integrated with **PokeAPI** (a RESTful API) and a secure **Login/Register system** designed with industry best practices.

## 🚀 Live Demo

You can check out a live demo of the application [here](https://your-livesite-link.com).

---

## 🛠️ Features

- **User Authentication**: Implemented secure **Login/Register** functionality with **Flask-Login** session management.
- **CRUD Operations**: Allows users to **Create, Read, Update, and Delete** to manage Pokémons, utilizing PokeAPI.
- **Restful API**:  The application uses a full **RESTful API** (PokeAPI) to handle all data interactions. This ensures that the *front-end* communicates with the *back-end* using **HTTP** methods **(GET, POST, PUT, DELETE)** to manage resources.
- **Database Management**: The application uses **PostgreSQL** for reliable data storage.
- **Responsive Design**: Can be used for both desktop and mobile devices.

---

## 🗄️ PostgreSQL Integration

This application uses **PostgreSQL** as the relational database management system to store and manage application data. PostgreSQL was chosen for its robustness, scalability, and support for complex queries and transactions.

### 🛠️ Database Schema

The application follows best practices for database design by organizing data into **two well-defined tables**. The schema is optimized for performance, data integrity, and maintainability.

- **Table 1:** *[Table Name]*  
  This table is responsible for [brief description of its purpose]. It contains columns such as:
  - `id` (Primary Key)
  - `[Column 1]` (Data Type) — [brief description of column]
  - `[Column 2]` (Data Type) — [brief description of column]
  
- **Table 2:** *[Table Name]*  
  This table manages [brief description of its purpose]. It includes:
  - `id` (Primary Key)
  - `[Column 1]` (Data Type) — [brief description of column]
  - `[Column 2]` (Data Type) — [brief description of column]

Both tables are designed with **referential integrity**, ensuring that relationships between tables are enforced via **foreign keys** (where applicable). This ensures the consistency and reliability of data across the application.