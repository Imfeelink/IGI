def repeat_run(func):
    '''decorator:
    gets function, launches it and asking user if he needs to launch program again
    uses decorator'''
    def wrapper(*args, **kwargs):
        while True:
            func(*args, **kwargs)

            answer = input("Wanna launch program again(y - yes, n - no): ").strip().lower()
            if(answer == 'yes' or answer == 'y'):
                continue
            elif(answer == 'no' or answer == 'n'):
                break
            else:
                break
    return wrapper