class CollegeModel:
    def __init__(self, db):
        self.db = db

    def get_colleges(self):
        """Fetch all colleges."""
        with self.db.cursor() as cursor:
            cursor.execute("SELECT code, name FROM college")
            colleges = cursor.fetchall()
        return colleges

    def search_colleges(self, search_query, search_by):
        """Search colleges based on a query and search field."""
        sql = "SELECT code, name FROM college"
        params = None

        if search_query:
            if search_by == "College Code":
                sql += " WHERE code LIKE %s"
            elif search_by == "College Name":
                sql += " WHERE name LIKE %s"
            params = (f"%{search_query}%",)

        with self.db.cursor() as cursor:
            cursor.execute(sql, params)
            colleges = cursor.fetchall()
        return colleges

    def insert_college(self, code, name):
        """Insert a new college."""
        try:
            with self.db.cursor() as cursor:
                cursor.execute("INSERT INTO college (code, name) VALUES (%s, %s)", (code, name))
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error inserting college: {e}")
            return False

    def update_college(self, old_code, new_code, name):
        """Update an existing college."""
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    "UPDATE college SET code=%s, name=%s WHERE code=%s",
                    (new_code, name, old_code)
                )
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error updating college: {e}")
            return False

    def delete_college(self, code):
        """Delete a college by code."""
        try:
            with self.db.cursor() as cursor:
                cursor.execute("DELETE FROM college WHERE code = %s", (code,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(f"Error deleting college: {e}")

    def fetch_college_by_code(self, code):
        """Fetch a college by its code."""
        with self.db.cursor() as cursor:
            cursor.execute("SELECT code, name FROM college WHERE code = %s", (code,))
            college = cursor.fetchone()
        if college:
            return {"code": college[0], "name": college[1]}
        return None

    def college_exists(self, code):
        """Check if a college exists by code."""
        with self.db.cursor() as cursor:
            cursor.execute("SELECT code FROM college WHERE code = %s", (code,))
            return cursor.fetchone() is not None
