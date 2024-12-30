import psycopg2
from psycopg2.extras import RealDictCursor

# Configuración de conexión a la base de datos
DB_CONFIG = {
    "host": "aws-0-us-east-1.pooler.supabase.com",
    "database": "postgres",
    "user": "postgres.ysyjydrzdsdfiwyaydhe",
    "password": "EvaluacionesTI",
}

def connect_to_db():

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print("Error al conectar con la base de datos:", e)
        return None

#
def register_data(table, data):
    conn = connect_to_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                columns = ', '.join(data.keys())
                placeholders = ', '.join(['%s'] * len(data))
                values = tuple(data.values())
                query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                cursor.execute(query, values)
                conn.commit()
                print(f"Datos insertados correctamente en la tabla {table}.")
        except Exception as e:
            print(f"Error al insertar datos en la tabla {table}: {e}")
        finally:
            conn.close()

#            
def get_user_role(username, password):
    conn = connect_to_db()
    if conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT user_role FROM evaluacionesTI.Usuarios WHERE username = %s AND password = %s",
                    (username, password),
                )
                user = cursor.fetchone()
                return user["user_role"] if user else None
        except Exception as e:
            print(f"Error al obtener rol del usuario: {e}")
            return None
        finally:
            conn.close()

#
def query_data(table, conditions=None):
    conn = connect_to_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                query = f"SELECT * FROM {table}"
                if conditions:
                    query += f" WHERE {conditions}"
                cursor.execute(query)
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(f"Error al consultar datos de la tabla {table}: {e}")
            return []
        finally:
            conn.close()

#
def update_data(table, updates, conditions, values):
    conn = connect_to_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                set_clause = ', '.join([f"{key} = %s" for key in updates.keys()])
                query = f"UPDATE {table} SET {set_clause} WHERE {conditions}"
                cursor.execute(query, values)  # Aquí pasa el `values` correctamente
                conn.commit()
                print(f"Datos actualizados correctamente en la tabla {table}.")
                return True  # Retornar True si se actualizó correctamente
        except Exception as e:
            print(f"Error al actualizar datos en la tabla {table}: {e}")
            return False
        finally:
            conn.close()

#
def check_if_exists(query, params):
    """Verifica si existe un registro en la base de datos usando una consulta SQL."""
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()[0]  # Devolver el número de registros que coinciden con la condición
        conn.close()

        return result > 0  # Si existe al menos un registro, retornamos True
    except Exception as e:
        print(f"Error al verificar la existencia: {e}")
        return False

#
def join_tables(table1, table2, common_column, columns_to_select=None, conditions=None):

    conn = connect_to_db()
    if conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Determinar las columnas a seleccionar
                select_clause = ', '.join(columns_to_select) if columns_to_select else '*'
                
                # Construir la consulta
                query = f"""
                SELECT {select_clause}
                FROM {table1}
                INNER JOIN {table2} ON {table1}.{common_column} = {table2}.{common_column}
                """
                if conditions:
                    query += f" WHERE {conditions}"

                cursor.execute(query)
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(f"Error al realizar el JOIN entre {table1} y {table2}: {e}")
            return []
        finally:
            conn.close()