#8,5 Std

# Importieren u. initialisieren der Pygame-Bibliothek
import pygame
from pygame.locals import *
from random import shuffle
pygame.init()

# Variablen/KONSTANTEN setzen
EDGE = 10
FPS  = 60
BLACK = ( 0, 0, 0)
WHITE   = ( 255, 255, 255)
BACKGROUND_CARD = pygame.image.load("pics/UI/2.png")
COVER_CARD = pygame.image.load("pics/UI/4.png")
MAP_WIDTH = 6
MAP_HEIGHT = 4
FONTSIZE = 40
BUTTTON_CLICK_OFFSET = 3
W = BACKGROUND_CARD.get_rect().width * MAP_WIDTH + EDGE * MAP_WIDTH + EDGE
H = BACKGROUND_CARD.get_rect().height * MAP_HEIGHT + EDGE * MAP_HEIGHT + EDGE + FONTSIZE
shown_cards = 0
game_over = True

# für Textausgabe
font = pygame.font.Font(None, FONTSIZE)


# Definieren und Öffnen eines neuen Fensters
pygame.display.set_caption("Memory")
clock = pygame.time.Clock()

fenster = pygame.display.set_mode((W, H))

# Create card-variables
icons = []
for i in range(1, 13):
    icons.append({"icon_num": i, "surface": pygame.image.load("pics/ico/" + str(i) + ".png").convert_alpha(), "sprite": None, "hidden": True, "match": False})
    icons.append({"icon_num": i, "surface": pygame.image.load("pics/ico/" + str(i) + ".png").convert_alpha(), "sprite": None, "hidden": True, "match": False})

shuffle(icons)

selected_card = 0
selected_sprite = None

# Schleife Hauptprogramm
while True:
    # Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        # Beenden bei [ESC] oder [X]
        if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
            pygame.quit()

        # handle MOUSEBUTTONUP
        if event.type == pygame.MOUSEBUTTONUP:
            if shown_cards == 2:
                for i in range(len(icons)):
                    icons[i]["hidden"] = True

                shown_cards = 0
                selected_card = 0
                selected_sprite = None
            else:
                pos = pygame.mouse.get_pos()
                for icon in icons:
                    if icon["sprite"].collidepoint(pos) and not icon["match"]:
                        if selected_sprite != icon["sprite"]:
                            if shown_cards == 0:
                                icon["hidden"] = False
                                selected_card = icon["icon_num"]
                                selected_sprite = icon["sprite"]
                                selected_sprite.left = selected_sprite.left + BUTTTON_CLICK_OFFSET
                                selected_sprite.top = selected_sprite.top + BUTTTON_CLICK_OFFSET
                                
                                shown_cards = shown_cards + 1

                            elif shown_cards == 1:
                                # Check if other card has same icon_num
                                if icon["icon_num"] == selected_card:
                                    icon["match"] = True
                                    for j in icons:
                                        if j["icon_num"] == icon["icon_num"] :
                                            j["match"] = True

                                        shown_cards = 0
                                        selected_card = 0
                                        selected_sprite = None
                                else:      
                                    icon["hidden"] = False    
                                    shown_cards = shown_cards + 1

    # Spiellogik
    matchcount = 0
    for icon in icons:
        if icon["match"]:
            matchcount = matchcount + 1

    if matchcount == len(icons):
        game_over = True

    # Spielfeld löschen
    fenster.fill(BLACK)

    # Spielfeld/figuren zeichnen
    if game_over:
        inhalt2 = "Game Over!"
        text2 = font.render(inhalt2, 1, WHITE)
        fenster.blit(text2, (W / 2 - text2.get_width() / 2, H / 2 - text2.get_height() / 2))
        
    else:
        if selected_card == 0:
            selected_card = ""

        else:
            inhalt = "Card selected: {}".format(selected_card)
            text = font.render(inhalt, 1, WHITE)
            fenster.blit(text, (20,20))

        

        image_count = 0
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                if not icons[image_count]["match"]:                
                    if icons[image_count]["hidden"]:
                        sprite = fenster.blit(COVER_CARD, (EDGE + BACKGROUND_CARD.get_rect().width * x + EDGE * x ,
                        EDGE + BACKGROUND_CARD.get_rect().height * y + EDGE * y + FONTSIZE))

                    else:
                        sprite = fenster.blit(BACKGROUND_CARD, (EDGE + BACKGROUND_CARD.get_rect().width * x + EDGE * x + BUTTTON_CLICK_OFFSET,
                        EDGE + BACKGROUND_CARD.get_rect().height * y + EDGE * y + FONTSIZE + BUTTTON_CLICK_OFFSET))

                        fenster.blit(icons[image_count]["surface"], (EDGE + ((BACKGROUND_CARD.get_rect().width - icons[image_count]["surface"].get_rect().width) / 2) + BACKGROUND_CARD.get_rect().width * x + EDGE * x + BUTTTON_CLICK_OFFSET,
                        EDGE + (BACKGROUND_CARD.get_rect().height - icons[image_count]["surface"].get_rect().height) / 2 + BACKGROUND_CARD.get_rect().height * y + EDGE * y + FONTSIZE + BUTTTON_CLICK_OFFSET))

                    icons[image_count]["sprite"] = sprite

                image_count = image_count + 1

    # Fenster aktualisieren
    pygame.display.flip()
    clock.tick(FPS)