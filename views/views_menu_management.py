class MenuManagementView:
    def menu_management(self, username):
        while True:
            print(f"MANAGEMENT MENU | WELCOME, {username}")
            print("* " * 16)
            print("\t1. Create a user")
            print("\t2. Update a user")
            print("\t3. Deactivate a user")
            print("\t4. Create a contract")
            print("\t5. Update a contract")
            print("\t6. Display events without assigned support")
            print("\t7. Assign support to an event")
            print("\t8. Display all the clients")
            print("\t9. Display all the contracts")
            print("\t10. Display all the events")
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
