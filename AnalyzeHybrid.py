import re

# Функція для обчислення кількості рядків коду (SLOC)
def count_sloc(code):
    return len([line for line in code.splitlines() if line.strip() and not line.strip().startswith('//')])

# Функція для обчислення метрики Холстеда
def halstead_metrics(code):
    operators = re.findall(r'[+\-*/=<>!&|^~%]', code)
    operands = re.findall(r'\w+', code)
    
    n1 = len(set(operators))  # Кількість унікальних операторів
    n2 = len(set(operands))   # Кількість унікальних операндів
    N1 = len(operators)       # Загальна кількість операторів
    N2 = len(operands)        # Загальна кількість операндів

    # Метрики Холстеда
    vocabulary = n1 + n2
    length = N1 + N2
    difficulty = (n1 / 2) * (N2 / n2) if n2 != 0 else 0
    effort = difficulty * length

    return vocabulary, length, difficulty, effort

# Функція для обчислення метрики Маккейба
def mcCabe_metric(code):
    conditionals = len(re.findall(r'(if|else|for|while|switch|case)', code))
    return conditionals + 1  # Включаємо 1 для загальної кількості базових блоків

# Функція для розрахунку гібридної метрики за формулою Кокола
def kokola_metric(base_metric, *other_metrics):
    R = [0.2, 0.3, 0.5]  
    weighted_sum = base_metric + sum(R[i] * other_metrics[i] for i in range(len(other_metrics)))
    normalization_factor = 1 + sum(R)
    return weighted_sum / normalization_factor

# Головна функція для аналізу
def analyze_code_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read()

        # Розрахунок метрик
        sloc = count_sloc(code)
        halstead_metrics_result = halstead_metrics(code)
        mcCabe = mcCabe_metric(code)
        
        # Гібридна метрика
        hybrid_metric = kokola_metric(sloc, halstead_metrics_result[3], mcCabe)
        
        # Вивести результати
        print(f"SLOC (Lines of Code): {sloc}")
        print(f"Halstead Effort: {halstead_metrics_result[3]}")
        print(f"McCabe Cyclomatic Complexity: {mcCabe}")
        print(f"Hybrid Metric (Kokola): {hybrid_metric}")

    except FileNotFoundError:
        print(f"File '{file_path}' not found. Please check the path.")

if __name__ == "__main__":
    file_path = '/tmp/file_to_analyze.cpp'  # Local path to the C++ file
    analyze_code_from_file(file_path)
