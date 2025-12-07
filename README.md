# 🚀 Space Invaders - Projeto UniSenac

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Pygame](https://img.shields.io/badge/Library-Pygame-green?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Concluído-success?style=for-the-badge)

> Um jogo de "Space Invaders" desenvolvido como trabalho final para a disciplina de Algoritmos e Estrutura de Dados.

## 🖼️ Preview do Jogo

<p><img src="img/screenshot1.png" alt="Screenshot do Jogo" width="300">
<img src="img/screenshot2.png" alt="Screenshot do Jogo" width="300"></p>

## 📝 Sobre o Projeto

Este projeto foi desenvolvido como requisito avaliativo para a cadeira de **Algoritmos e Estrutura de Dados** do curso de **Análise e Desenvolvimento de Sistemas** da **UniSenac Pelotas**.

O objetivo inicial era aplicar matrizes e outras estruturas de dados em um jogo com emojis. Porém resolvi utilizar a biblioteca gráfica Pygame para otimizar o jogo.

## 🎮 Mecânicas e Regras

O jogo consiste em defender a base contra ondas de naves inimigas.

### 🌊 Sistema de Waves (Ondas)
O jogo possui um total de **5 Waves**.
* A cada nova wave, a dificuldade aumenta:
    * **Quantidade:** Maior número de naves inimigas.
    * **Velocidade:** As naves descem mais rápido.

### 🎯 Pontuação
A pontuação escala conforme a dificuldade da wave aumenta.
* **Fórmula:** `1 ponto * x`
* **Valor de X:** Inicia em 5 e aumenta +5 a cada nova wave.
    * *Wave 1:* 5 pontos por nave.
    * *Wave 2:* 10 pontos por nave.
    * *Wave 3:* 15 pontos por nave, etc.

### ⚠️ Penalidades e Game Over
* **Penalidade:** Para cada nave inimiga que "sobrar" (passar pelo jogador sem ser destruída) ao final da wave, o jogador perde **-5 pontos**.
* **Game Over:** Se qualquer nave inimiga **colidir** com a nave do jogador, o jogo encerra imediatamente.

## 💻 Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:
* [Python 3.x](https://www.python.org/downloads/)
* Gerenciador de pacotes `pip`
* Pygame

## 🚀 Instalação e Execução

1. **Clone o repositório**
   ```bash
   git clone [https://github.com/devtatowurdig/Python-Space-Invaders.git](https://github.com/devtatowurdig/Python-Space-Invaders.git)
   cd Python-Space-Invaders
   python pythonspaceinvaders.py
