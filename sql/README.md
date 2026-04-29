# SQL Structure and Usage Documentation

This README file provides an overview of the SQL structure used in the ChatBot-Flask application, including the creation of tables and seeding of initial data.

## Directory Structure

The SQL files are located in the `sql/Estruturas` directory and include the following:

- `create_tables.sql`: Contains SQL commands to create the necessary tables in the SQLite database.
- `seed_data.sql`: Contains SQL commands to populate the database with initial data.

## Usage

To set up the SQLite database for the ChatBot-Flask application, follow these steps:

1. **Create the Database**:
   - Run the `create_tables.sql` script to create the required tables in your SQLite database.

2. **Seed Initial Data**:
   - After creating the tables, execute the `seed_data.sql` script to populate the database with initial data.

## Example Commands

You can execute the SQL scripts using a SQLite client or through a Python script. For example, if using the command line:

```bash
sqlite3 your_database.db < create_tables.sql
sqlite3 your_database.db < seed_data.sql
```

## Notes

- Ensure that you have SQLite installed and accessible from your command line.
- Modify the database file name as needed to match your setup.
- The structure and data defined in these SQL files are essential for the proper functioning of the ChatBot application.