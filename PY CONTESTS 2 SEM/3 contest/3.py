'''Для выведения новых видов несуразных существ уже знакомые вам нейросети решили заняться
генной инженерией. Одна из задач, которая перед ними встала -- обнаружение мутаций и сравнение
последовательностей ДНК. ДНК представляет из себя последовательность четырех нуклеотидов -- 
аденина, гуанина, цитозина и тимина. Мутация означает, что в конкретной позиции нуклеотид у
двух последовательностей будет отличаться. Ситуацию осложняет то, что редко когда получается
прочитать всю последовательность ДНК, поэтому исследуются "отрезки" ДНК и производится поиск
корреляций с различными циклическими сдвигами сравниваемых отрезков. Вам на вход приходит два
отрезка ДНК одинаковой длины M (M является степенью двойки). Вам необходимо максимальное количество
позиций, которые могут совпадать между двумя последовательностями.

Формат ввода
В первой строке входного файла записано одно число M(4≤М≤2**16), которое является степенью двойки.
Следующие две строки содержат ДНК, которые необходимо исследовать. Обе эти строки содержат ровно M символов,
каждый из которых – это одна из следующих латинских букв: 'A', 'C', 'G' или 'T' (они обозначают аденин,
цитозин, гуанин или тимин, соответственно).

Формат вывода
Вывести коэффициент совпадения -- максимальное число символов, которые будут 
совпадать между двумя последовательностями при каком-то циклическом сдвиге одной из них.'''





def my_exp(real, imag):
    # e^(a+bi) = e^a * (cos(b) + i*sin(b))
    e_real = 2.718281828459045 ** real
    return (e_real * my_cos(imag), e_real * my_sin(imag))
def my_cos(x):
    x = x % (2 * 3.141592653589793)
    term = 1.0
    sum = term
    for n in range(1, 15):
        term *= -x * x / ((2 * n - 1) * (2 * n))
        sum += term
    return sum
def complex_mult(a_real, a_imag, b_real, b_imag):
    return (a_real * b_real - a_imag * b_imag, a_real * b_imag + a_imag * b_real)
def complex_conj(real, imag):
    return (real, -imag)
def complex_div(real, imag, divisor):
    return (real / divisor, imag / divisor)
def my_sin(x):
    x = x % (2 * 3.141592653589793)
    term = x
    sum = term
    for n in range(1, 15):
        term *= -x * x / ((2 * n) * (2 * n + 1))
        sum += term
    return sum
def fast_fourier_transform(signal, inverse=False):
    N = len(signal)
    logN = 0
    while (1 << logN) < N:
        logN += 1
    for i in range(N):
        rev_i = 0
        tmp = i
        for _ in range(logN):
            rev_i = (rev_i << 1) | (tmp & 1)
            tmp >>= 1
        if i < rev_i:
            signal[i], signal[rev_i] = signal[rev_i], signal[i]
    current_size = 1
    while current_size < N:
        angle = -6.283185307179586 / (2 * current_size)
        if inverse:
            angle = -angle
        w_real, w_imag = my_exp(0, angle)
        for start in range(0, N, 2 * current_size):
            root_real, root_imag = 1.0, 0.0
            for offset in range(current_size):
                even_real, even_imag = signal[start + offset]
                odd_real, odd_imag = signal[start + offset + current_size]
                prod_real, prod_imag = complex_mult(root_real, root_imag, odd_real, odd_imag)
                signal[start + offset] = (even_real + prod_real, even_imag + prod_imag)
                signal[start + offset + current_size] = (even_real - prod_real, even_imag - prod_imag)
                root_real, root_imag = complex_mult(root_real, root_imag, w_real, w_imag)
        current_size *= 2
    if inverse:
        for i in range(N):
            signal[i] = complex_div(*signal[i], N)
    return signal
def count_matches(m):
    s = input().strip()
    t = input().strip()
    result, bases  = [0] * m, 'ACGT'
    for base in bases:
        s_bits = [(1.0 if c == base else 0.0, 0.0) for c in s]
        t_bits = [(1.0 if c == base else 0.0, 0.0) for c in t]
        ft_s = fast_fourier_transform(s_bits.copy())
        ft_t = fast_fourier_transform(t_bits.copy())
        cross = []
        for i in range(m):
            conj_real, conj_imag = complex_conj(*ft_t[i])
            cross.append(complex_mult(*ft_s[i], conj_real, conj_imag))
        inv_ft = fast_fourier_transform(cross, inverse=True)
        for i in range(m):
            result[i] += int(round(inv_ft[i][0]))
    return max(result)
print(count_matches(int(input())))