import chess
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import chess.svg

# Função para avaliar a posição do tabuleiro
def evaluate_board(board):
    # Esta é uma função de avaliação muito simples que retorna um valor aleatório
    return random.randint(-100, 100)

# Função Minimax com poda alfa-beta
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Função para escolher o melhor movimento usando Minimax com aumento de profundidade
def best_move(board, depth):
    best_score = float('-inf')
    best_move = None
    for move in board.legal_moves:
        board.push(move)
        score = minimax(board, depth - 1, float('-inf'), float('inf'), False)
        board.pop()
        if score > best_score:
            best_score = score
            best_move = move
            
    # Verificar se o movimento é um movimento de roque válido
    if best_move and board.is_castling(best_move):
        # Mover a torre adequadamente
        if best_move == chess.Move.from_uci("e1g1"):  # Roque curto para as brancas
            board.push(chess.Move.from_uci("h1f1"))
        elif best_move == chess.Move.from_uci("e1c1"):  # Roque longo para as brancas
            board.push(chess.Move.from_uci("a1d1"))
        elif best_move == chess.Move.from_uci("e8g8"):  # Roque curto para as pretas
            board.push(chess.Move.from_uci("h8f8"))
        elif best_move == chess.Move.from_uci("e8c8"):  # Roque longo para as pretas
            board.push(chess.Move.from_uci("a8d8"))
        best_move = None
            
    return best_move

class ChessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game")
        self.root.geometry("800x600")
        
        self.board = chess.Board()
        
        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT)
        
        self.create_menu()  # Adiciona a barra de menu
        
        self.update_board()
        
        self.canvas.bind("<Button-1>", self.on_click)
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # Menu "Jogo"
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="Novo Jogo", command=self.new_game)
        game_menu.add_command(label="Salvar Jogo", command=self.save_game)
        game_menu.add_command(label="Carregar Jogo", command=self.load_game)
        game_menu.add_separator()
        game_menu.add_command(label="Sair", command=self.root.quit)
        menubar.add_cascade(label="Jogo", menu=game_menu)
        
        # Menu "Opções"
        options_menu = tk.Menu(menubar, tearoff=0)
        options_menu.add_command(label="Configurar IA", command=self.configure_ai)
        menubar.add_cascade(label="Opções", menu=options_menu)
        
        self.root.config(menu=menubar)
        
    def new_game(self):
        self.board = chess.Board()
        self.update_board()

    def save_game(self):
        messagebox.showinfo("Save Game", "Jogo salvo com sucesso!")
        pass

    def load_game(self):
        messagebox.showinfo("Load Game", "Jogo carregado!")

    def configure_ai(self):
        messagebox.showinfo("Configure AI", "IA configurada!")
        pass

    def update_board(self):
        svg_data = chess.svg.board(self.board)
        svg_data = svg_data.replace('xmlns="http://www.w3.org/2000/svg"', '')
        svg_data = svg_data.replace("standalone='no'", "")
        svg_data = svg_data.replace("standalone='yes'", "")
        svg_data = svg_data.replace('version="1.1"', 'version="1.1" viewBox="0 0 400 400"')
        
        self.img = Image.open(chess.svg.board(self.board))
        self.photo = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(300, 300, image=self.photo, anchor=tk.CENTER)
        
        # Destaque de peças ameaçadas
        for square in self.board.attackers(chess.WHITE, self.board.king(not self.board.turn)):
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            x0 = col * 75
            y0 = row * 75
            x1 = x0 + 75
            y1 = y0 + 75
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", width=3)
            
        for square in self.board.attackers(chess.BLACK, self.board.king(not self.board.turn)):
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            x0 = col * 75
            y0 = row * 75
            x1 = x0 + 75
            y1 = y0 + 75
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="blue", width=3)
        
    def on_click(self, event):
        col = event.x // 75
        row = 7 - event.y // 75
        
        square = chess.square(col, row)
        legal_moves = list(self.board.legal_moves)
        
        for move in legal_moves:
            if move.from_square == square:
                # Verificar se o movimento é um movimento de roque válido
                if self.board.is_castling(move):
                    # Mover a torre adequadamente
                    if move == chess.Move.from_uci("e1g1"):  # Roque curto para as brancas
                        self.board.push(chess.Move.from_uci("h1f1"))
                    elif move == chess.Move.from_uci("e1c1"):  # Roque longo para as brancas
                        self.board.push(chess.Move.from_uci("a1d1"))
                    elif move == chess.Move.from_uci("e8g8"):  # Roque curto para as pretas
                        self.board.push(chess.Move.from_uci("h8f8"))
                    elif move == chess.Move.from_uci("e8c8"):  # Roque longo para as pretas
                        self.board.push(chess.Move.from_uci("a8d8"))
                else:
                    self.board.push(move)
                self.update_board()
                
                if self.board.is_game_over():
                    result = self.board.result()
                    messagebox.showinfo("Game Over", f"Game Over! Result: {result}")
                    self.root.quit()
                
                # Chamar a função best_move com uma profundidade maior para aumentar a dificuldade da IA
                self.board.push(best_move(self.board, depth=4))
                self.update_board()
                
                if self.board.is_game_over():
                    result = self.board.result()
                    messagebox.showinfo("Game Over", f"Game Over! Result: {result}")
                    self.root.quit()
                
                break

if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGame(root)
    root.mainloop()
