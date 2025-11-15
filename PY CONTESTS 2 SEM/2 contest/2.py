'''Дано множество точек на плоскости, соответствующих расположению электроопор.
Необходимо спроектировать подземную кабельную сеть минимальной стоимости, соединяющую все опоры,
при следующих условиях:

Кабели прокладываются строго по прямой между опорами.
Никакие два кабеля не должны пересекаться, кроме как в узлах.
Любые две опоры должны быть соединены либо напрямую, либо через другие опоры.
Стоимость прокладки кабеля определяется расстоянием между опорами.

Формат ввода
Состоит из нескольких тестов. В первой строке задается количество тестов t. Каждый тест
начинается количеством точек n (2 ≤ n ≤ 1000). Каждая из следующих n строк содержит два 
целых числа x и y (-1000 ≤ x, y ≤ 1000), где (x, y) – местоположения точек. Все точки различны.

Формат вывода
Для каждого теста в отдельной строке вывести одно действительное число, равное совокупной 
длине кабеля, достаточного для построения связной сети. Вывести это число с двумя знаками после запятой.'''


def primFindMST(matrix): # matrix = [[AA, AB, ...], [BA, BB, ...], ...]
    length = len(matrix)
    key = [float('inf')] * length
    p = [-1] * length
    key[0] = 0
    q = [True] * length
 
    for _ in range(length):
        min_key = float('inf')
        v = -1
        for i in range(length):
            if q[i] and key[i] < min_key:
                min_key = key[i]
                v = i
        q[v] = False
        for u in range(length):
            if q[u] and key[u] > matrix[v][u]:
                p[u] = v
                key[u] = matrix[v][u]
    print("{0:.2f}".format(sum(key)))


amount_of_tests = int(input())
for _ in range(amount_of_tests):
    amount_of_points = int(input())
    list_of_points = [0 for _ in range(amount_of_points)]
    for i in range(amount_of_points):
        some_point = list(map(int, input().split()))
        list_of_points[i] = some_point
    matrix = [[ ((list_of_points[i][0] - list_of_points[j][0])**2 + (list_of_points[i][1] - list_of_points[j][1])**2)**0.5  for j in range(amount_of_points)] for i in range(amount_of_points) ]
    primFindMST(matrix)
    
