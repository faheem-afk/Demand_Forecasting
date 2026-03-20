import psycopg2
from psycopg2 import sql
from meal_demand.utils.common import get_logger
import pandas as pd
import io 


logger = get_logger()

def upload_to_postgres(
    df,
    table_name,
    dbname="postgres",
    user="postgres",
    host="localhost",
    port=5432
):
    logger.info("Uploading to postgres...")

    with psycopg2.connect(
        dbname=dbname,
        user=user,
        host=host,
        port=port
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(sql.SQL("DROP TABLE IF EXISTS {table}").format(
                    table=sql.Identifier(table_name)
                    ))
            create_table_query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS {table} (
                    {fields}
                )
            """).format(
                table=sql.Identifier(table_name),
                fields=sql.SQL(", ").join(
                    sql.SQL("{} {}").format(
                        sql.Identifier(col),
                        sql.SQL(pandas_to_postgres_type(str(df[col].dtype)))
                    )
                    for col in df.columns
                )
            )
            cur.execute(create_table_query)

            buffer = io.StringIO()
            df.to_csv(buffer, index=False, header=False, na_rep="\\N")
            buffer.seek(0)

            copy_query = sql.SQL("""
                COPY {table} ({fields})
                FROM STDIN WITH CSV NULL '\\N'
            """).format(
                table=sql.Identifier(table_name),
                fields=sql.SQL(", ").join(map(sql.Identifier, df.columns))
            )

            cur.copy_expert(copy_query, buffer)

    logger.info("Upload successful.")

def pandas_to_postgres_type(dtype):
    if dtype in ("int64", "int32"):
        return "INTEGER"
    elif dtype in ("float64", "float32"):
        return "DOUBLE PRECISION"
    elif dtype == "bool":
        return "BOOLEAN"
    elif "datetime" in dtype:
        return "TIMESTAMP"
    else:
        return "TEXT"

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
    