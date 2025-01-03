from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# Window dimensions
screenWidth = 500
screenHeight = 800

# Game variables
lanes = [100, 200, 300, 400, 500]  # Lane x-positions
player_x = lanes[1] - 50  # Player car starts in the second lane
player_y = 100  # Player car's initial y-position
car_width, car_height = 50, 100
oncoming_cars = []
immunity_circles = []
coins = []
special_coins = []
magnet = []
score = 0
start_time = time.time()
game_over = True
paused = False

#-------Nodi variables--------------#

# Initialize leaderboard
try:
    with open("leaderboard.txt", "r") as file:
        leaderboard = [int(score.strip()) for score in file.readlines()]
except FileNotFoundError:
    leaderboard = [0, 0, 0]  # Default leaderboard if file is missing



#--------rafi variables added----------#
# Game states
game_state = 0  # 0: Main menu, 1: Difficulty menu, 2: Game
immunity_active = False
magnet_active = False
immunity_start_time = 0
magnet_start_time = 0

#--------rafi close----------#



# Midpoint Line Algorithm
def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx > 0 and dy >= 0:
            return 0
        elif dx <= 0 and dy > 0:
            return 3
        elif dx < 0 and dy <= 0:
            return 4
        else:
            return 7
    else:
        if dx >= 0 and dy > 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx <= 0 and dy < 0:
            return 5
        else:
            return 6

