import pygame #import the pygame library
import os #import the os library for loading images
import random #imports the random library
import time #imports the time library
import sqlite3 
pygame.font.init() #allows me to use fonts
from pygame.locals import *

wndw = pygame.display.set_mode((1000,600)) #create a window with dimensions 1000x600


pygame.display.set_caption('Volatile Void') #creates a header for the program labelled 'Volatile Void'

fps = 60 #Frames per second
speed = 5 #Speed at which the player character moves per second
bullets_speed = 20 #Speed at which the player's bullets moves per second
enemy_bullet_speed = 10 #Speed at which the enemy's bullets moves per second

shooter_list = [] #list of all shooter enemies on the screen
enemy_list = [] #list of all enemies on the screen

arial = pygame.font.SysFont('arial', 40) #font arial size 40

aurora = pygame.transform.scale(pygame.image.load(os.path.join('Assets','aurora.png')),(1100,700))
player_sprite = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets','spaceship_yellow.png')),(55,40)),90)
ufoenemy = pygame.transform.scale(pygame.image.load(os.path.join('Assets','ufo.png')),(65,50)) 
heart = pygame.transform.scale(pygame.image.load(os.path.join('Assets','pixel-heart.png')),(55,40)) 
boss_sprite = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets','spaceship_red.png')),(55,40)),270)
menu_background = pygame.transform.scale(pygame.image.load(os.path.join('Assets','menu.png')),(1100,700)) #initialises the main menu background

player_hit = pygame.USEREVENT+1
enemy_hit = pygame.USEREVENT+2

class enemies: #parent class for all enemies
    def __init__(self,health,pic,w,l,xpos,ypos):
        self.__health = health #health of enemy
        self.__pic = pic #picture of enemy
        self.rec = pygame.Rect(w,l,xpos,ypos) #enemy hitbox/position 

    def __del__(self): #deletes an instantiated object in a class
         pass
        
    def get_pic(self): #getter for enemy picture
        return self.__pic

    def damage(self): #used when enemy takes damage
        self.__health -= 1
    
    def get_health(self): #getter for enemy health
        return self.__health
    
    def rectangle(self): #getter for enemy hitbox/posisiton 
        return self.rec

class shooters(enemies): #subclass for the shooter emey
    def __init__(self,health,pic,w,l,xpos,ypos,up,bullet_num):
        super().__init__(health,pic,w,l,xpos,ypos)
        self.__up = up #used to tell if the enemy is moving up or down
        self.__bullet_num = bullet_num #counter for number of bullets the enemy has on the screen
        self.__bullet = pygame.Rect(self.rec.x + self.rec.width, self.rec.y + self.rec.height,10,5) #bullets for the enemy to shoot

    def movement(self,player): #movement method
        if self.rec.y + self.rec.height > 600: #if at bottom of screen up becomes true 
             self.__up = True
        elif self.rec.y < 0: #if at top of screen up becomes false 
             self.__up = False
        if self.__up: #if up true, enemy moves up at a constant speed
            self.rec.y -= speed
        else: #if up false, enemy down up at a constant speed
            self.rec.y += speed 
        
    def make_bullet(self): #getter for a bullet
        return self.__bullet
    
    def bullet_edit(self,num): #increases the counter for number of bullets the enemy has on the screen
        self.__bullet_num += num

    def get_bullet_num(self): #getter for the counter for number of bullets the enemy has on the screen
        return self.__bullet_num

class crashers(enemies):
    def __init__(self,health,pic,w,l,xpos,ypos):
        super().__init__(health,pic,w,l,xpos,ypos)

    def movement(self,player):#movement method
        if round(self.rec.y,-2) < round(player.y,-2): #each if statement used to move the enemy closer to the player 
            self.rec.y += 5
        elif round(self.rec.y,-2) > round(player.y,-2):
            self.rec.y -= 5
        if round(self.rec.x,-2) < round(player.x,-2):
            self.rec.x += 5
        elif round(self.rec.x,-2) > round(player.x,-2):
            self.rec.x -= 5

class boss(enemies):
    def __init__(self,health,pic,w,l,xpos,ypos,bullet_num):
        super().__init__(health,pic,w,l,xpos,ypos)
        self.__bullet = pygame.Rect(self.rec.x + self.rec.width, self.rec.y + self.rec.height,10,5) #bullets for the enemy to shoot
        self.__bullet_num = bullet_num #counter for number of bullets the enemy has on the screen

    def movement(self,player):#movement method
        num = random.randint(0,180) 
        if num == 0: #if random number is 0 teleports enemy
            self.rec.x = random.randint(400,900)
            self.rec.y = random.randint(0,500)

    def make_bullet(self): #getter for a bullet
        return self.__bullet

    def bullet_edit(self,num): #increases the counter for number of bullets the enemy has on the screen
        self.__bullet_num += num

    def get_bullet_num(self): #getter for the counter for number of bullets the enemy has on the screen
        return self.__bullet_num


