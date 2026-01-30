def demo(x):
    try:                        # This block could be risky and only
        print("A")
        y = 10 / x
    except ZeroDivisionError:   # Handle specific exception
        print("B")
    else:                       # Runs if no exception occurs
        print("C")
    finally:                    # Always runs
        print("D")

demo(2)         # A C D
print("-----")
demo(0)         # A B D