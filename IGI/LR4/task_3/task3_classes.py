import math
import statistics
import matplotlib.pyplot as plt

def get_float_number(message: str) -> float:
    """
    returns float number, checks wrong input.
    """
    while True:
        user_input = input(message)
        try:
            x = float(user_input)
            return x
        except ValueError:
            print("Wrong input! Try again.")

class StatisticsMixin:
    """
    Mixin class that provides statistical operations for a sequence of numbers.
    """
    
    def print_stats(self, data_list: list):
        """
        Gets data_list, calculates and prints arithmetic mean, median, mode, variance, and standard deviation.
        """
        print("\n--- Statistics of the Sequence of Series Terms ---")
        
        print(f"Mean: {statistics.mean(data_list):.6f}")
        print(f"Median: {statistics.median(data_list):.6f}")
        
        try:
            print(f"Mode: {statistics.mode(data_list):.6f}")
        except statistics.StatisticsError:
            print("Mode: There is no unique mode")
        
        if len(data_list) > 1:
            print(f"Dispersion: {statistics.variance(data_list):.6f}")
            print(f"SKO(Root-mean-square deviation): {statistics.stdev(data_list):.6f}")


class PlotterMixin:
    """
    Mixin class that provides plotting and saving capabilities using matplotlib.
    """
    
    def save_and_show_plot(self, n_list: list, sums_list: list, exact_value: float, filename: str = "plot.png"):
        """
        Draws and saves a plot of the series convergence.
        """
        plt.figure(figsize=(10, 6))
        
        plt.plot(n_list, sums_list, color='blue', marker='o', label='Series expansion of F(x)')
        
        plt.axhline(y=exact_value, color='red', linestyle='--', label='Exact value (math)')
        
        plt.title('Convergence of the Taylor Series for ln(1-x)')
        plt.xlabel('Number of series terms (n)')
        plt.ylabel('Function value')
        
        plt.annotate(f'Exact: {exact_value:.4f}', 
                     xy=(1, exact_value), 
                     xytext=(1, exact_value * 1.1),
                     arrowprops=dict(facecolor='black', arrowstyle='->'))
        
        plt.grid(True)
        plt.legend()
        
        plt.savefig(filename)
        plt.show()


class LnSeriesCalculator(StatisticsMixin, PlotterMixin):
    """
    Main calculator class representing the Taylor series for ln(1-x).
    Inherits capabilities from StatisticsMixin and PlotterMixin.
    """
    
    def __init__(self, x: float, eps: float, max_iter: int = 500):
        """
        Initializes the calculator with target precision and mathematical arguments.
        """
        self.x = x
        self.eps = eps
        self.max_iter = max_iter
        
        self.n_values =[]     
        self.sums_values =[]  
        self.terms_values =[]  
        
        self.exact_val = math.log(1 - self.x)

    def calculate(self):
        """
        Performs the series calculation until the required precision is met.
        """
        current_sum = 0.0
        
        for n in range(1, self.max_iter + 1):
            term = -1 * (self.x ** n) / n
            current_sum += term
            
            self.n_values.append(n)
            self.sums_values.append(current_sum)
            self.terms_values.append(term)
            
            if abs(term) < self.eps:
                break

    def print_table(self):
        """
        Prints a formatted table displaying the calculation process step by step.
        """
        print("\nResults Table:")
        print(f"{'x':<8} | {'n':<6} | {'F(x) (Sum)':<12} | {'Math F(x)':<12} | {'eps'}")
        print("-" * 55)
        
        for i in range(len(self.n_values)):
            print(f"{self.x:<8.4f} | {self.n_values[i]:<6} | {self.sums_values[i]:<12.5f} | "
                  f"{self.exact_val:<12.5f} | {self.eps}")
            