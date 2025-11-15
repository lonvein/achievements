'''В индуизме считается, что в мире существуют три начала -- созидательное (представленное Брахмой), 
защитительное (представленное Вишну) и разрушительное (представленное Шивой). В предыдущих задачах 
вы реализовывали свое созидательное начало, а в этом вам предстоит почувствовать себя Шивой. Между 
каждой парой городов страны имеется прямая двусторонняя дорога. Вам надо уничтожить такое количество
дорог, чтобы образовалось хотя бы два города, проезд между которыми был бы невозможен. Поскольку вы
живете в Кали-юге, причина вам не нужна.

Вам известна стоимость уничтожения каждой дороги. Найти наименьшую стоимость, необходимую для совершения задуманного.

Формат ввода
В первой строке содержится t -- количество тестов. Первая строка каждого теста содержит 
количество n (n ≤ 50) городов в стране. Следующие n строк описывают дороги: j-ый символ 
i-ой строки является цифрой, задающей стоимость уничтожения дороги, ведущей из i-го города в j-ый.'''


t = input()
for _ in range(int(t)):
    n = int(input())
    co = [[0]*n for _ in range(n)]
    best = float('inf')
    cost = [[0]*n for _ in range(n)]
    for i in range(n):
        line = input().strip()
        for j in range(n):
            cost[i][j] = int(line[j])
    for i in range(n):
        for j in range(n):
            co[i][j] = cost[i][j]
    ver = list(range(n))
    for nothing in range(n-1):
        a ,A = 0, [ver[0]]
        subset = set(A)
        w = [0]*n
        for it in ver[1:]:
            w[it] = co[ver[0]][it]
        prev = ver[0]
        for _ in range(len(ver)-1):
            next_node = -1
            max_w = -1
            for it in ver:
                if it not in subset and w[it] > max_w:
                    max_w = w[it]
                    next_node = it
            if next_node == -1:
                next_node = ver[-1]
            A.append(next_node)
            subset.add(next_node)
            if len(A) == len(ver):
                break
            prev = next_node
            for it in ver:
                if it not in subset:
                    w[it] += co[next_node][it]
        s, t = A[-2], A[-1]
        current_cut, new_vertices = w[t], []
        best = min(best, current_cut)
        for v in ver:
            if v != t:
                new_vertices.append(v)
        ver = new_vertices
        for i in range(n):
            co[i][s] += co[i][t]
            co[s][i] += co[t][i]
        co[s][s] = 0
    print(best)
