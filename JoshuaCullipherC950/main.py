# Joshua Cullipher

import routing
import datetime

# Display message that shows when program starts -> O(1)
print('WGUPS Tracking System\n\n')
print('Current route was completed in', "{0:.2f}".format(routing.get_total_distance(), 2), ' miles\n')


# Gets initial user input -> O(1)
user_selection = input("""
Select an option:
1. View all packages delivery status at a specific time
2. View a specific package at a specific time
Type 'q' to exit
""")

while True:
    # If user selects 1 -> O(N^3)
    if user_selection == '1':
        try:
            input_time = input('Enter a time in hh:mm 24-hour format: ')
            (hrs, mins) = input_time.split(':')
            input_time_datetime = datetime.time(int(hrs), int(mins))

            routing.update_package_position(input_time_datetime)
            routing.print_all_packages()
        except ValueError:
            print('Invalid Entry')
            pass

    # If user selects 2 -> O(N^3)
    elif user_selection == '2':
        try:
            input_package = input('Enter a package ID: ')
            input_time = input('Enter a time in hh:mm 24-hour format: ')
            (hrs, mins) = input_time.split(':')
            input_time_datetime = datetime.time(int(hrs), int(mins))

            routing.update_package_position(input_time_datetime)
            routing.print_package(int(input_package))
        except ValueError:
            print('Invalid Entry')
            pass

    elif user_selection == 'q':
        break

    else:
        print('Invalid Entry')

    # Gets next user input -> O(1)
    user_selection = input("""
    Select an option:
    1. View all packages delivery status at a specific time
    2. View a specific package at a specific time
    Type 'q' to exit
    """)
