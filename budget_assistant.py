"""
Этот модуль с основным классом бюджетного помощника.
Он реализует функционал учета расходов с использованием:
- префиксных сумм для быстрых запросов по диапазону дней
- стека для отмены последней операции
- бинарного дерева поиска для хранения транзакций
- сортировки вставками для категорий
"""
from bst import BinarySearchTree
from sort import insertion_sort

class BudgetAssistant:
    """
        Бюджетный помощник для учета ежедневных расходов.
        Он позволяет добавлять расходы, получать сумму за период,
        находить день с максимальными тратами, получать отсортированные категории,
        отменять последнюю операцию и выполнять поиск по дереву.
        Attributes:
            daily_expenses - массив расходов по дням (индексы 1-31)
            prefix_sums - массив префиксных сумм для быстрых запросов
            category_totals - словарь {категория: общая сумма}
            undo_stack - стек для отмены операций
            bst - дерево для хранения транзакций
            next_id - счетчик для генерации уникальных id транзакций
        """
    def __init__(self):
        """Функция инициализирует бюджетный помощник.
        Создает массивы для 31 дня (индексы 1-31, индекс 0 не используется),
        пустой стек отмен, пустое дерево и счётчик id начиная с 1.
        """
        self.daily_expenses = [0.0] * 32
        self.prefix_sums = [0.0] * 32
        self.category_totals = {}
        self.undo_stack = []
        self.bst = BinarySearchTree()
        self.next_id = 1

    def recalc_prefix_sums(self):
        """Функция Пересчитывает массив префиксных сумм за O(31).
        Префиксная сумма для дня i = сумма расходов за дни с 1 по i.
        Позволяет получать сумму за период [a, b] за O(1) по формуле:
        sum(a,b) = prefix_sums[b] - prefix_sums[a-1]
        Вызывается после каждого добавления или отмены операции.
        """
        for i in range(1, 32):
            # префиксная сумма = предыдущая префиксная сумма + расход за текущий день
            self.prefix_sums[i] = self.prefix_sums[i-1] + self.daily_expenses[i]

    def add_expense(self, day, amount, category):
        """Функция добавляет новый расход
        и возвращает уникальный идентификатор созданной транзакции.
        """
        # валидация входных данных
        if not (1 <= day <= 31) or amount <= 0:
            raise ValueError("День должен быть от 1 до 31, сумма > 0")

        # генерация уникального id
        tid = self.next_id
        self.next_id += 1

        # обновляем дневной расход
        self.daily_expenses[day] += amount
        # обновляем сумму по категории
        self.category_totals[category] = self.category_totals.get(category, 0) + amount
        # пересчитываем префиксные суммы
        self.recalc_prefix_sums()
        # добавляем узел в дерево
        self.bst.insert(tid, day, amount, category)
        # сохраняем в стек для возможной отмены
        self.undo_stack.append({
            'id': tid,
            'day': day,
            'amount': amount,
            'category': category
        })
        return tid

    def get_sum_period(self, a, b):
        """Функция вычисляет сумму расходов за период с дня a по день b.
        Использует префиксные суммы для ответа за O(1).
        Вовзвращает сумму расходов за указанный период.
        """
        if not (1 <= a <= b <= 31):
            raise ValueError("Некорректный период: a и b должны быть от 1 до 31, a <= b")
        return self.prefix_sums[b] - self.prefix_sums[a-1]

    def find_day_max_expense(self):
        """Функция находит день с максимальной суммой расходов.
        Использует линейный поиск по массиву daily_expenses.
        Возвращает кортеж (номер_дня, сумма_расходов) для дня с максимальными тратами.
        """
        # начинаем с первого дня
        max_day = 1
        max_val = self.daily_expenses[1]
       # линейный проход по всем дням
        for day in range(2, 32):
            if self.daily_expenses[day] > max_val:
                max_day = day
                max_val = self.daily_expenses[day]
        return max_day, max_val

    def get_categories_sorted(self):
        """Функция возвращает категории, отсортированные по убыванию суммы трат.
        Использует сортировку вставками (реализована вручную).
        """
        # преобразуем словарь в список пар (категория, сумма)
        items = list(self.category_totals.items())
        # сортируем вставками по убыванию суммы
        insertion_sort(items, key=lambda x: x[1], reverse=True)
        return items

    def undo_last(self):
        """Функция отменяет последнюю добавленную операцию.
        Восстанавливает состояние до последнего добавления:
        - удаляет транзакцию из дерева
        - уменьшает дневной расход
        - обновляет сумму по категории
        - пересчитывает префиксные суммы
        Возвращает True если операция отменена, False если стек пуст"""
        if not self.undo_stack:
            print("Операций для отмены не найдено, список транзакций пуст")
            return False

        # извлекаем последнюю операцию из стека
        last = self.undo_stack.pop()
        tid = last['id']
        day = last['day']
        amount = last['amount']
        category = last['category']

        # удаляем транзакцию из дерева
        self.bst.delete(tid)

        # откатываем изменения
        self.daily_expenses[day] -= amount
        self.category_totals[category] -= amount
        if self.category_totals[category] == 0:
            del self.category_totals[category]

        # пересчитываем префиксные суммы
        self.recalc_prefix_sums()
        return True