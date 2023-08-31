import logging
import psycopg2

from bank_parser.config import db_config


LOGGER = logging.getLogger(__name__)


def connect():
    try:
        # read connection parameters
        params = db_config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        if conn is not None:
            return conn

        raise Exception("Could not connect to PostgreSQL")

    except (Exception, psycopg2.DatabaseError) as err:
        LOGGER.critical(err)


def insert_bank_info(banks_list):
    query = """INSERT INTO bank_info (name, address, rate, review_numbers) 
               VALUES (%s, %s, %s, %s) 
            """
    try:
        conn = connect()
        with conn.cursor() as cursor:
            cursor.executemany(query, banks_list)

        conn.commit()
        conn.close()
        return True

    except Exception as err:
        LOGGER.error(f"Error insert bank info: {err}")
        return False


def insert_review_info():
    pass
