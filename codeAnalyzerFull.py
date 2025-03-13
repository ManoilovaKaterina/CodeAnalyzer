import os
import re
import sys

# Функція для визначення мови програмування
def detect_language(file_path):
    if file_path.endswith(".cpp") or file_path.endswith(".h"):
        return "cpp"
    elif file_path.endswith(".py"):
        return "python"
    return None

# Функція для підрахунку рядків коду (SLOC)
def count_sloc(code):
    return len([line for line in code.splitlines() if line.strip() and not line.strip().startswith(("//", "#"))])

# Функція для підрахунку кількості функцій, класів, коментарів
def count_functions_classes_comments(code, language):
    if language == "cpp":
        functions = len(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\s+\w+\s*\(.*\)\s*{', code))
        classes = len(re.findall(r'\bclass\s+[A-Za-z_][A-Za-z0-9_]*', code))
        comments = len(re.findall(r'//.*|/\*.*?\*/', code, re.DOTALL))
    elif language == "python":
        functions = len(re.findall(r'\bdef\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(', code))
        classes = len(re.findall(r'\bclass\s+[A-Za-z_][A-Za-z0-9_]*', code))
        comments = len(re.findall(r'#.*', code))
    else:
        return 0, 0, 0
    return functions, classes, comments

# Функція для обчислення метрики Маккейба (цикломатична складність)
def mcCabe_metric(code, language):
    if language == "cpp":
        conditionals = len(re.findall(r'\b(if|else if|for|while|switch|case)\b', code))
    elif language == "python":
        conditionals = len(re.findall(r'\b(if|elif|for|while|try|except)\b', code))
    else:
        return 0
    return conditionals + 1

# Функція для обчислення метрик Холстеда
def halstead_metrics(code):
    operators = re.findall(r'[+\-*/=<>!&|^~%]', code)
    operands = re.findall(r'\b\w+\b', code)
    
    n1 = len(set(operators))  # Унікальні оператори
    n2 = len(set(operands))   # Унікальні операнди
    N1 = len(operators)       # Загальна кількість операторів
    N2 = len(operands)        # Загальна кількість операндів

    vocabulary = n1 + n2
    length = N1 + N2
    difficulty = (n1 / 2) * (N2 / n2) if n2 != 0 else 0
    effort = difficulty * length
    return vocabulary, length, difficulty, effort

# Функція для розрахунку гібридної метрики Кокола
def kokola_metric(base_metric, *other_metrics):
    R = [0.2, 0.3, 0.5]  
    weighted_sum = base_metric + sum(R[i] * other_metrics[i] for i in range(len(other_metrics)))
    normalization_factor = 1 + sum(R)
    return weighted_sum / normalization_factor

# Основна функція аналізу коду
def analyze_code_from_file(file_path):
    language = detect_language(file_path)
    if not language:
        print(f"Unsupported file type: {file_path}")
        return
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
        
        sloc = count_sloc(code)
        functions, classes, comments = count_functions_classes_comments(code, language)
        halstead_metrics_result = halstead_metrics(code)
        mcCabe = mcCabe_metric(code, language)
        hybrid_metric = kokola_metric(sloc, halstead_metrics_result[3], mcCabe)
        
        # Вивід результатів
        print(f"=== Code Analysis Report for {file_path} ===")
        print(f"Language: {language.capitalize()}")
        print(f"SLOC (Lines of Code): {sloc}")
        print(f"Functions: {functions}")
        print(f"Classes: {classes}")
        print(f"Comments: {comments}")
        print(f"Halstead Effort: {halstead_metrics_result[3]:.2f}")
        print(f"McCabe Cyclomatic Complexity: {mcCabe}")
        print(f"Hybrid Metric (Kokola): {hybrid_metric:.2f}")
    
    except FileNotFoundError:
        print(f"File '{file_path}' not found. Please check the path.")

# Запуск аналізу
def main():
    if len(sys.argv) != 2:
        print("Usage: python codeAnalyzerFull.py <file_path>")
        return
    file_path = sys.argv[1]
    analyze_code_from_file(file_path)

if __name__ == "__main__":
    main()
