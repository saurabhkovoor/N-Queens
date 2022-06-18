from os import system
import time
from Chessboard import Chessboard


def menu():
    system('cls||clear')

    print("N-Queens Solution Simulator Based on Depth-First Search and Backtracking")
    print("------------------------------------------------------------------------")

    boardSize = input("Enter the size of the chessboard/number of queens, N (1-26):\n->")
    boardSize = int(boardSize)
    # Requesting input from user for number of queens/size of chessboard, N
    # performing data validation to ensure input is within 1-26 for correct program execution and displaying appropriate error message

    while (True):
        if (int(boardSize) in range(2,4)):
            boardSize = input("There does not exist any solutions to the 2-Queens and 3-Queens problem. Enter a different integer number between 1 - 26:\n->")
            boardSize = int(boardSize)
            continue

        elif (int(boardSize) < 1) or (int(boardSize) > 26):
            boardSize = input("Wrong Input! Enter a different integer number between 1 - 26:\n->")
            boardSize = int(boardSize)
            continue

        else:
            break

    # Requesting input from user for menu option, for type of simulation the program should perform
    print("\nHow would you like to visualise the solutions for this {}-Queens problem?".format(str(boardSize)))
    print("[1] Pause After Every Action(Placement of Queen on the Chessboard")
    print("[2] Pause After Every Goal State/Solution")
    print("[3] Display Every Goal State/Solution at Once (Shows the Program's Execution Time)")
    print("[4] Quit the Program")

    simOption = int(input("Choose any of the options above by entering the corresponding number (1-4):\n->"))
    # Performing data validation to ensure input is within 1-26 for correct program execution and displaying appropriate error message
    while (True):
        if (int(simOption) not in range(1,5)):
            simOption = input("Wrong Input! Enter a menu option between 1 - 5:\n->")
            continue

        else:
            break

    system('cls||clear')
    startTime = time.time() #start time for tracking the program's execution time
    chessboard = Chessboard(boardSize) #instantiating the Chessboard object to use its methods
    boardStates = chessboard.getBoardStates(simOption) # generating all the goal states/solutions as well as other board states (only for mode 1, simulation)

    chessboard.chooseSimOption(simOption, boardStates) # based on the chosen simulation option, the board states/solutions are displayed accordingly
    endTime = time.time() #end time for tracking program execution time

    #calculating program execution time duration (only for immediate display of board states)
    if simOption == 3:
        print("    Execution Time: " + str(round(endTime-startTime, 5)) + "s")

if __name__ == '__main__': # ensures menu function is called when file is executed, so program starts
    menu()