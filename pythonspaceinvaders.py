import random
import pygame


TAMANHO_GRADE = 17
TAMANHO_BOX = 28
MARGEM = 2

PLAYER = 'P'
INIMIGO = 'I'
TIRO_PLAYER = '.'
COLISAO = 'X'
VAZIO = ' '



tabuleiro = []

def cria_tabuleiro():
    for i in range(17):
        tabuleiro.append([]) #adiciona um array dentro do array
        for _ in range(17):
            tabuleiro[i].append(' ')
            
def posiciona_player(player_x, player_y):
    tabuleiro[player_y][player_x] = PLAYER

def posiciona_inimigos():
    colunas_inimigos = random.sample(range(17), 2) #sorteia 2 números do range para posicionar os inimigos
    for c in colunas_inimigos:
        tabuleiro[0][c] = INIMIGO
        
def conta_inimigos(tabuleiro):
    contador_total = 0
    for linha in tabuleiro:
        inimigos_ingame = linha.count(INIMIGO)
        contador_total = contador_total + inimigos_ingame
    return contador_total



def desenha_tabuleiro(screen, tabuleiro):
    for indice_linha in range(TAMANHO_GRADE):
        for indice_coluna in range (TAMANHO_GRADE):
            pos_x = indice_coluna * (TAMANHO_BOX + MARGEM) + MARGEM
            pos_y = indice_linha * (TAMANHO_BOX + MARGEM) + MARGEM
            cor = (40, 40, 40) 
            if tabuleiro[indice_linha][indice_coluna] == PLAYER:
                cor = (0, 255, 0)
            elif tabuleiro[indice_linha][indice_coluna] == INIMIGO:
                cor = (255, 0, 0)
            elif tabuleiro[indice_linha][indice_coluna] == TIRO_PLAYER:
                cor = (255, 255, 0)
            elif tabuleiro[indice_linha][indice_coluna] == COLISAO:
                cor = (255, 0, 255)
            pygame.draw.rect(screen, cor, (pos_x, pos_y, TAMANHO_BOX, TAMANHO_BOX)) # Onde desenhar, a cor, posicoes, largura, altura.

def move_inimigo(tabuleiro, player_x, player_y):
    for indice_linha in range(len(tabuleiro)-2, -1, -1):
        for indice_coluna in range(len(tabuleiro[indice_linha])):
            
            if tabuleiro[indice_linha][indice_coluna] == INIMIGO:
                linha_abaixo = indice_linha + 1
                
                if linha_abaixo == player_y and indice_coluna == player_x: # Se o inimigo encostou no player
                    tabuleiro[indice_linha][indice_coluna] = VAZIO
                    tabuleiro[player_y][player_x] = COLISAO
                    return True
                
                if tabuleiro[linha_abaixo][indice_coluna] == VAZIO: # Move para espaço vazio
                    tabuleiro[linha_abaixo][indice_coluna] = INIMIGO
                    tabuleiro[indice_linha][indice_coluna] = VAZIO
    
    ultima_linha= len(tabuleiro) -1
    for indice_coluna in range(len(tabuleiro[ultima_linha])): # Tira do tabuleiro inimigos que chegam no final
        if tabuleiro[ultima_linha][indice_coluna] == INIMIGO:
            tabuleiro[ultima_linha][indice_coluna] = VAZIO
    
    return False

def conta_tiros(tabuleiro):
    contador_total = 0
    for linha in tabuleiro:
        tiros_ingame = linha.count(TIRO_PLAYER)
        contador_total = contador_total + tiros_ingame
        
def atirar(tabuleiro, player_x, player_y):
    if conta_tiros(tabuleiro) == 0:
        if player_y > 0 and tabuleiro[player_y - 1][player_x] == VAZIO:
            tabuleiro[player_y - 1][player_x] = TIRO_PLAYER
            
def move_tiros(tabuleiro):
    linha_topo = 0
    for indice_coluna in range(TAMANHO_GRADE): 
        if tabuleiro[linha_topo][indice_coluna] == TIRO_PLAYER:
            tabuleiro[linha_topo][indice_coluna] = VAZIO
    
    for indice_linha in range(1, TAMANHO_GRADE):
        for indice_coluna in range(TAMANHO_GRADE):
            
            if tabuleiro[indice_linha][indice_coluna] == TIRO_PLAYER:
                linha_acima = indice_linha - 1
                
                if tabuleiro[linha_acima][indice_coluna] == INIMIGO:
                   tabuleiro[linha_acima][indice_coluna] = VAZIO #remove inimigo
                   tabuleiro[indice_linha][indice_coluna] = VAZIO #remove tiro
                   
                elif tabuleiro[linha_acima][indice_coluna] == VAZIO:
                    tabuleiro[linha_acima][indice_coluna] = TIRO_PLAYER
                    tabuleiro[indice_linha][indice_coluna] = VAZIO
                
                else:
                    tabuleiro[indice_linha][indice_coluna] = VAZIO

                    
cria_tabuleiro()
player_x = 9
player_y = 16
inimigo_timer = 0
inimigo_intervalo = 10

def tela_start(screen):
    imagem = pygame.image.load("/img/start.png")
    imagem = pygame.transform.scale(imagem, (screen.get_width(), screen.get_height()))
    rect = imagem.get_rect(screen.get_width() // 2, screen.get_height() // 2)
    esperando = True
    while esperando:
        screen.fill((0, 0, 0))
        screen.blit(imagem, rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                esperando = False
                
def tela_nome_jogador(screen):
    fonte = pygame.font.SysFont("bold", 48)
    nome = ""
    ativo = True
    while ativo:
        screen.fill((0, 0, 0))
        texto = fonte.render("Digite seu nome:", True, (255, 255, 255))
        rect = texto.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 40))
        screen.blit(texto, rect)
        texto_nome = fonte.render(nome, True, (0, 255, 0))
        rect_nome = texto_nome.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 20))
        screen.blit(texto_nome, rect_nome)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(nome) > 0:
                    ativo = False
                elif event.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                else:
                    if len(nome) < 12 and event.unicode.isprintable():
                        nome += event.unicode
    return nome