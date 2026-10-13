#Gregg Marshall
#3/9/2026

ROWS = 10  # number of rows
COLS = 4  # number of columns

'''
This first function opens the text file containing the information for the booked
seats on the flight. It creates a nested list from the stripped lines. I print
the column letters at the top, add a space between the second and third columns,
and lastly, I use enumerate to print the rest of the rows. There is an error handler
at the bottom that triggers if the file is not found when trying to open it. 

'''

def display(menu_code): #menu_code is the placeholder I have for every function. It holds the input from the user in the main code. Then it calls a function based on the user's input. 
    try:
        with open("seats.txt", "r") as display: #display is the variable assigned to the file being opened. 
            content = display.read() #content is the variable assigned to the raw information from the file.
            seating_chart = [] #seating_chart is an empty list ready to hold the lines of data from the file.
            lines = content.splitlines() #lines holds the version of the data that has been turned into a list of strings by starting each new line at the line breaks in the original data.
            for line in lines: #line represents each item in the list lines.
                seating_chart.append(list(line))
            for row in seating_chart: #row represents each item in the list seating_chart. 
                row.insert(2," ")
            print("   AB CD")
            for row_num, row in enumerate(seating_chart): #row_num is the variable assigned to represent the number of each row on the left side of the seating display in the terminal. 
                if row_num == 9:
                    print(f"{row_num + 1} {"".join(row)}")
                else:
                    print(f"{row_num + 1}  {"".join(row)}")
    except FileNotFoundError:
        print(f"The file containing the seating chart was not found.")


'''
This function prompts the user to select a seat on the plane. It then runs
the user's input through a series of tests to ensure the input is correctly 
formatted. Next, it opens the text file to check if the seat is available
by searching the file for an 'X' or '.' using the translated coordinates of 
the selected seat. If the seat is available, this function calls the assign_seat 
function. If not, the function runs an algorithm that searches every seat adjacent 
to the user's selected seat and lets the user know which of those seats are available.
The user is prompted again to select a new seat. The function returns a boolean 
to the main code depending on whether it was successfully written to the file and
prints a message regarding if the flight data was updated. Lastly, the function has
an exception handler for if the file holding the flight data cannot be found.
'''
def purchase(menu_code):

    while True: #True in this loop runs the code until the user has a successful input.

        selection = input("To purchase a seat, please enter your row number and column letter (e.g. 7A or 10B): ") #selection holds the user's seat choice.
            
        if len(selection) < 2 or len(selection) > 3:
            print("Invalid entry. Entry must be a number 1-10 followed by a letter A-D.")
            continue 

        row_input = selection[0:-1] #row_input holds the first slice of the user's input that's supposed to represent the row of the seating chart.
        column = selection[-1].upper() #column holds the end slice of the user's input that's supposed to represent the column of the seating chart. 

        valid_row = list(range(1,11)) #valid_row is a list of integers that holds the accepted input for user's row selection.
        valid_column = ["A", "B", "C", "D"] #valid_column holds a list of acceptable column names for the user's column selection.

        if not row_input.isdigit():
            print("Invalid row. Row must be a number. Column must be only one letter.")
            continue

        row_num = int(row_input) #row_num holds the integer version of the sliced user's input for row.
        if row_num not in valid_row:
            print("Invalid row. Row must be a number 1-10.")
            continue

        if column not in valid_column:
            print("Invalid column. Column must be A, B, C, or D.")
            continue

        break

    try:
        with open("seats.txt", "r") as seats: #seats is the name assigned to the file containing the data for the seats available on the flight.
            content = seats.read() #content holds the raw data from the file.
            seating_chart = [] #seating_chart is an empty list ready to hold the cleaned data.
            lines = content.splitlines() #lines holds the version of the data that has been turned into a list of strings by starting each new line at the line breaks in the original data.
            for line in lines: #line represents each string of data in lines while this loop iterates through it.
                clean_line = line.replace(" ", "") #clean_line holds the data from line after it has had its white space removed.
                seating_chart.append(list(clean_line))

            cord1 = (row_num - 1) #cord1 is the row number minus one. This translation is required due to how Python indexes lists starting at 0 instead of 1.

            if column == "A":
                cord2 = 0 #cord2 is the translation of the column number needed to search seating_chart.
            elif column == "B":
                cord2 = 1
            elif column == "C":
                cord2 = 2
            elif column == "D":
                cord2 = 3
            
            if seating_chart[cord1][cord2] == ".": #cord1 and cord2 are used together to search the nested list seating_chart to confirm the seat's availability. 
                print("Seat is available.")
                print("Assigning seat...")
                return assign_seat(menu_code, cord1, cord2) #This is where these variables are sent to the assign_seat function and where this function receives the boolean from assign_seat.

            elif seating_chart[cord1][cord2] == "X":
                print("Seat is unavailable.")


                nearby_seats = [] #nearby_seats is an empty list that will hold the results of the search algorithm. 

                for i in range(-1,2): #i represents the values iterated through the y coordinate range (row) for the search algorithm.
                    for r in range(-1,2): #r represents the values iterated through the x coordinate range (column) for the search algorithm.
                        if i == 0 and r == 0:
                            continue

                        new_row = cord1 + i #new_row and new_column are the iterated coordinates that the search algorithm generates to search the seats around the selected seat.
                        new_column = cord2 + r

                        if len(seating_chart) > new_row >= 0 and len(seating_chart[0]) > new_column >= 0:
                            if seating_chart[new_row][new_column] == ".":
                                row_display = new_row + 1 #row_display and column_display are the translated seat names so that they match the seating display visible to the user and not where they live in nearby_seats.
                                column_display = valid_column[new_column]
                                nearby_seats.append((row_display, column_display))

                print("Available seats nearby: ", end="")
                for av_row, av_col in nearby_seats: #av_row and av_col represent the translated row and column coordinates that are stored as tuples in nearby_seats which are then iterated through and formatted for the user to read.
                    print(f"{av_row}{av_col},", end=" ")
                print()
                return False #This boolean is returned to the main code to signal that the flight log was not updated.
        
        
        


    except FileNotFoundError:
        print(f"The file containing the seating chart was not found.")
    
