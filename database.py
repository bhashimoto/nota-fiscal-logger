from datetime import datetime
from os.path import isfile
import sqlite3
import logging

logger = logging.getLogger(__name__)

class DBManager:
    def __init__(self, filename=""):
        self.db_name:str = filename if filename != "" else "database.db"
        self.connect()


    def connect(self):
        logger.info("Trying to connect to database")
        db_exists = isfile(self.db_name)
        self.connection:sqlite3.Connection = sqlite3.connect(self.db_name)
        if not db_exists:
            logger.info("Database file not found, creating tables")
            self._generate_tables()
        logger.info("Connection successful")


    def _generate_tables(self):
        logger.info("Creating table")
        # NF table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS nota_fiscal
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cnpj TEXT,
                number INTEGER,
                series INTEGER,
                issue_date TEXT,
                UNIQUE(cnpj, number, series)
            );
        """)
        # items table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS items 
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    value REAL,
                    item_nf INTEGER,
                    FOREIGN KEY(item_nf) REFERENCES nota_fiscal(id)
                );
            """)

    def insert_nf(self, data:dict):
        logger.info(f"Inserting Nota Fiscal: {data}")
        cur = self.connection.cursor()
        cur.execute("""
            INSERT INTO nota_fiscal (cnpj, number, series, issue_date) VALUES
            (:cnpj, :number, :series, :issue_date);
        """, data)

    def insert_item(self, data:dict):
        logger.info(f"Inserting item: {data}")
        cur = self.connection.cursor()
        cur.executemany("INSERT INTO items (name, value) VALUES (:name, :value)",(data,))
        self.connection.commit()
