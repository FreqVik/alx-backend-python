import time
import sqlite3 
import functools


query_cache = {}
def with_db_connection(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

"""your code goes here"""
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = args[1] if len(args) > 1 else kwargs.get("query", "")
        if query in query_cache:
            print(f"[CACHE] Using cached result for query: {query}")
            return query_cache[query]
        else:
            print(f"[CACHE] Executing and caching result for query: {query}")
            result = func(*args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper

@with_db_connection
@cache_query

def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")