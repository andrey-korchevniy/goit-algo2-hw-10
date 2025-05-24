# Визначення класу Teacher
class Teacher:
    def __init__(self, first_name, last_name, age, email, can_teach_subjects):
        """
        Initialize Teacher object with personal info and teaching capabilities.
        
        Args:
            first_name (str): Teacher's first name
            last_name (str): Teacher's last name
            age (int): Teacher's age
            email (str): Teacher's email address
            can_teach_subjects (set): Set of subjects teacher can teach
        """
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.can_teach_subjects = can_teach_subjects
        self.assigned_subjects = set()  # Subjects assigned to this teacher
    
    def __str__(self):
        """String representation of the teacher"""
        return f"{self.first_name} {self.last_name} ({self.age} years)"
    
    def __repr__(self):
        """Detailed representation of the teacher"""
        return f"Teacher({self.first_name} {self.last_name}, {self.age}, {self.email}, {self.can_teach_subjects})"


def create_schedule(subjects, teachers):
    """
    Create class schedule using greedy algorithm for set cover problem.
    
    Algorithm:
    1. Start with empty schedule and full set of uncovered subjects
    2. At each step, choose teacher who can cover the most uncovered subjects
    3. If multiple candidates, choose youngest by age
    4. Assign all subjects this teacher can teach from uncovered subjects
    5. Remove covered subjects from uncovered set
    6. Repeat until all subjects covered or no teachers can cover remaining subjects
    
    Args:
        subjects (set): Set of all subjects that need to be covered
        teachers (list): List of Teacher objects
        
    Returns:
        list: List of teachers with assigned subjects, or None if impossible to cover all subjects
    """
    # Make copies to avoid modifying original data
    uncovered_subjects = subjects.copy()
    available_teachers = [teacher for teacher in teachers]
    selected_teachers = []
    
    # Reset assigned subjects for all teachers
    for teacher in available_teachers:
        teacher.assigned_subjects = set()
    
    print("Початковий стан:")
    print(f"Предмети для покриття: {uncovered_subjects}")
    print(f"Доступні викладачі: {len(available_teachers)}")
    print("-" * 50)
    
    step = 1
    
    while uncovered_subjects:
        print(f"Крок {step}:")
        print(f"Непокриті предмети: {uncovered_subjects}")
        
        # Find teacher who can cover the most uncovered subjects
        best_teacher = None
        max_coverage = 0
        
        for teacher in available_teachers:
            # Calculate how many uncovered subjects this teacher can teach
            coverage = len(teacher.can_teach_subjects & uncovered_subjects)
            
            if coverage > max_coverage:
                max_coverage = coverage
                best_teacher = teacher
            elif coverage == max_coverage and coverage > 0:
                # If same coverage, choose younger teacher
                if teacher.age < best_teacher.age:
                    best_teacher = teacher
        
        # If no teacher can cover any uncovered subjects, schedule is impossible
        if best_teacher is None or max_coverage == 0:
            print(f"Неможливо покрити предмети: {uncovered_subjects}")
            return None
        
        # Assign subjects to the best teacher
        subjects_to_assign = best_teacher.can_teach_subjects & uncovered_subjects
        best_teacher.assigned_subjects = subjects_to_assign
        
        print(f"Обрано викладача: {best_teacher}")
        print(f"Призначені предмети: {subjects_to_assign}")
        
        # Remove covered subjects and used teacher
        uncovered_subjects -= subjects_to_assign
        available_teachers.remove(best_teacher)
        selected_teachers.append(best_teacher)
        
        print(f"Залишилося предметів: {len(uncovered_subjects)}")
        print("-" * 50)
        
        step += 1
    
    print("Розклад успішно створено!")
    return selected_teachers


def print_detailed_schedule(schedule):
    """Print detailed schedule information"""
    if not schedule:
        print("Розклад відсутній.")
        return
    
    print("\n" + "=" * 60)
    print("ДЕТАЛЬНИЙ РОЗКЛАД ЗАНЯТЬ")
    print("=" * 60)
    
    all_assigned_subjects = set()
    
    for i, teacher in enumerate(schedule, 1):
        print(f"\n{i}. {teacher.first_name} {teacher.last_name}")
        print(f"   Вік: {teacher.age} років")
        print(f"   Email: {teacher.email}")
        print(f"   Може викладати: {', '.join(sorted(teacher.can_teach_subjects))}")
        print(f"   Призначені предмети: {', '.join(sorted(teacher.assigned_subjects))}")
        all_assigned_subjects.update(teacher.assigned_subjects)
    
    print(f"\n" + "=" * 60)
    print(f"СТАТИСТИКА:")
    print(f"Загальна кількість викладачів у розкладі: {len(schedule)}")
    print(f"Покриті предмети: {', '.join(sorted(all_assigned_subjects))}")
    print(f"Кількість покритих предметів: {len(all_assigned_subjects)}")


