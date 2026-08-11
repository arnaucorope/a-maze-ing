def show_menu() -> str:
    running = True

    while running:
        print("\nA-Maze-ing")
        print("1. Generate animated maze")
        print("2. Re-generate a new maze")
        print("3. Show/Hide the shortest path")
        print("4. Rotate the wall colours")
        print("5. Quit")

        option = input("Choice? (1-4): ")
        if option == "2":
            types = input("Animated or fixed maze? :")
            return types

    return option
