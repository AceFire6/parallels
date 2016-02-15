import pygame
from pygame import Color, display

from ui import UIGroup, UIText
from utils import center_element_x


class MainMenu(UIGroup):
    def __init__(self):
        super(MainMenu, self).__init__(0, 0, 'main_menu')
        self.setup_menu()
        self.in_help = False

    def setup_menu(self):
        y = 0
        heading_colour = Color('aquamarine')

        menu_group = UIGroup(0, 0, 'menu')
        heading = UIText('Parallels', 0, 0, 'heading', 120, heading_colour)
        y += heading.get_height() + 20
        start = UIText('Start', 0, y, 'start_btn', 80)
        y += start.get_height() + 20
        help = UIText('Help', 0, y, 'help_btn', 80)
        y += help.get_height() + 20
        exit = UIText('Exit', 0, y, 'exit_btn', 80)

        menu_group.add_element(heading)

        for element in [start, help, exit]:
            element.x = center_element_x(element, heading.get_width()).x
            menu_group.add_element(element)

        width = pygame.display.get_surface().get_width()
        menu_group.set_position(center_element_x(heading, width).x, 80)

        self.add_element(menu_group)

        help_group = UIGroup(0, 0, 'help_screen')
        y = 0
        heading = UIText('Help', 0, 0, 'help_heading', 100, heading_colour)
        y += heading.get_height() + 20
        texts = [
            'Connect all of the terminal pairs to finish the level.',
            'R: Restart', 'Esc: Return to the main menu.',
            'Right Click: Select and place terminal connectors.',
            'Left Click: Cancel the current line\'s construction.',
        ]
        help_group.add_element(heading)
        for text in texts:
            instruction = UIText(text, 0, y, '', 30)
            y += instruction.get_height() + 5
            help_group.add_element(instruction)

        help_group.set_position(50, 80)
        help_group.hide()
        self.add_element(help_group)

    def render(self):
        screen = pygame.display.get_surface()

        screen.fill((0, 0, 0))

        for element in self.elements:
            if not element.hidden:
                if type(element) == UIGroup:
                    for el in element.elements:
                        screen.blit(el.rendered_text, el.pos)
                else:
                    screen.blit(element.rendered_text, element.pos)

    def handle_click(self, mouse_pos):
        element = self.get_element_by_pos(mouse_pos)

        if not self.in_help and element:
            if element.name == 'start_btn':
                self.hide()
            elif element.name == 'help_btn':
                self.get_element_by_name('help_screen').show()
                self.in_help = True
                self.get_element_by_name('menu').hide()
            elif element.name == 'exit_btn':
                return False
        return True
