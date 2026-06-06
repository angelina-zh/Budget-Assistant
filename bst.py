"""
Этот модуль с реализацией бинарного дерева поиска для хранения транзакций. 
Ключом выступает id транзакции.
Узлы содержат день, сумму и категорию.
Он обеспечивает вставку, удаление и обход узлов в порядке возрастания ключей.
"""

class TreeNode:
    """Узел бинарного дерева поиска.
    Где:
        key - уникальный идентификатор транзакции (ключ для BST)
        day - день месяца (1-31)
        amount - сумма расхода
        category - категория расхода (строка)
        left - левый потомок (TreeNode или None)
        right - правый потомок (TreeNode или None)
        """

    def __init__(self, tid, day, amount, category):
        """"Функция инициализирует новый узел дерева"""
        self.key = tid          
        self.day = day
        self.amount = amount
        self.category = category
        self.left = None        
        self.right = None

def min_value_node(node):
    """Функция находит узел с минимальным ключом в поддереве
    и возвращает узел с наименьшим значением ключа.
    """
    current = node
    while current.left is not None:
        current = current.left
    return current


class BinarySearchTree:
    """Бинарное дерево поиска для хранения транзакций по id.
    Оно позволяет вставлять, удалять и выполнять обход узлов
    в порядке возрастания ключей.
    """
    def __init__(self):
        """Функция инициализирует пустое бинарное дерево поиска."""
        self.root = None

    def insert(self, tid, day, amount, category):
        """Функция добавляет новую транзакцию в дерево.
        Если дерево пустое, то создает корневой узел.
        Иначе рекурсивно находит подходящее место для вставки.
        """
        if self.root is None:
            # дерево пустое - создаем корень
            self.root = TreeNode(tid, day, amount, category)
        else:
            # рекурсивно вставляем в подходящее место
            self.insert_recursive(self.root, tid, day, amount, category)

    def insert_recursive(self, node, tid, day, amount, category):
        """Функция рекурсивно вставляет новый узел в поддерево."""
        if tid < node.key:
            # если новый ключ меньше - идем в левое поддерево
            if node.left is None:
                node.left = TreeNode(tid, day, amount, category)
            else:
                self.insert_recursive(node.left, tid, day, amount, category)
        elif tid > node.key:
            # если новый ключ больше - идем в правое поддерево
            if node.right is None:
                node.right = TreeNode(tid, day, amount, category)
            else:
                self.insert_recursive(node.right, tid, day, amount, category)
        # если tid равен ключу – ничего не делаем, id уникальны

    def delete(self, tid):
        """Функция удаляет транзакцию с указанным id из дерева."""
        self.root = self.delete_recursive(self.root, tid)

    def delete_recursive(self, node, tid):
        """Функуия рекурсивно удаляет узел с указанным ключом из поддерева
        и возвращает новый корень поддереав после удаления.
        Алгоритм:
            1. если узел None - ничего не делаем
            2. если ключ меньше - рекурсивно удаляем из левого поддерева
            3. если ключ больше - рекурсивно удаляем из правого поддерева
            4. если нашли узел для удаления:
               - если нет левого потомка - возвращаем правого
               - если нет правого потомка - возвращаем левого
               - если есть оба потомка - находим минимальный узел в правом
                 поддереве, копируем его данные в текущий узел и удаляем его
                 """
        if node is None:
            return None
        if tid < node.key:
            node.left = self.delete_recursive(node.left, tid)
        elif tid > node.key:
            node.right = self.delete_recursive(node.right, tid)
        else:
            # узел найден
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # два потомка, из них ищем минимальный в правом поддереве
                min_node = min_value_node(node.right)
                node.key = min_node.key
                node.day = min_node.day
                node.amount = min_node.amount
                node.category = min_node.category
                node.right = self.delete_recursive(node.right, min_node.key)
        return node

    def inorder_traversal(self):
        """Функция выполняет симметричный обход дерева
        и возвращает список кортежей в порядке возрастания id транзакций.
        """
        result = []
        self.inorder_recursive(self.root, result)
        return result

    def inorder_recursive(self, node, result):
        """Функция рекурсивно выполняет симметричный обход поддерева."""
        if node:
            self.inorder_recursive(node.left, result)
            result.append((node.key, node.day, node.amount, node.category))
            self.inorder_recursive(node.right, result)