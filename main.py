"""
Это главный модуль бюджетного помощника.
Он содержит консольный интерфейс для взаимодействия с пользователем.
"""

from budget_assistant import BudgetAssistant

def main():
    """
        Главная функция программы.
        Реализует основной цикл консольного интерфейса бюджетного помощника.
        Предоставляет пользователю меню со следующими опциями:
            1. добавить расход
            2. сумма за период
            3. день с максимальным расходом
            4. категории по сумме трат (сортировка вставками)
            5. отменить последнюю операцию
            6. показать все транзакции (обход дерева)
            7. выход
        """
    app = BudgetAssistant()

    while True:
        # Вывод меню
        print("\n Бюджетный помощник ")
        print("1. Добавить расход")
        print("2. Сумма за период")
        print("3. День с максимальным расходом")
        print("4. Категории по сумме трат (сортировка вставками)")
        print("5. Отменить последнюю операцию")
        print("6. Показать все транзакции (обход дерева)")
        print("7. Выход")
        choice = input("Выберите действие: ")

        # обработка выбора пользователя
        if choice == '1':
            try:
                day = int(input("День (1-31): "))
                amount = float(input("Сумма: "))
                category = input("Категория: ")
                tid = app.add_expense(day, amount, category)
                print(f"Добавлено! id = {tid}")
            except Exception as e:
                print("Ошибка:", e)

        elif choice == '2':
            try:
                a = int(input("Начальный день: "))
                b = int(input("Конечный день: "))
                s = app.get_sum_period(a, b)
                print(f"Расходы с {a} по {b}: {s:.2f}")
            except Exception as e:
                print("Ошибка:", e)

        elif choice == '3':
            day, val = app.find_day_max_expense()
            print(f"День {day}, сумма {val:.2f}")

        elif choice == '4':
            sorted_cats = app.get_categories_sorted()
            if not sorted_cats:
                print("Нет данных")
            else:
                print("Категории (от больших трат к меньшим):")
                for cat, total in sorted_cats:
                    print(f"{cat}: {total:.2f}")

        elif choice == '5':
            if app.undo_last():
                print("Последняя операция отменена")

        elif choice == '6':
            transactions = app.bst.inorder_traversal()
            if not transactions:
                print("Транзакций пока нет")
            else:
                print("Все транзакции:")
                for tid, day, amount, category in transactions:
                    print(f"ID:{tid:3d} | День:{day:2d} | {amount:7.2f} | {category}")

        elif choice == '7':
            print("До свидания!")
            break
        else:
            print("Неверный ввод номера операции, выберите значение из перечня.")


if __name__ == "__main__":
    main()