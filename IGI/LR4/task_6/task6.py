"""
analyze melbourne houses using pandas
create multi-level structure 'MultiIndex'
compare the prices of houses with max and min number of rooms but more then 0
Lab 4
variant 14
v1
Kryshalovich Ivan Pavlovich
14.05.2026
"""

from task6_classes import MelbourneHousingAnalyzer
import pandas as pd

def task6_main():
    csv_file = "melb_data.csv"
    
    try:
        analyzer = MelbourneHousingAnalyzer(csv_file)

        print("\n[Task A] MultiIndex Series:")
        multi_series = analyzer.perform_task_a()

        print(multi_series)
        
        print(f"\nIndex levels names: {multi_series.index.names}")

        print("\n[Task B] Statistical Analysis:")
        ratio = analyzer.perform_task_b()
        
        print(f"The average price of houses with the MAXIMUM number of rooms is "
              f"{ratio} times greater than houses with the MINIMUM number of rooms (>0).")

    except Exception as err:
        print(f"An error occurred during analysis: {err}")

if __name__ == "__main__":
    task6_main()