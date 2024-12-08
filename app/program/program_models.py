def get_colleges(db):
    """Fetch all colleges."""
    cursor = db.cursor()
    cursor.execute("SELECT code, name FROM college")
    colleges = cursor.fetchall()
    cursor.close()
    return colleges

def get_programs(db, search_query=None, search_by=None):
    """Fetch all programs or programs matching a search query."""
    cursor = db.cursor()
    sql = "SELECT code, name, college FROM program"
    if search_query and search_by:
        if search_by == "Program Code":
            sql += " WHERE code LIKE %s"
        elif search_by == "Program Name":
            sql += " WHERE name LIKE %s"
        elif search_by == "College Code":
            sql += " WHERE college LIKE %s"
        search_pattern = f"%{search_query}%"
        cursor.execute(sql, (search_pattern,))
    else:
        cursor.execute(sql)
    programs = cursor.fetchall()
    cursor.close()
    return programs

def get_program(db, program_code):
    """Fetch a single program by its code."""
    cursor = db.cursor()
    cursor.execute("SELECT code, name, college FROM program WHERE code = %s", (program_code,))
    program = cursor.fetchone()
    cursor.close()
    return program

def add_program(db, program_code, program_name, college_code):
    """Add a new program to the database."""
    cursor = db.cursor()
    try:
        sql = "INSERT INTO program (code, name, college) VALUES (%s, %s, %s)"
        cursor.execute(sql, (program_code, program_name, college_code))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()

def update_program(db, program_code, new_program_code, program_name, college_code):
    """Update an existing program."""
    cursor = db.cursor()
    try:
        sql = """
            UPDATE program
            SET code = %s, name = %s, college = %s
            WHERE code = %s
        """
        cursor.execute(sql, (new_program_code, program_name, college_code, program_code))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()

def delete_program(db, program_code):
    """Delete a program by its code."""
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM program WHERE code = %s", (program_code,))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()

def existing_program(db, program_code):
    """Check if a program with the given code exists."""
    cursor = db.cursor()
    cursor.execute("SELECT code FROM program WHERE code = %s", (program_code,))
    program = cursor.fetchone()
    cursor.close()
    return bool(program)
