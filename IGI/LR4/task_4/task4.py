"""
gets user input
creates object based on rectangle class
draws it using matplotlib
Lab 4
variant 14
v1
Kryshalovich Ivan Pavlovich
08.05.2026
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from task4_classes import Square, repeat_run

def input_parameters() -> tuple:
    """
    Handles user input for figure parameters and text label.
    """
    r_input = input("Enter radius of inscribed circle: ")
    color_input = input("Enter color of square: ")
    label_input = input("Enter text label for square: ")
    return r_input, color_input, label_input

def draw_figure(square_obj: Square, label_text: str):
    """
    Builds, fills, and saves the plot of the geometric figure using matplotlib.
    """
    fig, ax = plt.subplots()
    
    bottom_left_x = -square_obj.r
    bottom_left_y = -square_obj.r
    side_length = 2 * square_obj.r
    
    square_patch = patches.Rectangle(
        (bottom_left_x, bottom_left_y), 
        side_length, 
        side_length, 
        linewidth=2, 
        edgecolor='black', 
        facecolor=square_obj.color_obj.color
    )
    
    circle_patch = patches.Circle(
        (0, 0), 
        square_obj.r, 
        fill=False, 
        linestyle='-', 
        edgecolor='black'
    )
    
    ax.add_patch(square_patch)
    ax.add_patch(circle_patch)
    
    ax.text(0, 0, label_text, color='white', fontsize=12, fontweight='bold',
            horizontalalignment='center', verticalalignment='center')
            
    ax.set_xlim(-square_obj.r * 1.5, square_obj.r * 1.5)
    ax.set_ylim(-square_obj.r * 1.5, square_obj.r * 1.5)
    ax.set_aspect('equal') 
    ax.grid(True)
    ax.set_title(square_obj.get_info())

    plt.savefig("square_plot.png")
    print("Graph successfully saved to 'square_plot.png'.")
    plt.show()

@repeat_run
def task4_main():
    try:
        r_input, color_input, text_input = input_parameters()
        my_square = Square(r_input, color_input)
        
        print("\nObject successfully created:")
        print(my_square.get_info())
        
        draw_figure(my_square, text_input)

    except ValueError as err:
        print("Error creating figure:", err)

    except Exception as err:
        print("Unexpected error: ", err)

if __name__ == '__main__':
    task4_main()