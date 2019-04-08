import pygame

# Screen Dimensions
screenTitle = 'Cross Da Road'
screenWidth = 800
screenHeight = 800
# General colors to fill screen - RGB 
colorWhite = (255, 255, 255)
colorBlack = (0, 0, 0)
# Clock used to update game events and frames
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)


class Game:

    # Typical rate of 60, equivalent to FPS
    tickRate = 60
    # Initializer for the game class to set up the dimensions 
    def __init__(self, imagePath, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        # Create the window of specified size in white to display the game
        self.gameScreen = pygame.display.set_mode((width, height))
        # Set the game window color to white
        self.gameScreen.fill(colorWhite)
        pygame.display.set_caption(title)

        # Load and set the background image for the scene
        backgroundImage = pygame.image.load(imagePath)
        self.image = pygame.transform.scale(backgroundImage, (width, height))

    def runGameLoop(self, levelSpeed):
        isGameOver = False
        didWin = False
        direction = 0

        playerCharacter = PlayerCharacter('Character.png', 375, 673, 50, 80)
        enemy0 = NonPlayerCharacter('enemy.png', 20, 600, 50, 50) 
        # Speed increased as we advance in difficulty
        enemy0.speed *= levelSpeed

        # Create another enemy
        enemy1 = NonPlayerCharacter('enemy.png', self.width - 40, 400, 50, 50)
        enemy1.speed *= levelSpeed

        # Create another enemy
        enemy2 = NonPlayerCharacter('enemy.png', 20, 200, 50, 50)
        enemy2.speed *= levelSpeed

        treasure = GameObject('treasure.png', 375, 50, 50, 50)

        # Main game loop, used to update all gameplay such as movement, checks, and graphics
        # Runs until isGameOver = True
        while not isGameOver:

            # A loop to get all of the events occuring at any given time
            # Events are most often mouse movement, mouse and button clicks, or exit events
            for event in pygame.event.get():
                # If we have a quite type event (exit out) then exit out of the game loop
                if event.type == pygame.QUIT:
                    isGameOver = True
                # Detect when key is pressed down
                elif event.type == pygame.KEYDOWN:
                    # Move up if up key pressed
                    if event.key == pygame.K_UP:
                        direction = 1
                    # Move down if down key pressed
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                # Detect when key is released
                elif event.type == pygame.KEYUP:
                    # Stop movement when key no longer pressed
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0
                print(event)

            # Redraw the screen to be a blank white window
            self.gameScreen.fill(colorWhite)
            # Draw the image onto the background
            self.gameScreen.blit(self.image, (0, 0))

            # Draw the treasure
            treasure.draw(self.gameScreen)

            # Update the player position
            playerCharacter.move(direction, self.height)
            # Draw the player at the new position
            playerCharacter.draw(self.gameScreen)

            # Move and draw the enemy character
            enemy0.move(self.width)
            enemy0.draw(self.gameScreen)

            # Move and draw more enemies when we reach higher levels of difficulty
            if levelSpeed > 2:
                enemy1.move(self.width)
                enemy1.draw(self.gameScreen)
            if levelSpeed > 4:
                enemy2.move(self.width)
                enemy2.draw(self.gameScreen)

            # End game if collision between enemy and treasure
            # Close game if we lose
            # Restart game loop if we win
            if playerCharacter.detectCollision(enemy0):
                isGameOver = True
                didWin = False
                text = font.render('You lose! :(', True, colorBlack)
                self.gameScreen.blit(text, (275, 350))
                pygame.display.update()
                clock.tick(1)
                break
            elif playerCharacter.detectCollision(treasure):
                isGameOver = True
                didWin = True
                text = font.render('You win! :)', True, colorBlack)
                self.gameScreen.blit(text, (275, 350))
                pygame.display.update()
                clock.tick(1)
                break

            # Update all game graphics
            pygame.display.update()
            # Tick the clock to update everything within the game
            clock.tick(self.tickRate)

        # Restart game loop if we won
        # Break out of game loop and quit if we lose
        if didWin:
            self.runGameLoop(levelSpeed + 0.5)
        else:
            return


# Generic game object class to be subclassed by other objects in the game
class GameObject:

    def __init__(self, imagePath, x, y, width, height):
        objectImage = pygame.image.load(imagePath)
        # Scale the image up
        self.image = pygame.transform.scale(objectImage, (width, height))

        self.xPos = x
        self.yPos = y

        self.width = width
        self.height = height

    # Draw the object by blitting it onto the background (game screen)
    def draw(self, background):
        background.blit(self.image, (self.xPos, self.yPos))


# Class to represent the character contolled by the player
class PlayerCharacter(GameObject):

    # How many tiles the character moves per second
    speed = 10

    def __init__(self, imagePath, x, y, width, height):
        super().__init__(imagePath, x, y, width, height)

    # Move function will move character up if direction > 0 and down if < 0
    def move(self, direction, maxHeight):
        if direction > 0:
            self.yPos -= self.speed
        elif direction < 0:
            self.yPos += self.speed
        # Make sure the character never goes past the bottom of the screen
        if self.yPos >= maxHeight - 40:
            self.yPos = maxHeight - 40

    # Return False (no collision) if y positions and x positions do not overlap
    # Return True x and y positions overlap
    def detectCollision(self, otherBody):
        if self.yPos > otherBody.yPos + otherBody.height:
            return False
        elif self.yPos + self.height < otherBody.yPos:
            return False

        if self.xPos > otherBody.xPos + otherBody.width:
            return False
        elif self.xPos + self.width < otherBody.xPos:
            return False

        return True


# Class to represent the enemies moving horizontally
class NonPlayerCharacter(GameObject):

    # How many tiles the character moves per second
    speed = 10

    def __init__(self, imagePath, x, y, width, height):
        super().__init__(imagePath, x, y, width, height)

    # Move function will move character right once it hits the far left of the
    # screen and left once it hits the far right of the screen
    def move(self, maxWidth):
        if self.xPos <= 20:
            self.speed = abs(self.speed)
        elif self.xPos >= maxWidth - 40:
            self.speed = -abs(self.speed)
        self.xPos += self.speed


pygame.init()

newGame = Game('background.png', screenTitle, screenWidth, screenHeight)
newGame.runGameLoop(1)

# Quit pygame and the program
pygame.quit()
quit()
