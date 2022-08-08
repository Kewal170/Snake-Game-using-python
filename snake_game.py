import pygame
import random
import os
pygame.mixer.init()
pygame.init()                #compulsory to write this


white = (255 , 255 , 255)    # colours   rgb number is there no tension
red = (255 , 0 , 0)
black = (0 , 0 , 0)

screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width,screen_height))   #made screen

#back ground
bgimg = pygame.image.load("1snakegamebg.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width,screen_height)).convert_alpha()


pygame.display.set_caption("Snakes With Kewal")        #add title
pygame.display.update()                                 #update
clock = pygame.time.Clock()                     # clock
font = pygame.font.SysFont(None,45) # (text style , text size)
 
def text_screen(text,color,x,y):                  #score print
	screen_text = font.render(text,True,color)
	gameWindow.blit(screen_text, [x,y] )

def plot_snake(gameWindow , color , snk_list , snake_size):
	for x,y in snk_list:
		pygame.draw.rect(gameWindow , color , [x , y , snake_size , snake_size]) # creating snake
	
def welcome():
	exit_game = False
	while not exit_game:
		gameWindow.fill((233,200,220))
		text_screen("Welcome to Snakes", black , 300 , 160)
		text_screen("Press  SpaceBar  to  Play",black , 260 , 200)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit_game = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					gameloop()

		pygame.display.update()
		clock.tick(60)

def gameloop():
	#########      declaring variables
	exit_game = False
	game_over = False
	snake_x = 45
	snake_y = 55
	velocity_x = 0
	velocity_y = 0
	snk_list = []
	snk_length = 1
	if(not os.path.exists("hiscore.txt")):
		with open("hiscore.txt",'w') as f:
			f.write("0")
	with open("hiscore.txt") as f:
		hiscore = f.read()

	food_x = random.randint(20 , screen_width/2)
	food_y = random.randint(20 , screen_height/2)
	score = 0
	init_velocity = 4
	snake_size = 15
	fps = 60

	while not exit_game:
		if game_over:
			with open("hiscore.txt",'w') as f:
				f.write(str(hiscore))

			gameWindow.fill((233,200,220))
			text_screen("Game Over!", red , 350 , 100)
			text_screen("Press Enter to Continue", red , 270 , 180)

			for event in pygame.event.get():             # quit      
				if event.type == pygame.QUIT:
					exit_game = True
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						welcome()
					
		else:
			for event in pygame.event.get():             # quit      
				if event.type == pygame.QUIT:
					exit_game = True

				if event.type == pygame.KEYDOWN:        
					if event.key == pygame.K_RIGHT:       # move right
						velocity_x = +init_velocity
						velocity_y = 0
					if event.key == pygame.K_LEFT:       # move left
						velocity_x = -init_velocity
						velocity_y = 0
					if event.key == pygame.K_UP:         # move up
						velocity_y = -init_velocity
						velocity_x = 0
					if event.key == pygame.K_DOWN:       # move down
						velocity_y = +init_velocity
						velocity_x = 0

					if event.key == pygame.K_2:
						init_velocity = init_velocity + 0.5
					if event.key == pygame.K_1:
						init_velocity = init_velocity - 0.5
					if event.key == pygame.K_3:
						snk_length += 8



			snake_x += velocity_x
			snake_y += velocity_y

			if abs(snake_x - food_x)<14 and abs(snake_y - food_y)<14:
				pygame.mixer.music.load('foodeating.wav')
				pygame.mixer.music.play()
				score += 10
				food_x = random.randint(20 , screen_width/2)
				food_y = random.randint(20 , screen_height/2)
				snk_length += 5
				if score > int(hiscore):
					hiscore = score

			gameWindow.fill(white) #made window white
			gameWindow.blit(bgimg,(0,0))
			text_screen(f"Score : {str(score)} ", red , 5 , 5 )  # (text,color,x,y)
			text_screen(f"HighScore : {str(hiscore)}",red, 600 , 5)
			pygame.draw.rect(gameWindow , red , [food_x , food_y , snake_size , snake_size])     # creating food

			head = []
			head.append(snake_x)
			head.append(snake_y)
			snk_list.append(head)

			if len(snk_list) > snk_length:
				del snk_list[0]

			if head in snk_list[:-1]:
				pygame.mixer.music.load('gameover.wav')
				pygame.mixer.music.play()
				game_over = True

			if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
				pygame.mixer.music.load('gameover.wav')
				pygame.mixer.music.play()
				game_over = True
			plot_snake(gameWindow,black, snk_list , snake_size)
		pygame.display.update()
		clock.tick(fps)


	pygame.quit()
	quit()
welcome()