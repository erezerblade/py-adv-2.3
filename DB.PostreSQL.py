import psycopg2 as pg

student1 = {
    "name": "Корво Аттано",
    "gpa": "6",
    "birth": "2016-06-22"
}
student2 = {
    "name": "Эцио Аудиторэ де Ферензе",
    "gpa": "9",
    "birth": "1633-07-24"
}
student3 = {
    "name": "Гаррет",
    "gpa": "8",
    "birth": "1733-07-24"
}


def create_db(): # создает таблицы
    cur.execute('''CREATE TABLE STUDENT
        (id SERIAL PRIMARY KEY NOT NULL,
        name VARCHAR(100) NOT NULL,
        gpa NUMERIC(10,2),
        birth TIMESTAMPTZ);
        ''')
    cur.execute('''CREATE TABLE COURSE
        (id SERIAL PRIMARY KEY NOT NULL,
        name VARCHAR(100) NOT NULL);
        ''')
    cur.execute('''CREATE TABLE COURSE_LISTING
        (id SERIAL PRIMARY KEY NOT NULL,
        student_id INT NOT NULL,
        course_id INT NOT NULL);
        ''')
    pass


def get_students(course_id): # возвращает студентов определенного курса
    cur.execute("SELECT student_id from COURSE_LISTING where course_id = %s", (course_id, ))
    rows = cur.fetchall()
    namelist = []
    for row in rows:
        cur.execute("SELECT name from STUDENT where id = %s", (row[0],))
        name = cur.fetchall()[0][0]
        namelist.append(name)
    return namelist


def add_students(course_id, students: dict): # создает студентов и записывает их на курс
    cur.execute("INSERT INTO STUDENT (name, gpa, birth) VALUES (%s, %s, %s)",
                (students.get('name'), students.get('gpa'), students.get('birth'), ))
    cur.execute("SELECT id from STUDENT where name = %s", (students.get('name'), ))
    stud_id = cur.fetchall()[0][0]
    cur.execute("INSERT INTO COURSE_LISTING (student_id, course_id) VALUES (%s, %s)", (stud_id, course_id, ))
    pass


def add_student(student: dict): # просто создает студента
    cur.execute("INSERT INTO STUDENT (name, gpa, birth) VALUES (%s, %s, %s)",
                (student.get('name'), student.get('gpa'), student.get('birth'), ))
    pass


def get_student(student_id): # возвращает просто студента
    cur.execute("SELECT * from STUDENT where id = %s", (student_id, ))
    for row in cur:
        print("ID =", row[0])
        print("NAME =", row[1])
        print("GPA =", row[2])
        print("BIRTH =", row[3], "\n")
    pass


if __name__ == '__main__':
    with pg.connect("dbname=postgres user=postgres password=1234") as conn:
        with conn.cursor() as cur:
            create_db()
