class StudentModel:
    def __init__(self, db):
        self.db = db

    def get_students(self, search_query='', search_by='ID Number'):
        cursor = self.db.cursor()
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

    def add_student(self, student_data):
        cursor = self.db.cursor()
        sql = """
            INSERT INTO student (id_number, first_name, last_name, gender, program, year_level, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            student_data["id_number"],
            student_data["first_name"], 
            student_data["last_name"], 
            student_data["gender"], 
            student_data["program"], 
            student_data["year_level"], 
            student_data["image_url"]
        ))
        self.db.commit()
        cursor.close()

    def get_student_by_id(self, id_number):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM student WHERE id_number=%s", (id_number,))
        student = cursor.fetchone()
        cursor.close()
        return student

    def update_student(self, student_data, id_number):
        cursor = self.db.cursor()
        sql = """
            UPDATE student 
            SET first_name=%s, last_name=%s, gender=%s, program=%s, year_level=%s, image_url=%s 
            WHERE id_number=%s
        """
        
        # Ensure that student_data values are extracted in the correct order and combined with id_number
        cursor.execute(sql, (
            student_data["first_name"], 
            student_data["last_name"], 
            student_data["gender"], 
            student_data["program"], 
            student_data["year_level"], 
            student_data["image_url"], 
            id_number
        ))
        
        self.db.commit()
        cursor.close()


    def delete_student(self, id_number):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM student WHERE id_number = %s", (id_number,))
        self.db.commit()
        cursor.close()

    def student_exists(self, id_number):
        cursor = self.db.cursor()
        cursor.execute("SELECT id_number FROM student WHERE id_number = %s", (id_number,))
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists
