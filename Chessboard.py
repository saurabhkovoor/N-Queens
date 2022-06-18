class Chessboard:
    # constructor method to initialise attributes and chessboard required for implementation
    def __init__(self, boardSize=1):
        boardState = [-1] * boardSize #instantiates the initial state, a blank chessboard with no placement of queens, blank boxes with no queens represented by -1
        self.boardState = boardState
        self.boardSize = boardSize
    
    # action variable keeps tracks of number of actions taken to find goal state and all goal states/solutions
    actions = 0

    # Method to update the chessboard/boardState list by adding queen at the specified row and column
    def placeQueen(self, row, col):
        self.boardState[row] = col 
        Chessboard.actions+=1 # placement of queen on the board is considered 1 action in this problem, so increment by 1 for every action

    # Method to generate chessboard states (for mode 1 only, simulation) and solutions/goal states  
    def getBoardStates(self, simOption, treeDepth=1): #starts with depth 1
        # The tree depth value begins from 1 whereas rows begin from 0 (0-indexed)
        row = treeDepth - 1
        
        # Generates all the possible queen placements options on a col (returns col, where queen can be placed) in the current row where no collision occurs
        placementOpp = Chessboard.getPlacementOpp(self.boardState, row)
        for col in placementOpp:
            # calling previously defined function to add queen to board at specified row and col, based on what exists in the placement opportunities list
            self.placeQueen(row, col)
            
            # program progresses till all four tree depth/chessboard rows are reached (has a queen)
            if treeDepth < self.boardSize:
                # Mode 1 visualises the actions to reach a solution, so the following yields/returns the states to reach the solution
                if simOption == 1:
                    yield self.boardState.copy()

                # Adding board states of following row/tree depth to the list
                yield from self.getBoardStates(simOption, treeDepth + 1) #recursion to execute this same function but at the next depth of the DFS tree
            else:
                yield self.boardState.copy() #all depths have been explored, so the final depth equals boardsize, so all rows have queen, and this state is returned/yielded as a solution

            #to reset the chessboard/board state, to allow new placement of queens to find next solution
            self.boardState[row] = -1
        
    # method to generate all the placement opportunities (col values for particular given row) where it is correct and not mutually-attacking another queen 
    def getPlacementOpp(boardState, row):
        for col in range(len(boardState)):
            if Chessboard.checkCorrectPlacement(boardState, row, col): #calls function to check if the placement of queen at the particular column in that row is correct (not mutually attacking antoher), then return the col
                yield col
                
    # method to check/validate if the positioning of a queen is correct not mutually attacking another queen, doesn't share same column, diagonals
    def checkCorrectPlacement(boardState, row, col):
        # starting from row 0 till the current row (row), checks if there exists queen for every previous row(prevRow, prevCol) that is sharing same col or diagonals with the current cell (row,col)
        prevRow = 0
        while prevRow < row:
            # Based on the previous row, finding the col of the queen present their to get its coordinates for comparing to check for clashes
            prevCol = boardState[prevRow]

            # The placement is incorrect if the queen shares the same col (first conditional) or shares the same diagonals (2nd conditional)
            if (col == prevCol) or (abs(row - prevRow) == abs(col - prevCol)):
                return False

            prevRow = prevRow + 1

        # The placement is correct if it is not sharing column or diagonals with another queen
        return True


    #method to display chessboard, states and goal states in the Python terminal
    def displayChessboard(boardState, message=''):
        # Values for chessboard Columns
        boardColumns = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

        #chessboard size (number rows/cols, i.e., 4,5,6,7,8...)
        boardSize = len(boardState)

        # display the chessboard's top edge, based on chessboard size
        print("    ╔═══" + "╦═══" * (boardSize-1) + "╗")

        # Iterating through the rows in the boardState in a reverse manner, so A1 appears at the bottom left
        for row in range(boardSize-1, -1, -1):
            print(" " + str(format(row+1, "2d")) + " ", end="") # Displaying the first column of row coordinate values

            for col in range(0, boardState[row]): # First blank squares in the cells leading up to the queen positionm,also the left border of the chessboard
                print("║   ", end="")

            if boardState[row] != -1: # Displaying queen in the row in that board state if not empty (does not contain -1)
                print("║ ♕ ", end="")

            for col in range(boardState[row] + 1, boardSize): # Following blank squares after a queens position in the row till the border
                print("║   ", end="")

            # right border of the chessboard
            print("║")

            # Border lines within the body that distinguish the rows for when the row is not the last, else it is the last row, and the bottom border should be generated instead
            if row != 0:
                print("    ╠═══" + "╬═══" * (boardSize-1) + "╣")
            else:
                print("    ╚═══" + "╩═══" * (boardSize-1) + "╝")

                # Displaying the chessboard column values at the bottom of the chessboard. Offsetted by 4 pixels so in line with the board
                print("      ", end="")
                for i in range(0, boardSize):
                    print(boardColumns[i], end="")

                    # if it's not the last col, blank spaces to separate the board column values so its in line with its corresponding column, else a newline to not print anymore columns
                    if (i != boardSize - 1):
                        print("   ", end="")
                    else:
                        print()
                
                # Displaying any message after the chessboard to indicate action has been made (only for mode 1) or solution has been found, else only blank line is printed 
                if message != "":
                    print("\n    " + message, end="\n\n")
                else:
                    print()

    #static method so can be directly accessed and called in the main class without creating or referencing instance
    #method to choose simulation method to display the states/goal states/solutions accordingly
    @staticmethod
    def chooseSimOption(simOption, boardStates):
        # Tracks the number of solutions found so far
        noOfSolutions = 0

        # Mode 1 shows every state explored to reach solution, so it prints and pauses (waiting for user's Enter) after every action/state
        if simOption == 1:
            for boardState in boardStates:
                if (-1 not in boardState): #-1 signifies rows where there is no queens placed, so if a board state does not contain -1 it is the solution
                    noOfSolutions += 1
                    message = "↑ This is solution " + str(noOfSolutions) + "! Continue by pressing any key/Enter." #returns message to print, indicate result of placement, and required user action/input 
                    Chessboard.displayChessboard(boardState, message) # calls the previous method to display the chessboard matrix in the terminal for the given state with the message 
                    print("    Number of actions to get this solution: " + str(Chessboard.actions))
                    input()
                else: # This is not a solution/goal state but an action or state where not every row is filled or has a queen. Displays only for mode 1, for visualisation purposes
                    Chessboard.displayChessboard(boardState)
                    print("    Actions: " + str(Chessboard.actions))
                    input()

        # Mode 2 displays every solution/goal state 1-by-1/individually. User has to press any key or Enter to view the next solution
        elif simOption == 2:
            for boardState in boardStates:
                noOfSolutions += 1
                message = "↑ This is solution " + str(noOfSolutions) + "! Continue by pressing any key/Enter."
                Chessboard.displayChessboard(boardState, message)
                print("    Actions: " + str(Chessboard.actions))
                input()

        # Mode 3 displays every solution/goal state at once  
        elif simOption == 3:  
            for boardState in boardStates:
                noOfSolutions += 1
                message = "↑ This is solution " + str(noOfSolutions) + "!"
                Chessboard.displayChessboard(boardState, message)
                print()
        
        # Mode 4 is to stop the program execution
        elif simOption == 4:
            quit()            

        # Displays to user final output, which is number of solutions/goal states and total number of actions
        print("\n    All " + str(noOfSolutions) + " solutions were found.")
        print("    Total actions: " + str(Chessboard.actions))
        print()