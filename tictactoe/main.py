import sys
from game import TicTacToe
from ai import AIPlayer

""" def play_game():
    choice = input("Play as (X/O)? ").upper()
    human_letter = 'X' if choice == 'X' else 'O'
    ai_letter = 'O' if human_letter == 'X' else 'X'

    print("\n" + "="*50)
    print("wellcome to Tic-Tac-Toe")
    print("="*50)
    difficulty = input("Choose AI difficulty (easy/medium/hard): ").lower() 

    while difficulty not in ['easy', 'medium', 'hard']:
        print("Invalid difficulty. Choose from: easy, medium, hard")
        difficulty = input("Choose AI difficulty (easy/medium/hard): ").lower()

    game = TicTacToe()
    game.player = human_letter
    ai = AIPlayer(ai_letter,difficulty)

    while game.empty_squares():
        if game.player == human_letter:
            valid_move = False
            while not valid_move:
                try:
                    square = int(input("Your move(1-9)")) -1
                    if square < 1 or square > 9:
                        print("Invalid move. Try again.")
                        continue
                    game.make_move(square,human_letter)
                    valid_move = True
                except ValueError:
                    print("Please enter a number from 1 to 9")

        else:
            print("AI's move...")
            square = ai.get_move(game)
            game.make_move(square, ai_letter)
            print(f"AI chose cell {square}")

        game.print_board()
        print("-"* 20)

        if game.current_winner:
            if game.current_winner == 'X':
                print("you win")
            else:
                print("you lose")
            break

        game.player = 'O' if game.player == 'X' else 'X'

        if not game.current_winner:
            print("draw") """



def print_welcome():
    """Print welcome message and instructions"""
    choice = input("Play as (X/O)? ").upper()
    human_letter = 'X' if choice == 'X' else 'O'
    ai_letter = 'O' if human_letter == 'X' else 'X'

    print("\n" + "="*50)
    print("wellcome to Tic-Tac-Toe")
    print("="*50)
    difficulty = input("Choose AI difficulty (easy/medium/hard): ").lower() 
   # print("\n" + "="*50)
   # print("        WELCOME TO TIC-TAC-TOE AI")
  #  print("="*50)
  #  print("\nInstructions:")
  #  print("  • You play as X, AI plays as O")
  #  print("  • Enter numbers 0-8 to make your move")
   # print("  • Board positions:")
    
    # Show board positions
    example_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
    for row in example_board:
        print(f"     | {' | '.join(row)} |")
    
    print("\n" + "="*50)

def select_difficulty():
    """Let player select AI difficulty"""
    print("\nSelect AI difficulty:")
    print("  1. Easy")
    print("  2. Medium")
    print("  3. Hard")
    
    while True:
        try:
            choice = input("\nEnter choice (1-3): ").strip()
            if choice == '1':
                return 'easy'
            elif choice == '2':
                return 'medium'
            elif choice == '3':
                return 'hard'
            else:
                print("Please enter 1, 2, or 3")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit(0)

""" def play_console_game():
    difficulty = select_difficulty()
    
    game = TicTacToe()
    ai = AIPlayer('O', difficulty)
    
    print(f"\nStarting game with {difficulty} AI...")
    print("")
    
    while True:
        game.print_board_with_numbers()
        game.print_board()
        
        if game.player == 'X':
            while True:
                try:
                    move = input("\nYour move (1-9, or 'q' to quit): ").strip().lower()
                    
                    if move == 'q':
                        print("\nThanks for playing!")
                        return
                    
                    move = int(move)
                    
                    if move < 1 or move > 9:
                        print("Please enter a number between 1 and 9")
                        continue
                    
                    if move not in game.available_moves():
                        print("That position is already taken!")
                        continue
                    
                    if game.make_move(move, 'X'):
                        break
                        
                except ValueError:
                    print("Please enter a valid number")
                except KeyboardInterrupt:
                    print("\n\nGoodbye!")
                    sys.exit(0)
        
        # AI's turn
        else:
            print("\nAI is thinking...")
            move = ai.get_move(game)
            print(f"AI chooses position {move}")
            game.make_move(move, 'O')
        
        if game.current_winner:
            game.print_board()
            if game.current_winner == 'X':
                print("\n CONGRATULATIONS! YOU WIN!🎉")
            else:
                print("\n AI WINS! Better luck next time! ")
            break
        
        if not game.empty_squares():
            game.print_board()
            print("\n IT'S A DRAW! ")
            break

        game.player = 'O' if game.player == 'X' else 'X'
    
    while True:
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again == 'y':
            return True
        elif again == 'n':
            return False
        else:
            print("Please enter 'y' or 'n'") """


def play_console_game():
    """MAIN GAME LOGIC - весь игровой процесс"""
    # 1. Выбор сложности
    difficulty = select_difficulty()
    
    # 2. Инициализация
    game = TicTacToe()
    ai = AIPlayer('O', difficulty)  # AI всегда 'O'
    
    print(f"\nStarting game with {difficulty} AI...")
    print("You are X, AI is O\n")
    
    # 3. Главный игровой цикл
    while game.empty_squares() and not game.current_winner:
        # Показать доску
        print("\nCurrent board:")
        game.print_board()
        
        # Показать доступные ходы
        available = [i+1 for i in game.available_moves()]
        print(f"Available moves: {available}")
        
        if game.player == 'X':  # Человек
            while True:
                try:
                    move = input("\nYour move (1-9, 'q' to quit): ").strip().lower()
                    
                    if move == 'q':
                        print("\nThanks for playing!")
                        return False
                    
                    move = int(move) - 1  # Конвертируем в 0-8
                    
                    if move not in game.available_moves():
                        print("Invalid move! Choose from available moves.")
                        continue
                    
                    # Делаем ход
                    game.make_move(move, 'X')
                    break
                    
                except ValueError:
                    print("Please enter a number 1-9")
                except KeyboardInterrupt:
                    print("\n\nGame interrupted!")
                    sys.exit(0)
        
        else:  # AI
            print("\nAI is thinking...")
            move = ai.get_move(game)
            game.make_move(move, 'O')
            print(f"AI placed O at position {move + 1}")
        
        # Смена игрока
        game.player = 'O' if game.player == 'X' else 'X'
    
    # 4. Конец игры
    print("\n" + "="*50)
    print("FINAL BOARD:")
    game.print_board()
    
    if game.current_winner:
        if game.current_winner == 'X':
            print("🎉 CONGRATULATIONS! YOU WIN! 🎉")
        else:
            print("🤖 AI WINS! Better luck next time! 🤖")
    else:
        print("🤝 IT'S A DRAW! 🤝")
    
    print("="*50)
    
    # 5. Сыграть еще раз?
    while True:
        again = input("\nPlay again? (y/n): ").lower().strip()
        if again == 'y':
            return True
        elif again == 'n':
            return False
        else:
            print("Please enter 'y' or 'n'")


def main():
    """Main function"""
    print_welcome()
    
    play_again = True
    while play_again:
        play_again = play_console_game()
    
    print("\n" + "="*50)
    print("         THANKS FOR PLAYING!")
    print("="*50 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)