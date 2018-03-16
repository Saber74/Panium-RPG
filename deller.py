import pygame
import pytmx

pygame.init()


display_width = 800
display_height = 800

white = (255, 255, 255)

gameScreen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('2d Game')
clock = pygame.time.Clock()
gameScreen.fill(white)
# load map data
gameMap = pytmx.load_pygame('desert.tmx')

def game_loop():
    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               gameExit = True

    # draw map data on screen
    for layer in gameMap.visible_layers:
        for x, y, gid, in layer:
            tile = gameMap.get_tile_image_by_gid(gid)
            gameScreen.blit(tile, (x * gameMap.tilewidth,
                                   y * gameMap.tileheight))
    pygame.display.update()
    clock.tick(30)

game_loop()
pygame.quit()