def makewindow(player,bullets,enemy_bullets,health,score): #handles display
    wndw.blit(aurora,(0,0)) #draws background image
    for x in range(0,health):
        wndw.blit(heart,(30+x*60,30))
    wndw.blit(player_sprite,(player.x,player.y)) #draws player
    for bullet in bullets: #draws all bullets in the game
        pygame.draw.rect(wndw,(255,0,0),bullet)
    for enemy in enemy_list: #iterates all enemies in the list
        enemy.movement(player) #calls each enemy's movement fucntion
        wndw.blit(enemy.get_pic(),(enemy.rectangle().x,enemy.rectangle().y)) #draws each enemy
    for enemy in enemy_bullets:
        pygame.draw.rect(wndw,(0,255,0),enemy.make_bullet())
    text = arial.render(str(score),1 , (255,255,255)) #creates text of the score with the colour of RGB code (255,255,255) (white)
    wndw.blit(text, (1000 - text.get_width(), 0 + text.get_height()/2)) #draws text in the top left corner
    pygame.display.update() #refreshes the screen

def movement(pressed, player): #handles movement
        if pressed[pygame.K_a] and player.x - speed > 0:
            player.x -= speed
        if pressed[pygame.K_d] and player.x + speed + player.width < 1000:
            player.x += speed
        if pressed[pygame.K_w] and player.y - speed > 0: 
            player.y -= speed
        if pressed[pygame.K_s] and player.y + speed + player.height < 600:
            player.y += speed

def bullets_handling(bullets,player,enemy_bullets): #handles player bullets
    for bullet in bullets: 
        bullet.x += bullets_speed
        if bullet.x > 1000: #removes bullets if they go off screen
            bullets.remove(bullet)
        for enemy in enemy_list: #iterates through all enemies
            if enemy.rectangle().colliderect(bullet): #if an enemy is hit with a bullet it takes damage
                enemy.damage()
                pygame.event.post(pygame.event.Event(enemy_hit)) #event for when an enemy takes damage
                if bullet in bullets:
                    bullets.remove(bullet)

    for enemy in enemy_bullets: #iterates through all enemies with bullets
        if player.colliderect(enemy.make_bullet()): #if the player collides with an enemy bullet
            enemy_bullets.remove(enemy) #bullet removed
            pygame.event.post(pygame.event.Event(player_hit)) #event for player getting hit occurs 

def collisions(player,enemy_list): #collisions subprogram
    for enemy in enemy_list: 
        if player.colliderect(enemy.rectangle()): #if an enemy hits player player_hit event occurs
            enemy.damage() 
            pygame.event.post(pygame.event.Event(player_hit))

def enemy_bullets_handling(enemy_bullets,boss_ig): #handles shooter enemy bullets
    for enemy in enemy_bullets:
        enemy.make_bullet().x -= enemy_bullet_speed #moves the bullet right at a constant speed
        if enemy.make_bullet().x < 0: #if the bullet goes off screen it is removed 
            enemy_bullets.remove(enemy) 
            enemy.bullet_edit(-1)

def draw_menu_text(text, font, colour, surface, x, y): #draws menu text
    text_obj = font.render(text, 1, colour) #creates the text 
    text_rect = text_obj.get_rect() #the length ,width and temporary coordiantes of the text
    text_rect.topleft = (x, y) #changes the x and y coordiantes of the text to the values passed into the subprogram
    surface.blit(text_obj, text_rect) #draws the text

def update_db(username,score,difficulty): #updates the database with the data from the last run
    database = sqlite3.connect('Scores.db') #links the program to the database 'Scores.db' (if it isn't present it creates the database then links)
    cursor = database.cursor() #used to execute SQL statements onto the database
    cursor.execute('''CREATE TABLE IF NOT EXISTS Scores ( 
ScoreID VARCHAR(4) NOT NULL,
Score INT(8) NOT NULL,
Difficulty VARCHAR(6) NOT NULL,
Player_Name VARCHAR(12) NOT NULL,
PRIMARY KEY (ScoreID)
)
''') #creates a database table ,if one is not already present, with the 4 listed columns
    cursor.execute('SELECT * FROM SCORES') #selects all data from the scores database
    items = cursor.fetchall() #defines items as all the data selected from the database
    if len(items) == 0:
        newID = 0 #makes newID 0 if the database was empty
    else:
        cursor.execute('SELECT MAX(scoreID) FROM SCORES')
        newID= int(cursor.fetchall()[0][0]) + 1 #if the database has a value in it, newID is set to a value one greater than the largest value in the table
    cursor.execute('''INSERT INTO Scores VALUES
    (?,?,?,?)''',(newID,score,difficulty,username)) #inserts the listed values into the database
    database.commit() #saves the changes to the database
    database.close() #closes the connection with the database


