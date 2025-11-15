'''Дан неориентированный граф. Над ним в заданном порядке производится два типа 
операций: cut – удалить ребро из графа; ask – проверить в одной ли компоненте связности 
лежат две вершины. Известно, что после выполнения всех операций типа cut рёбер в графе не 
осталось. Найдите результат выполнения каждой из операций типа ask.

Формат ввода
Первая строка содержит три целых числа, разделённых пробелами – количество вершин 
графа n, количество рёбер m и количество операций k (1 ≤ n ≤ 20000, 0 ≤ m ≤ 50000, m ≤ k ≤ 100000).

Следующие m строк задают рёбра графа. Вершины нумеруются с единицы.

Далее следует k строк, описывающих операции. Операция типа cut задаётся строкой 
“cut u v” (1 ≤ u, v ≤ n), которая означает. что из графа удаляют ребро между вершинами 
u и v. Операция типа ask задаётся строкой “ask u v” (1 ≤ u, v ≤ n), которая вопрошает, 
лежат ли в данный момент вершины u и v в одной компоненте связности. Гарантируется, что 
каждое ребро графа встретится в операциях типа cut ровно один раз.

Формат вывода
Для каждой операции ask в порядке их вызова выведите в отдельной строке слово “YES”, 
если две указанные вершины лежат в одной компоненте связности, и “NO” в противном случае.'''


n, m, k = map(int, input().split())
edges = []
for _ in range(m):
    u, v = map(int, input().split())
    edges.append((u, v))
ops = []
for _ in range(k):
    parts = input().split()
    ops.append((parts[0], int(parts[1]), int(parts[2])))
parent = [i for i in range(n + 1)]
def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]
def union(x, y):
    x_root = find(x)
    y_root = find(y)
    if x_root != y_root:
        parent[y_root] = x_root
edge_set = set()
for u, v in edges:
    if u > v:
        u, v = v, u
    edge_set.add((u, v))
result = []
for op in reversed(ops):
    if op[0] == 'cut':
        u, v = op[1], op[2]
        if u > v:
            u, v = v, u
        if (u, v) in edge_set:
            edge_set.remove((u, v))
        union(u, v)
    else:
        u, v = op[1], op[2]
        if find(u) == find(v):
            result.append("YES")
        else:
            result.append("NO")
for ans in reversed(result):
    print(ans)