'''
This function opens and reads the data file we've been working with and creates 
a list of all the characters in the raw data. Each "X" and "." is counted and 
then used to calculate the percentage of seats occupied. The function includes 
an exception to alert the user if the data file cannot be opened.
'''
def statistics(menu_code):
    try:
        with open("seats.txt", "r") as seat_data: #seat_data is what we are calling the file when it is called in this function.
            content = seat_data.read() #content stores the raw data from seat_data.
            data = list(content) #data is the raw data formatted as a list.
            occupied = 0 #occupied is a variable assigned to the number of times "X" appears in data.
            free = 0 #free is a variable assigned to the number of times "." appears in data.
            for char in data: #char is the variable assigned to hold the place of each character in data as this loop iterates through data. 
                if char == "X":
                    occupied += 1
                elif char == ".":
                    free += 1
                else:
                    pass
            occupancy = float((occupied / (occupied + free)) * 100) #occupancy is assigned to the result of the occupied seats divided by the total amount of seats on the plane to calculate how full the plane is as a percentage.
            print(f"The flight is currently {occupancy:.1f}% occupied.")

    except FileNotFoundError:
        print(f"The file containing the seating chart was not found.")
    
'''
This function takes the coordinates of the chosen seat from purchase() and opens 
the data file for reading and writing. It creates a nested list from the rows 
read from the file. It then updates the chosen seat value with an "X". The updated 
data is converted back into strings with newlines, the cursor is moved to the 
beginning of the file, and the file is overwritten with the new data. There is 
an exception at the end of the function to alert the user if the file cannot be 
opened.
'''
def assign_seat(menu_code, cord1, cord2):
    try:
        with open("seats.txt", "r+") as seat_data: #seat_data is the name the file is given in this function.
            content = seat_data.read().splitlines() #content is assigned to hold the list made from the stripped rows from the file.
            
            seat_update = [] #seat_update an empty list ready to become a nested list holding each seat value.

            for old_row in content: #old_row is assigned to hold the value of each string in content as this loop iterates through them and turns the strings into lists. 
                 seat_update.append(list(old_row))

            seat_update[cord1][cord2] = "X"

            updated_content = "" #updated_content is an empty string to be used to house the results of turning the lists of individual seats back into strings. 

            for new_row in seat_update: #new_row is a variable used to iterate through each list in seat_update.
                row_string = "" #row_string is an empty string used to hold each character from the list the loop is currently iterating through and then added to updated_content.
                for character in new_row: #character is a variable used to represent each character in the list new_row as it is iterated through. 
                      row_string += character
                updated_content += row_string + "\n"
            
            seat_data.seek(0)
            seat_data.write(updated_content)
            print("Seat Assigned!")
            return True #True signals that the function was able to update the file.

    except FileNotFoundError:
        print(f"The file containing the seating chart was not found.")
        return False #False signals that there was an error in updating the file.

'''
This is the main menu of the program. It provides the user with a list of inputs 
for the functions they can run, validates the user input, and uses a set of if 
statements to call the appropriate function. The if statements are housed in a 
while loop that runs until the user enters the input to quit the menu. It is in 
this section that the program checks the boolean confirming if assign_seat 
successfully wrote the data to the file.
'''

menu_code = input("Select an option from the menu:\nD to display the seat chart\nP to purchase a seat\nS to compute statistics\nQ to quit\nEnter menu selection: ").upper() 
#menu_code is the variable that is used to call the functions in this program. The following while loop calls a function depending on the user_input assigned to menu_code.
while menu_code != "Q":

    if menu_code == "D":
        display(menu_code)

    elif menu_code == "P":
        if purchase(menu_code):
            print("You have successfully booked your flight.")
            print("Flight log updated!")
        else:
            print("Flight log not updated.")
    elif menu_code == "S":
        statistics(menu_code)

    else:
        print("Invalid entry. Valid entry: D, P, S, or Q,")

    menu_code = input("Please select an option from the menu (D, P, S, or Q): ").upper()


print("Thank you for flying with DSE 502 Air!")
print("Goodbye!")