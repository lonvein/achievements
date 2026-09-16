# achievements — Портфолио ML & Computer Vision проектов (Егор Карпунин, МФТИ)

![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white)
![C++](https://img.shields.io/badge/C%2B%2B-00599C?logo=c%2B%2B&logoColor=white)
![Computer Vision](https://img.shields.io/badge/Computer%20Vision-0A66C2)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?logo=opencv&logoColor=white)

Репозиторий содержит подборку практических проектов, учебно-исследовательских ML/CV-работ и алгоритмических решений: физически-обоснованная реконструкция изображений в рассеивающей среде, правило-ориентированный NLP-пайплайн для e-commerce и набор задач по алгоритмам/структурам данных.

---

## Навигация по репозиторию

```text
/
├── qoc(optics_mipt)/
│   ├── ai_studio_code.ipynb
│   ├── d1_0_d2_8.ipynb
│   ├── d1_0_d2_8_noise.ipynb
│   ├── d1_1_d2_8.ipynb
│   ├── learning_curves.png
│   ├── comparison_results.png
│   ├── noise_stability_comparison.png
│   ├── image.png
│   ├── Карпунин_Егор_ВПВ (1).pdf
│   └── data/MNIST/raw/...
├── e-commerce_rule_based_attributes/
│   └── Карпунин Егор Сергеевич. Data Scientis. Понимание запросов.pdf
└── PY CONTESTS 2 SEM/
    ├── 1 contest/
    │   ├── 1.py
    │   ├── 2.py
    │   └── 3.py
    ├── 2 contest/
    │   ├── 1.py
    │   ├── 2.py
    │   ├── 3.py
    │   └── 4.py
    └── 3 contest/
        ├── 1.py
        ├── 2.py
        └── 3.py
```

---

## Детальный разбор проектов

### 1) Численное моделирование и восстановление изображений через рассеивающую среду
**📁 /qoc(optics_mipt)**

**Задача и физико-математическая суть**  
Восстановление амплитудного изображения (MNIST-цифр) из спекл-картины после прохождения через случайный фазовый экран. Прямая задача моделируется волновой оптикой (Angular Spectrum Method), обратная задача — ill-posed phase retrieval с шумом и потерей фазовой информации.

**Архитектура и методы**  
- Физический движок: `propagate_asm`, генерация фазового экрана `generate_phase_screen`, фиксированный `STATIC_PHASE_MASK`.
- Параметры моделирования (из ноутбуков): `N=128`, `dx=4.0e-6`, `wavelength=532e-9`, `corr_len=12e-6`, `sigma_phi=1.5π`.
- Геометрии экспериментов:  
  - `d1_0_d2_8.ipynb`: `d1=0`, `d2=0.008`  
  - `d1_1_d2_8.ipynb`: `d1=0.001`, `d2=0.008`  
  - `ai_studio_code.ipynb`: `d1=0.001`, `d2=0.002`  
  - `d1_0_d2_8_noise.ipynb`: шумовой стресс-тест по SNR.
- Пайплайн датасета: синтетика на базе `torchvision.datasets.MNIST`, сборка выборок `X_train/Y_train` и `X_val/Y_val` (`3000` train, `500` val), `DataLoader(batch_size=32)`.
- Модель: U-Net (`DoubleConv`, encoder/decoder skip-connections).
- Функция потерь: гибрид `HybridLoss = α*MSE + (1-α)*(1-SSIM)`, `α=0.2`.
- Оптимизация: `Adam`, scheduler `ReduceLROnPlateau`, обучение `15` эпох.
- Базовый классический метод: `fienup_hio` (Hybrid Input-Output, 400–500 итераций).

**Метрики и результаты**  
- `ai_studio_code.ipynb`:  
  - финал обучения: `Train Loss 0.02516`, `Val Loss 0.03869`;  
  - пример: `U-Net SSIM=0.9679, MSE=0.00144` vs `HIO SSIM=0.0244, MSE=0.08389`;  
  - среднее (подвыборка): `U-Net SSIM=0.9532, MSE=0.00221`; `HIO SSIM=0.0207, MSE=0.09028`.
- `d1_0_d2_8.ipynb`:  
  - финал обучения: `Train Loss 0.04818`, `Val Loss 0.09220`;  
  - среднее: `U-Net SSIM=0.8431, MSE=0.01716`; `HIO SSIM=0.1175, MSE=0.08912`.
- `d1_1_d2_8.ipynb`:  
  - финал обучения: `Train Loss 0.05070`, `Val Loss 0.09485`;  
  - среднее: `U-Net SSIM=0.8481, MSE=0.01715`; `HIO SSIM=0.1202, MSE=0.08824`.
- `d1_0_d2_8_noise.ipynb` (устойчивость к шуму):  
  - пример для `SNR=0 dB`: `U-Net SSIM=0.7268` vs `HIO SSIM=0.0204`;  
  - для `SNR=10 dB`: `0.9185` vs `0.0630`;  
  - для `SNR=100 dB`: `0.9323` vs `0.1035`.  
  U-Net стабильно превосходит HIO на всем диапазоне SNR.

**Ключевые файлы для запуска**  
- `/qoc(optics_mipt)/ai_studio_code.ipynb`  
- `/qoc(optics_mipt)/d1_0_d2_8.ipynb`  
- `/qoc(optics_mipt)/d1_1_d2_8.ipynb`  
- `/qoc(optics_mipt)/d1_0_d2_8_noise.ipynb`

**Стек**  
`Python`, `PyTorch`, `TorchVision`, `NumPy`, `Matplotlib`, `scikit-image`, `PIL`, `tqdm`.

---

### 2) Правило-ориентированное извлечение атрибутов e-commerce запросов
**📁 /e-commerce_rule_based_attributes**

**Задача и физико-математическая суть**  
Извлечение товарных атрибутов (категория, цвет, размеры/specs, бренд, целевая группа) из коротких noisy-запросов маркетплейса с опечатками, транслитом и неоднородным форматом единиц измерения.

**Архитектура и методы**  
- EDA + очистка `query_text` (20k запросов, без пропусков и точных дублей).
- Признаки и разведка данных: длины строк, число слов, наличие цифр/латиницы.
- Лексический анализ: `CountVectorizer` (n-grams), `TF-IDF`.
- Ненадзорная структура: `TruncatedSVD(n_components=50)` + `KMeans(n_clusters=10, n_init=10)`.
- Каскадный rule-based экстрактор (`RuleBasedAttributeExtractor`):  
  regex-паттерны для размеров/единиц, словари брендов/цветов/категорий, дедупликация пересекающихся матчей, морфологическая нормализация через `pymorphy3`.
- Fuzzy matching: `rapidfuzz`.

**Метрики и результаты**  
- Объем: `20000` уникальных запросов (`100%` уникальности, `0%` пропусков).  
- Покрытие по атрибутам:  
  - Category: `~37.2%`  
  - Colors: `~6.9%`  
  - Sizes & Specs: `~21.6%`  
  - Brands: `~22.0%`  
  - Target Group: `~12.4%`
- Ручной аудит (микро-валидация):  
  - `~88–92%` точность для структурированных атрибутов (размеры/цвета);  
  - около `50%` корректности полного разбиения запроса по всем атрибутам (просадка на редких категориях и long-tail кейсах).

**Ключевые файлы для запуска**  
- `/e-commerce_rule_based_attributes/Карпунин Егор Сергеевич. Data Scientis. Понимание запросов.pdf` (полный пайплайн, код и анализ в отчете).

**Стек**  
`Python`, `pandas`, `NumPy`, `scikit-learn`, `rapidfuzz`, `pymorphy3`, `matplotlib`, `seaborn`, `re`.

---

### 3) Алгоритмические контесты (Python, 2 семестр)
**📁 /PY CONTESTS 2 SEM**

**Задача и физико-математическая суть**  
10 задач по графам, строкам, комбинаторной оптимизации и численным алгоритмам: offline dynamic connectivity, топологическая сортировка, MST/минимальный разрез, bipartite matching, суффиксный автомат, FFT-корреляция ДНК и др.

**Архитектура и методы (по файлам)**  
- `/PY CONTESTS 2 SEM/1 contest/1.py` — минимальное время достижения станции в расписании поездов (граф по событиям остановок).  
- `/PY CONTESTS 2 SEM/1 contest/2.py` — `cut/ask` в графе через DSU (offline в обратном порядке операций).  
- `/PY CONTESTS 2 SEM/1 contest/3.py` — проверка единственности топологической сортировки (Kahn + проверка размера очереди).  
- `/PY CONTESTS 2 SEM/2 contest/1.py` — constrained network design с «небезопасными» вершинами (вариант MST с ограничениями маршрутизации).  
- `/PY CONTESTS 2 SEM/2 contest/2.py` — евклидов MST на плоскости (Prim по полной матрице расстояний).  
- `/PY CONTESTS 2 SEM/2 contest/3.py` — максимум неатакующих ладей на доске с вырезами (максимальное паросочетание в двудольном графе, DFS augmenting paths).  
- `/PY CONTESTS 2 SEM/2 contest/4.py` — глобальный минимальный разрез неориентированного графа (Stoer–Wagner).  
- `/PY CONTESTS 2 SEM/3 contest/1.py` — склейка слов с максимальным overlap префикс/суффикс (rolling hash).  
- `/PY CONTESTS 2 SEM/3 contest/2.py` — подсчет числа различных подстрок через суффиксный автомат.  
- `/PY CONTESTS 2 SEM/3 contest/3.py` — максимум совпадений ДНК при циклическом сдвиге через FFT-корреляцию для алфавита `A/C/G/T`.

**Метрики и результаты**  
- Контестный формат: решения читают `stdin`, печатают `stdout`; численные метрики качества модели не предусмотрены.  
- В коде зафиксированы большие лимиты входа (например, до `n=20000`, `k=100000`, длина строки до `5000`, `M≤2^16` для FFT-кейса), что отражает ориентацию на асимптотически эффективные алгоритмы.

**Стек**  
`Python` (базовые структуры данных, графовые алгоритмы, DSU, suffix automaton, FFT-реализация).

---

## Инструкция по установке и запуску

> В репозитории отсутствует `requirements.txt`, поэтому зависимости ставятся вручную.

### 1) Клонирование
```bash
git clone https://github.com/lonvein/achievements.git
cd achievements
```

### 2) Виртуальное окружение (venv)
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\\Scripts\\activate  # Windows PowerShell
```

### 3) Установка зависимостей
```bash
pip install --upgrade pip
pip install numpy matplotlib torch torchvision scikit-image pillow tqdm
pip install pandas seaborn scikit-learn rapidfuzz pymorphy3 jupyter
```

### Альтернатива (conda)
```bash
conda create -n achievements python=3.11 -y
conda activate achievements
pip install numpy matplotlib torch torchvision scikit-image pillow tqdm pandas seaborn scikit-learn rapidfuzz pymorphy3 jupyter
```

### 4) Запуск основных проектов

#### CV / Задача обратного восстановления в оптике (ноутбуки)
```bash
jupyter notebook "qoc(optics_mipt)/d1_0_d2_8.ipynb"
```
Аналогично можно запускать:
- `qoc(optics_mipt)/d1_1_d2_8.ipynb`
- `qoc(optics_mipt)/d1_0_d2_8_noise.ipynb`
- `qoc(optics_mipt)/ai_studio_code.ipynb`

#### Алгоритмические решения (stdin/stdout)
```bash
python "PY CONTESTS 2 SEM/1 contest/2.py" < input.txt
python "PY CONTESTS 2 SEM/3 contest/3.py" < input.txt
```

#### Извлечение атрибутов e-commerce
Практическая реализация и аналитика находятся в PDF-отчете:
```text
e-commerce_rule_based_attributes/Карпунин Егор Сергеевич. Data Scientis. Понимание запросов.pdf
```

---

## Автор и контакты

- **Егор Карпунин** — студент МФТИ  
- **Telegram:** [@ek_mipt](https://t.me/ek_mipt)  
- **Email:** [karpunin.es@phystech.edu](mailto:karpunin.es@phystech.edu)
