# populate_tables.py
from matematik import create_app, clear_and_fill_tables

app = create_app()

if __name__ == "__main__":
    clear_and_fill_tables(app)

