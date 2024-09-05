import json
import threading
from tkinter import messagebox

import pygame


class TicTacToe:
    def __init__(self, send, recv):
        pygame.init()
        self.width = 500
        self.height = 500
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"Tic Tac Toe")
        # show your turn
        self.board = [['', '', ''], ['', '', ''], ['', '', '']]
        self.turn = 'X'
        self.winner = None
        self.font = pygame.font.Font(None, 100)
        self.your_turn = True
        self.send = send
        self.recv = recv
        self.game_over = False
    
    def start_game(self):
        self.multiplayer()

    def draw_board(self):
        self.screen.fill((255,255,240))
        for i in range(1, 3):
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.height / 3), 
                             (self.width, i * self.height / 3), 5)
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.width / 3, 0), 
                             (i * self.width / 3, self.height), 5)
        for i in range(3):
            for j in range(3):
                text = self.font.render(self.board[i][j], True, (0, 0, 0))
                text_rect = text.get_rect(
                    center=((j * self.width / 3) + self.width / 6, 
                            (i * self.height / 3) + self.height / 6))
                self.screen.blit(text, text_rect)

    def make_move(self, row, col):
        if self.board[row][col] == '':
            self.board[row][col] = self.turn
            if self.turn == 'X':
                self.turn = 'O'
            else:
                self.turn = 'X'
            self.send(json.dumps({"action": "gaming", 
                                  "choice": [row, col], 
                                  "turn": self.turn}))
        self.check_winner()

    def recv_data(self):
        while not self.winner:
            data = self.recv()
            if data:
                print("recv", data)
                data = json.loads(data)
                self.make_move(data["choice"][0], 
                               data["choice"][1])
                self.your_turn = True

    def check_winner(self):
        def is_board_full(board):
            for row in board:
                for cell in row:
                    if cell == '':
                        return False
            return True

        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                self.winner = self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                self.winner = self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            self.winner = self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            self.winner = self.board[0][2]
        if is_board_full(self.board) and not self.winner:
            self.winner = 'tie'
        if self.winner:
            print(self.winner)
            self.send(json.dumps({"action": "gameover", "winner": self.winner}))
            self.game_over = True
            return self.winner

    def multiplayer(self):
        pygame.display.set_caption(f"Tic Tac Toe - You: {'  X ' if self.your_turn else ' O  '}")
        global event
        recv_thread = threading.Thread(target=self.recv_data)
        recv_thread.daemon = True
        recv_thread.start()
        while not self.winner:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    return
            self.show_turn()

            if self.your_turn:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = int(x // (self.width / 3))
                    row = int(y // (self.height / 3))
                    self.make_move(row, col)
                    self.draw_board()
                    pygame.display.update()
                    self.your_turn = False
            if self.game_over:
                break
        self.show_turn()
        
        # create a message box to display the winner's information
        messagebox.showinfo("Game Over", f"{self.winner} wins !")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def show_turn(self):
        self.draw_board()
        pygame.display.update()
    
    def game_is_over(self):
        return self.game_over


class ResultScreen:
    def __init__(self, winner):
        pygame.init()
        self.width = 600
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game Over")
        self.font = pygame.font.Font(None, 100)
        self.winner_text = self.font.render(f"{winner}", True, (255, 255, 255))
        self.winner_rect = self.winner_text.get_rect(center=(self.width / 2, self.height / 2))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    return
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.winner_text, self.winner_rect)
            pygame.display.update()


if __name__ == '__main__':
    game = TicTacToe(send=None, recv=None)
    game.start_game()
    while not game.game_is_over():
        pass
    winner = 'X'  # or 'O'
    result_screen = ResultScreen(winner)
    result_screen.run()
