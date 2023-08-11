class MenuSalesView:
    def menu_sales(self, username):
        while True:
            print(f"SALES MENU | WELCOME, {username}")
            print("* " * 16)
            print("\t1. Create a client")
            print("\t2. Update a client you are in charge of")
            print("\t3. Update the contract of one of your clients")
            print("\t4. Display contracts that haven't been signed yet")
            print("\t5. Display contracts that haven't been fully paid")
            print("\t6. Create an event (for a client whose contract was signed)")
            print("\t7. Display all the clients")
            print("\t8. Display all the contracts")
            print("\t9. Display all the events")
            print("\n\tdisconnect. DISCONNECT and go back to authentication")

            menu_choice = input("Your choice: ")
            if menu_choice in [
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "disconnect",
            ]:
                return menu_choice
            else:
                print("\n\tERROR: Please enter an existing option.\n")
                continue
