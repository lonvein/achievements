'''Вам известно, что на шахматной доске вырезано несколько клеток, 
координаты которых вам заданы. Необходимо разместить наибольшее количество 
ладей на шахматной доске, чтобы они не атаковали друг друга. Ладья атакует 
те клетки шахматной доски, которые находятся в одной с ней горизонтали или
вертикали. Ладьи нельзя размещать на вырезанных квадратах, но ладья может атаковать 
через вырезанные квадраты.

Формат ввода
Состоит из нескольких тестов. Первая строка каждого теста содержит три целых числа:
ширина rows и длина cols (1 ≤ rows, cols ≤ 300) доски в клетках, а также количество 
вырезанных клеток cuts. Следующая строка содержит список (x, y) координат вырезанных 
клеток, разделенных пробелом. Список имеет вид x1 y1 x2 y2 x3 y3 ... xcuts ycuts. 
Известно, что 0 ≤ xi ≤ rows – 1, 0 ≤ yi ≤ cols – 1.

Формат вывода
Для каждого теста выведите в отдельной строке наибольшее количество ладей, 
которое можно расположить на доске так, чтобы они не били друг друга.'''

aaa = int(input())
for i in range(aaa):   
    rows, cols, cuts = map(int, input().split())
    cuts_data = list(map(int, input().split()))
    if cuts == 0:
        print(min(rows, cols))
    else:
        blocked = set()
        for i in range(0, len(cuts_data), 2):
            x = cuts_data[i]
            y = cuts_data[i + 1]
            blocked.add((x, y))
        graph = [[] for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                if (i, j) not in blocked:
                    graph[i].append(j)
        match_to_column = [-1] * cols
        result = 0
        def dfs(row, visited):
            for j in graph[row]:
                if not visited[j]:
                    visited[j] = True
                    if match_to_column[j] == -1 or dfs(match_to_column[j], visited):
                        match_to_column[j] = row
                        return True
            return False
        for i in range(rows):
            visited = [False] * cols
            if dfs(i, visited):
                result += 1
        print(result)
