# Install numpy 
# set wd same as the file location

import numpy as np

# read the text file into matrix
floor_plan = [];
with open('floorplan01.txt') as file:
    for line in file.read().splitlines():
        floor_plan.append(list(line))

# seperator characters
seperator = {'+', '-', '|', '/', '\\'}

#Number of Rows
number_of_rows = len(floor_plan)

#Number of Columns
number_of_columns = len(floor_plan[0])

#Matrix to keep track of points visited
visited = np.zeros(shape=(number_of_rows, number_of_columns), dtype=bool)

# contains a list of tuples; where the first element in tuple is room name and the second element is list of chairs in that room
room_with_chairs = []

# we store all the chairs present in the whole floor plan
list_of_all_letters = []

# we should not visit a visited cell or a seperator (which is defined above)
def shouldvisit(cell):
    x = cell[0]
    y = cell[1]
    return not(visited[x][y] or (floor_plan[x][y] in seperator))

# Checks if both given cells contain separators
def are_both_separators(cell1, cell2):
    return (floor_plan[cell1[0]][cell1[1]] in seperator) and (floor_plan[cell2[0]][cell2[1]] in seperator)

# gets all the valid adjacent cells which can be at most 8
def get_neighbours(cell):
    x = cell[0]
    y = cell[1]
    neighbours = []

    # check for floor plan boundary
    y_0 = y > 0 #check if current position is not along left-most verticle edge of floor plan
    y_max = y < number_of_columns - 1 #check if current position is not along right-most verticle edge of floor plan
    x_0 = x > 0 #check if current position is not along top-most horizontal edge of floor plan
    x_max = x < number_of_rows - 1 #check if current position is not along bottom-most horizontal edge of floor plan

    if(x_0):
        # The second condition is necessary because while checking a diagonal neighbour, we must make sure that
        # the cells along the other diagonal do not contain separators as in that case the diagonal neighbour would be on the other side of the boundary
        if(y_0 and not are_both_separators((x-1, y), (x, y-1))):
            neighbours.append((x-1, y-1))
        neighbours.append((x-1, y))
        if(y_max) and not are_both_separators((x-1, y), (x, y+1)):
            neighbours.append((x-1, y+1))
    if(y_0):
        neighbours.append((x, y-1))
    if(y_max):
        neighbours.append((x, y+1))
    if(x_max):
        if(y_0 and not are_both_separators((x+1, y), (x, y-1))):
            neighbours.append((x+1, y-1))
        
        neighbours.append((x+1, y))
        
        if(y_max and not are_both_separators((x+1, y), (x, y+1))):
            neighbours.append((x+1, y+1))
    
    return neighbours

# it gets the current box name, for instance, office, hallway, etc
def get_room_name(cell):
    x = cell[0]
    y = cell[1]
    row = ''.join(floor_plan[x]) #for string conversion
    l=y;
    r=y;
    while(l>0 and row[l]!='('):
        l-=1;
    while(r<len(row)-1 and row[r]!=')'):
        r+=1;
    return row[l+1:r]


#This function searches a given box in a breadth-first search (BFS) manner starting from a cell
def bfs(cell):
    queue = [cell]
    chairs = []
    area_name = None
    visited[cell[0]][cell[1]] = True    
    
    while(queue != []):
        curr_cell = queue.pop()
        x = curr_cell[0]
        y = curr_cell[1]

        curr_char = floor_plan[x][y]
        if(curr_char.isupper()):
            chairs.append(curr_char)

        elif((curr_char.islower() or curr_char == '(' or curr_char == ')') and area_name == None):
            area_name = get_room_name(curr_cell)

        for neighbour in get_neighbours(curr_cell):
            if(shouldvisit(neighbour)):
                visited[neighbour[0]][neighbour[1]] = True
                queue.append(neighbour)
    return (area_name, chairs)

# Doing BFS over every unvisited non-separator cell
for i, row in enumerate(floor_plan):
    for j, _ in enumerate(row):
        if(shouldvisit((i, j))):
            local_outcome = bfs((i, j))
            if(local_outcome[0] != None):
                room_with_chairs.append(local_outcome)
                list_of_all_letters.extend(local_outcome[1])

# final solution is the formatted version of above found solution where we are calculating frequency of letters corresponding to each box
final_outcome = {}

# set_of_unique_letters finds the unique set of letters present in all the blocks which is in list_of_all_letters
set_of_unique_letters=set(list_of_all_letters)
#for downstream compliance for old machine if W, P, S, C are found as chairs then they must appear in W then P then S then C order and rest to remain as is 
reorder_set_of_unique_letters = []
dupchairs = ['W','P','S','C']
reorder_set_of_unique_letters = [chair for chair in dupchairs if chair in set_of_unique_letters]
remainderlist = [chair for chair in set_of_unique_letters if chair not in dupchairs]
if len(remainderlist) !=0:
    set_of_unique_letters = reorder_set_of_unique_letters.extend(remainderlist)
else:
    set_of_unique_letters = reorder_set_of_unique_letters

# calculating frequency of all the letters corresponding to every box
for tuple in room_with_chairs:
    freq={}
    for letter in set_of_unique_letters:
        freq[letter]=0
    for letter in tuple[1]:
        freq[letter]+=1
    final_outcome[tuple[0]]=freq

# calculating the total frequency of all the letters in all the boxes
total_freq = {}
for letter in set_of_unique_letters:
    total_freq[letter]=0
for tuple in room_with_chairs:
    for letter in tuple[1]:
        total_freq[letter]+=1
final_outcome['Total'] = total_freq

# Creating a Old Machine complaint .txt file at the input file location
chairorder = {}
chairorder = {key: value for key, value in sorted(final_outcome.items())}
chairorder = {key if key != 'Total' else 'total': value for key, value in chairorder.items()}
finishedorder = open('chairorder.txt', "w")
for key, value in chairorder.items():
    finishedorder.write(str(key) + ':' +'\n' + str(value).replace("{","").replace("}", "").replace("'","") + '\n')
finishedorder.close()

print("Brady Technologies Chair Order Extractor: Your file is ready. Please close this command line")