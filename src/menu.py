__all__ = ["show_menu", "get_choice"]

def show_menu():
    print("(0) - Only print statements")
    print("(1) - Write screenshots to file system")
    print("(2) - Show screenshots in photo viewer")
    print("(3) - Show screenshots for specific player")
    print("(4) - One iteration at a time")
    print("(5) - No print statements")

def get_choice():
    choice = input("Select mode: ")

    if (choice == "3"):
        player_choice = int(input("Select player number (i.e. 3): "))

        player_choices = {
            1: "p1",
            2: "p2",
            3: "p3",
            4: "p4"
        }
        return player_choices.get(player_choice)
    return choice
