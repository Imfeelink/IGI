import circle  # Импортируем файл из библиотеки
import square
import os      # Для работы с переменными окружения

def main():
    # Получаем значение из переменной окружения RADIUS, если её нет — берем 5
    radius = float(os.getenv("RADIUS", 5))
    # Получаем значение стороны квадрата SIDE, если её нет — берем 10
    side = float(os.getenv("SIDE", 10))

    print(f"--- Результаты расчетов ---")
    print(f"Круг (радиус {radius}):")
    print(f"  Площадь: {circle.area(radius)}")
    print(f"  Периметр: {circle.perimeter(radius)}")

    print(f"Квадрат (сторона {side}):")
    print(f"  Площадь: {square.area(side)}")
    print(f"  Периметр: {square.perimeter(side)}")

if __name__ == "__main__":
    main()