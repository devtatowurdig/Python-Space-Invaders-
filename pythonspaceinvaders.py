import random
import pygame
import time
import math

pygame.mixer.init()


explosoes = []
TEMPO_EXPLOSAO = 300
TAMANHO_GRADE = 21
TAMANHO_BOX = 22
MARGEM = 10

PLAYER = 'P'
INIMIGO = 'I'
TIRO_PLAYER = '.'
COLISAO = 'X'
VAZIO = ' '
TAMANHO_TELA_CALCULADO = (TAMANHO_BOX + MARGEM) * TAMANHO_GRADE + MARGEM

sprite_player = pygame.transform.scale(pygame.image.load("naves/player.png"), (TAMANHO_BOX, TAMANHO_BOX))
sprite_inimigo_facil = pygame.transform.scale(pygame.image.load("naves/inimigo.png"), (TAMANHO_BOX, TAMANHO_BOX))
sprite_inimigo_medio = pygame.transform.scale(pygame.image.load("naves/inimigo2.png"), (TAMANHO_BOX, TAMANHO_BOX))
sprite_inimigo_dificil = pygame.transform.scale(pygame.image.load("naves/inimigo3.png"), (TAMANHO_BOX, TAMANHO_BOX))
sprite_tiro = pygame.transform.scale(pygame.image.load("naves/tiro.png"), (TAMANHO_BOX, TAMANHO_BOX))
sprite_colisao = pygame.transform.scale(pygame.image.load("naves/colisao.png"), (TAMANHO_BOX, TAMANHO_BOX))
    
#Sons do jogo

som_tiro = pygame.mixer.Sound("sound/tiro2.mp3")   
som_tiro.set_volume(0.1)

som_colisao = pygame.mixer.Sound("sound/explode.mp3")
som_colisao.set_volume(0.05)

som_inicio = pygame.mixer.Sound("sound/starttheme.mp3")
som_inicio.set_volume(0.3)

som_go = pygame.mixer.Sound("sound/gameover.mp3")
som_go.set_volume(0.3)

som_jogo = pygame.mixer.Sound("sound/theme.mp3")
som_jogo.set_volume(0.3)
        


    
tabuleiro = []

def cria_tabuleiro():
    tabuleiro.clear()
    for i in range(TAMANHO_GRADE):
        tabuleiro.append([]) #adiciona um array dentro do array
        for _ in range(TAMANHO_GRADE):
            tabuleiro[i].append(' ')
            
def posiciona_player(player_x, player_y):
    for linha in tabuleiro:
        for i in range(len(linha)):
            if linha[i] == PLAYER:
                linha[i] = VAZIO
                
    tabuleiro[player_y][player_x] = PLAYER

def posiciona_inimigos(qtd_inimigos):
    padroes = {
        1: [[1,5,10,15,19]],
        2: [[1,5,9,11,15,19], [3, 17]],
        3: [[1,5,9,11,15,19],[2,4,10,16,18], [3,17]],
        4: [[1,3,5,8,9,11,12,15,17,19],[2,4,10,16,18], [3,10,17]],
        # 5: [[1,2,3,4,5,7,8,9,10,11,12,13,15,16,17,18,19], [2,3,4,8,9,10,11,12,16,17,18], [3,9,10,11,17], [10]]
        5: [[1,3,5,8,9,11,12,15,17,19], [2,4,10,16,18,17], [3,17], [2,4,10,16,18], [3,10,17]]
    }   
    
    padrao = padroes.get(wave, [[i for i in range(qtd_inimigos)]])
    
    for linha, colunas in enumerate(padrao):
        for indice_coluna in colunas:
            tabuleiro[linha][indice_coluna] = INIMIGO
        
        
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
                screen.blit(sprite_player, (pos_x, pos_y))
            elif tabuleiro[indice_linha][indice_coluna] == INIMIGO:
                if wave == 1:
                    screen.blit(sprite_inimigo_facil, (pos_x, pos_y))
                elif wave > 1 and wave <=3:
                    screen.blit(sprite_inimigo_medio, (pos_x, pos_y))
                else:
                    screen.blit(sprite_inimigo_dificil, (pos_x, pos_y))
                    
            elif tabuleiro[indice_linha][indice_coluna] == TIRO_PLAYER:
                screen.blit(sprite_tiro, (pos_x, pos_y))
            elif tabuleiro[indice_linha][indice_coluna] == COLISAO:
                screen.blit(sprite_colisao, (pos_x, pos_y))
                som_colisao.play()
            # pygame.draw.rect(screen, cor, (pos_x, pos_y, TAMANHO_BOX, TAMANHO_BOX)) # Onde desenhar, a cor, posicoes, largura, altura.

