'''
calculates sum of a series until epsilant precision
counts necessary members
prints result of python function calculating same sum of a series 
Determination of additional parameters: arithmetic mean of the sequence elements, median, mode, variance, and standard deviation of the sequence
Make graphics using matplotlib
Lab #4
v1
variant 14
Kryshalovich Ivan Pavlovich
07.05.2026 
'''
import task3_classes

def task3_main():
    '''
    calculates sum of a series until epsilant precision
    counts necessary members
    prints result of python function calculating same sum of a series
    '''
    while True:
        x = task3_classes.get_float_number("print x, |x| < 1: ")
        if(abs(x) < 1): break
            
    eps = task3_classes.get_float_number("Enter eps precision(for example 0.001): ")

    calculator = task3_classes.LnSeriesCalculator(x, eps)

    calculator.calculate()
    calculator.print_table()
    
    calculator.print_stats(calculator.terms_values)
    
    calculator.save_and_show_plot(
        n_list=calculator.n_values, 
        sums_list=calculator.sums_values, 
        exact_value=calculator.exact_val
    ) 

if(__name__ == "__main__"):
    task3_main()