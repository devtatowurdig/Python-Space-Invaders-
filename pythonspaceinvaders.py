import random
import pygame

tabuleiro = []

def cria_tabuleiro():
    for i in range(17):
        tabuleiro.append([]) #adiciona um array dentro do array
        for _ in range(17):
            tabuleiro[i].append("")
            
def posiciona_player(player_x, player_y):
    tabuleiro[player_y][player_x] = "P"

def posiciona_inimigos():
    colunas_inimigos = random.sample(range(17), 2) #sorteia 2 números do range para posicionar os inimigos
    for c in colunas_inimigos:
        tabuleiro[0][c] = "I"
        
def conta_inimigos(tabuleiro):
    contador_total = 0
    for linha in tabuleiro:
        inimigos_ingame = linha.count("I")
        contador_total = contador_total + inimigos_ingame
    return contador_total

tamanho_grade = 17
tamanho_box = 28
margem = 2

def desenha_tabuleiro(screen, tabuleiro):
    for indice_linha in range(tamanho_grade):
        for indice_coluna in range (tamanho_grade):
            pos_x = indice_coluna * (tamanho_box + margem) + margem
            pos_y = indice_linha * (tamanho_box + margem) + margem
            cor = (40, 40, 40) 
            if tabuleiro[indice_linha][indice_coluna] == "P":
                cor = (0, 255, 0)
            elif tabuleiro[indice_linha][indice_coluna] == "I":
                cor = (255, 0, 0)
            elif tabuleiro[indice_linha][indice_coluna] == ".":
                cor = (255, 255, 0)
            elif tabuleiro[indice_linha][indice_coluna] == ".":
                cor = (255, 0, 255)
            pygame.draw.rect(screen, cor, (pos_x, pos_y, tamanho_box, tamanho_box)) # Onde desenhar, a cor, posicoes, largura, altura.
    
    