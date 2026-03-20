import psycopg2
from psycopg2 import sql
from meal_demand.utils.common import get_logger

logger = get_logger()


def upload_to_postgres(df, table_name, dbname="postgres", user="postgres", host='meal_demand_postgres', port=5432, upload=False):
    if upload:
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
        