#!/usr/bin/python3
import random
import os

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Minesweeper:
    def __init__(self, width=8, height=8, mines=10):
        self.width = width
        self.height = height
        self.mines = set(random.sample(range(width * height), mines))
        self.revealed = [[False]*width for _ in range(height)]

    def count_mines_nearby(self, x, y):
        count = 0
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (ny*self.width + nx) in self.mines:
                        count += 1
        return count

    def print_board(self, reveal=False):
        clear_screen()
        print("   " + " ".join(str(i) for i in range(self.width)))
        for y in range(self.height):
            print(y, end="  ")
            for x in range(self.width):
                if reveal or self.revealed[y][x]:
                    if (y*self.width+x) in self.mines:
                        print(RED+"*"+RESET, end=" ")
                    else:
                        c = self.count_mines_nearby(x,y)
                        if c == 0:
                            print(" ", end=" ")
                        else:
                            print(BLUE+str(c)+RESET, end=" ")
                else:
                    print(".", end=" ")
            print()

    def reveal(self,x,y):
        if (y*self.width+x) in self.mines:
            return False
        self.revealed[y][x] = True

        if self.count_mines_nearby(x,y) == 0:
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    nx, ny = x+dx, y+dy
                    if 0<=nx<self.width and 0<=ny<self.height:
                        if not self.revealed[ny][nx]:
                            self.reveal(nx,ny)
        return True

    def play(self):
        while True:
            self.print_board()
            try:
                x = int(input("x: "))
                y = int(input("y: "))

                if not (0 <= x < self.width and 0 <= y < self.height):
                    print("Out of range!")
                    continue

                if not self.reveal(x,y):
                    self.print_board(reveal=True)
                    print(RED+"Game Over! You hit a mine."+RESET)
                    break

            except ValueError:
                print("Enter numbers only!")

if __name__ == "__main__":
    Minesweeper().play()