def game_over(score,difficulty): #creates the game over screen
    pygame.display.update() 
    text = arial.render('Game Over',1 , (0,0,0)) #creates text 'game over' with the colour of RGB code (0,0,0) (black)
    text2 = arial.render('Please Enter Your Name (12 characters max)',1 , (0,0,0)) #creates text 'game over' with the colour of RGB code (0,0,0) (black)
    text3 = arial.render('Press Enter When Done',1 , (0,0,0)) #creates text 'game over' with the colour of RGB code (0,0,0) (black)
    username = '' #stores the player inputs
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #used to stop the code running if the program is closed
                pygame.close()
            if event.type == pygame.KEYDOWN:
                if event.key == K_BACKSPACE: 
                    username = username[:-1] #removes the last character from username
                elif event.key == K_RETURN and len(username) > 0:
                    update_db(username,score,difficulty)
                    main_menu() #takes the user back to the main menu once they input a name then press enter
                elif len(username)<12:
                    username += event.unicode #edits username with key pressed
        username_text = arial.render(username,1 , (0,0,0))
        wndw.blit(aurora,(0,0)) #draws background image
        wndw.blit(text, (1000/2 - text.get_width() / 2, 600/2 - text.get_height()/2 - 100)) #draws text above the middle of screen
        wndw.blit(text2, (1000/2 - text2.get_width() / 2, 600/2 - text2.get_height()/2 - 50)) #draws text above the middle of screen
        wndw.blit(text3,(1000/2 - text3.get_width() /2, 600/2 - text3.get_height()/2 +50)) #draws text below the middle of screen
        wndw.blit(username_text,(1000/2 - username_text.get_width() /2, 600/2 - username_text.get_height()/2)) #draws player text in the middle of screen
        pygame.display.update() 
        
