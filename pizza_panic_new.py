# Pizza Panic
# Player must catch falling pizzas before they hit the ground

from livewires import games, color
import random

games.init(screen_width = 640, screen_height = 480, fps = 50)

class Pan(games.Sprite):
	"""
	A pan controlled by player to catch falling pizzas.
	"""
	image = games.load_image("pan.bmp")

	def __init__(self):
		""" Initialize Pan object and create Text object for score. """
		super(Pan, self).__init__(image = Pan.image,
								  x = games.mouse.x,
								  bottom = games.screen.height)
		
		self.score = games.Text(value = 0, size = 25, color = color.black,
								top = 5, right = games.screen.width - 10)

		games.screen.add(self.score)
		

	def update(self):
		""" Move to mouse x position. """
		self.x = games.mouse.x
		
		if self.left < 0:
			self.left = 0
			
		if self.right > games.screen.width:
			self.right = games.screen.width
			
		self.check_catch()

	def check_catch(self):
		""" Check if catch pizzas. """
		for pizza in self.overlapping_sprites:
			if pizza.which_image == 0:
                                self.score.value += 10
			elif pizza.which_image == 1:
                                self.score.value += 25
			self.score.right = games.screen.width - 10 
			pizza.handle_caught()


class Pizza(games.Sprite):
	"""
	A pizza which falls to the ground.
	""" 
	image = games.load_image("pizza.bmp")
	fast_pizza = games.load_image("fast_pizza.bmp")
	dont_click_pizza = games.load_image("dont_click.bmp")
	speed = 1
	fast_pizza_speed = 2.5
	dont_click_pizza_speed = 1.5
	miss_limit = games.Text(value = 3, size = 25, color = color.black, top = 5, right = games.screen.width - 50)
	games.screen.add(miss_limit)
	

	def __init__(self, x, y = 90, which_image = 0):
                """ Initialize a Pizza object. """
                if which_image == 0:
                        super(Pizza, self).__init__(image = Pizza.image,x = x, y = y,dy = Pizza.speed)
                elif which_image == 1:
                        super(Pizza, self).__init__(image = Pizza.fast_pizza,x = x, y = y,dy = Pizza.fast_pizza_speed)
                elif which_image == 2:
                        super(Pizza, self).__init__(image = Pizza.dont_click_pizza,x =x, y = y, dy = Pizza.dont_click_pizza_speed)
                self.which_image = which_image
                

	def update(self):
		""" Check if bottom edge has reached screen bottom. """
		if self.bottom > games.screen.height:
                        if self.which_image != 2:
                                if Pizza.miss_limit.value > 0:
                                        Pizza.miss_limit.value -= 1
                                if Pizza.miss_limit.value == 0:
                                        self.end_game()

                        self.destroy()

	def handle_caught(self):
		""" Destroy self if caught. """
		if self.which_image == 2:
                        if Pizza.miss_limit.value > 0:
                                Pizza.miss_limit.value -= 1
                        if Pizza.miss_limit.value == 0:
                                self.end_game()

                        
		self.destroy()

	def end_game(self):
		""" End the game. """
		end_message = games.Message(value = "Game Over",
									size = 90,
									color = color.red,
									x = games.screen.width/2,
									y = games.screen.height/2,
									lifetime = 5 * games.screen.fps,
									after_death = games.screen.quit)
		games.screen.add(end_message)

		
class Chef(games.Sprite):
	"""
	A chef which moves left and right, dropping pizzas.
	"""
	image = games.load_image("chef.bmp")
	mad_chef = games.load_image("madchef.bmp")

	def __init__(self, y = 55, speed = 2, odds_change = 200, which_chef = 0):
		""" Initialize the Chef object. """
		if which_chef == 0:
        		super(Chef, self).__init__(image = Chef.image,
								   x = games.screen.width / 2,
								   y = y,
								   dx = speed)
		elif which_chef == 1:
        		super(Chef, self).__init__(image = Chef.mad_chef,
								   x = games.screen.width / 2,
								   y = y,
								   dx = speed+3)

		
		self.odds_change = odds_change
		self.time_til_drop = 0


	def update(self):
		""" Determine if direction needs to be reversed. """
		if self.left < 0 or self.right > games.screen.width:
			self.dx = -self.dx
		elif random.randrange(self.odds_change) == 0:
		   self.dx = -self.dx
				
		self.check_drop()


	def check_drop(self):
		""" Decrease countdown or drop pizza and reset countdown. """
		if self.time_til_drop > 0:
			self.time_til_drop -= 1
		else:
                        #Pizza.speed = random.randrange(1,3)
                        ran = random.randint(0,2)
                        if ran == 0:
                                new_pizza = Pizza(x = self.x)
                                games.screen.add(new_pizza)
                        elif ran == 1:
                                new_pizza = Pizza(x = self.x, which_image = 1)
                                games.screen.add(new_pizza)
                        elif ran == 2:
                                new_pizza = Pizza(x = self.x, which_image = 2)
                                games.screen.add(new_pizza)
                                
			# set buffer to approx 30% of pizza height, regardless of pizza speed
                        self.time_til_drop = int(new_pizza.height * 1.3 / Pizza.speed) + 1


def main():
	""" Play the game. """
	wall_image = games.load_image("wall.bmp", transparent = False)
	games.screen.background = wall_image

        
	the_chef = Chef()
	the_chef1 = Chef(55,2,200,1)
	games.screen.add(the_chef)
	games.screen.add(the_chef1)

	the_pan = Pan()
	games.screen.add(the_pan)

	games.mouse.is_visible = False

	#games.screen.event_grab = True
	games.screen.mainloop()

# start it up!
main()