def ConvertMtoZero(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def ConvertZeroToM(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def midpointLine(x1, y1, x2, y2, zone):
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    x, y = x1, y1

    cx, cy = ConvertMtoZero(x, y, zone)
    setPixel(cx, cy)

    while x < x2:
        if d <= 0:
            d += incE
            x += 1
        else:
            d += incNE
            x += 1
            y += 1

        cx, cy = ConvertZeroToM(x, y, zone)
        setPixel(cx, cy)

def midpointLineEightWay(x1, y1, x2, y2):
    zone = findZone(x1, y1, x2, y2)
    ax1, ay1 = ConvertMtoZero(x1, y1, zone)
    ax2, ay2 = ConvertMtoZero(x2, y2, zone)
    midpointLine(ax1, ay1, ax2, ay2, zone)

def setPixel(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def drawImmunityCoin():
    global immunity_circles
    for circle in immunity_circles:
        glBegin(GL_POINTS)
        glColor3f(0.0, 1.0, 0.0)  # Green color
        MidpointCircle(10, circle[0], circle[1])
        glEnd()
# Draw Lane Lines
def drawLanes():
    glColor3f(1.0, 1.0, 1.0)  # White color
    glBegin(GL_POINTS)
    for lane in lanes:
        for y in range(screenHeight):
            glVertex2f(lane, y)
    glEnd()


# Draw Player Car
def drawPlayerCar():
    glColor3f(1.0, 1.0, 1.0)  # Blue color
    #------Nodi added part-------#
    if immunity_active:  # Change color when immunity is active
        glColor3f(0.0, 1.0, 1.0)  # Cyan for immunity
    #------Nodi part end ------#
    midpointLineEightWay(player_x - car_width // 2, player_y, player_x + car_width // 2, player_y)

    midpointLineEightWay(player_x + car_width // 2, player_y, player_x + car_width // 2, player_y + car_height)
    midpointLineEightWay(player_x - car_width // 2, player_y + car_height, player_x + car_width // 2, player_y + car_height)
    midpointLineEightWay(player_x - car_width // 2, player_y, player_x - car_width // 2, player_y + car_height)

    midpointLineEightWay(player_x - car_width // 2+15, player_y+25, player_x + car_width // 2-15, player_y+25)
    midpointLineEightWay(player_x - car_width // 2+15, player_y+25, player_x - car_width // 2, player_y)
    midpointLineEightWay(player_x + car_width // 2-15, player_y+25, player_x + car_width // 2, player_y)

    midpointLineEightWay(player_x - car_width // 2+5, player_y+70, player_x + car_width // 2-5, player_y+70)
    midpointLineEightWay(player_x - car_width // 2, player_y+75, player_x + car_width // 2, player_y+75)

    midpointLineEightWay(player_x - car_width // 2+5, player_y+70, player_x - car_width // 2+15, player_y+55)
    midpointLineEightWay(player_x + car_width // 2-5, player_y+70, player_x + car_width // 2-15, player_y+55)
    midpointLineEightWay(player_x - car_width // 2+15, player_y+55, player_x + car_width // 2-15, player_y+55)

    midpointLineEightWay(player_x - car_width // 2+15, player_y+55, player_x - car_width // 2+15, player_y+25)
    midpointLineEightWay(player_x + car_width // 2-15, player_y+55, player_x + car_width // 2-15, player_y+25)





def drawOncomingCars():
    global car_height, car_width
    glColor3f(1.0, 0.0, 0.0)  # Red color
    for car in oncoming_cars:
        x, y = car[0], car[1]
        midpointLineEightWay(x - car_width // 2, y, x + car_width // 2, y)
        midpointLineEightWay(x + car_width // 2, y, x + car_width // 2, y + 100)

        midpointLineEightWay(x - car_width // 2, y + car_height, x + car_width // 2, y + car_height)
        midpointLineEightWay(x - car_width // 2, y, x - car_width // 2, y + car_height)

# Draw Coins
def drawCoins():
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 0.0)  # Yellow color
    for coin in coins:
        MidpointCircle(10, coin[0], coin[1])
    glEnd()

def drawDoubleCoins():
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.5, 1.0)
    for coin in special_coins:
        MidpointCircle(10, coin[0], coin[1])
    glEnd()

def drawMagnet():
    global magnet
    for circle in magnet:
        glBegin(GL_POINTS)
        glColor3f(0.21, 0.0, 0.74)  # Green color
        MidpointCircle(10, circle[0], circle[1])
        glEnd()


# Midpoint Circle Algorithm


def MidpointCircle(radius, cx, cy):
    d = 1 - radius
    x = 0
    y = radius
    circlePoints(x, y, cx, cy)
    while x <= y:
        if d < 0:
            d = d + 2 * x + 3
            x += 1
        else:
            d = d + 2 * (x - y) + 5
            x += 1
            y -= 1
        circlePoints(x, y, cx, cy)

def circlePoints(x, y, cx, cy):
    
    glVertex2f(x + cx, y + cy)
    glVertex2f(y + cx, x + cy)
    glVertex2f(-x + cx, y + cy)
    glVertex2f(-y + cx, x + cy)
    glVertex2f(-y + cx, -x + cy)
    glVertex2f(-x + cx, -y + cy)
    glVertex2f(x + cx, -y + cy)
    glVertex2f(y + cx, -x + cy)
   

# Display Score and Time
def displayScoreAndTime():
    glColor3f(1.0, 0.0, 0.0)
    glRasterPos2f(10, screenHeight - 20)
    elapsed_time = int(time.time() - start_time)
    score_text = f"Score: {score} Time: {elapsed_time}s"
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

# Update Game State
def update(value):
    global player_x, player_y, oncoming_cars, coins, score, game_over, paused, lane_speed, magnet

    if game_over:
        return
    elif paused:
        return
    if time.time() - start_time > 5:
        lane_speed = lane_speed + 0.001
    # Move oncoming cars
    for car in oncoming_cars:
        car[1] -= lane_speed
    oncoming_cars = [car for car in oncoming_cars if car[1] > -car_height]

    # Move coins
    for coin in coins:
        coin[1] -= lane_speed
    coins = [coin for coin in coins if coin[1] > -10]

    for circle in immunity_circles:
        circle[1] -= lane_speed
    for circle in magnet:
        circle[1] -= lane_speed
    for circle in special_coins:
        circle[1] -= lane_speed

    # Check collisions
    check_collisions()        

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

# Spawn Oncoming Cars and Coins
def spawnObjects(value):
    global immunity_circles, game_over, paused, magnet_active, magnet, special_coins, coins, oncoming_cars
    if not game_over and paused == False:
        lane = random.choice(lanes) - 50
        probability = random.random()
        if probability < 0.7:  
            oncoming_cars.append([lane, screenHeight])
        elif probability > 0.95:
            circle_data = [lane, screenHeight, True, 5]
            immunity_circles.append(circle_data)
        elif probability > 0.9:
            magnet.append([lane, screenHeight])
        else: 
            if random.random() > 0.8:  
                special_coins.append([lane, screenHeight])
                print(f"Special coin spawned at lane {lane}")
            else:
                coins.append([lane, screenHeight])
                print(f"Regular coin spawned at lane {lane}")
                          
        
        glutTimerFunc(700, spawnObjects, 0)

# Keyboard Controls
def keyboardListener(key, x, y):
    global player_x,player_y, paused

    if key == b'a' and player_x > lanes[0]:  # Move left
        player_x -= 100
    elif key == b'd' and player_x + 100 <= lanes[-1]:  # Move right
        player_x += 100
    elif key == b'w' and player_y < screenHeight - car_height:  # Move up
        player_y += 20
    elif key == b's' and player_y > 0:  # Move down
        player_y -= 20
    elif key == b'\x1b':  # Escape key
        paused = not paused
        glutTimerFunc(16, update, 0)
        glutTimerFunc(1000, spawnObjects, 0)
       

    glutPostRedisplay()  # Redraw the screen to update

#-----------RafiPart-------------------------#

class Box:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        # Draw the rectangle
        midpointLineEightWay(self.x, self.y, self.x + self.width, self.y)
        midpointLineEightWay(self.x + self.width, self.y, self.x + self.width, self.y + self.height)
        midpointLineEightWay(self.x + self.width, self.y + self.height, self.x, self.y + self.height)
        midpointLineEightWay(self.x, self.y + self.height, self.x, self.y)

class Letter:
    def __init__(self, lines):
        self.lines = lines  # List of tuples: [(x1, y1, x2, y2), ...]

    def draw(self, offset_x, offset_y):
        """
        Draws the letter at the specified offset position.
        """
        for line in self.lines:
            x1, y1, x2, y2 = line
            midpointLineEightWay(x1 + offset_x, y1 + offset_y, x2 + offset_x, y2 + offset_y)

def create_letter_p():
    return Letter([
        (0, 0, 0, 20),  # Vertical line
        (0, 20, 10, 20),  # Top horizontal line
        (10, 20, 10, 12),  # Right vertical
        (10, 12, 0, 12)  # Middle horizontal line
    ])

def create_letter_l():
    return Letter([
        (0, 0, 0, 20),  # Vertical line
        (0, 0, 10, 0)  # Bottom horizontal line
    ])

def create_letter_a():
    return Letter([
        (0, 0, 5, 20),  # Left diagonal
        (5, 20, 10, 0),  # Right diagonal
        (2, 10, 8, 10)  # Middle horizontal line
    ])

def create_letter_y():
    return Letter([
        (0, 20, 5, 10),  # Left diagonal
        (10, 20, 5, 10),  # Right diagonal
        (5, 10, 5, 0)  # Vertical line
    ])

def create_letter_e():
    return Letter([
        (0, 0, 0, 20),  # Vertical line
        (0, 20, 10, 20),  # Top horizontal line
        (0, 10, 8, 10),  # Middle horizontal line
        (0, 0, 10, 0)  # Bottom horizontal line
    ])

def create_letter_d():
    return Letter([
        (0, 0, 0, 20),  # Vertical line
        (0, 20, 8, 18),  # Top curve
        (8, 18, 8, 2),  # Right vertical
        (8, 2, 0, 0)  # Bottom curve
    ])

def create_letter_r():
    return Letter([
        (0, 0, 0, 20),  # Vertical line
        (0, 20, 10, 20),  # Top horizontal
        (10, 20, 10, 12),  # Right vertical
        (10, 12, 0, 12),  # Middle horizontal
        (0, 12, 10, 0)  # Diagonal
    ])

def create_letter_b():
    return Letter([
        (0, 0, 0, 20),  # Vertical line
        (0, 20, 8, 18),  # Top curve
        (8, 18, 8, 12),  # Right vertical (top half)
        (8, 12, 0, 12),  # Middle horizontal
        (0, 12, 8, 10),  # Bottom curve
        (8, 10, 8, 0),  # Right vertical (bottom half)
        (8, 0, 0, 0)  # Bottom horizontal
    ])

def create_letter_o():
    return Letter([
        (0, 0, 0, 20),  # Left vertical
        (0, 20, 10, 20),  # Top horizontal
        (10, 20, 10, 0),  # Right vertical
        (10, 0, 0, 0)  # Bottom horizontal
    ])

def create_letter_x():
    return Letter([
        (0, 0, 10, 20),  # Left diagonal
        (0, 20, 10, 0)  # Right diagonal
    ])

def create_letter_i():
    return Letter([
        (5, 0, 5, 20),  # Vertical line
        (0, 20, 10, 20),  # Top horizontal line
        (0, 0, 10, 0)  # Bottom horizontal line
    ])

def create_letter_t():
    return Letter([
        (5, 0, 5, 20),  # Vertical line
        (0, 20, 10, 20)  # Top horizontal line
    ])
def create_letter_s():
    return Letter([
        (10, 20, 0, 20),  # Top horizontal line
        (0, 20, 0, 10),   # Left vertical (top half)
        (0, 10, 10, 10),  # Middle horizontal line
        (10, 10, 10, 0),  # Right vertical (bottom half)
        (10, 0, 0, 0)     # Bottom horizontal line
    ])

def create_letter_m():
    return Letter([
        (0, 0, 0, 20),  # Left vertical line
        (0, 20, 5, 10),  # Left diagonal
        (5, 10, 10, 20),  # Right diagonal
        (10, 20, 10, 0)   # Right vertical line
    ])

def create_letter_u():
    return Letter([
        (0, 20, 0, 0),  # Left vertical line
        (0, 0, 10, 0),  # Bottom horizontal line
        (10, 0, 10, 20)  # Right vertical line
    ])

def create_letter_h():
    return Letter([
        (0, 0, 0, 20),  # Left vertical line
        (0, 10, 10, 10),  # Middle horizontal line
        (10, 0, 10, 20)  # Right vertical line
    ])

def create_letter_q():
    return Letter([
        (0, 0, 0, 20),  # Left vertical
        (0, 20, 10, 20),  # Top horizontal
        (10, 20, 10, 0),  # Right vertical
        (10, 0, 0, 0),  # Bottom horizontal
        (6, 4, 10, 0)  # Tail of Q
    ])

def create_letter_g():
    return Letter([
        (10, 20, 0, 20),  # Top horizontal line
        (0, 20, 0, 0),  # Left vertical line
        (0, 0, 10, 0),  # Bottom horizontal line
        (10, 0, 10, 10),  # Right vertical line
        (10, 10, 5, 10)  # Inner horizontal line
    ])

def create_letter_k():
    return Letter([
        (0, 0, 0, 20),  # Vertical line
        (0, 10, 10, 20),  # Upper diagonal
        (0, 10, 10, 0)  # Lower diagonal
    ])

def create_letter_v():
    return Letter([
        (0, 20, 5, 0),  # Left diagonal
        (5, 0, 10, 20)  # Right diagonal
    ])

def create_letter_w():
    return Letter([
        (0, 20, 3, 0),  # Left diagonal
        (3, 0, 5, 10),  # Middle diagonal (upward)
        (5, 10, 7, 0),  # Middle diagonal (downward)
        (7, 0, 10, 20)  # Right diagonal
    ])

def create_letter_z():
    return Letter([
        (0, 20, 10, 20),  # Top horizontal line
        (10, 20, 0, 0),  # Diagonal line
        (0, 0, 10, 0)  # Bottom horizontal line
    ])

def create_letter_f():
    return Letter([
        (0, 0, 0, 20),  # Vertical line
        (0, 20, 10, 20),  # Top horizontal line
        (0, 10, 8, 10)  # Middle horizontal line
    ])

def create_letter_n():
    return Letter([
        (0, 0, 0, 20),  # Left vertical line
        (0, 20, 10, 0),  # Diagonal
        (10, 0, 10, 20)  # Right vertical line
    ])

def create_letter_c():
    return Letter([
        (10, 20, 0, 20),  # Top horizontal line
        (0, 20, 0, 0),  # Left vertical line
        (0, 0, 10, 0)  # Bottom horizontal line
    ])

def create_space():
    return Letter([])  # No lines for a space

def draw_word(word, start_x, start_y, spacing=15):
    letters = {
        "P": create_letter_p(),
        "L": create_letter_l(),
        "A": create_letter_a(),
        "Y": create_letter_y(),
        "E": create_letter_e(),
        "D": create_letter_d(),
        "R": create_letter_r(),
        "B": create_letter_b(),
        "O": create_letter_o(),
        "X": create_letter_x(),
        "I": create_letter_i(),
        "T": create_letter_t(),
        "S": create_letter_s(),
        "M": create_letter_m(),
        "U": create_letter_u(),
        "H": create_letter_h(),
        "Q": create_letter_q(),
        "G": create_letter_g(),
        "K": create_letter_k(),
        "V": create_letter_v(),
        "W": create_letter_w(),
        "Z": create_letter_z(),
        "F": create_letter_f(),
        "N": create_letter_n(),
        "C": create_letter_c(),
        " ": create_space()  # Space character
    }

    x_offset = start_x
    for char in word:
        if char.upper() in letters:  # Handle case insensitivity
            letters[char.upper()].draw(x_offset, start_y)
            x_offset += spacing  # Add spacing between letters



#-------------------Numbers--------------------------#

class Number:
    def __init__(self, segments):
        self.segments = segments  # List of line segments representing the number

    def draw(self, start_x, start_y):
        # Loop through each segment and draw it, adjusting the position for each number
        for (x1, y1, x2, y2) in self.segments:
            # Assuming you have a drawing function (e.g., draw_line)
            midpointLineEightWay(start_x + x1, start_y + y1, start_x + x2, start_y + y2)


def create_digit_0():
    return Number([
        (0, 0, 0, 20),  # Left vertical
        (0, 20, 10, 20),  # Top horizontal
        (10, 20, 10, 0),  # Right vertical
        (10, 0, 0, 0)  # Bottom horizontal
    ])

def create_digit_1():
    return Number([
        (5, 0, 5, 20),  # Vertical line
    ])

def create_digit_2():
    return Number([
        (10, 20, 0, 20),  # Top horizontal line
        (0, 20, 0, 10),   # Left vertical (top half)
        (0, 10, 10, 10),  # Middle horizontal line
        (10, 10, 10, 0),  # Right vertical (bottom half)
        (10, 0, 0, 0)     # Bottom horizontal line
    ])

def create_digit_3():
    return Number([
        (0, 0, 10, 0),  # Top horizontal line
        (10, 0, 10, 10),  # Right vertical line (top half)
        (0, 10, 10, 10),  # Middle horizontal line
        (0, 10, 0, 0),  # Left vertical line (bottom half)
        (10, 0, 10, 10)  # Right vertical line (bottom half)
    ])

def create_digit_4():
    return Number([
        (0, 0, 0, 20),  # Left vertical line
        (0, 10, 10, 10),  # Horizontal line in the middle
        (10, 10, 10, 0)  # Right vertical line
    ])

def create_digit_5():
    return Number([
        (10, 20, 0, 20),  # Top horizontal line
        (0, 20, 0, 10),   # Left vertical (top half)
        (0, 10, 10, 10),  # Middle horizontal line
        (10, 10, 10, 0),  # Right vertical (bottom half)
        (10, 0, 0, 0)     # Bottom horizontal line
    ])

def create_digit_6():
    return Number([
        (10, 20, 0, 20),  # Top horizontal line
        (0, 20, 0, 0),  # Left vertical line
        (0, 0, 10, 0),  # Bottom horizontal line
        (10, 0, 10, 10),  # Right vertical line
        (10, 10, 5, 10)  # Inner horizontal line
    ])

def create_digit_7():
    return Number([
        (0, 0, 10, 0),  # Top horizontal line
        (10, 0, 10, 20)  # Right vertical line
    ])

def create_digit_8():
    return Number([
        (10, 20, 0, 20),  # Top horizontal line
        (0, 20, 0, 0),  # Left vertical line
        (0, 0, 10, 0),  # Bottom horizontal line
        (10, 0, 10, 10),  # Right vertical line
        (10, 10, 0, 10)  # Middle horizontal line
    ])

def create_digit_9():
    return Number([
        (0, 0, 0, 20),  # Left vertical
        (0, 20, 10, 20),  # Top horizontal
        (10, 20, 10, 0),  # Right vertical
        (10, 0, 0, 0),  # Bottom horizontal
        (5, 10, 10, 0)  # Tail of 9
    ])

def create_digit_space():
    return Number([])  # No lines for a space

# Function to draw a number with a given starting position
def draw_number(number, start_x, start_y, spacing=15):
    digits = {
        "0": create_digit_0(),
        "1": create_digit_1(),
        "2": create_digit_2(),
        "3": create_digit_3(),
        "4": create_digit_4(),
        "5": create_digit_5(),
        "6": create_digit_6(),
        "7": create_digit_7(),
        "8": create_digit_8(),
        "9": create_digit_9(),
        " ": create_digit_space()  # Space character
    }
    
    x_offset = start_x
    for digit in str(number):
        number_obj = digits[digit]
        number_obj.draw(x_offset, start_y)  # Assuming `draw` method exists for Number class
        x_offset += spacing  # Adjust the horizontal position for the next digit

#---------BOX CREATION--------------#
play_box = Box(180, 490, 150, 60)
leaderboard_box = Box(140, 400, 230, 60)
exit_box = Box(180, 310, 150, 60)
easy_box = Box(180, 490, 150, 60)
medium_box = Box(180, 400, 150, 60)
hard_box = Box(180, 310, 150, 60)
over_box = Box(180, 400, 150, 60)
restart_box = Box(60, 270, 150, 60)
mainmenu_box = Box(300, 270, 150, 60)
resume_box = Box(180, 400, 150, 60)
exit_box2 = Box(60, 270, 150, 60)

player_score1=Box(140, 490, 230, 60)
player_score2=Box(140, 400, 230, 60)
player_score3=Box(140, 310, 230, 60)
mainmenu_box2 = Box(178, 220, 150, 60)

def drawMainMenu():
    glColor3f(1.0, 0.0, 0.0) 
    play_box.draw()
    glColor3f(0.0, 1.0, 0.0)
    leaderboard_box.draw()
    glColor3f(0.0, 0.0, 1.0)
    exit_box.draw()
    glColor3f(1.0, 1.0, 1.0)  # White color
    # Draw the words
    draw_word("PLAY", 228, 510)
    draw_word("LEADERBOARD", 175, 420)
    draw_word("EXIT", 225, 330)

def drawDifficultyMenu():
    glColor3f(0.1, 0.6, 0.7) 
    easy_box.draw()
    glColor3f(0.0, 1.0, 0.0)    
    medium_box.draw()
    glColor3f(1.0, 0.0, 0.0)    
    hard_box.draw()
    glColor3f(1.0, 1.0, 1.0)  # White color
    # Draw the words
    draw_word("EASY", 228, 510)
    draw_word("MEDIUM", 215, 420)
    draw_word("HARD", 225, 330)

def drawGameover():
    glColor3f(1.0, 0.0, 0.0) 
    over_box.draw()
    draw_word("GAME OVER", 190, 420)
    glColor3f(0.0, 0.7, 0.6) 
    restart_box.draw()
    draw_word("RESTART", 85, 290)
    glColor3f(0.0, 1.0, 0.0) 
    mainmenu_box.draw()
    draw_word("MAINMENU", 320, 290)
    
def drawPaused():
    glColor3f(0.0, 1.0, 0.0) 
    resume_box.draw()
    draw_word("RESUME", 215, 420)
    glColor3f(0.0, 0.7, 0.6) 
    mainmenu_box.draw()
    draw_word("MAINMENU", 320, 290)
    glColor3f(1.0, 0.0, 0.0) 
    exit_box2.draw()
    draw_word("EXIT", 110, 290)

def drawLeaderboard():
    global leaderboard  # Declare leaderboard as global
    glColor3f(0.0, 0.2, 0.6)
    player_score1.draw()
    player_score2.draw()
    player_score3.draw()
    glColor3f(0.0, 0.7, 0.6)
    mainmenu_box2.draw()
    draw_word("MAINMENU", 195, 240)
    draw_number(str(leaderboard[0]) if len(leaderboard) > 0 else 0,230, 510)
    draw_number(str(leaderboard[1]) if len(leaderboard) > 1 else 0,230, 420)
    draw_number(str(leaderboard[2]) if len(leaderboard) > 2 else 0,230, 330)

def is_point_in_rect(px, py, rect: Box):
    """
    Check if a point (px, py) is inside a given rectangle.
    """
    x1, y1 = rect.x, rect.y
    x2, y2 = rect.x + rect.width, rect.y + rect.height
    print(px, py, "Checking Point")
    return x1 <= px <= x2 and y1 <= py <= y2

def restartGame():
    global player_x, player_y, oncoming_cars, coins, immunity_circles, score, start_time, game_over, paused, immunity_active

    # Reset player position
    player_x = lanes[1] - 50
    player_y = 100

    # Clear game objects
    oncoming_cars = []
    coins = []
    immunity_circles = []

    # Reset game variables
    score = 0
    start_time = time.time()
    game_over = False
    paused = False
    immunity_active = False

    # Restart timers
    glutTimerFunc(16, update, 0)
    glutTimerFunc(1000, spawnObjects, 0)

    # Redraw the screen
    glutPostRedisplay()


def mouse_click(button, state, x, y):
    """
    Handle mouse click events and determine actions based on the click position.
    """
    global lane_speed, game_state, easy_box, play_box, leaderboard_box, exit_box, medium_box, hard_box, restart_box, mainmenu_box, game_over, paused

    # Adjust the y-coordinate because many graphical frameworks use inverted y-axis for mouse clicks
    adjusted_y = screenHeight - y  # Replace `screenHeight` with the actual height of your window

    print(f"Mouse Click at: {x}, {adjusted_y}")

    if button == 0 and state == 0:  # Left mouse button pressed
        if game_state == 0:  # Main menu
            if is_point_in_rect(x, adjusted_y, play_box):
                game_state = 1
            elif is_point_in_rect(x, adjusted_y, leaderboard_box):
                game_state =3  # Add leaderboard functionality here
            elif is_point_in_rect(x, adjusted_y, exit_box):
                glutLeaveMainLoop()
        elif game_state == 1:  # Difficulty selection screen
            if is_point_in_rect(x, adjusted_y, easy_box):
                restartGame()
                game_state = 2
                lane_speed = 2.5
            elif is_point_in_rect(x, adjusted_y, medium_box):
                restartGame()
                game_state = 2
                lane_speed = 3.5
            elif is_point_in_rect(x, adjusted_y, hard_box):
                restartGame()
                game_state = 2
                lane_speed = 4.5
        elif game_state == 2 and game_over:  # Game over screen
            if is_point_in_rect(x, adjusted_y, restart_box):
                restartGame()
                game_state = 2  # Stay in game state
                game_over = False
            elif is_point_in_rect(x, adjusted_y, mainmenu_box):
                game_state = 0  # Return to main menu
        elif game_state == 2 and paused:  # Game over screen
            if is_point_in_rect(x, adjusted_y, resume_box):
                paused = False
                glutTimerFunc(16, update, 0)
                glutTimerFunc(1000, spawnObjects, 0)

            elif is_point_in_rect(x, adjusted_y, mainmenu_box):
                game_state = 0  # Return to main menu
            elif is_point_in_rect(x, adjusted_y, exit_box2):
                glutLeaveMainLoop()
        elif game_state == 3:
            if is_point_in_rect(x, adjusted_y, mainmenu_box2):
                game_state = 0
    glutPostRedisplay()
#-----------handling Leaderboard------------------------#
# Save leaderboard to a file
def saveLeaderboard():
    with open("leaderboard.txt", "w") as file:
        for score in leaderboard:
            file.write(f"{score}\n")

# Update the leaderboard when the game ends
def updateLeaderboard():
    global score, leaderboard
    leaderboard.append(score)
    leaderboard = sorted(leaderboard, reverse=True)[:3]
    saveLeaderboard()
    print("Leaderboard updated:", leaderboard)
#---------------------leaderboard end-------------------#    


def check_collisions():
    global player_x, player_y, car_width, car_height, oncoming_cars, coins, immunity_circles, score, game_over, immunity_active,immunity_start_time,leaderboard, magnet_active, magnet_start_time, special_coins

    # Player car bounding box
    player_left = player_x - car_width // 2
    player_right = player_x + car_width // 2
    player_top = player_y + car_height
    player_bottom = player_y

    # Check collision with oncoming cars
    for car in oncoming_cars:
        car_x, car_y = car[0], car[1]
        car_left = car_x - car_width // 2
        car_right = car_x + car_width // 2
        car_top = car_y + car_height
        car_bottom = car_y

        # Check for overlap
        if (
            player_right > car_left and
            player_left < car_right and
            player_top > car_bottom and
            player_bottom < car_top
        ):
            if immunity_active:
                print("Collision avoided due to immunity!")
            else:
                print("Collision detected with an oncoming car!")
                updateLeaderboard() 
                game_over = True
                return

    # Check collision with regular coins
    coin_radius = 10  # Radius of the coin
    for coin in coins[:]:  # Iterate over a copy since we might remove coins
        coin_x, coin_y = coin[0], coin[1]
        coin_left = coin_x - coin_radius
        coin_right = coin_x + coin_radius
        coin_top = coin_y + coin_radius
        coin_bottom = coin_y - coin_radius

        # Check for overlap
        if (
            player_right > coin_left and
            player_left < coin_right and
            player_top > coin_bottom and
            player_bottom < coin_top
        ):
            print(" Regular Coin collected!")
            score += 10
            coins.remove(coin)  # Remove collected coin
    
     # Check collision with special coins
    for coin in special_coins[:]:
        coin_x, coin_y = coin
        coin_left = coin_x - coin_radius
        coin_right = coin_x + coin_radius
        coin_top = coin_y + coin_radius
        coin_bottom = coin_y - coin_radius

        if (
            player_right > coin_left and
            player_left < coin_right and
            player_top > coin_bottom and
            player_bottom < coin_top
        ):
            print("Special coin collected! Double points awarded!")
            score += 20  # Double points
            special_coins.remove(coin)
    # Check collision with immunity circles
    immunity_radius = 10  
    for circle in immunity_circles[:]:
        circle_x, circle_y, is_active, radius = circle
        circle_left = circle_x - immunity_radius
        circle_right = circle_x + immunity_radius
        circle_top = circle_y + immunity_radius
        circle_bottom = circle_y - immunity_radius

        # Check for overlap
        if (
            player_right > circle_left and
            player_left < circle_right and
            player_top > circle_bottom and
            player_bottom < circle_top
        ):
            print("Immunity power-up collected!")
            immunity_active = True
            immunity_start_time = time.time()
            immunity_circles.remove(circle)  # Remove collected immunity circle
    if immunity_active and (time.time() - immunity_start_time) > 10:
        print("Immunity has expired!")
        immunity_active = False  # Deactivate immunity
    magnet_radius = 10  
    for circle in magnet[:]:
        circle_x, circle_y = circle
        circle_left = circle_x - magnet_radius
        circle_right = circle_x + magnet_radius
        circle_top = circle_y + magnet_radius
        circle_bottom = circle_y - magnet_radius

        # Check for overlap
        if (
            player_right > circle_left and
            player_left < circle_right and
            player_top > circle_bottom and
            player_bottom < circle_top
        ):
            magnet_active = True
            magnet_start_time = time.time()
            magnet.remove(circle)  # Remove collected immunity circle
    if magnet_active and (time.time() - magnet_start_time) > 5:
        print("Magnet has expired!")
        magnet_active = False  # Deactivate immunity
    elif magnet_active:
        for coin in coins[:]:
            if coin[1] < player_top:
                coins.remove(coin)
                score += 10
        for coin in special_coins[:]:
            if coin[1] < player_top:
                special_coins.remove(coin)
                score += 20



#-------------------RafiEnd-------------------#

# ------------------- Visual Effects and Immunity Feature ------------------- #

def drawImmunityEffect():
    """
    Draws a flashing visual effect around the player car when immunity is active.
    """
    if immunity_active:
        elapsed = time.time() - immunity_start_time
        if int(elapsed * 5) % 2 == 0:  # Flashing effect based on time
            glColor3f(1.0, 1.0, 0.0)  # Yellow for immunity
            glLineWidth(3)
            midpointLineEightWay(player_x - car_width // 2 - 10, player_y - 10, 
                                 player_x + car_width // 2 + 10, player_y - 10)
            midpointLineEightWay(player_x + car_width // 2 + 10, player_y - 10, 
                                 player_x + car_width // 2 + 10, player_y + car_height + 10)
            midpointLineEightWay(player_x + car_width // 2 + 10, player_y + car_height + 10, 
                                 player_x - car_width // 2 - 10, player_y + car_height + 10)
            midpointLineEightWay(player_x - car_width // 2 - 10, player_y - 10, 
                                 player_x - car_width // 2 - 10, player_y + car_height + 10)

def activateImmunity():
    """
    Activates immunity for the player, enabling visual and gameplay effects.
    """
    global immunity_active, immunity_start_time
    immunity_active = True
    immunity_start_time = time.time()

def checkImmunityTimer():
    """
    Deactivates immunity when the timer runs out.
    """
    global immunity_active
    if immunity_active and time.time() - immunity_start_time > 15:  # Immunity lasts 15 seconds
        immunity_active = False

def drawCoinEffect(x, y):
    """
    Draws a sparkling effect at the specified position when a coin is collected.
    """
    glColor3f(1.0, 1.0, 0.0)  # Yellow for coins
    for _ in range(10):
        glBegin(GL_POINTS)
        glVertex2f(x + random.randint(-10, 10), y + random.randint(-10, 10))
        glEnd()

# ------------------- End of Visual Effects and Immunity Feature ------------------- #


# Display Function
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    if game_state == 0:  # Main menu
        drawMainMenu()
    elif game_state == 1:  # Difficulty menu
        drawDifficultyMenu()
    elif game_state == 2 and not game_over:
        if paused == False:  # Gameplay
            glClear(GL_COLOR_BUFFER_BIT)
            drawLanes()
            drawPlayerCar()
            drawImmunityEffect() # Draw immunity effect
            drawOncomingCars()
            drawCoins()
            drawImmunityCoin()
            drawMagnet()
            drawDoubleCoins()    
            displayScoreAndTime()
        else:
            glClear(GL_COLOR_BUFFER_BIT)
            drawPaused()
    elif game_state == 3:
        glClear(GL_COLOR_BUFFER_BIT)
        drawLeaderboard()
    elif game_over:
        glClear(GL_COLOR_BUFFER_BIT)
        drawGameover()
    glutSwapBuffers()

# Initialize OpenGL
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, screenWidth, 0, screenHeight)


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(screenWidth, screenHeight)
glutCreateWindow(b"DHAKA NITRO")
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouse_click)
glutTimerFunc(0, update, 0)
glutTimerFunc(1000, spawnObjects, 0)
glutMainLoop()
