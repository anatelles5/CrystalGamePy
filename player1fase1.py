import pygame
import sys
import random
import menu  # para voltar ao menu

pygame.init()

# CONFIGURAÇÕES
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Crystal Game - Fase 1")

clock = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 32, bold=True)

# ÁUDIO
pygame.mixer.music.load("happy-relaxing-loop.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

som_jewel = pygame.mixer.Sound("collect-points.mp3")
som_rock = pygame.mixer.Sound("laser.mp3")

# FUNDO PARALLAX
planos = [
    {"img": pygame.image.load("plan5.png").convert_alpha(), "vel": 1, "x": 0},
    {"img": pygame.image.load("plan4.png").convert_alpha(), "vel": 2, "x": 0},
    {"img": pygame.image.load("plan3.png").convert_alpha(), "vel": 3, "x": 0},
    {"img": pygame.image.load("plan2.png").convert_alpha(), "vel": 4, "x": 0},
    {"img": pygame.image.load("plan1.png").convert_alpha(), "vel": 5, "x": 0},
]
for p in planos:
    p["img"] = pygame.transform.scale(p["img"], (LARGURA, ALTURA))

def desenhar_fundo():
    for p in planos:
        tela.blit(p["img"], (p["x"], 0))
        tela.blit(p["img"], (p["x"] + LARGURA, 0))
        p["x"] -= p["vel"]
        if p["x"] <= -LARGURA:
            p["x"] = 0

# CLASSE PLAYER
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        imagem_original = pygame.image.load("player1.png").convert_alpha()
        self.image = pygame.transform.scale(imagem_original, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = ALTURA // 2
        self.vel = 5
        self.score = 0

    def update(self):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_UP]:
            self.rect.y -= self.vel
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.vel
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.vel
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.vel

        # Impedir de sair da tela
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > ALTURA:
            self.rect.bottom = ALTURA
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA

# OBJETOS (joias/pedras)
class Objeto(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo

        if tipo == "jewel":
            imagem_original = pygame.image.load("3.png").convert_alpha()
            self.image = pygame.transform.scale(imagem_original, (60, 60))  # joia menor que o player
            self.rect = self.image.get_rect()
            self.rect.x = LARGURA + random.randint(60, 200)
            self.rect.y = random.randint(60, ALTURA - 60)
            self.vel = random.randint(4, 7)

        else:
            imagem_original = pygame.image.load("Rock1_1.png").convert_alpha()
            self.image = pygame.transform.scale(imagem_original, (70, 70))  # pedra quase do tamanho do player
            self.rect = self.image.get_rect()
            self.rect.x = LARGURA + random.randint(20, 100)
            self.rect.y = random.randint(50, ALTURA - 50)
            self.vel = random.randint(4, 7)

    def update(self):
        self.rect.x -= self.vel
        if self.rect.right < 0:
            self.kill()

# FASE 1
def fase1():
    player = Player()
    todos = pygame.sprite.Group()
    objetos = pygame.sprite.Group()

    todos.add(player)

    tempo_inicial = pygame.time.get_ticks()
    duracao = 25  # segundos

    rodando = True
    while rodando:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        desenhar_fundo()
        todos.update()
        todos.draw(tela)

        # Criar objetos aleatórios
        if random.randint(1, 40) == 1:
            tipo = random.choice(["jewel", "rock"])
            obj = Objeto(tipo)
            todos.add(obj)
            objetos.add(obj)

        objetos.update()

        # Colisões
        hits = pygame.sprite.spritecollide(player, objetos, True)
        for h in hits:
            if h.tipo == "jewel":
                player.score += 10
                som_jewel.play()
            else:
                player.score -= 3
                som_rock.play()

        # score e timer
        segundos = (pygame.time.get_ticks() - tempo_inicial) // 1000
        tempo_restante = max(0, duracao - segundos)

        texto = fonte.render(f"Score: {player.score}   Timer: {tempo_restante}", True, (255, 255, 255))
        tela.blit(texto, (20, 20))

        todos.draw(tela)

        if tempo_restante <= 0:
            rodando = False

        pygame.display.flip()

    # TELA FINAL
    tela.fill((0, 0, 0))
    fim_texto = fonte.render(f"Time is over - Score: {player.score}", True, (255, 255, 255))
    fim_rect = fim_texto.get_rect(center=(LARGURA//2, ALTURA//2 - 50))
    tela.blit(fim_texto, fim_rect)

    # Botão MENU
    botao_texto = fonte.render("Menu", True, (0, 0, 0))
    botao_rect = pygame.Rect(LARGURA//2 - 60, ALTURA//2 + 20, 120, 50)
    pygame.draw.rect(tela, (200, 200, 200), botao_rect)
    tela.blit(botao_texto, botao_texto.get_rect(center=botao_rect.center))

    pygame.display.flip()

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if botao_rect.collidepoint(event.pos):
                    esperando = False
                    menu.menu()

        clock.tick(30)

if __name__ == "__main__":
    fase1()