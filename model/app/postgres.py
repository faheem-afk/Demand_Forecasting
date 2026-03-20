import psycopg2
from psycopg2 import sql
from meal_demand.utils.common import get_logger
import pandas as pd

logger = get_logger()

def upload_to_postgres(df, table_name, dbname="postgres", user="postgres", host='localhost', port=5432):
 
    logger.info("Uploading to postgres.....")
    # Connect to PostgreSQL
    conn = psycopg2.connect(dbname=dbname, user=user, host=host, port=port)
    cur = conn.cursor()
    
    # Create table if it doesn't exist
    create_table_query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS {table} (
            {fields}
        )
    """).format(
        table=sql.Identifier(table_name),
        fields=sql.SQL(', ').join(
            sql.SQL("{} {}").format(sql.Identifier(col), sql.SQL(pandas_to_postgres_type(str(df[col].dtype)))) for col in df.columns
        )
    )
    cur.execute(create_table_query)
    conn.commit()
    # Insert data into table
    for index, row in df.iterrows():
        insert_query = sql.SQL("""
            INSERT INTO {table} ({fields}) VALUES ({values})
        """).format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(', ').join(map(sql.Identifier, df.columns)),
            values=sql.SQL(', ').join(sql.Placeholder() * len(df.columns))
        )
        cur.execute(insert_query, tuple(row))
    
    conn.commit()
    cur.close()
    conn.close()
    logger.info("....Successful.")

def pandas_to_postgres_type(dtype):
    if dtype == 'int64':
        return 'INTEGER'
    elif dtype == 'float64':
        return 'FLOAT'
    elif dtype == 'bool':
        return 'BOOLEAN'
    else:
        return 'TEXT'


def run_query(query, fetch=True, dbname="postgres", user="postgres", host="localhost", port=5432):
    conn = psycopg2.connect(dbname=dbname, user=user, host=host, port=port)
    cur = conn.cursor()

    logger.info("Dropping the older table...")
    cur.execute(query)
    conn.commit()
    logger.info("Older Table dropped Successfully.")

    if fetch:
        rows = cur.fetchall()
        colnames = [desc.name for desc in cur.description]

        cur.close()
        conn.close()

        df = pd.DataFrame(rows, columns = colnames)

        return df
    