def main(difficulty_rate,difficulty_name): #main game loop
    global enemy_list
    global shooter_list
    player = pygame.Rect(100,300,55,40) #player rectangle
    bullets = [] #list of player bullets
    enemy_bullets = [] #list of enemys with bullets on screen
    enemy_counter = 0 #number of enemies in the game
    boss_ig = [] #boss enemy
    health = 3
    score = 0
    start_time = time.perf_counter()
    difficulty = (time.perf_counter()-start_time )/difficulty_rate 
    run = True
    clock = pygame.time.Clock()
    while run: #loop occurs while the game is running
        clock.tick(fps) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #used to stop the code running if the program is closed
                run = False
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE: #occurs when the space bar is pressed
                    bullet = pygame.Rect(player.x + 55,player.y + 20,10,5) 
                    bullets.append(bullet) 
            if event.type == player_hit:  #if the event for the player getting hit occurs health decreases by 1
                health -= 1
                if health <= 0: #if health is 0 or below gameover function called
                    makewindow(player,bullets,enemy_bullets,health,score) #calls the function to handle display 
                    game_over(score,difficulty_name)
            difficulty = (time.perf_counter()-start_time )/difficulty_rate
            for enemy in enemy_list: 
                        if enemy.get_health() <= 0:#if enemy has no health removes it from enemy_list
                            enemy_list.remove(enemy)
                            if enemy in shooter_list: #removes enemy from shooter list if it is a shooter
                                shooter_list.remove(enemy)
                                score +=300
                            elif enemy in boss_ig:
                                boss_ig.remove(enemy) #removed enemy from boss_ig if the enemy is a boss
                                score += 1000
                            else:
                                score += 500 #score for defeating a crasher
                            del enemy #removes enemy from the class
                            enemy_counter -= 1
            for enemy in shooter_list: 
                if round(enemy.rectangle().y,-2) == round(player.y,-2) and enemy.get_bullet_num() == 0: #if player on similar Y level to player and does not have a bullet on screen
                    enemy.make_bullet().x = enemy.rectangle().x 
                    enemy.make_bullet().y = enemy.rectangle().y 
                    enemy_bullets.append(enemy) #adds the enemy to a list showing all the enemies that have bullets on screen
                    enemy.bullet_edit(1) #adds a bullet to the enemy's bullet number
            for boss_enemy in boss_ig:
                if boss_enemy.get_bullet_num() == 0:
                    boss_enemy.make_bullet().x = boss_enemy.rectangle().x 
                    boss_enemy.make_bullet().y = boss_enemy.rectangle().y 
                    enemy_bullets.append(boss_enemy) #adds the enemy to a list showing all the enemies that have bullets on screen
                    boss_enemy.bullet_edit(1) #
            if enemy_counter < difficulty: #creates an enemy if the amount of enemies in the game is below the max
                enemy_type = random.randint(1,3) #used to determine which enemy spawns
                if enemy_type == 1:
                    enemy_created = shooters(1,ufoenemy,random.randint(400,900),random.randint(0,500),65,50,True,0) #creates a shooter enemy with a random spawn location
                    shooter_list.append(enemy_created)
                elif enemy_type == 2:
                        enemy_created = crashers(1,pygame.transform.rotate(ufoenemy,90),random.randint(400,900),random.randint(0,500),65,50) #creates a crasher enemy with a random spawn location
                elif enemy_type == 3:
                        if len(boss_ig) == 0 and difficulty > 4: 
                            enemy_created = boss(3,boss_sprite,random.randint(400,900),random.randint(0,500),65,50,0) #creates a boss enemy with a random spawn location
                            boss_ig.append(enemy_created)
                        else:
                            enemy_created = shooters(1,ufoenemy,random.randint(400,900),random.randint(0,500),65,50,True,0) #creates a shooter enemy with a random spawn location
                            shooter_list.append(enemy_created)
                enemy_list.append(enemy_created)
                enemy_counter += 1
    

        pressed = pygame.key.get_pressed() 
        bullets_handling(bullets,player,enemy_bullets) 
        makewindow(player,bullets,enemy_bullets,health,score)  
        movement(pressed,player) 
        enemy_bullets_handling(enemy_bullets,boss_ig) 
        collisions(player,enemy_list) 
    pygame.quit()

def difficulty_selection(): #creates the difficulty selection menu
    click = False
    while True:
        wndw.blit(menu_background,(0,0)) #draws background image
        draw_menu_text('Select Difficulty', arial, (255, 255, 255), wndw, 400, 20) #calls the subprogram to draw text at the top of the screen
        mx, my = pygame.mouse.get_pos() 
        button_1 = pygame.Rect(400, 200, 200, 50) #initialises buttons with their coordinates and dimensions
        button_2 = pygame.Rect(400, 300, 200, 50)
        button_3 = pygame.Rect(400, 400, 200, 50)
        button_4 = pygame.Rect(400, 500, 200, 50)
        if button_1.collidepoint((mx, my)): #checks if the mouse collides with the easy button
            if click:
                difficulty = 'Easy'
                main(20,difficulty)
        if button_2.collidepoint((mx, my)): #checks if the mouse collides with the medium button
            if click:
                difficulty = 'Medium'
                main(15,difficulty)
        if button_3.collidepoint((mx, my)): #checks if the mouse collides with the hard button
            if click:
                difficulty = 'Hard'
                main(10,difficulty)
        if button_4.collidepoint((mx, my)): #checks if the mouse collides with the back button
            if click:
                main_menu()
        draw_menu_text('Easy', arial, (255, 255, 255), wndw, 460, 200) #calls the function to draw the text for the buttons
        draw_menu_text('Medium', arial, (255, 255, 255), wndw, 440, 300)
        draw_menu_text('Hard', arial, (255, 255, 255), wndw, 460, 400)
        draw_menu_text('Back', arial, (255, 255, 255), wndw, 460, 500)
        click = False 
        for event in pygame.event.get():
            if event.type == KEYDOWN: #when escape is pressed the program closes
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == MOUSEBUTTONDOWN: #makes click true when the player clicks
                if event.button == 1:
                    click = True
            if event.type == pygame.QUIT: #used to stop the code running if the program is closed
                pygame.quit()
        pygame.display.update()
        pygame.time.Clock().tick(fps) #loop runs once every frame 