def analyze_coverage(subjects, teachers):
    """Analyze if all subjects can be theoretically covered"""
    print("\nАНАЛІЗ ПОКРИТТЯ:")
    print("-" * 30)
    
    all_teachable_subjects = set()
    for teacher in teachers:
        all_teachable_subjects.update(teacher.can_teach_subjects)
    
    missing_subjects = subjects - all_teachable_subjects
    
    if missing_subjects:
        print(f"УВАГА! Предмети, які неможливо покрити: {missing_subjects}")
        return False
    else:
        print("УСПІХ! Теоретично всі предмети можуть бути покриті")
        return True


def test_impossible_schedule():
    """Test case where it's impossible to cover all subjects"""
    print("\n" + "=" * 60)
    print("ТЕСТ: НЕМОЖЛИВИЙ РОЗКЛАД")
    print("=" * 60)
    
    # Test with subjects that cannot be covered
    test_subjects = {'Математика', 'Фізика', 'Хімія', 'Астрономія', 'Геологія'}
    test_teachers = [
        Teacher("Тест", "Викладач1", 30, "test1@example.com", {'Математика'}),
        Teacher("Тест", "Викладач2", 35, "test2@example.com", {'Фізика', 'Хімія'}),
    ]
    
    print(f"Тестові предмети: {test_subjects}")
    print(f"Тестові викладачі: {len(test_teachers)}")
    
    # Аналіз покриття
    analyze_coverage(test_subjects, test_teachers)
    
    # Спроба створити розклад
    print("\nСпроба створення розкладу:")
    print("-" * 30)
    test_schedule = create_schedule(test_subjects, test_teachers)
    
    if test_schedule:
        print("Неочікувано: розклад створено!")
        print_detailed_schedule(test_schedule)
    else:
        print("Очікувано: неможливо створити повний розклад.")


if __name__ == '__main__':
    # Множина предметів
    subjects = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія'}
    
    # Створення списку викладачів
    teachers = [
        Teacher("Олександр", "Іваненко", 45, "o.ivanenko@example.com", 
                {'Математика', 'Фізика'}),
        Teacher("Марія", "Петренко", 38, "m.petrenko@example.com", 
                {'Хімія'}),
        Teacher("Сергій", "Коваленко", 50, "s.kovalenko@example.com", 
                {'Інформатика', 'Математика'}),
        Teacher("Наталія", "Шевченко", 29, "n.shevchenko@example.com", 
                {'Біологія', 'Хімія'}),
        Teacher("Дмитро", "Бондаренко", 35, "d.bondarenko@example.com", 
                {'Фізика', 'Інформатика'}),
        Teacher("Олена", "Гриценко", 42, "o.grytsenko@example.com", 
                {'Біологія'})
    ]
    
    print("СИСТЕМА СТВОРЕННЯ РОЗКЛАДУ ЗАНЯТЬ")
    print("=" * 60)
    print(f"Предмети для розподілу: {subjects}")
    print(f"Кількість викладачів: {len(teachers)}")
    
    # Аналіз можливості покриття
    can_cover_all = analyze_coverage(subjects, teachers)
    
    print("\n" + "=" * 60)
    print("СТВОРЕННЯ РОЗКЛАДУ ЖАДІБНИМ АЛГОРИТМОМ")
    print("=" * 60)
    
    # Виклик функції створення розкладу
    schedule = create_schedule(subjects, teachers)
    
    # Виведення розкладу
    if schedule:
        print("\nРозклад занять:")
        for teacher in schedule:
            print(f"{teacher.first_name} {teacher.last_name}, {teacher.age} років, email: {teacher.email}")
            print(f"   Викладає предмети: {', '.join(teacher.assigned_subjects)}\n")
        
        # Детальний розклад
        print_detailed_schedule(schedule)
        
        # Перевірка повноти покриття
        all_covered = set()
        for teacher in schedule:
            all_covered.update(teacher.assigned_subjects)
        
        if all_covered == subjects:
            print("\n[УСПІХ] Всі предмети успішно покриті!")
        else:
            uncovered = subjects - all_covered
            print(f"\n[ПОМИЛКА] Не покриті предмети: {uncovered}")
            
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")
        
        # Показати яких предметів не вистачає
        all_possible = set()
        for teacher in teachers:
            all_possible.update(teacher.can_teach_subjects)
        missing = subjects - all_possible
        if missing:
            print(f"Предмети без викладачів: {missing}")
    
    # Тест неможливого розкладу
    test_impossible_schedule() 