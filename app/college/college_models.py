from flask import current_app

def fetch_all_colleges():
    db = current_app.config['db']
    cursor = db.cursor()
    cursor.execute("SELECT code, name FROM college")
    colleges = cursor.fetchall()
    cursor.close()
    return colleges

def search_colleges(search_query, search_by):
    db = current_app.config['db']
    cursor = db.cursor()

    sql = "SELECT code, name FROM college"
    if search_query:
        if search_by == "College Code":
            sql += " WHERE code LIKE %s"
        elif search_by == "College Name":
            sql += " WHERE name LIKE %s"
        search_pattern = f"%{search_query}%"
        cursor.execute(sql, (search_pattern,))
    else:
        cursor.execute(sql)

    colleges = cursor.fetchall()
    cursor.close()
    return colleges

def insert_college(code, name):
    db = current_app.config['db']
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO college (code, name) VALUES (%s, %s)", (code, name))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error inserting college: {e}")
        return False
    finally:
        cursor.close()

def update_college(old_code, new_code, name):
    db = current_app.config['db']
    cursor = db.cursor()
    try:
        cursor.execute("""
            UPDATE college SET code=%s, name=%s WHERE code=%s
        """, (new_code, name, old_code))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error updating college: {e}")
        return False
    finally:
        cursor.close()

def delete_college(code):
    db = current_app.config['db']
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM college WHERE code = %s", (code,))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error deleting college: {e}")
    finally:
        cursor.close()

def fetch_college_by_code(code):
    db = current_app.config['db']
    cursor = db.cursor()
    cursor.execute("SELECT code, name FROM college WHERE code = %s", (code,))
    college = cursor.fetchone()
    cursor.close()
    if college:
        return {"code": college[0], "name": college[1]}
    return None

def college_exists(code):
    db = current_app.config['db']
    cursor = db.cursor()
    cursor.execute("SELECT code FROM college WHERE code = %s", (code,))
    exists = cursor.fetchone() is not None
    cursor.close()
    return exists
