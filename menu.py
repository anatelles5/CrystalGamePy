import pygame
import sys
import os
import subprocess
import player1fase1

# Inicializa o pygame
pygame.init()

# Janela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Crystal Game - Menu")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def load_image(nome, scale_to=None):
    base = os.path.dirname(os.path.abspath(sys.argv[0]))
    caminho = os.path.join(base, nome)
    if not os.path.exists(caminho):
        surf = pygame.Surface(scale_to or (300, 100))
        surf.fill((200, 40, 40))  # fallback vermelho
        return surf.convert_alpha()
    img = pygame.image.load(caminho).convert_alpha()
    if scale_to:
        img = pygame.transform.smoothscale(img, scale_to)
    return img

# Fontes
fonte_titulo = pygame.font.SysFont("arial", 64, bold=True)
fonte_botao  = pygame.font.SysFont("arial", 40, bold=True)


# Imagens
background = load_image("backgroundcapa.png", (LARGURA, ALTURA))
imagem_botao = load_image("botao.png")
botao_largura, botao_altura = imagem_botao.get_size()

def desenhar_botao(texto, x, y):
    tela.blit(imagem_botao, (x, y))
    texto_render = fonte_botao.render(texto, True, BLACK)
    texto_rect = texto_render.get_rect(center=(x + botao_largura // 2, y + botao_altura // 2))
    tela.blit(texto_render, texto_rect)
    return pygame.Rect(x, y, botao_largura, botao_altura)


def menu():
    rodando = True
    while rodando:
        # Desenha o fundo
        tela.blit(background, (0, 0))

        # Título
        titulo = fonte_titulo.render("Crystal Game", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(LARGURA//2, ALTURA//3 - 50))
        tela.blit(titulo, titulo_rect)

        # Botão Play logo abaixo do título
        botao_y = titulo_rect.bottom + 40  # 40px abaixo do título
        botao_play = desenhar_botao("Play", LARGURA // 2 - botao_largura // 2, botao_y)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if botao_play.collidepoint(event.pos):
                    print("Iniciando Fase 1...")
                    rodando = False
                    player1fase1.fase1()  # chama a fase

        pygame.display.flip()

if __name__ == "__main__":
    menu()