def move_inimigo(tabuleiro, player_x, player_y, pontuacao):
    escapou = False
    
    for indice_linha in range(len(tabuleiro)-2, -1, -1):
        for indice_coluna in range(len(tabuleiro[indice_linha])):
            
            if tabuleiro[indice_linha][indice_coluna] == INIMIGO:
                linha_abaixo = indice_linha + 1
               
                if linha_abaixo == player_y and indice_coluna == player_x:
                    tabuleiro[indice_linha][indice_coluna] = VAZIO #inimigo some
                    tabuleiro[player_y][player_x] = COLISAO
                    screen.fill((0, 0, 0))
                    desenha_tabuleiro(screen, tabuleiro)
                    pygame.display.flip()
                    time.sleep(0.7)
                    
                    pontuacao = max(0, pontuacao - 5) #perde 5 pontos
                    
                    if pontuacao <= 0:
                        tabuleiro[player_y][player_x] = COLISAO
                    
                    return pontuacao, True, escapou
                    
                elif tabuleiro[linha_abaixo][indice_coluna] == VAZIO:
                    tabuleiro[linha_abaixo][indice_coluna] = INIMIGO
                    tabuleiro[indice_linha][indice_coluna] = VAZIO
                
                elif tabuleiro[linha_abaixo][indice_coluna] != VAZIO:
                    continue
                    
    ultima_linha = len(tabuleiro) - 1
    for indice_coluna in range(len(tabuleiro[ultima_linha])): # Tira do tabuleiro inimigos que chegam no final
        if tabuleiro[ultima_linha][indice_coluna] == INIMIGO:
            tabuleiro[ultima_linha][indice_coluna] = VAZIO
            pontuacao = max(0, pontuacao - 5)
            escapou = True
            
            if pontuacao <= 0:
                tabuleiro[player_y][player_x] = COLISAO
                return pontuacao, True, escapou
     
    return pontuacao, False, escapou

def conta_tiros(tabuleiro):
    contador_total = 0
    for linha in tabuleiro:
        tiros_ingame = linha.count(TIRO_PLAYER)
        contador_total = contador_total + tiros_ingame
    return contador_total
        
def atirar(tabuleiro, player_x, player_y):
    som_tiro.stop()
    if player_y > 0 and tabuleiro[player_y - 1][player_x] == VAZIO:
        tabuleiro[player_y - 1][player_x] = TIRO_PLAYER
        som_tiro.play()
            
def move_tiros(tabuleiro):
    global explosoes
    inimigos_abatidos = 0
    linha_topo = 0
    for indice_coluna in range(TAMANHO_GRADE): 
        if tabuleiro[linha_topo][indice_coluna] == TIRO_PLAYER:
            tabuleiro[linha_topo][indice_coluna] = VAZIO
    
    for indice_linha in range(1, TAMANHO_GRADE):
        for indice_coluna in range(TAMANHO_GRADE):
            
            if tabuleiro[indice_linha][indice_coluna] == TIRO_PLAYER:
                linha_acima = indice_linha - 1
                
                if tabuleiro[linha_acima][indice_coluna] == INIMIGO:
                   tabuleiro[linha_acima][indice_coluna] = COLISAO
                   explosoes.append((linha_acima, indice_coluna, pygame.time.get_ticks()))
                   tabuleiro[indice_linha][indice_coluna] = VAZIO #remove tiro
                   inimigos_abatidos += 1
                elif tabuleiro[linha_acima][indice_coluna] == VAZIO:
                    tabuleiro[linha_acima][indice_coluna] = TIRO_PLAYER
                    tabuleiro[indice_linha][indice_coluna] = VAZIO
                
                else:
                    tabuleiro[indice_linha][indice_coluna] = VAZIO
    return inimigos_abatidos
def tela_start(screen):
    som_inicio.play()
    
    imagem = pygame.image.load("img/start.png")
    imagem = pygame.transform.scale(imagem, (screen.get_width(), screen.get_height()))
    rect = imagem.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
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
    som_inicio.stop()
    return nome


