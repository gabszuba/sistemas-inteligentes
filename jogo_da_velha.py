import tkinter as tk
from tkinter import messagebox
import csv

class JogoDaVelha:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Velha")
        self.botao = [[None, None, None] for _ in range(3)]
        self.jogador_atual = 'X'
        self.ia = 'O'
        self.humano = 'X'
        self.jogadas = []
        self.arquivo_csv = open(r"jogadas.csv", "a", newline='')  # Abre o arquivo CSV para anexar jogadas
        self.writer = csv.writer(self.arquivo_csv)
        self.writer.writerow(['vencedor', 'mandala'])  # Cabeçalho do CSV
        self.criar_interface()
        self.fim_de_jogo = False

    def criar_interface(self):
        """Cria a interface utilizando o TKInter com o tabuleiro vazio e botão de reinício"""
        for i in range(3):
            for j in range(3):
                self.botao[i][j] = tk.Button(self.root, text='', font=('Arial', 40), width=5, height=2,
                                             command=lambda i=i, j=j: self.humano_jogar(i, j))
                self.botao[i][j].grid(row=i, column=j)
        
        self.botao_reiniciar = tk.Button(self.root, text='Reiniciar', font=('Arial', 20), command=self.reiniciar_jogo)
        self.botao_reiniciar.grid(row=3, column=0, columnspan=3, sticky="nsew")

    def eh_fim_de_jogo(self, jogador_atual) -> bool:
        """Verifica se o jogo acabou e exibe uma mensagem de vitória ou empate"""
        if self.checar_vencedor(jogador_atual):
            messagebox.showinfo("Fim de Jogo", f"Jogador {jogador_atual} venceu!")
            mandala = self.mandala_vencedora(jogador_atual)
            self.gravar_mandala(jogador_atual, mandala)
            self.fim_de_jogo = True
            return True
        elif self.checar_empate():
            messagebox.showinfo("Empate", "O jogo empatou!")
            self.fim_de_jogo = True
            return True
        return False

    def minimax(self, eh_maximizador):
        """Algoritmo Minimax para calcular o valor ótimo do movimento e o movimento em si"""
        if self.checar_vencedor(self.ia):
            return 1, None
        elif self.checar_vencedor(self.humano):
            return -1, None
        elif self.checar_empate():
            return 0, None

        melhor_movimento = None

        if eh_maximizador:
            melhor_valor = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.botao[i][j]['text'] == '':
                        self.botao[i][j]['text'] = self.ia
                        valor, _ = self.minimax(False)
                        self.botao[i][j]['text'] = ''
                        if valor > melhor_valor:
                            melhor_valor = valor
                            melhor_movimento = (i, j)
            return melhor_valor, melhor_movimento
        
        melhor_valor = float('inf')
        for i in range(3):
            for j in range(3):
                if self.botao[i][j]['text'] == '':
                    self.botao[i][j]['text'] = self.humano
                    valor, _ = self.minimax(True)
                    self.botao[i][j]['text'] = ''
                    if valor < melhor_valor:
                        melhor_valor = valor
                        melhor_movimento = (i, j)
        return melhor_valor, melhor_movimento

    def humano_jogar(self, i, j):
        """Define a lógica do jogador humano e define a próxima jogada ou o fim do jogo (vitória, empate ou IA)"""
        if self.botao[i][j]['text'] == '' and self.jogador_atual == 'X' and not self.fim_de_jogo:
            self.botao[i][j]['text'] = self.jogador_atual
            self.jogadas.append((i, j))
            if not self.eh_fim_de_jogo(self.jogador_atual):
                self.jogador_atual = 'O'
                self.ia_jogar()

    def ia_jogar(self):
        """Define a jogada da IA e verifica o estado do jogo após a jogada da IA"""
        _, movimento = self.minimax(True)
        if movimento:
            i, j = movimento
            self.botao[i][j]['text'] = 'O'
            self.jogadas.append((i, j))
            if not self.eh_fim_de_jogo(self.ia):
                self.jogador_atual = 'X'

    def checar_vencedor(self, jogador):
        """Verifica se o jogador especificado venceu"""
        for i in range(3):
            if self.botao[i][0]['text'] == self.botao[i][1]['text'] == self.botao[i][2]['text'] == jogador:
                return True
            if self.botao[0][i]['text'] == self.botao[1][i]['text'] == self.botao[2][i]['text'] == jogador:
                return True
        if self.botao[0][0]['text'] == self.botao[1][1]['text'] == self.botao[2][2]['text'] == jogador:
            return True
        if self.botao[0][2]['text'] == self.botao[1][1]['text'] == self.botao[2][0]['text'] == jogador:
            return True
        return False

    def checar_empate(self):
        """Verifica se o jogo empatou"""
        for i in range(3):
            for j in range(3):
                if self.botao[i][j]['text'] == '':
                    return False
        return True

    def reiniciar_jogo(self):
        """Reinicia o tabuleiro e o jogador atual"""
        self.fim_de_jogo = False
        for i in range(3):
            for j in range(3):
                self.botao[i][j]['text'] = ''
        self.jogador_atual = 'X'
        self.jogadas = []

    def mandala_vencedora(self, jogador):
        """Retorna a sequência de jogadas vencedoras"""
        return self.jogadas[::2] if jogador == self.humano else self.jogadas[1::2]
    
    def gravar_mandala(self, jogador, mandala):
        """Grava a sequência de jogadas vencedoras em um arquivo CSV"""
        mandala_str = ';'.join([f"{i},{j}" for i, j in mandala])  # Converte a mandala em string
        self.writer.writerow([jogador, mandala_str])
    
    def fechar_arquivo(self):
        """Fecha o arquivo quando o jogo termina"""
        self.arquivo_csv.close()

if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoDaVelha(root)
    root.protocol("WM_DELETE_WINDOW", lambda: [jogo.fechar_arquivo(), root.destroy()])
    root.mainloop()
