import sqlite3
import datetime as dt


# Initiates DB with table users. If users already exists, parameter decides whether or not to wipe it.
# Returns True if table was created or wiped and False if already inhabited table exists and persists.
def init_users(wipe=False):
    conn = sqlite3.connect('database.db')
    try:
        conn.execute(
            'CREATE TABLE users (name TEXT, email TEXT UNIQUE , phone TEXT UNIQUE, areacode TEXT, comment TEXT)')
        return True
    except:
        if not wipe:
            return False
        else:
            reset_users()


# Wipes the currently existing table users and creates a new empty one.
# Returns true if table is successfully wiped and False if users table did not exist.
def reset_users():
    conn = sqlite3.connect('database.db')
    try:
        conn.execute("DROP TABLE users")
        conn.execute(
                'CREATE TABLE users (name TEXT, email TEXT UNIQUE , phone TEXT UNIQUE, areacode TEXT, comment TEXT)')
        return True
    except:
        return False


def init_attempts(wipe=False):
    conn = sqlite3.connect('database.db')
    try:
        conn.execute(
            'CREATE TABLE attempts (ip TEXT UNIQUE , num_attempts INT, lastAttempt DATETIME)')
        return True
    except:
        if not wipe:
            return False
        else:
            reset_attempts()


def reset_attempts():
    conn = sqlite3.connect('database.db')
    try:
        conn.execute("DROP TABLE attempts")
        conn.execute(
            'CREATE TABLE attempts (ip TEXT UNIQUE , numAttempts INT, lastAttempt DATETIME)')
        return True
    except:
        return False


def get_attempts(ip):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM attempts WHERE ip=?", (ip,))
    result = cur.fetchone()
    if result is None:
        now = dt.datetime.now()
        cur.execute(
            "INSERT INTO attempts (ip,numAttempts,lastAttempt) VALUES (?,?,?)", (ip, 1, now))
        conn.commit()
        return 1
    else:
        limit = dt.datetime.now() - dt.timedelta(minutes=20)
        lastAttempt = dt.datetime.strptime(result['lastAttempt'],'%Y-%m-%d %H:%M:%S.%f')
        if lastAttempt < limit:
            clear_attempts(ip)
            return 1
        else:
            num_attempts = result['numAttempts'] + 1
            update_attempts(ip, num_attempts)
            return num_attempts


def clear_attempts(ip):
    conn = sqlite3.connect('database.db')
    conn.cursor().execute("UPDATE attempts SET numAttempts=1 WHERE ip=?", (ip,))
    conn.commit()


def update_attempts(ip, num_attempts):
    now = dt.datetime.now()
    conn = sqlite3.connect('database.db')
    conn.cursor().execute("UPDATE attempts SET numAttempts=?, lastAttempt=? WHERE ip=?", (num_attempts, now, ip))
    conn.commit()
