import sqlite3
from PyQt5.QtGui import QStandardItem
import pandas as pd


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Administrator (
            ID       INTEGER PRIMARY KEY ASC AUTOINCREMENT,
            FullName TEXT    NOT NULL,
            Login    TEXT    NOT NULL,
            Password TEXT    NOT NULL
        );
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Curator (
            ID       INTEGER PRIMARY KEY ASC AUTOINCREMENT,
            FullName TEXT    NOT NULL,
            Login    TEXT    NOT NULL,
            Password TEXT    NOT NULL
        );
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Teacher (
            ID       INTEGER PRIMARY KEY ASC AUTOINCREMENT,
            FullName TEXT    NOT NULL,
            Login    TEXT    NOT NULL,
            Password TEXT    NOT NULL
        );
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Branch (
            ID         INTEGER PRIMARY KEY ASC AUTOINCREMENT,
            BranchName TEXT    NOT NULL
        );
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Student (
            ID       INTEGER PRIMARY KEY ASC AUTOINCREMENT,
            FullName TEXT    NOT NULL,
            Login    TEXT    NOT NULL,
            Password TEXT    NOT NULL,
            BranchID INTEGER,
            FOREIGN KEY (
                BranchID
            )
            REFERENCES Branch (ID) 
        );
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS "Group" (
            ID             INTEGER PRIMARY KEY ASC AUTOINCREMENT,
            Name           TEXT    NOT NULL,
            CuratorID      INTEGER,
            DateOfCreation TEXT    DEFAULT (strftime('%d-%m-%Y', 'now') ),
            FOREIGN KEY (CuratorID)
                REFERENCES Curator (ID)
                ON DELETE CASCADE
        );

        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS GroupTeacher (
            ID        INTEGER PRIMARY KEY ASC AUTOINCREMENT,
            GroupID   INTEGER REFERENCES [Group] (ID) ON DELETE CASCADE
                                                    ON UPDATE CASCADE,
            TeacherID INTEGER REFERENCES Teacher (ID) ON DELETE CASCADE
                                                    ON UPDATE CASCADE,
            FOREIGN KEY (
                GroupID
            )
            REFERENCES [Group] (ID),
            FOREIGN KEY (
                TeacherID
            )
            REFERENCES Teacher (ID) 
        );
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS GroupStudent (
            ID        INTEGER PRIMARY KEY ASC AUTOINCREMENT,
            GroupID   INTEGER REFERENCES [Group] (ID) ON DELETE CASCADE
                                                    ON UPDATE CASCADE,
            StudentID INTEGER REFERENCES Student (ID) ON DELETE CASCADE
                                                    ON UPDATE CASCADE,
            FOREIGN KEY (
                GroupID
            )
            REFERENCES [Group] (ID),
            FOREIGN KEY (
                StudentID
            )
            REFERENCES Student (ID) 
        );
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Test (
            ID           INTEGER PRIMARY KEY ASC AUTOINCREMENT,
            TeacherID    INTEGER,
            GroupID      INTEGER,
            Name         TEXT    NOT NULL,
            AttemptCount INTEGER,
            DateAdded    TEXT,
            TimeTakeTest INTEGER NOT NULL
                                DEFAULT (strftime('%d-%m-%Y', 'now') ),
            FOREIGN KEY (
                TeacherID
            )
            REFERENCES Teacher (ID),
            FOREIGN KEY (
                GroupID
            )
            REFERENCES [Group] (ID) 
        );
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS TestContent (
            ID INTEGER PRIMARY KEY,
            TestID INTEGER,
            Question TEXT NOT NULL,
            Answers TEXT NOT NULL,
            CorrectAnswer TEXT NOT NULL,
            FOREIGN KEY (TestID) REFERENCES Test(ID)
        );
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS TestResult (
            ID INTEGER PRIMARY KEY,
            TestID INTEGER,
            StudentID INTEGER,
            CorrectAnswerCount INTEGER,
            CorrectAnswerPercent INTEGER,
            TestTime TEXT,
            Grade TEXT,
            Attempt TEXT,
            FOREIGN KEY (TestID) REFERENCES Test(ID),
            FOREIGN KEY (StudentID) REFERENCES Student(ID)
        );
        ''')

        self.conn.commit()

    def verification_of_authorization(self, login, password):
        self.cur.execute(
            "SELECT * FROM Administrator WHERE Login = ? AND Password = ?", (login, password))
        user = self.cur.fetchone()
        if user:
            return user, 0

        self.cur.execute(
            "SELECT * FROM Teacher WHERE Login = ? AND Password = ?", (login, password))
        user = self.cur.fetchone()
        if user:
            return user, 2

        self.cur.execute(
            "SELECT * FROM Curator WHERE Login = ? AND Password = ?", (login, password))
        user = self.cur.fetchone()
        if user:
            return user, 1

        self.cur.execute(
            "SELECT * FROM Student WHERE Login = ? AND Password = ?", (login, password))
        user = self.cur.fetchone()
        if user:
            return user, 3

    def add_user(self, name, login, password, role, table):
        self.cur.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT Login FROM Administrator WHERE Login=?
                UNION ALL
                SELECT Login FROM Curator WHERE Login=?
                UNION ALL
                SELECT Login FROM Teacher WHERE Login=?
            ) AS AllLogins
        """, (login, login, login))

        count = self.cur.fetchone()[0]
        if count > 0:
            return False
        else:
            if role == 0:
                self.cur.execute(
                    "INSERT INTO Administrator (FullName, Login, Password) VALUES (?, ?, ?)", (name, login, password))
                self.conn.commit()

                self.populate_treeview(table, role)

            if role == 1:
                self.cur.execute(
                    "INSERT INTO Curator (FullName, Login, Password) VALUES (?, ?, ?)", (name, login, password))
                self.conn.commit()

                self.populate_treeview(table, role)

            if role == 2:
                self.cur.execute(
                    "INSERT INTO Teacher (FullName, Login, Password) VALUES (?, ?, ?)", (name, login, password))
                self.conn.commit()

                self.populate_treeview(table, role)

        return True

    def add_student(self, name, login, password, branch, table, role):
        self.cur.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT Login FROM Student WHERE Login=?
            ) AS AllLogins
        """, (login,))

        count = self.cur.fetchone()[0]
        if count > 0:
            return False
        else:
            self.cur.execute(
                "INSERT INTO Student (FullName, Login, Password, BranchID) VALUES (?, ?, ?, ?)", (name, login, password, branch))
            self.conn.commit()

            self.populate_treeview(table, role)

        return True

    def delete_user(self, user_id, role, tree):
        try:
            if role == 0:
                self.cur.execute(
                    "DELETE FROM Administrator WHERE ID=?", (user_id,))
                self.conn.commit()

                self.populate_treeview(tree.model().sourceModel(), role)

                return True
            if role == 1:
                self.cur.execute(
                    "DELETE FROM Curator WHERE ID=?", (user_id,))
                self.conn.commit()

                self.populate_treeview(tree.model().sourceModel(), role)

                return True
            if role == 2:
                self.cur.execute(
                    "DELETE FROM Teacher WHERE ID=?", (user_id,))
                self.conn.commit()

                self.populate_treeview(tree.model().sourceModel(), role)

                return True
            if role == 3:
                self.cur.execute(
                    "DELETE FROM Student WHERE ID=?", (user_id,))
                self.conn.commit()

                self.populate_treeview(tree.model().sourceModel(), role)

                return True
        except sqlite3.Error as e:
            print("Ошибка удаления пользователя:", e)
            return False

    def add_group(self, name, curator_id, model):
        try:
            self.cur.execute("INSERT INTO [Group] (Name, CuratorID) VALUES (?, ?)",
                             (name, curator_id))
            self.conn.commit()

            self.populate_treeview_group(model)

            return True
        except sqlite3.Error as e:
            print(f"Error adding group: {e}")
            return False

    def get_all_curators(self):
        try:
            self.cur.execute("SELECT ID, FullName FROM Curator")
            curators = self.cur.fetchall()
            return curators
        except sqlite3.Error as e:
            print(f"Error fetching curators: {e}")
            return []

    def add_student_to_group(self, group_id, user_id, model, code):
        if code == 0:
            self.cur.execute(
                "SELECT * FROM GroupTeacher WHERE GroupID = ? AND TeacherID = ?", (group_id, user_id))
            result = self.cur.fetchone()
            if result is None:
                self.cur.execute(
                    "INSERT INTO GroupTeacher (GroupID, TeacherID) VALUES (?, ?)", (group_id, user_id))
                self.conn.commit()
                self.get_data_teachers_students_test(model, group_id, 0)

        if code == 1:
            self.cur.execute(
                "SELECT * FROM GroupStudent WHERE GroupID = ? AND StudentID = ?", (group_id, user_id))
            result = self.cur.fetchone()
            if result is None:
                self.cur.execute(
                    "INSERT INTO GroupStudent (GroupID, StudentID) VALUES (?, ?)", (group_id, user_id))
                self.conn.commit()
                self.get_data_teachers_students_test(model, group_id, 1)

    def remove_from_group(self, group_id, user_id, model, code):
        if code == 0:
            self.cur.execute(
                "DELETE FROM GroupTeacher WHERE GroupID = ? AND TeacherID = ?", (group_id, user_id))
            self.conn.commit()
            self.get_data_teachers_students_test(model, group_id, 0)

        if code == 1:
            self.cur.execute(
                "DELETE FROM GroupStudent WHERE GroupID = ? AND StudentID = ?", (group_id, user_id))
            self.conn.commit()
            self.get_data_teachers_students_test(model, group_id, 1)

    def import_users(self, file_path, role, table):
        data = pd.read_csv(file_path, header=None)
        table_name = {0: 'Administrator', 1: 'Curator',
                      2: 'Teacher', 3: 'Student'}.get(role, 'Users')
        for _, row in data.iterrows():
            user_data = row[0].split(';')
            existing_user = self.cur.execute(
                f"SELECT * FROM {table_name} WHERE Login = ?", (user_data[1],)).fetchone()
            if not existing_user:
                if role == 3:
                    branch_id = self.cur.execute(
                        f"SELECT ID FROM Branch WHERE BranchName = ?", (user_data[3],)).fetchone()[0]
                    self.cur.execute(f"INSERT INTO {table_name} (FullName, Login, Password, Branch) VALUES (?, ?, ?, ?)",
                                     (user_data[0], user_data[1], user_data[2], branch_id))
                else:
                    self.cur.execute(f"INSERT INTO {table_name} (FullName, Login, Password) VALUES (?, ?, ?)",
                                     (user_data[0], user_data[1], user_data[2]))
                self.conn.commit()
                self.populate_treeview(table.model().sourceModel(), role)

    def edit_user(self, name, login, password, role, table, user_id):
        self.cur.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT Login FROM Administrator WHERE Login=? AND ID<>?
                UNION ALL
                SELECT Login FROM Curator WHERE Login=? AND ID<>?
                UNION ALL
                SELECT Login FROM Teacher WHERE Login=? AND ID<>?
            ) AS AllLogins
        """, (login, user_id, login, user_id, login, user_id))

        user = self.cur.fetchone()

        if user[0] > 0:
            return False

        if role == 0:
            self.cur.execute(
                "UPDATE Administrator SET FullName=?, Login=?, Password=? WHERE ID=?", (name, login, password, user_id))
            self.conn.commit()

            self.populate_treeview(table, role)

        elif role == 1:
            self.cur.execute(
                "UPDATE Curator SET FullName=?, Login=?, Password=? WHERE ID=?", (name, login, password, user_id))
            self.conn.commit()

            self.populate_treeview(table, role)

        elif role == 2:
            self.cur.execute(
                "UPDATE Teacher SET FullName=?, Login=?, Password=? WHERE ID=?", (name, login, password, user_id))
            self.conn.commit()

            self.populate_treeview(table, role)

        return True

    def edit_student(self, fullname, login, password, branch_id, table, user_id):
        query = "UPDATE Student SET FullName = ?, Login = ?, Password = ?, BranchID = ? WHERE ID = ?"
        self.cur.execute(
            query, (fullname, login, password, branch_id, user_id))
        self.conn.commit()

        self.populate_treeview(table, role=3)

    def get_user_info(self, user_id, login, role):
        if role == 0:
            query = "SELECT FullName, Login, Password FROM Administrator WHERE ID = ? AND Login = ?"
        elif role == 1:
            query = "SELECT FullName, Login, Password FROM Curator WHERE ID = ? AND Login = ?"
        elif role == 2:
            query = "SELECT FullName, Login, Password FROM Teacher WHERE ID = ? AND Login = ?"
        elif role == 3:
            query = "SELECT FullName, Login, Password, BranchID FROM Student WHERE ID = ? AND Login = ?"

            self.cur.execute(query, (user_id, login))
            user_info = self.cur.fetchone()

            if user_info:
                return {'name': user_info[0], 'login': user_info[1], 'password': user_info[2], 'branch': user_info[3]}
            else:
                return

        self.cur.execute(query, (user_id, login))
        user_info = self.cur.fetchone()

        if user_info:
            return {'name': user_info[0], 'login': user_info[1], 'password': user_info[2]}
        else:
            return None

    def get_all_branches(self):
        self.cur.execute("SELECT ID, BranchName FROM Branch")
        branches = self.cur.fetchall()
        return branches

    def get_user(self, role):
        if role == 0:
            users = self.cur.execute("SELECT * FROM Administrator")

            return users

    def populate_treeview_group(self, model):
        model.removeRows(0, model.rowCount())

        self.cur.execute("""SELECT "Group".ID, "Group".Name, Curator.FullName, "Group".DateOfCreation
                            FROM "Group"
                            INNER JOIN Curator ON "Group".CuratorID = Curator.ID""")
        rows = self.cur.fetchall()
        for row in rows:
            items = [QStandardItem(str(field)) for field in row]
            model.appendRow(items)

    def populate_treeview(self, model, role):
        model.clear()

        if role == 0:
            self.cur.execute(
                "SELECT ID, FullName, Login, Password FROM Administrator")
            model.setHorizontalHeaderLabels(["ID", "Имя", "Логин", "Пароль"])
        elif role == 1:
            self.cur.execute(
                "SELECT ID, FullName, Login, Password FROM Curator")
            model.setHorizontalHeaderLabels(["ID", "Имя", "Логин", "Пароль"])
        elif role == 2:
            self.cur.execute(
                "SELECT ID, FullName, Login, Password FROM Teacher")
            model.setHorizontalHeaderLabels(["ID", "Имя", "Логин", "Пароль"])
        elif role == 3:
            self.cur.execute("""
                        SELECT Student.ID, Student.FullName, Student.Login, Student.Password, Branch.BranchName
                        FROM Student
                        INNER JOIN Branch ON Student.BranchID = Branch.ID
                    """)
            model.setHorizontalHeaderLabels(
                ["ID", "Имя", "Логин", "Пароль", "Филиал"])

        users = self.cur.fetchall()

        for user in users:
            items = [QStandardItem(str(field)) for field in user]
            model.appendRow(items)  

    def update_group(self, group_id, groupname, curator_id, model):
        try:
            self.cur.execute("""
                UPDATE [Group]
                SET Name = ?, CuratorID = ?
                WHERE ID = ?
            """, (groupname, curator_id, group_id))
            self.conn.commit()

            self.populate_treeview_group(model)

            return True
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return False

    def get_curator_id_for_group(self, group_id):
        self.cur.execute(
            "SELECT CuratorID FROM [Group] WHERE ID = ?", (group_id,))
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            return None

    def delete_group(self, group_id, model):
        self.cur.execute("DELETE FROM 'Group' WHERE ID = ?", (group_id,))
        self.conn.commit()

        self.populate_treeview_group(model)

    def get_data_teachers_students_test(self, model, group_id, code):
        model.removeRows(0, model.rowCount())

        if code == 0:
            self.cur.execute("""
                SELECT Teacher.ID, Teacher.FullName, Teacher.Login
                FROM Teacher
                INNER JOIN GroupTeacher ON Teacher.ID = GroupTeacher.TeacherID
                WHERE GroupTeacher.GroupID = ?
            """, (group_id,))
            teachers = self.cur.fetchall()

            for teacher in teachers:
                items = [QStandardItem(str(field)) for field in teacher]
                model.appendRow(items)

        elif code == 1:
            self.cur.execute("""
                SELECT Student.ID, Student.FullName, Student.Login, Student.Password, Branch.BranchName
                FROM Student
                INNER JOIN GroupStudent ON Student.ID = GroupStudent.StudentID
                INNER JOIN Branch ON Student.BranchID = Branch.ID
                WHERE GroupStudent.GroupID = ?
            """, (group_id,))

            students = self.cur.fetchall()

            for student in students:
                items = [QStandardItem(str(field)) for field in student]
                model.appendRow(items)

        elif code == 2:
            if group_id == -1:
                self.cur.execute("""
                    SELECT Test.ID, Teacher.FullName, 'Group'.Name, Test.Name, Test.AttemptCount, Test.TimeTakeTest, Test.DateAdded
                    FROM Test
                    INNER JOIN Teacher ON Test.TeacherID = Teacher.ID
                    INNER JOIN 'Group' ON Test.GroupID = 'Group'.ID
                """)
            else:
                self.cur.execute("""
                    SELECT Test.ID, Teacher.FullName, 'Group'.Name, Test.Name, Test.AttemptCount, Test.TimeTakeTest, Test.DateAdded
                    FROM Test
                    INNER JOIN Teacher ON Test.TeacherID = Teacher.ID
                    INNER JOIN 'Group' ON Test.GroupID = 'Group'.ID
                    WHERE Test.GroupID = ?
                """, (group_id,))

            tests = self.cur.fetchall()

            for test in tests:
                items = [QStandardItem(str(field)) for field in test]
                model.appendRow(items)

    def fill_list(self, list, code):
        if code == 0:
            self.cur.execute("SELECT * FROM Teacher")
        elif code == 1:
            self.cur.execute("SELECT * FROM Student")

        data = self.cur.fetchall()

        for i in range(len(data)):
            item_text = ' / '.join(str(value) for value in data[i])
            list.insertItem(i, item_text)

    def get_all_teachers(self):
        self.cur.execute("SELECT ID, FullName FROM Teacher")
        teacher = self.cur.fetchall()
        return teacher

    def get_all_groups(self):
        self.cur.execute("SELECT ID, Name FROM 'Group'")
        group = self.cur.fetchall()
        return group

    def get_ud_group(self, name_group):
        self.cur.execute("SELECT ID FROM 'Group' WHERE Name = ?", (name_group,))
        
        data = self.cur.fetchall()
        
        for d in data:
            listr = []
            listr.append(d)
        
        return listr

    def add_test(self, teacher_id, group_id, name, attempts, time, model):
        self.cur.execute("""
        INSERT INTO Test (TeacherID, GroupID, Name, AttemptCount, TimeTakeTest, DateAdded)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
        """, (teacher_id, group_id, name, attempts, time))
        
        self.conn.commit()
        self.get_data_teachers_students_test(model, group_id, 2)

    def delete_test_group(self, id_test, model, id_group):
        self.cur.execute("DELETE FROM Test WHERE ID = ?", (id_test,))
        self.conn.commit()
        self.get_data_teachers_students_test(model, id_group, 2)
        