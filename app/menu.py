def show_menu() -> None:
    running = True

    while running:
        print("\nA-Maze-ing")
        print("1. Re-generate a new maze")
        print("2. Show/Hide the shortest path")
        print("3. Rotate the wall colours")
        print("4. Quit")

        option = input("Choice? (1-4): ")

        if option == "1":
            print("Generating a new maze...")
        elif option == "2":
            print("Showing or hiding shortest path...")
        elif option == "3":
            print("Rotating wall colours...")
        elif option == "4":
            running = False
        else:
            print("Invalid option")

show_menu()
