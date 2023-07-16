import pygame
import time
import random
import sys


class Button:

    def __init__(self, text, width, height, pos, col, elev, screen, flag, meaning, button=None):
        self.text = text
        self.elev = elev
        self.flag = flag
        self.meaning = meaning
        self.button = button
        self.dynamic_elev = elev
        self.screen = screen
        self.original_pos = pos[1]
        self.top_color = col
        self.old_color = col
        self.pressed = False
        self.is_known = False

        gui_font = pygame.font.Font(None, 30)
        self.top_rect = pygame.Rect(pos, (width, height))
        self.text_surf = gui_font.render(text, True, "#FFFFFF")
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        self.bottom_rect = pygame.Rect(pos, (width, elev))
        self.bottom_color = (70, 70, 120)

    def draw(self):
        self.top_rect.y = self.original_pos - self.dynamic_elev
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elev
        r1 = self.bottom_color[0]
        g1 = self.bottom_color[1]
        b1 = self.bottom_color[2]
        pygame.draw.rect(self.screen, (r1, g1, b1), self.bottom_rect, border_radius=12)
        r = self.top_color[0]
        g = self.top_color[1]
        b = self.top_color[2]
        pygame.draw.rect(self.screen, (r, g, b), self.top_rect, border_radius=12)
        self.screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = (180, 30, 40)
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elev = 0
                self.pressed = True
            else:
                self.dynamic_elev = self.elev
                if self.pressed == True:
                    self.pressed = False
        else:
            self.pressed = False
            self.dynamic_elev = self.elev
            self.top_color = self.old_color


