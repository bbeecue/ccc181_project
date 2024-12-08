def get_programs(db):
    cursor = db.cursor()
    cursor.execute("SELECT code, name FROM program")
    programs = cursor.fetchall()
    cursor.close()
    return programs

def get_students(db, search_query='', search_by='ID Number'):
    cursor = db.cursor()
    sql = "SELECT id_number, first_name, last_name, gender, program, year_level, image_url FROM student"
    
    if search_query:
        if search_by == "ID Number":
            sql += " WHERE id_number LIKE %s"
        elif search_by == "Name":
            sql += " WHERE CONCAT(first_name, ' ', last_name) LIKE %s"
        elif search_by == "Gender":
            sql += " WHERE LOWER(gender) = LOWER(%s)"
        elif search_by == "Program":
            sql += " WHERE program LIKE %s"
        elif search_by == "Year Level":
            sql += " WHERE year_level LIKE %s"

        search_pattern = f"%{search_query}%" if search_by != "Gender" else search_query
        cursor.execute(sql, (search_pattern,))
    else:
        cursor.execute(sql)
    
    students = cursor.fetchall()
    cursor.close()
    return students

def add_student(db, student_data):
    cursor = db.cursor()
    sql = """
        INSERT INTO student (id_number, first_name, last_name, gender, program, year_level, image_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, student_data)
    db.commit()
    cursor.close()

def get_student_by_id(db, id_number):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM student WHERE id_number=%s", (id_number,))
    student = cursor.fetchone()
    cursor.close()
    return student

def update_student(db, student_data, id_number):
    cursor = db.cursor()
    sql = """
        UPDATE student SET first_name=%s, last_name=%s, gender=%s, program=%s, year_level=%s, image_url=%s 
        WHERE id_number=%s
    """
    cursor.execute(sql, student_data + (id_number,))
    db.commit()
    cursor.close()

def delete_student(db, id_number):
    cursor = db.cursor()
    cursor.execute("DELETE FROM student WHERE id_number = %s", (id_number,))
    db.commit()
    cursor.close()

def student_exists(db, id_number):
    cursor = db.cursor()
    cursor.execute("SELECT id_number FROM student WHERE id_number = %s", (id_number,))
    exists = cursor.fetchone() is not None
    cursor.close()
    return exists
