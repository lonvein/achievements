'''Мэр города хочет провести локальную городскую сеть для использования в экстренных
ситуациях в случае серьезных бедствий, когда город будет отрезан от внешнего мира. Некоторые
пары зданий в городе могут быть напрямую связаны интернет-проводом. Инженеры подготовили 
оценку стоимости подключения любой такой пары.

Мэр, безусловно, хочет построить самую дешевую сеть, соединяющую все здания в городе
и удовлетворяющую мерам эффективности и безопасности: связь здания A с другим зданием B
должна совершаться по простому пути (который не содержит повторяющихся зданий). Существует
несколько зданий, в которых проживают хакеры, способные перехватывать данные, идущие по сети
через их дом. Эти здания тоже нужно подключить к сети, но они не должны участвовать в
маршрутизации -- никакое соединение между зданиями A и B не должно проходить через небезопасное
здание C в сети (C отлично от A и B).

Формат ввода
Первая строка содержит три целых числа n, m, p, где n (1 ≤ n ≤ 1000) – количество домов, m (0 ≤ m ≤ 10^5)
– количество возможных прямых соединений между парами домов, а p (0 ≤ p ≤ n) – количество небезопасных зданий
. Здания пронумерованы от 1 до n. Вторая строка содержит p различных целых чисел от 1 до n (включительно)
– номера небезопасных зданий. Каждая из следующих m строк содержит три целых числа xi, yi и li описывающих
одну потенциальную прямую линию, где xi и yi (1 ≤ xi, yi ≤ n) – различные номера зданий, которые она соединяет
, а li (1 ≤ li ≤ 10000) – стоимость соединения этих зданий. Между любыми двумя зданиями существует не более 
одного прямого соединения.

Формат вывода
Выведите стоимость самой дешевой сети, удовлетворяющей по возможности 
условиям безопасности. Иначе выведите “impossible”.'''



def main():
    import sys
    input = sys.stdin.read().split()
    ptr = 0 
    n = int(input[ptr])
    ptr += 1
    m = int(input[ptr])
    ptr += 1
    p = int(input[ptr])
    ptr += 1
    unsafe = set()
    if p > 0:
        unsafe = set(map(int, input[ptr:ptr + p]))
        ptr += p
    edges = []
    for _ in range(m):
        x = int(input[ptr])
        ptr += 1
        y = int(input[ptr])
        ptr += 1
        l = int(input[ptr])
        ptr += 1
        edges.append((l, x, y))
    safe_edges = []
    unsafe_edges = []
    for l, x, y in edges:
        if x not in unsafe and y not in unsafe:
            safe_edges.append((l, x, y))
        else:
            unsafe_edges.append((l, x, y))
    safe_edges.sort()
    unsafe_edges.sort()
    parent = [i for i in range(n + 1)]
    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u
    def union(u, v):
        u_root = find(u)
        v_root = find(v)
        if u_root != v_root:
            parent[v_root] = u_root
    mst_cost = 0
    safe_nodes = set(range(1, n + 1)) - unsafe
    if not safe_nodes:
        all_edges = sorted(edges)
        parent_all = [i for i in range(n + 1)]
        def find_all(u):
            while parent_all[u] != u:
                parent_all[u] = parent_all[parent_all[u]]
                u = parent_all[u]
            return u
        total_cost = 0
        count = 0
        for l, x, y in all_edges:
            x_root = find_all(x)
            y_root = find_all(y)
            if x_root != y_root:
                parent_all[y_root] = x_root
                total_cost += l
                count += 1
                if count == n - 1:
                    break
        if count == n - 1:
            print(total_cost)
        else:
            print("impossible")
        return
    count_safe = 0
    for l, x, y in safe_edges:
        if find(x) != find(y):
            union(x, y)
            mst_cost += l
            count_safe += 1
    root = None
    for node in safe_nodes:
        if root is None:
            root = find(node)
        elif find(node) != root:
            print("impossible")
            return
    min_edge_for_unsafe = {}
    for l, x, y in unsafe_edges:
        if x in unsafe and y not in unsafe:
            if x not in min_edge_for_unsafe or l < min_edge_for_unsafe[x][0]:
                min_edge_for_unsafe[x] = (l, y)
        elif y in unsafe and x not in unsafe:
            if y not in min_edge_for_unsafe or l < min_edge_for_unsafe[y][0]:
                min_edge_for_unsafe[y] = (l, x)
    if len(min_edge_for_unsafe) != len(unsafe):
        print("impossible")
        return
    for u in unsafe:
        l, y = min_edge_for_unsafe[u]
        if find(u) != find(y):
            union(u, y)
            mst_cost += l
        else:
            pass
    root = None
    for node in range(1, n + 1):
        if root is None:
            root = find(node)
        elif find(node) != root:
            print("impossible")
            return
    print(mst_cost)
main()