class Simu:

    def __init__(self, words, choice):
        self.score = 0
        pygame.init()
        self.words = words
        random_img = random.choice(["img (1).jpg", "img (2).jpg", "img (3).jpg"])
        if choice == "phrase":
            self.screen = pygame.display.set_mode((1400, 700))
            background = pygame.image.load(f"images\\{random_img}")
            self.back_img = pygame.transform.scale(background, (1400, 700))
        else:
            self.screen = pygame.display.set_mode((1000, 700))
            background = pygame.image.load(f"images\\{random_img}")
            self.back_img = pygame.transform.scale(background, (1000, 700))


    def set_up(self):
        pygame.display.set_caption("Simulation")
        icon = pygame.image.load("gamepad.png")
        pygame.display.set_icon(icon)
        self.create_picture(self.words)

    def box(self, x, y, img):
        self.screen.blit(img, (x, y))

    def create_picture(self, words):
        x_axis = 100
        name = words[0][0]
        meaning = words[0][1]
        shape, color = get_shape_color(words[0])
        sp_color = get_color(color)
        # word2
        name2 = words[1][0]
        meaning2 = words[1][1]
        shape2, color2 = get_shape_color(words[1])
        sp_color2 = get_color(color2)
        # word3
        name3 = words[2][0]
        meaning3 = words[2][1]
        shape3, color3 = get_shape_color(words[2])
        sp_color3 = get_color(color3)

        clock = pygame.time.Clock()
        # left
        temp_list = list()
        answer_diction_1 = {}
        answer_diction_2 = {}

        for i in range(3):
            answer_diction_1[words[i][1]] = words[i][0]
            answer_diction_2[words[i][0]] = words[i][1]
            temp_list.append(words[i][1])


        secret1 = random.choice(temp_list)
        temp_list.remove(secret1)

        secret2 = random.choice(temp_list)
        temp_list.remove(secret2)

        secret3 = random.choice(temp_list)
        temp_list.remove(secret3)

        button1 = Button(name, 300, 90, (50, 100), sp_color, 6, self.screen, meaning,1)
        button2 = Button(name2, 300, 90, (50, 300), sp_color2, 6, self.screen, meaning2, 1)
        button3 = Button(name3, 300, 90, (50, 500), sp_color3, 6, self.screen, meaning3, 1)
        # right
        inputs = [button1, button2, button3]

        if len(secret1) < 20:
            button4 =  Button(secret1, 300, 90, (550, 100), (40, 40, 40), 6, self.screen, answer_diction_1[secret1], 2,
                              get_word(inputs, answer_diction_1[secret1]))
        else:
            button4 = Button(secret1, 300 * (len(secret1)/25), 90, (550, 100), (40, 40, 40), 6,
                             self.screen, answer_diction_1[secret1], 2,
                             get_word(inputs, answer_diction_1[secret1]))

        if len(secret2) < 20:
            button5 = Button(secret2, 300, 90, (550, 300), (40, 40, 40), 6, self.screen, answer_diction_1[secret2], 2,
                             get_word(inputs, answer_diction_1[secret2]))
        else:
            button5 = Button(secret2, 300 * (len(secret2)/25), 90, (550, 300), (40, 40, 40), 6, self.screen,
                             answer_diction_1[secret2], 2, get_word(inputs, answer_diction_1[secret2]))

        if len(secret3) < 20:
            button6 = Button(secret3, 300, 90, (550, 500), (40, 40, 40), 6, self.screen, answer_diction_1[secret3], 2,
                             get_word(inputs, answer_diction_1[secret3]))
        else:
            button6 = Button(secret3, 300 * (len(secret3)/25), 90, (550, 500), (40, 40, 40), 6, self.screen,
                             answer_diction_1[secret3], 2, get_word(inputs, answer_diction_1[secret3]))
        current_clicked = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
            self.screen.blit(self.back_img, (0, 0))
            if not button1.is_known:
                print(button1.text, " is not known")
                button1.draw()
            if not button2.is_known:
                print(button2.text, " is not known")
                button2.draw()
            if not button3.is_known:
                print(button3.text, " is not known")
                button3.draw()

            if (button4 is not None) and button4.button != current_clicked:
                print(button4.text, " is not None")
                button4.draw()
            elif (button4 is not None) and button4.button == current_clicked:
                current_clicked.is_known = True
                button4.is_known = True

            if (button5 is not None) and button5.button != current_clicked:
                print(button5.text, " is not None")
                button5.draw()
            elif (button5 is not None) and button5.button == current_clicked:
                current_clicked.is_known = True
                button5.is_known = True

            if (button6 is not None) and button6.button != current_clicked:
                print(button6.text, " is not None")
                button6.draw()
            elif (button6 is not None) and button6.button == current_clicked:
                current_clicked.is_known = True
                button6.is_known = True

            if button1.pressed:
                print(button1.text, " is clicked")
                current_clicked = button1
            elif button2.pressed:
                print(button2.text, " is clicked")
                current_clicked = button2
            elif button3.pressed:
                print(button3.text, " is clicked")
                current_clicked = button3

            if current_clicked is not None:
                print("Current clicked button is ", current_clicked)
                if (button4 is not None) and button4.pressed:
                    print(button4.text," is pressed")
                    if button4.text == current_clicked:
                        print(button4.text, current_clicked)
                        button4.is_known = True
                        print(button4.text, inputs, answer_diction_1)
                        self.score += 50
                        button4.pressed = False
                        button4 = None
                    else:
                        self.score -= 5
                    current_clicked = None

                if (button5 is not None) and button5.pressed:
                    print(button4.text," is pressed")
                    if button5.text == current_clicked:
                        print(button5.text, current_clicked)
                        button5.is_known = True
                        print(button5.text, inputs, answer_diction_1)
                        self.score += 50
                        button5.pressed = False
                        button5 = None
                    else:
                        self.score -= 5
                    current_clicked = None

                if (button6 is not None) and button6.pressed:
                    print(button4.text, " is pressed")
                    if button6.text == current_clicked:
                        print(button6.text, current_clicked)
                        button6.is_known = True
                        print(button6.text, inputs, answer_diction_1)
                        self.score += 50
                        button6.pressed = False
                        button6 = None
                    else:
                        self.score -= 5
                    current_clicked = None

                adjust(inputs)

            print("Current after if-else: ", current_clicked, "\n")
            boolean = (button1.is_known and button2.is_known and button3.is_known
                       and (button4 is None) and (button5 is None) and (button6 is None))
            if boolean:
                break
            pygame.display.update()
            clock.tick(60)

def get_shape_color(word):
    shape, color = None, None
    if len(word) == 6:
        shape = word[4]
        color = word[5]
    elif len(word) == 7:
        shape = word[5]
        color = word[6]
    elif len(word) == 8:
        shape = word[6]
        color = word[7]
    return shape, color

def get_color(color):
    color_splitted = color[1:-1].split(",")
    r = int(color_splitted[0])
    g = int(color_splitted[1])
    b = int(color_splitted[2])
    sp_color = (r, g, b)
    return sp_color

def adjust(buttons):
    result = None
    for but in buttons:
        if but.is_known:
            result = but
    if result is not None:
        buttons.remove(result)
    return result

def get_token_number(text):
    temp_text, new_text = "", ""
    temp_list = text.split(" ")
    token_list = list()
    for current in temp_list:
        if len(temp_text+current) <= 25:
            temp_text+= " " + current
        else:
            token_list.append(temp_text)
            temp_text = current
    return len(token_list)