def highscores():#handles the highscores page
    click = False
    database = sqlite3.connect('Scores.db') #links the program to the database 'Scores.db' (if it isn't present it creates the database then links)
    cursor = database.cursor() #used to execute SQL statements onto the database
    cursor.execute('''CREATE TABLE IF NOT EXISTS Scores ( 
    ScoreID VARCHAR(4) NOT NULL,
    Score INT(8) NOT NULL,
    Difficulty VARCHAR(6) NOT NULL,
    Player_Name VARCHAR(12) NOT NULL,
    PRIMARY KEY (ScoreID)
    )''') #creates a database table ,if one is not already present, with the 4 listed columns
    cursor.execute('''SELECT Score, Difficulty, Player_name 
    FROM Scores
    ORDER BY Score DESC
    ''') #Selects the Score, Difficulty, Player_name from the Scores database and orders the values in descending order of score
    values = cursor.fetchall() #sets values to the data selected from the database
    while True:
        wndw.blit(menu_background,(0,0)) #draws background image
        draw_menu_text('Highscores', arial, (255, 255, 255), wndw, 420, 20) #calls the subprogram to draw text at the top of the screen
        mx, my = pygame.mouse.get_pos() #gets the coordinated of the mouse
        back_button = pygame.Rect(400, 500, 200, 50)
        if back_button.collidepoint((mx, my)): #checks if the mouse collides with the back button
            if click:
                database.close() #closes the connection with the database
                main_menu()
        draw_menu_text('Back', arial, (255, 255, 255), wndw, 450, 500) #calls the function to draw the text for the buttons
        click = False
        if len(values) < 5: #used to determine how many score values need to be drawb
            num = len(values)
        else:
            num = 5
        for x in range (0,num): #loop used to draw all the data needed from database onto the screen
            draw_menu_text(str(values[x][0]), arial, (255, 255, 255), wndw, 100, 200+(x*50))
            draw_menu_text(str(values[x][1]), arial, (255, 255, 255), wndw, 450, 200+(x*50))
            draw_menu_text(str(values[x][2]), arial, (255, 255, 255), wndw, 800, 200+(x*50))
        for event in pygame.event.get():
            if event.type == KEYDOWN: #when escape is pressed the program closes
                if event.key == K_ESCAPE:
                    database.close() #closes the connection with the database
                    main_menu()
            if event.type == MOUSEBUTTONDOWN: #makes click true when the player clicks
                if event.button == 1:
                    click = True
            if event.type == pygame.QUIT: #used to stop the code running if the program is closed
                pygame.quit()
        pygame.display.update()
        pygame.time.Clock().tick(fps) #loop runs once every frame 

def main_menu(): #creates the main menu
    click = False
    while True:
        wndw.blit(menu_background,(0,0)) #draws background image
        draw_menu_text('Volatile Void', arial, (255, 255, 255), wndw, 400, 20) #calls the subprogram to draw text at the top of the screen
        mx, my = pygame.mouse.get_pos() #coordinates of cursor
        button_1 = pygame.Rect(400, 200, 200, 50) #initialises buttons with their coordinates and dimensions
        button_2 = pygame.Rect(400, 300, 200, 50)
        button_3 = pygame.Rect(400, 400, 200, 50)
        if button_1.collidepoint((mx, my)): #checks if the mouse collides with the start button
            if click: #takes the user to the difficulty selection screen when the start button is clicked
                    difficulty_selection()
        if button_2.collidepoint((mx, my)): #checks if the mouse collides with the highscore button
            if click: #takes the user to the highscore screen when the highscore button is clicked
                highscores()
        if button_3.collidepoint((mx, my)): #checks if the mouse collides with the quit button
            if click: #closes the game when the quit button is clicked
                pygame.quit()
        draw_menu_text('Start', arial, (255, 255, 255), wndw, 460, 200) #calls the function to draw the text for the buttons
        draw_menu_text('Highscores', arial, (255, 255, 255), wndw, 410, 300)
        draw_menu_text('Quit', arial, (255, 255, 255), wndw, 460, 400)
        click = False  #sets click back to false 
        for event in pygame.event.get():
            if event.type == KEYDOWN: #when escape is pressed the program closes
                if event.key == ESCAPE: 
                    pygame.quit()
            if event.type == MOUSEBUTTONDOWN: #makes click true when the player clicks
                if event.button == 1:
                    click = True
            if event.type == pygame.QUIT: #used to stop the code running if the program is closed
                pygame.quit()
        pygame.display.update()
        pygame.time.Clock().tick(fps) #loop runs once every frame 

main_menu()

'''
def difficulty_selection(): #test for difficulty selection
    selection = str(input('input difficulty'))
    if selection = 'Easy':
        main(20)
    if selection = 'Medium':
        main(15)
    if selection = 'hard':
        main(10)
'''
