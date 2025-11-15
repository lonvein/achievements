'''
Как известно, древние люди тоже любили брейнрот-мемы и регулярно пополняли их
список такими представителями как сфинкс, химера, кентавр, ламмасу, цилинь и прочая.
Известен миф про сфинкса, которая приставала к ничего не подозревающим путникам с 
давно опостылевшей загадкой, и убивала тех, кто не мог ее отгадать. И лишь греческий 
царь Эдип отгадал загадку, вызвал у сфинкса экзистенциальный кризис после которого она 
сгинула с горы в пропасть.

Тралалеро Тралала пришел к вам с загадкой про строки.

Для 'a' и для любой строки из одного символа ОНО равно 1.
Для 'aa', 'bb' и так далее ОНО равно 2, а для 'ab' или 'ba' 3.
Для 'aaa' ОНО равно 3, для 'aba' равно 5, а для 'abc' равно 6.
Посчитайте ЕГО для произвольной строки.

Формат ввода
Дана строка S из строчных латинских символов. Ее длина не превосходит 5000 символов.

Формат вывода
Выведите ЕГО.
'''

a = input()

edges = [{}]
link = [-1]
len_ = [0]
last = 0
size = 1

def new_state():
    global edges, link, len_, size
    edges.append({})
    link.append(-1)
    len_.append(0)
    size += 1
    return size - 1

def clone(q):
    new = new_state()
    edges[new] = edges[q].copy()
    link[new] = link[q]
    len_[new] = len_[q]
    return new

def add_char(c):
    global last, edges, link, len_, size
    cur = new_state()
    len_[cur] = len_[last] + 1
    p = last
    while p != -1 and c not in edges[p]:
        edges[p][c] = cur
        p = link[p]
    if p == -1:
        link[cur] = 0
    else:
        q = edges[p][c]
        if len_[p] + 1 == len_[q]:
            link[cur] = q
        else:
            new = clone(q)
            len_[new] = len_[p] + 1
            link[new] = link[q]
            link[q] = new
            link[cur] = new
            current_p = p
            while current_p != -1 and edges[current_p].get(c) == q:
                edges[current_p][c] = new
                current_p = link[current_p]
    last = cur

for c in a:
    add_char(c)

result = 0
for i in range(1, size):
    result += len_[i] - len_[link[i]]
print(result)