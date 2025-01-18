import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(True)  # Make the mouse pointer visible
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.start_game = False  # New flag to check if the game has started
        self.font = pg.font.Font(None, 74)  # Font for text
        self.background_image = pg.transform.scale(pg.image.load("main.png"), RES)  # Load and scale background image

    def display_start_screen(self):
        """Displays the start screen with buttons."""
        while not self.start_game:
            self.screen.blit(self.background_image, (0, 0))  # Draw the scaled background image to cover the screen
            
            # Display title text
            title_text = self.font.render("EWUianFPS", True, (255, 255, 0))
            dedicated_text = self.font.render("Dedicated to DTBI Sir", True, (255, 255, 0))
            start_button_text = self.font.render("Start", True, (0, 0, 0))
            exit_button_text = self.font.render("Exit", True, (0, 0, 0))
            group_text = pg.font.Font(None, 50).render("Created By Group 1", True, (255, 255, 0))
            names = ["Md. Azharul Islam", "Azizur Rahman", "Litaz Anwar Saif", "Samir Hassan", "Miftahul Kamal Jannat"]

            # Draw the title
            title_rect = title_text.get_rect(center=(RES[0] // 2, RES[1] // 5))
            dedicated_rect = dedicated_text.get_rect(center=(RES[0] // 2, RES[1] // 5 + 80))  # Added more space below the title
            self.screen.blit(title_text, title_rect)
            self.screen.blit(dedicated_text, dedicated_rect)

            # Draw the start button
            start_button_rect = pg.Rect(RES[0] // 2 - 100, RES[1] // 2 - 40, 200, 60)
            pg.draw.rect(self.screen, (255, 255, 255), start_button_rect)
            start_button_text_rect = start_button_text.get_rect(center=start_button_rect.center)
            self.screen.blit(start_button_text, start_button_text_rect)

            # Draw the exit button
            exit_button_rect = pg.Rect(RES[0] // 2 - 100, RES[1] // 2 + 40, 200, 60)
            pg.draw.rect(self.screen, (255, 255, 255), exit_button_rect)
            exit_button_text_rect = exit_button_text.get_rect(center=exit_button_rect.center)
            self.screen.blit(exit_button_text, exit_button_text_rect)

            # Draw the group text
            group_text_rect = group_text.get_rect(center=(RES[0] // 2, RES[1] * 3 // 4))
            self.screen.blit(group_text, group_text_rect)

            # Draw names below group text
            for i, name in enumerate(names):
                name_text = pg.font.Font(None, 36).render(name, True, (255, 255, 0))
                name_rect = name_text.get_rect(center=(RES[0] // 2, RES[1] * 3 // 4 + 50 + i * 30))
                self.screen.blit(name_text, name_rect)

            # Check for events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if start_button_rect.collidepoint(event.pos):
                        self.start_game = True
                        self.new_game()
                    elif exit_button_rect.collidepoint(event.pos):
                        pg.quit()
                        sys.exit()

            pg.display.flip()
            self.clock.tick(60)

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def game_over(self):
        """Handles game over or returning to the main menu."""
        self.start_game = False
        self.display_start_screen()

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.object_renderer.draw()
        self.weapon.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.game_over()  # Return to the main menu
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        self.display_start_screen()  # Display the start screen
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()

