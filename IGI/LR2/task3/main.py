import circle  
import square
import os      

def main():
    radius = float(os.getenv("RADIUS", 5))
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