# # <p align="center"> 👾 Pokepy 👾 </p>
---

This is a simple, yet complete, full-stack web application built in **Flask/Python** that demonstrates all the **CRUD** (Create, Read, Update, Delete) operations, integrated with **PokeAPI** (a RESTful API) and a secure **Login/Register system** designed with industry best practices.

<br>

![Application Image](https://i.imgur.com/1cpg5jh.png)

<br>

<p align="center"> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" /> <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" /> <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" /> <img src="https://img.shields.io/badge/Railway-000000?style=for-the-badge&logo=railway&logoColor=white" /> </p>

<br>

## 🚀 Live Demo

You can check out the application [here](https://pokepy-crud-production.up.railway.app/).
<br>
<br>

----

## 🛠️ Features

- **User Authentication**: Implemented secure **Login/Register** functionality with **Flask-Login** session management.

- **CRUD Operations**: Allows users to **Create, Read, Update, and Delete** to manage Pokémons, utilizing PokeAPI.

- **Restful API**:  The application uses a full **RESTful API** (PokeAPI) to handle all data interactions. This ensures that the *front-end* communicates with the *back-end* using **HTTP** methods **(GET, POST, PUT, DELETE)** to manage resources.

- **Database Management**: The application uses **PostgreSQL** for reliable data storage.

- **Responsive Design**: Can be used for both desktop and mobile devices.

<br>

## 🗄️ PostgreSQL Integration

This application uses **PostgreSQL** as the relational database management system to store and manage data.

### 🛠️ Database Schema

The application follows best practices for database design by organizing data into two well-defined tables. The schema is optimized for performance, data integrity, and maintainability.

- Table 1: users

This table is responsible for managing registered users of the application. It contains columns such as:

    - uid (Integer, Primary Key) — A unique identifier for each user.

    - username (String, Unique, Not Null) — The login name chosen by the user.

    - password (String, Not Null) — A securely hashed password.

    - gender (Boolean, Not Null) — Gender of the user (True for male, False for female).

    - created_at (DateTime) — Timestamp of when the user was created (defaults to the current time).

- Table 2: pokemons

This table manages the Pokémon collected by each user. It includes:

    - id (Integer, Primary Key) — A unique identifier for each Pokémon entry.

    - pokemon_name (String, Not Null) — The name of the Pokémon.

    - user_id (Integer, Foreign Key) — References users.uid; identifies the owner of the Pokémon.

    - added_at (DateTime) — Timestamp of when the Pokémon was added to the user's collection (defaults to the current time).


Both tables are designed with referential integrity, ensuring that relationships between tables are enforced via foreign keys (where applicable). This ensures the consistency and reliability of data across the application.
<br>
<br>