def atualiza_ranking(jogador, pontuacao): 
    NOME_ARQUIVO = "ranking.txt"
    ranking = []
    
    try:
        with open(NOME_ARQUIVO, "r") as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas:
                partes = linha.strip().split(';')
                if len(partes) == 2:
                    ranking.append((partes[0], int(partes[1])))
    except FileNotFoundError:
        pass
    
    ranking.append((jogador, pontuacao))
    ranking = sorted(ranking, key = lambda x: x[1], reverse = True)[:5]
    
    with open(NOME_ARQUIVO, "w") as arquivo:
        for nome, pontos in ranking:
            if pontos > 0:
                arquivo.write(f"{nome};{pontos}\n")
            
    return ranking

def tela_ranking(screen, ranking_lista):
    fonte_titulo = pygame.font.SysFont("bold", 64)
    fonte_texto = pygame.font.SysFont(None, 48)
    
    screen.fill((5 , 5, 5))
    
    titulo = fonte_titulo.render("Ranking - Top 5", True, (255, 255, 0))
    rect_titulo = titulo.get_rect(center=(screen.get_width() // 2, 80))
    screen.blit(titulo, rect_titulo)
    
    posicao_y = 160
    for indice, (nome, pontos) in enumerate(ranking_lista):
        if pontos > 0:
            texto_ranking = f"{indice + 1}. {nome} - {pontos}"
            
            superficie_texto = fonte_texto.render(texto_ranking, True, (255, 255, 255))
            rect_texto = superficie_texto.get_rect(topleft=(40, posicao_y))
            screen.blit(superficie_texto, rect_texto)
            
            posicao_y += 60
        
    pygame.display.flip()
    time.sleep(4)
    
def tela_gameover(screen):
    som_go.play()
    
    imagem = pygame.image.load("img/gameover.png")
    imagem = pygame.transform.scale(imagem, (screen.get_width(), screen.get_height()))
    rect = imagem.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
    screen.fill((0 , 0, 0))
    screen.blit(imagem, rect)
    pygame.display.flip()
    time.sleep(3)

    som_go.stop()
def tela_continue(screen):
    fonte = pygame.font.SysFont(None, 25)
    esperando = True
    
    while esperando:
        screen.fill((0, 0, 0))
        
        texto_render = fonte.render("Pressione ENTER para jogar novamente ou ESC para sair", True, (255, 255, 255))
        rect_texto = texto_render.get_rect(center=(screen.get_width() // 2, screen.get_height() - 20 ))
        screen.blit(texto_render, rect_texto)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
                         
def tela_pause(screen):   
    fonte = pygame.font.SysFont("bold", 50)
    fonte2 = pygame.font.SysFont("bold", 25)
    esperando = True
    while esperando:
        screen.fill((0, 0, 0))
        texto = fonte.render("Jogo Pausado", True, (255, 255, 255))            
        rect = texto.get_rect(center=(screen.get_width() // 5, screen.get_height()  - 120))
        screen.blit(texto, rect)
        texto2= fonte2.render("ENTER para continuar", True, (120, 120, 120))
        rect2 = texto.get_rect(center=(screen.get_width() // 5, screen.get_height() - 50))
        screen.blit(texto2, rect2)
        texto3= fonte2.render("ESC para sair", True, (120, 120, 120))
        rect3 = texto.get_rect(center=(screen.get_width() // 5, screen.get_height() - 30))
        screen.blit(texto3, rect3)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
        


## Programa 

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((TAMANHO_TELA_CALCULADO, TAMANHO_TELA_CALCULADO))
pygame.display.set_caption("Python Space Invaders - Matriz")
clock = pygame.time.Clock()



jogando_app = True


while jogando_app:
    
    som_jogo.play()
    tela_start(screen)
    pygame.event.clear()
    jogador = ""
    while not jogador:
        jogador = tela_nome_jogador(screen)

    
    wave = 1
    max_waves = 5
    game_over = False
    vitoria = False
    font_wave = pygame.font.SysFont(None, 32)
    pontuacao = 0


    cria_tabuleiro()
    
    
    player_x = math.ceil(TAMANHO_GRADE / 2)
    player_y = TAMANHO_GRADE - 1
    posiciona_player(player_x, player_y)
    posiciona_inimigos(2)
    inimigo_timer = 0
    inimigo_intervalo = 12
    ultimo_tiro = 0
    intervalo_tiro = 200
    
    
        
    while not game_over: 
               
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                jogando_app = False
        #Pause
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                continuar = tela_pause(screen)
                if not continuar:
                    game_over = True
                    jogando_app = False
                    break
        
        keys = pygame.key.get_pressed()
        
        #Teclas de movimento do player
        if keys[pygame.K_a] and player_x > 0:
            tabuleiro[player_y][player_x] =  VAZIO
            player_x = player_x - 1
            tabuleiro[player_y][player_x] = PLAYER
        elif keys[pygame.K_d] and player_x < TAMANHO_GRADE - 1 :
            tabuleiro[player_y][player_x] =  VAZIO
            player_x = player_x + 1
            tabuleiro[player_y][player_x] =  PLAYER
            
        #Tiro
        if keys[pygame.K_SPACE] and tempo_atual - ultimo_tiro > intervalo_tiro:
            atirar(tabuleiro, player_x, player_y)
            ultimo_tiro = tempo_atual
        
        
        
        inimigo_timer = inimigo_timer + 1
        inimigo_escapou_aqui = False
        if inimigo_timer >= inimigo_intervalo:
            
            pontuacao, perdeu, escapou = move_inimigo(tabuleiro, player_x, player_y, pontuacao)
            
            if(perdeu):
                desenha_tabuleiro(screen, tabuleiro)
                pygame.display.flip()
                time.sleep(2)
                tela_gameover(screen)
                break
            if(escapou):
                inimigo_escapou_aqui = True
                
            inimigo_timer = 0
        pontuacao += move_tiros(tabuleiro) * (5 * wave)
               
        
        if conta_inimigos(tabuleiro) == 0 and not inimigo_escapou_aqui:
            if wave < max_waves:
                wave = wave + 1
                inimigo_intervalo = inimigo_intervalo - 1
                                
                for indice_linha in range(TAMANHO_GRADE):
                    for indice_coluna in range(TAMANHO_GRADE):
                        if tabuleiro[indice_linha][indice_coluna] in [INIMIGO, TIRO_PLAYER, COLISAO]:
                            tabuleiro[indice_linha][indice_coluna] = VAZIO
                            
                
                
                qtd_inimigos = min(2 + wave - 1, TAMANHO_GRADE)
                posiciona_inimigos(qtd_inimigos)
                
            else:
                vitoria = True
                game_over = True
            
        
        screen.fill((0, 0, 0))
        desenha_tabuleiro(screen, tabuleiro)
        
        texto_wave = font_wave.render(f'Wave: {wave}', True, (255, 255, 255))
        rect_wave = texto_wave.get_rect(right = screen.get_width() - 45, top = 10)
        screen.blit(texto_wave, rect_wave)
        
        texto_score = font_wave.render(f'Score: {pontuacao}', True, (255, 255, 0))
        rect_score = texto_wave.get_rect(right = screen.get_width() - 45, top = 40)
        screen.blit(texto_score, rect_score)
        
        text_player = font_wave.render(f"Player: {jogador}", True, (0, 255, 125))
        screen.blit(text_player, (10, 10))
        
        tempo_atual = pygame.time.get_ticks()
        for explosao in explosoes[:]:
            linha, coluna, tempo_explosao = explosao
            if tempo_atual - tempo_explosao > TEMPO_EXPLOSAO:
                tabuleiro[linha][coluna] = VAZIO
                explosoes.remove(explosao)
        
        pygame.display.flip()
        clock.tick(15)
        
        
        
        #Reiniciar o jogo
    
    if jogando_app:
        if vitoria:
            screen.fill((0, 0, 0))
            imagem = pygame.image.load("img/vitoria.png")
            imagem = pygame.transform.scale(imagem, (screen.get_width(), screen.get_height()))
            rect = imagem.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
            screen.blit(imagem, rect)
            pygame.display.flip()
            time.sleep(3)
            

        som_jogo.stop()
        ranking_atual = atualiza_ranking(jogador, pontuacao)
        tela_ranking(screen, ranking_atual)

        #Contiue
        jogando_app = tela_continue(screen)
        

pygame.quit()
exit()


