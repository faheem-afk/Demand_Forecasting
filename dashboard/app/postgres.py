import psycopg2
import pandas as pd


def run_postgres_query(query,
              fetch=True, 
              dbname="postgres", 
              user="postgres", 
              host="localhost", 
              port=5432):
    
    conn = psycopg2.connect(dbname=dbname, user=user, host=host, port=port)
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()


    if fetch:
        rows = cur.fetchall()
        colnames = [desc.name for desc in cur.description]

        cur.close()
        conn.close()

        df = pd.DataFrame(rows, columns = colnames)

        return df
    