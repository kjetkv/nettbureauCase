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


# Initiates table attempts. If table already exists, parameter decides whether or not to wipe it.
# Returns True if table was created or wiped and False if already inhabited table exists and persists.
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


# Wipes the currently existing table attempts and creates a new empty one.
# Returns true if table is successfully wiped and False if users table did not exist
def reset_attempts():
    conn = sqlite3.connect('database.db')
    try:
        conn.execute("DROP TABLE attempts")
        conn.execute(
            'CREATE TABLE attempts (ip TEXT UNIQUE , numAttempts INT, lastAttempt DATETIME)')
        return True
    except:
        return False


# returns the amount of recent attempts at posting to the server by the given
# ip-adress, and keeps the record in the attempts table updated.
def get_attempts(ip):
    # get the current amount of attempts the ip has and the timestamp of the last one.
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM attempts WHERE ip=?", (ip,))
    result = cur.fetchone()
    # If no record exists with the ip, insert one with the current timestamp and 1 attempt.
    if result is None:
        now = dt.datetime.now()
        cur.execute(
            "INSERT INTO attempts (ip,numAttempts,lastAttempt) VALUES (?,?,?)", (ip, 1, now))
        conn.commit()
        return 1
    # If a record exists, check if the timestamp is older than 20 minutes.
    else:
        limit = dt.datetime.now() - dt.timedelta(minutes=20)
        lastAttempt = dt.datetime.strptime(result['lastAttempt'],'%Y-%m-%d %H:%M:%S.%f')
        # If the timestamp is old, clear the attempts of the ip.
        if lastAttempt < limit:
            clear_attempts(ip)
            return 1
        # If the timestamp is new, increment the number of attempts and update record.
        else:
            num_attempts = result['numAttempts'] + 1
            update_attempts(ip, num_attempts)
            return num_attempts


# Sets the number of attempts for the ip's record to 1 (the one currently being processed).
def clear_attempts(ip):
    conn = sqlite3.connect('database.db')
    conn.cursor().execute("UPDATE attempts SET numAttempts=1 WHERE ip=?", (ip,))
    conn.commit()


# Updates the number of attempts for the given ip, and sets the timestamp to now.
def update_attempts(ip, num_attempts):
    now = dt.datetime.now()
    conn = sqlite3.connect('database.db')
    conn.cursor().execute("UPDATE attempts SET numAttempts=?, lastAttempt=? WHERE ip=?", (num_attempts, now, ip))
    conn.commit()
