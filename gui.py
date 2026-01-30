import tkinter as tk
from tkinter import messagebox, font
from game import TicTacToe
from ai import AIPlayer

class TicTacToeGUI:
    """GUI for Tic-Tac-Toe game"""
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("XOXO Game")
        self.window.geometry("400x900")
        self.window.configure(bg='#C7E6EF')

        self.colors = {
            'bg': "#050816", 
            'panel': "#050816",
            'accent': '#6C9CFF',
            'accent_soft': '#8FA8FF',
            'text': '#E6E6F0',
            'muted': '#9A9AB3',
            'x': '#6C9CFF',
            'o': '#FF7A9E',
            'cell': "#060A1D",
            'cell_hover': "#0D153A",
        }
        
        self.window.configure(bg=self.colors['bg'])

        self.game = None
        self.ai = None
        self.buttons = []
        self.human_letter = 'X'
        self.ai_difficulty = 'hard'

        self.wins = 0
        self.losses = 0
        self.draws = 0

        try:
            self.custom_font = font.Font(family="Segoe UI", size=12)
            self.title_font = font.Font(family="Segoe UI", size=32, weight="bold")
            self.board_font = font.Font(family="Segoe UI", size=40, weight="bold")
        except:
            self.custom_font = font.Font(family="Arial", size=12)
            self.title_font = font.Font(family="Arial", size=32, weight="bold")
            self.board_font = font.Font(family="Arial", size=40, weight="bold")
        
        self.create_menu()
        self.create_widgets()
        
        # Запускаем игру сразу
        self.start_new_game()

    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.start_new_game)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.window.quit)
        
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        
        # Difficulty submenu
        difficulty_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label="AI Difficulty", menu=difficulty_menu)
        difficulty_menu.add_command(label="Easy", command=lambda: self.set_difficulty('easy'))
        difficulty_menu.add_command(label="Medium", command=lambda: self.set_difficulty('medium'))
        difficulty_menu.add_command(label="Hard", command=lambda: self.set_difficulty('hard'))
        
        # Player selection
        player_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label="Play As", menu=player_menu)
        player_menu.add_command(label="X (First)", command=lambda: self.set_player('X'))
        player_menu.add_command(label="O (Second)", command=lambda: self.set_player('O'))
    
    def create_widgets(self):
        # MAIN CONTAINER 
        main_frame = tk.Frame(self.window, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        # HEADER 
        header_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 14))

        title_label = tk.Label(
            header_frame,
            text="XOXO",
            font=self.title_font,
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        title_label.pack(side=tk.LEFT)

        subtitle_label = tk.Label(
            header_frame,
            text="vs AI",
            font=self.custom_font,
            bg=self.colors['bg'],
            fg=self.colors['muted']
        )
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0), pady=12)

        # ===== STATS BAR =====
        self.stats_frame = tk.Frame(
            main_frame,
            bg=self.colors['panel'],
            padx=26,
            pady=5
        )
        self.stats_frame.pack(fill=tk.X, pady=(0, 15))

        self.stats_label = tk.Label(
            self.stats_frame,
            text="Ready to play!",
            font=self.custom_font,
            bg=self.colors['panel'],
            fg=self.colors['text']
        )
        self.stats_label.pack()

        # ===== SCORE DISPLAY =====
        self.score_label = tk.Label(
            main_frame,
            text="Wins: 0 | Losses: 0 | Draws: 0",
            font=self.custom_font,
            bg=self.colors['bg'],
            fg=self.colors['muted']
        )
        self.score_label.pack(pady=(0, 20))

        # ===== GAME BOARD =====
        board_container = tk.Frame(main_frame, bg=self.colors['bg'])
        board_container.pack()

        self.buttons = []

        def add_hover_effect(button):
            def on_enter(_):
                if button["state"] == tk.NORMAL and button["text"] == " ":
                    button.config(bg=self.colors['cell_hover'])

            def on_leave(_):
                button.config(bg=self.colors['cell'])

            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)

        for i in range(9):
            row, col = divmod(i, 3)

            cell_frame = tk.Frame(board_container, bg=self.colors['bg'])
            cell_frame.grid(row=row, column=col, padx=8, pady=8)

            btn = tk.Button(
                cell_frame,
                text=" ",
                font=self.board_font,
                width=3,
                height=1,
                bg=self.colors['cell'],
                fg=self.colors['text'],
                relief=tk.FLAT,
                bd=0,
                activebackground=self.colors['cell_hover'],
                cursor="hand2",
                state=tk.DISABLED,
                command=lambda idx=i: self.human_move(idx)
            )
            btn.pack()
            add_hover_effect(btn)
            self.buttons.append(btn)

        # ===== CONTROL PANEL =====
        control_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        control_frame.pack(fill=tk.X, pady=(32, 0))

        def create_modern_button(parent, text, command):
            btn = tk.Button(
                parent,
                text=text,
                font=self.custom_font,
                bg=self.colors['cell'],
                fg=self.colors['text'],
                relief=tk.FLAT,
                bd=0,
                padx=18,
                pady=8,
                cursor="hand2",
                command=command
            )
            btn.bind("<Enter>", lambda _: btn.config(bg=self.colors['cell_hover']))
            btn.bind("<Leave>", lambda _: btn.config(bg=self.colors['cell']))
            return btn

        # Left controls width
        left_controls = tk.Frame(control_frame, bg=self.colors['bg'])
        left_controls.pack(side=tk.LEFT, expand=True)

        new_game_btn = create_modern_button(
            left_controls,
            "New Game",
            self.start_new_game
        )
        new_game_btn.pack(side=tk.LEFT, padx=6)

        settings_btn = create_modern_button(
            left_controls,
            "Settings",
            self.show_settings_modal
        )
        settings_btn.pack(side=tk.LEFT, padx=6)

        # Right controls
        right_controls = tk.Frame(control_frame, bg=self.colors['bg'])
        right_controls.pack(side=tk.RIGHT)

        quit_btn = create_modern_button(
            right_controls,
            "Exit",
            self.window.quit
        )
        quit_btn.pack(side=tk.RIGHT, padx=6)

    def show_settings_modal(self):
        """Show settings modal window"""
        settings_window = tk.Toplevel(self.window)
        settings_window.title("Settings")
        settings_window.geometry("400x500")
        settings_window.configure(bg=self.colors['bg'])
        settings_window.resizable(False, False)
        settings_window.grab_set()  # Make modal
        
        # Center the window
        settings_window.transient(self.window)
        settings_window.grab_set()
        
        # Add settings content
        tk.Label(
            settings_window,
            text="Game Settings",
            font=self.title_font,
            bg=self.colors['bg'],
            fg=self.colors['accent']
        ).pack(pady=20)
        
        # Difficulty selection
        tk.Label(
            settings_window,
            text="AI Difficulty:",
            font=self.custom_font,
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(pady=10)
        
        difficulty_var = tk.StringVar(value=self.ai_difficulty)
        
        for diff in ['easy', 'medium', 'hard']:
            rb = tk.Radiobutton(
                settings_window,
                text=diff.capitalize(),
                variable=difficulty_var,
                value=diff,
                font=self.custom_font,
                bg=self.colors['bg'],
                fg=self.colors['text'],
                selectcolor=self.colors['panel'],
                command=lambda: self.set_difficulty(difficulty_var.get())
            )
            rb.pack()
        
        # Player selection
        tk.Label(
            settings_window,
            text="Play as:",
            font=self.custom_font,
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(pady=20)
        
        player_var = tk.StringVar(value=self.human_letter)
        
        for letter in ['X', 'O']:
            rb = tk.Radiobutton(
                settings_window,
                text=f"{letter} ({'First' if letter == 'X' else 'Second'})",
                variable=player_var,
                value=letter,
                font=self.custom_font,
                bg=self.colors['bg'],
                fg=self.colors['text'],
                selectcolor=self.colors['panel'],
                command=lambda: self.set_player(player_var.get())
            )
            rb.pack()
        
        # Close button
        close_btn = tk.Button(
            settings_window,
            text="Close",
            font=self.custom_font,
            bg=self.colors['accent'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            padx=0,
            pady=10,
            command=settings_window.destroy
        )
        close_btn.pack(pady=20)
    
    def set_difficulty(self, difficulty):
        """Set AI difficulty level"""
        self.ai_difficulty = difficulty
        self.start_new_game()
    
    def set_player(self, letter):
        """Set which letter human plays"""
        self.human_letter = letter
        self.start_new_game()

    def start_new_game(self):
        """Start a new game"""
        self.game = TicTacToe()
        self.ai = AIPlayer('X' if self.human_letter == 'O' else 'O', self.ai_difficulty)
        
        # Reset board buttons
        for btn in self.buttons:
            btn.config(text=' ', state=tk.NORMAL, bg=self.colors['cell'])
        
        # Update status
        self.update_board()
        self.update_status()
        
        # If AI goes first, make its move
        if self.human_letter == 'O':
            self.stats_label.config(text="Thinking... (You are O)")
            self.window.after(1000, self.ai_move)
    
    def update_status(self):
        """Update status label"""
        if self.game.current_winner:
            if self.game.current_winner == self.human_letter:
                self.stats_label.config(text="You win!", fg=self.colors['accent'])
            else:
                self.stats_label.config(text="You lose!", fg='#FF7A9E')
        elif not self.game.empty_squares():
            self.stats_label.config(text="It's a draw!", fg='#F39C12')
        elif self.game.player == self.human_letter:
            letter = 'X' if self.human_letter == 'X' else 'O'
            self.stats_label.config(text=f"Your turn! (You are {letter})", fg=self.colors['text'])
        else:
            self.stats_label.config(text="AI's turn...", fg=self.colors['muted'])

    def update_board(self):
        """Update button texts from game board"""
        for i, spot in enumerate(self.game.board):
            if spot == 'X':
                self.buttons[i].config(text='X', fg=self.colors['x'])
            elif spot == 'O':
                self.buttons[i].config(text='O', fg=self.colors['o'])
            else:
                self.buttons[i].config(text=' ', fg=self.colors['text'])

    def update_score_display(self):
        """Update the score display"""
        self.score_label.config(text=f"Wins: {self.wins} | Losses: {self.losses} | Draws: {self.draws}")
    
    def human_move(self, position):
        """Handle human player's move"""
        if (self.game.current_winner or 
            self.game.player != self.human_letter or
            self.game.board[position] != ' '):
            return
        
        # Make move
        if self.game.make_move(position, self.human_letter):
            self.update_board()
            
            if self.game.current_winner:
                self.game_over()
            elif not self.game.empty_squares():
                self.game_over()
            else:
                self.game.player = self.ai.letter
                self.update_status()
                self.window.after(500, self.ai_move)
    
    def ai_move(self):
        """Handle AI's move"""
        if self.game.current_winner or not self.game.empty_squares():
            return
        
        # Get AI move
        position = self.ai.get_move(self.game)
        
        # Make move
        if self.game.make_move(position, self.ai.letter):
            self.update_board()
            
            if self.game.current_winner:
                self.game_over()
            elif not self.game.empty_squares():
                self.game_over()
            else:
                self.game.player = self.human_letter
                self.update_status()
    
    def game_over(self):
        """Handle game over state"""
        self.update_status()
        
        # Disable all buttons
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        
        # Update scores
        if self.game.current_winner:
            if self.game.current_winner == self.human_letter:
                self.wins += 1
            else:
                self.losses += 1
        else:
            self.draws += 1
        
        self.update_score_display()
        
        # Show message
        if self.game.current_winner:
            winner = "You" if self.game.current_winner == self.human_letter else "AI"
            messagebox.showinfo("Game Over", f"{winner} win!")
        else:
            messagebox.showinfo("Game Over", "It's a draw!")
    
    def run(self):
        """Start the GUI application"""
        self.window.mainloop()

if __name__ == "__main__":
    app = TicTacToeGUI()
    app.run()