import pygame
import time
from network import Network
import pickle
pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

# Inicializa start_time como None
start_time = None
countdown_displayed = False  # Nueva variable global para controlar si se ha mostrado el mensaje de cuenta regresiva


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100
        self.blocked = False  # Nuevo atributo para indicar si el botón está bloqueado

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height and not self.blocked:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    global start_time, countdown_start, countdown_displayed

    win.fill((155, 89, 182))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255, 255, 255), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Player 1", 1, (0, 255, 255)) 
        win.blit(text, (80, 200))

        text = font.render("Player 2", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

        # Implementación de la cuenta regresiva
        if start_time is not None:
            elapsed_time = 4 - (time.time() - start_time)
            if elapsed_time > 0:
                font = pygame.font.SysFont("comicsans", 30)
                countdown_text = font.render(f"Tiempo: {int(elapsed_time)} seconds", 1, (255, 255, 255))
                win.blit(countdown_text, (width - countdown_text.get_width() - 10, 10))
            else:
                if not countdown_displayed:
                    start_time = time.time()  # Restablecer el inicio del contador cuando alcanza 0
                    # Mostrar el mensaje cuando el tiempo alcance cero
                    font = pygame.font.SysFont("comicsans", 40)
                    message_text = font.render("Tiempo finalizado", 1, (255, 0, 0))
                    win.blit(message_text, (width/2 - message_text.get_width()/2, height/2 - message_text.get_height()/2))
                    pygame.display.update()
                    pygame.time.delay(2000)
                    countdown_displayed = True

                # Bloquear los botones para que no puedan ser pulsados
                for btn in btns:
                    btn.blocked = True
                    btn.text = "Locked"
                    

    pygame.display.update()




btns = [Button("ROCK", 50, 500, "#FF3E4D"), Button("SCISSORS", 250, 500, "#FAD02E"), Button("PAPER", 450, 500, "#0ABDE3")]


def main():
    global start_time
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.connected() and start_time is None:
            start_time = time.time()  # Inicia el tiempo cuando ambos jugadores se conectan

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((155, 89, 182)) 
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 255, 255))
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()