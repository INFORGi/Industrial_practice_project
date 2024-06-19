import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Administrator (
    ID INTEGER PRIMARY KEY,
    FullName TEXT NOT NULL,
    Login TEXT NOT NULL,
    Password TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Curator (
    ID INTEGER PRIMARY KEY,
    FullName TEXT NOT NULL,
    Login TEXT NOT NULL,
    Password TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Teacher (
    ID INTEGER PRIMARY KEY,
    FullName TEXT NOT NULL,
    Login TEXT NOT NULL,
    Password TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Branch (
    ID INTEGER PRIMARY KEY,
    BranchName TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Student (
    ID INTEGER PRIMARY KEY,
    FullName TEXT NOT NULL,
    Login TEXT NOT NULL,
    Password TEXT NOT NULL,
    Branch INTEGER,
    FOREIGN KEY (Branch) REFERENCES Branch(ID)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS `Group` (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    CuratorID INTEGER,
    FOREIGN KEY (CuratorID) REFERENCES Curator(ID)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS GroupTeacher (
    ID INTEGER PRIMARY KEY,
    GroupID INTEGER,
    MemberID INTEGER,
    FOREIGN KEY (GroupID) REFERENCES `Group`(ID),
    FOREIGN KEY (MemberID) REFERENCES Teacher(ID)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS GroupStudent (
    ID INTEGER PRIMARY KEY,
    GroupID INTEGER,
    MemberID INTEGER,
    FOREIGN KEY (GroupID) REFERENCES `Group`(ID),
    FOREIGN KEY (MemberID) REFERENCES Student(ID)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Test (
    ID INTEGER PRIMARY KEY,
    TeacherID INTEGER,
    GroupID INTEGER,
    Name TEXT NOT NULL,
    AttemptCount INTEGER,
    DateAdded TEXT,
    FOREIGN KEY (TeacherID) REFERENCES Teacher(ID),
    FOREIGN KEY (GroupID) REFERENCES `Group`(ID)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS TestContent (
    ID INTEGER PRIMARY KEY,
    TestID INTEGER,
    Question TEXT NOT NULL,
    Answers TEXT NOT NULL,
    CorrectAnswer TEXT NOT NULL,
    FOREIGN KEY (TestID) REFERENCES Test(ID)
);
''')

cursor.execute('''
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

conn.commit()
conn.close()
