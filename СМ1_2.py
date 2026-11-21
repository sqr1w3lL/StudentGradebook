class Lesson:
    def __init__(self, date, time, subject, grade=None, present=False):
        self.date = date
        self.time = time
        self.subject = subject
        self.grade = grade
        self.present = present

    def show_info(self):
        print("--------------")
        print("Дата:", self.date)
        print("Час:", self.time)
        print("Предмет:", self.subject)
        print("Оцінка:", self.grade)
        print("Присутність:", self.present)
        print("--------------")


class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.lessons = []

    def add_lesson(self, lesson):
        self.lessons.append(lesson)


class Parent:
    def __init__(self, username, first_name, last_name, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.children = []

    def add_child(self, student):
        if student not in self.children:
            self.children.append(student)


class Teacher:
    def __init__(self, username, subject, password):
        self.username = username
        self.subject = subject
        self.password = password


students = {}
parents = {}
teachers = {}

users = {
    "admin": {"password": "admin", "role": "admin"}
}


def register():
    username = input("Логін: ")

    if username in users:
        print("Користувач вже існує\n")
        return

    password = input("Пароль: ")
    first_name = input("Ім'я: ")
    last_name = input("Прізвище: ")

    parents[username] = Parent(
        username,
        first_name,
        last_name,
        password
    )

    users[username] = {
        "password": password,
        "role": "parent"
    }

    print("Акаунт створено\n")


def login():
    username = input("Логін: ")
    password = input("Пароль: ")

    if username in users and users[username]["password"] == password:
        print("Вхід успішний\n")
        return users[username]["role"], username

    print("Помилка входу\n")
    return None, None


def add_student():
    student_id = input("ID учня: ")
    name = input("Ім'я: ")

    students[student_id] = Student(student_id, name)

    print("Учня додано\n")


def add_teacher():
    username = input("Логін вчителя: ")

    if username in users:
        print("Користувач вже існує\n")
        return

    subject = input("Предмет: ")
    password = input("Пароль: ")

    teachers[username] = Teacher(
        username,
        subject,
        password
    )

    users[username] = {
        "password": password,
        "role": "teacher"
    }

    print("Вчителя додано\n")


def add_parent_child():
    username = input("Логін батьків: ")

    if username not in parents:
        print("Батьків не знайдено\n")
        return

    while True:
        child_id = input("ID дитини (0 - вихід): ")

        if child_id == "0":
            break

        if child_id in students:
            parents[username].add_child(students[child_id])
            print("Дитину додано")
        else:
            print("Учня не знайдено")


def print_lessons(student, start_date=None, end_date=None, subject=None):
    filtered = []

    for lesson in student.lessons:

        if subject and lesson.subject != subject:
            continue

        if start_date and lesson.date < start_date:
            continue

        if end_date and lesson.date > end_date:
            continue

        filtered.append(lesson)

    filtered.sort(key=lambda lesson: lesson.date)

    for lesson in filtered:
        lesson.show_info()


def teacher_menu(username):
    teacher = teachers[username]

    while True:
        print("1 - Додати оцінку/відвідування")
        print("0 - Вийти")

        choice = input("Вибір: ")

        if choice == "1":

            student_id = input("ID учня: ")

            if student_id not in students:
                print("Учня не знайдено\n")
                continue

            date = input("Дата (YYYY-MM-DD): ")
            time = input("Час: ")

            print("1 - Оцінка")
            print("2 - Присутність")

            action = input("Вибір: ")

            if action == "1":
                grade = int(input("Оцінка: "))

                lesson = Lesson(
                    date,
                    time,
                    teacher.subject,
                    grade,
                    True
                )

            else:
                lesson = Lesson(
                    date,
                    time,
                    teacher.subject,
                    None,
                    True
                )

            students[student_id].add_lesson(lesson)

            print("Збережено\n")

        elif choice == "0":
            break


def parent_menu(username):
    parent = parents[username]

    while True:
        print("Перегляд успішності дітей\n")

        start_date = input("Дата від (YYYY-MM-DD або Enter): ")
        end_date = input("Дата до (YYYY-MM-DD або Enter): ")
        subject = input("Предмет (або Enter): ")

        start_date = start_date if start_date else None
        end_date = end_date if end_date else None
        subject = subject if subject else None

        for child in parent.children:
            print(f"\nДитина: {child.name}")

            print_lessons(
                child,
                start_date,
                end_date,
                subject
            )

        print("\n0 - Вийти")

        if input("Вибір: ") == "0":
            break


def admin_menu():
    while True:
        print("1 - Додати учня")
        print("2 - Прив'язати дитину до батьків")
        print("3 - Додати вчителя")
        print("0 - Вийти")

        choice = input("Вибір: ")

        if choice == "1":
            add_student()

        elif choice == "2":
            add_parent_child()

        elif choice == "3":
            add_teacher()

        elif choice == "0":
            break


teachers["Любов Роніна"] = Teacher(
    "Любов Роніна",
    "Математика",
    "111"
)

users["Любов Роніна"] = {
    "password": "111",
    "role": "teacher"
}


while True:
    print("1 - Реєстрація")
    print("2 - Вхід")
    print("0 - Вихід")

    choice = input("Вибір: ")

    if choice == "1":
        register()

    elif choice == "2":

        role, username = login()

        if role == "admin":
            admin_menu()

        elif role == "teacher":
            teacher_menu(username)

        elif role == "parent":
            parent_menu(username)

    elif choice == "0":
        break
