class ProgramModel:
    def __init__(self, db):
        self.db = db

    def get_programs(self, search_query=None, search_by=None):
        """Fetch all programs or programs matching a search query."""
        sql = "SELECT code, name, college FROM program"
        params = None

        if search_query and search_by:
            if search_by == "Program Code":
                sql += " WHERE code LIKE %s"
            elif search_by == "Program Name":
                sql += " WHERE name LIKE %s"
            elif search_by == "College Code":
                sql += " WHERE college LIKE %s"
            params = (f"%{search_query}%",)

        with self.db.cursor() as cursor:
            cursor.execute(sql, params) if params else cursor.execute(sql)
            return cursor.fetchall()

    def get_program(self, program_code):
        """Fetch a single program by its code."""
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT code, name, college FROM program WHERE code = %s",
                (program_code,)
            )
            return cursor.fetchone()

    def add_program(self, program_code, program_name, college_code):
        """Add a new program to the database."""
        sql = "INSERT INTO program (code, name, college) VALUES (%s, %s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql, (program_code, program_name, college_code))
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def update_program(self, program_code, new_program_code, program_name, college_code):
        """Update an existing program."""
        sql = """
            UPDATE program
            SET code = %s, name = %s, college = %s
            WHERE code = %s
        """
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    sql,
                    (new_program_code, program_name, college_code, program_code),
                )
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_program(self, program_code):
        """Delete a program by its code."""
        try:
            with self.db.cursor() as cursor:
                cursor.execute("DELETE FROM program WHERE code = %s", (program_code,))
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def program_exists(self, program_code):
        """Check if a program with the given code exists."""
        with self.db.cursor() as cursor:
            cursor.execute("SELECT code FROM program WHERE code = %s", (program_code,))
            return bool(cursor.fetchone())
