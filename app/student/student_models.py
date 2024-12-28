class StudentModel:
    def __init__(self, db):
        self.db = db

    def get_students(self, search_query='', search_by='ID Number', page=1, students_per_page=10):
        cursor = self.db.cursor()

        sql = """
            SELECT s.id_number, s.first_name, s.last_name, s.gender, p.code AS program_code, s.year_level, s.image_url, c.name AS college_name
            FROM student s
            LEFT JOIN program p ON s.program = p.code
            LEFT JOIN college c ON p.college = c.code
        """

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
            elif search_by == "College":
                sql += " WHERE c.name LIKE %s"   

            search_pattern = f"%{search_query}%" if search_by != "Gender" else search_query
            params = (search_pattern,)
        else:
            params = ()
        
        sql += " LIMIT %s OFFSET %s"
        offset = (page - 1) * students_per_page
        params += (students_per_page, offset)

        cursor.execute(sql, params)
        students = cursor.fetchall()
        cursor.close()

        student_list = []
        for student in students:
            student_dict = {
                'id_number': student[0],
                'first_name': student[1],
                'last_name': student[2],
                'gender': student[3],
                'program': student[4],
                'year_level': student[5],
                'image_url': student[6],
                'college': student[7]
            }
            student_list.append(student_dict)

        return student_list


    
    def count_students(self, search_query='', search_by='ID Number'):
        cursor = self.db.cursor()
        sql = """
            SELECT COUNT(*) FROM student s
            LEFT JOIN program p ON s.program = p.code
            LEFT JOIN college c ON p.college = c.code
            """

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
            elif search_by == "College":
                sql += " WHERE c.name LIKE %s" 
            

            search_pattern = f"%{search_query}%" if search_by != "Gender" else search_query
            params = (search_pattern,)
        else:
            params = ()

        cursor.execute(sql, params)
        total_students = cursor.fetchone()[0]
        cursor.close()

        return total_students

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
