import tkinter as tk
from tkinter import messagebox

# O jogador min -> quer minimizar o placar ->  value 1 
# X jogador max -> quer maximizar o placar -> value -1

class JogoDaVelha:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Velha")
        self.botao = [[None, None, None] for _ in range(3)]
        self.jogador_atual = 'X'
        self.ia = 'O'
        self.humano = 'X'
        self.criar_interface()

    def criar_interface(self):
        """Inicialmente cria a interface utilizando o TKInter com o tabuleiro vazio"""
        for i in range(3):
            for j in range(3):
                self.botao[i][j] = tk.Button(self.root, text='', font=('Arial', 40), width=5, height=2, command=lambda i=i, j=j: self.humano_jogar(i, j))
                self.botao[i][j].grid(row=i, column=j)

    def eh_fim_de_jogo(self, jogador_atual) -> bool:
        """Verifica se o jogo acabou e exibe uma mensagem de vitória ou empate"""
        if self.checar_vencedor(jogador_atual):
            messagebox.showinfo("Fim de Jogo", f"Jogador {jogador_atual} venceu!")
            self.reiniciar_jogo()
            return True
        elif self.checar_empate():
            messagebox.showinfo("Empate", "O jogo empatou!")
            self.reiniciar_jogo()
            return True
        return False

    def melhor_movimento_ia(self):
        """Calcula o melhor movimento para a IA usando o algoritmo Minimax"""
        melhor_valor = -float('inf')
        melhor_movimento = None

        for i in range(3):
            for j in range(3):
                if self.botao[i][j]['text'] == '':
                    # Faz o movimento
                    self.botao[i][j]['text'] = self.ia
                    movimento_valor = self.minimax(False)
                    # Desfaz o movimento
                    self.botao[i][j]['text'] = ''
                    if movimento_valor > melhor_valor:
                        melhor_valor = movimento_valor
                        melhor_movimento = (i, j)

        return melhor_movimento

    def minimax(self, eh_maximizador):
        """Algoritmo Minimax para calcular o valor ótimo do movimento"""
        if self.checar_vencedor(self.ia):
            return 1
        elif self.checar_vencedor(self.humano):
            return -1
        elif self.checar_empate():
            return 0

        if eh_maximizador:
            melhor_valor = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.botao[i][j]['text'] == '':
                        self.botao[i][j]['text'] = self.ia
                        valor = self.minimax(False)
                        self.botao[i][j]['text'] = ''
                        melhor_valor = max(melhor_valor, valor)
            return melhor_valor

        else:
            melhor_valor = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.botao[i][j]['text'] == '':
                        self.botao[i][j]['text'] = self.humano
                        valor = self.minimax(True)
                        self.botao[i][j]['text'] = ''
                        melhor_valor = min(melhor_valor, valor)
            return melhor_valor

    def humano_jogar(self, i, j):
        """Define a lógica do jogador humano e define a próxima jogada ou o fim do jogo (vitória, empate ou IA)"""
        if self.botao[i][j]['text'] == '' and self.jogador_atual == 'X':
            self.botao[i][j]['text'] = self.jogador_atual
            if not self.eh_fim_de_jogo(self.jogador_atual):
                self.jogador_atual = 'O'
                self.ia_jogar()

    def ia_jogar(self):
        """Define a jogada da IA e verifica o estado do jogo após a jogada da IA"""
        movimento = self.melhor_movimento_ia()
        if movimento:
            i, j = movimento
            self.botao[i][j]['text'] = 'O'
            if not self.eh_fim_de_jogo(self.jogador_atual):
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
        for i in range(3):
            for j in range(3):
                self.botao[i][j]['text'] = ''
        self.jogador_atual = 'X'

if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoDaVelha(root)
    root.mainloop()
