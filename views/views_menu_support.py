class MenuSupportView:
    def menu_support(self, username):
        while True:
            print(f"SUPPORT MENU | WELCOME, {username}")
            print("* " * 16)
            print("\t1. Update an event you are in charge of")
            print("\t2. Display the events you are in charge of")
            print("\t3. Display all the clients")
            print("\t4. Display all the contracts")
            print("\t5. Display all the events")
            print("\n\tdisconnect. DISCONNECT and go back to authentication")

            menu_choice = input("Your choice: ")
            if menu_choice in [
                "1",
                "2",
                "3",
                "4",
                "5",
                "disconnect",
            ]:
                return menu_choice
            else:
                print("\n\tERROR: Please enter an existing option.\n")
                continue
