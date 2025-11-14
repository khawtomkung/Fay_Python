"""
Tong777 Casino Game - Enhanced Version
========================================
This version incorporates:
- Error Handling (try-except, custom exceptions)
- OOP (classes for Player, Game, Wallet)
- File Handling with Context Managers
- Decorators (logging, timing, validation)
- Iterators and Generators
- NumPy for game statistics
- Matplotlib for game history visualization
"""

import random
import os
import sys
import tty
import termios
import time
import bcrypt

from datetime import datetime
from typing import Generator, Iterator, List, Dict, Tuple, Optional
import json
from functools import wraps
from abc import ABC, abstractmethod

# Optional imports (will handle if not available)
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("⚠️  NumPy not available. Statistics features will be limited.")

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  Matplotlib not available. Visualization features disabled.")

# ============================================================
# Banner / Pictures
# ============================================================
# RubiFont
tong_777_pic = r"""



                            ████████╗ ██████╗ ███╗   ██╗ ██████╗███████╗███████╗███████╗
                            ╚══██╔══╝██╔═══██╗████╗  ██║██╔════╝╚════██║╚════██║╚════██║
                              ██║   ██║   ██║██╔██╗ ██║██║  ███╗   ██╔╝    ██╔╝    ██╔╝
                              ██║   ██║   ██║██║╚██╗██║██║   ██║  ██╔╝    ██╔╝    ██╔╝ 
                              ██║   ╚██████╔╝██║ ╚████║╚██████╔╝  ██║     ██║     ██║  
                              ╚═╝    ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝   ╚═╝     ╚═╝     ╚═╝  


______________________________________________________________________________________________________________________________
"""

login_pic = r"""


                                            ▗▖    ▗▄▖  ▗▄▄▖▗▄▄▄▖▗▖  ▗▖
                                            ▐▌   ▐▌ ▐▌▐▌     █  ▐▛▚▖▐▌
                                            ▐▌   ▐▌ ▐▌▐▌▝▜▌  █  ▐▌ ▝▜▌
                                            ▐▙▄▄▖▝▚▄▞▘▝▚▄▞▘▗▄█▄▖▐▌  ▐▌


                                                   [1] Login
                                                   [2] Register
                                                   [3] Exit

"""

loading_pic = r"""


                                       ▗▖    ▗▄▖  ▗▄▖ ▗▄▄▄ ▗▄▄▄▖▗▖  ▗▖ ▗▄▄▖
                                       ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌  █  █  ▐▛▚▖▐▌▐▌   
                                       ▐▌   ▐▌ ▐▌▐▛▀▜▌▐▌  █  █  ▐▌ ▝▜▌▐▌▝▜▌
                                       ▐▙▄▄▖▝▚▄▞▘▐▌ ▐▌▐▙▄▄▀▗▄█▄▖▐▌  ▐▌▝▚▄▞▘ ▗▖▗▖▗▖
"""

menu_pic = r"""
                                             ▗▖  ▗▖▗▄▄▄▖▗▖  ▗▖▗▖ ▗▖
                                             ▐▛▚▞▜▌▐▌   ▐▛▚▖▐▌▐▌ ▐▌
                                             ▐▌  ▐▌▐▛▀▀▘▐▌ ▝▜▌▐▌ ▐▌
                                             ▐▌  ▐▌▐▙▄▄▖▐▌  ▐▌▝▚▄▞▘


                                                 [1] High-Low
                                                 [2] Coin Flip
                                                 [3] Blackjack
                                                 [4] Slots

                                           [5] Deposit    [7] Logout
                                           [6] Withdraw   [8] Exit
"""

qr_promptpay_pic = r"""
                                                         
                █████████████████████          ███   ███   ███   █████████          █████████████████████         
                ███               ███          ███                     ███          ██                ███         
                ███               ███    ███   ███      ███   ███      ███   ███    ██                ███         
                ███   █████████   ███       █████████         █████████   ███       ██    █████████   ███         
                ███   █████████   ███       █████████         █████████   ███       ██    █████████   ███         
                ███   █████████   ███          ███      ███   ███   ███   ███       ██    █████████   ███         
                ███   █████████   ███          ███            ███   ███             ██    █████████   ███         
                ███   █████████   ███    ███   ██████      ███████████████          ██    █████████   ███         
                ███               ███       █████████    ██   ███   ████████████    ██                ███         
                ███               ███       █████████   ███   ███   ████████████    ██                ███         
                █████████████████████    ███   ███   ███   ███   ███   ███   ███    █████████████████████         
                                                                            ███                                  
                                            ███         ███                  ██                                   
                ███   ███   ███   ███       ███   ███      ███   ████████████             ███      ███            
                ███   ███   ███   ███       ███   ███      ███   ████████████             ███      ███            
                ███   ███   ██████    ████████████   ██████            █████████    ██████████████████            
                ███   ██████   ██████    ██████   ███████████████   ██████    █████    ███         ███         
                ███   ██████   ██████    ██████   ███████████████   ██████    █████    ███         ███         
                ██████████████████    ██████   ████████████         ██████   ██████    ██     ██   ███            
                ██████████████████    ██████   ████████████         ██████   ██████    ██    ███   ███            
                ████████████   █████████████   ███   █████████               ███    ████████████   ██████         
                █████████             ██    ███   ███ █          ██████   ███    ██    ██          ██████         
                █████████             ██    ███   ████            █████   ███    ██    ██          ██████         
                ███         ███████████████████                  ██████          ██          ███   ███         
                ███         ███████████████████                  ██████          ██          ███   ███         
                ███      ███          ███   ███   █             ███████   ██████    ██████   ███   ███         
                ██ ███          █████          ██████                ███████████    ██    █████████   ███         
                ██████         ██████          ██████      ███   ███████████████    ██    █████████   ███         
                ███████████████    ██████      ███         ███   ███      ██████          ███   ███            
                ███████████████    ██████      ███         ███   ███      ██████          ███   ███            
                ███   █████████   ███    ██████   █████████      █████████   ███    ██    ███         ███         
                ███                ██████   ██ ███               ███   ███    ██    ██          ███            
                ███                ██████   ██████               ███   ███    ██    ██          ███            
                ███   ███   ███   ███    ██████      ███         ██████   █████████████████████████   ███         
                ███   ███   ███   ███    ██████      ███         ██████   █████████████████████████   ███         
                                        ███   ███   ██████         ███   ██████          ███   ██████            
                █████████████████████       ██████   ███   ███   ███      ██████    ██    ███         ███         
                █████████████████████       █████    ██    ███   ███      ██████    ██    ███         ███         
                ███               ███             ████████████      ███   ██████          ██████                  
                ███               ███             ████████████      ███   ██████          ██████                  
                ███   █████████   ███    ██████            ███      ██████   ████████████████████████████         
                ███   █████████   ███             ██████   ███   ██████   ███    █     ██    ███   ███            
                ███   █████████   ███             ██████   ███   ██████   ███    ██    ██    ███   ███            
                ███   █████████   ███    ███                                 ███          ███   ███   ███         
                ███   █████████   ███    ███                                 ███          ███   ███   ███         
                ███               ███       █████████   ███   ███      ███       █████       ██████               
                █████████████████████    ███   ███         ███   ███████████████          ███   ███   ███         
                █████████████████████    ███   ███         ███   ███████████████          ███   ███   ███         

                                                    Promptpay: 0952546825
                                                        Napat Buaklang
"""


# ============================================================
# CUSTOM EXCEPTIONS (Error Handling)
# ============================================================

class GameException(Exception):
    """
    Base exception for all game-related errors.
    
    Input:
        message (str): Error message to display
    
    Output:
        Exception instance
    
    Description:
        Custom base exception class for better error handling in the game.
    """
    pass


class InsufficientFundsError(GameException):
    """
    Exception raised when player doesn't have enough credits.
    
    Input:
        required (float): Amount required
        available (float): Amount available
    
    Output:
        Exception instance
    
    Description:
        Raised when attempting to bet more than available balance.
    """
    def __init__(self, required: float, available: float):
        self.required = required
        self.available = available
        super().__init__(f"Insufficient funds! Required: {required:.2f}, Available: {available:.2f}")


class InvalidBetError(GameException):
    """
    Exception raised for invalid bet amounts.
    
    Input:
        message (str): Description of why bet is invalid
    
    Output:
        Exception instance
    
    Description:
        Raised when bet amount is invalid (negative, zero, or malformed).
    """
    pass


class FileOperationError(GameException):
    """
    Exception raised for file operation failures.
    
    Input:
        operation (str): Type of operation (read/write)
        filename (str): Name of file
        original_error (Exception): Original exception that occurred
    
    Output:
        Exception instance
    
    Description:
        Raised when file operations fail (loading/saving player data).
    """
    def __init__(self, operation: str, filename: str, original_error: Exception):
        self.operation = operation
        self.filename = filename
        self.original_error = original_error
        super().__init__(f"Failed to {operation} file '{filename}': {str(original_error)}")


# ============================================================
# DECORATORS (Advanced Concept)
# ============================================================

def log_game_action(func):
    """
    Decorator to log game actions with timestamp.
    
    Input:
        func (callable): Function to be decorated
    
    Output:
        callable: Wrapped function that logs actions
    
    Description:
        Logs function calls with timestamp to game_log.txt.
        Useful for tracking player actions and debugging.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        func_name = func.__name__
        
        try:
            result = func(*args, **kwargs)
            log_entry = f"[{timestamp}] SUCCESS: {func_name}\n"
            with open("game_log.txt", "a") as log_file:
                log_file.write(log_entry)
            return result
        except Exception as e:
            log_entry = f"[{timestamp}] ERROR in {func_name}: {str(e)}\n"
            with open("game_log.txt", "a") as log_file:
                log_file.write(log_entry)
            raise
    
    return wrapper


def timing_decorator(func):
    """
    Decorator to measure function execution time.
    
    Input:
        func (callable): Function to be timed
    
    Output:
        callable: Wrapped function that prints execution time
    
    Description:
        Measures and prints how long a function takes to execute.
        Useful for performance optimization.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"⏱️  {func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper


def validate_positive(func):
    """
    Decorator to validate that bet amount is positive.
    
    Input:
        func (callable): Function that takes bet as first argument
    
    Output:
        callable: Wrapped function with validation
    
    Description:
        Ensures the first numeric argument (bet) is positive before execution.
        Raises InvalidBetError if validation fails.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Assume first numeric arg after self is the bet
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise InvalidBetError("Bet amount cannot be negative!")
        return func(*args, **kwargs)
    return wrapper


# ============================================================
# ITERATORS AND GENERATORS (Advanced Concept)
# ============================================================

class CardDeck(Iterator):
    """
    Iterator for dealing cards in sequence.
    
    Input:
        min_value (int): Minimum card value (default 1)
        max_value (int): Maximum card value (default 11)
    
    Output:
        Iterator yielding card values
    
    Description:
        Implements Iterator protocol for dealing cards.
        Shuffles deck when created and yields cards one by one.
    """
    def __init__(self, min_value: int = 1, max_value: int = 11):
        self.cards = list(range(min_value, max_value + 1)) * 4  # 4 suits
        random.shuffle(self.cards)
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self) -> int:
        if self.index >= len(self.cards):
            raise StopIteration
        card = self.cards[self.index]
        self.index += 1
        return card
    
    def reset(self):
        """Reset and reshuffle the deck."""
        random.shuffle(self.cards)
        self.index = 0


def game_history_generator(filename: str) -> Generator[Dict, None, None]:
    """
    Generator that yields game history entries one at a time.
    
    Input:
        filename (str): Path to history file
    
    Output:
        Generator yielding dict entries
    
    Description:
        Memory-efficient way to read large game history files.
        Yields one game record at a time without loading entire file.
    """
    try:
        with open(filename, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        continue
    except FileNotFoundError:
        return


def fibonacci_bet_sequence(max_bet: float) -> Generator[float, None, None]:
    """
    Generator for Fibonacci betting sequence.
    
    Input:
        max_bet (float): Maximum bet allowed
    
    Output:
        Generator yielding bet amounts
    
    Description:
        Yields Fibonacci sequence values as suggested bet amounts.
        Useful for progressive betting strategies.
        Stops when next value exceeds max_bet.
    """
    a, b = 1, 1
    while a <= max_bet:
        yield float(a)
        a, b = b, a + b


# ============================================================
# OOP CLASSES
# ============================================================

class Wallet:
    """
    Wallet class to manage player's money with transaction history.
    
    Input:
        initial_balance (float): Starting balance
    
    Output:
        Wallet instance
    
    Description:
        Manages player's balance with methods for deposit, withdraw, and bet.
        Maintains transaction history using NumPy arrays if available.
    """
    def __init__(self, initial_balance: float = 0.0):
        self._balance = float(initial_balance)
        self.transactions: List[Tuple[str, float, datetime]] = []
        
    @property
    def balance(self) -> float:
        """Get current balance."""
        return self._balance
    
    @balance.setter
    def balance(self, value: float):
        """Set balance with validation."""
        if value < 0:
            raise ValueError("Balance cannot be negative!")
        self._balance = value
    
    def deposit(self, amount: float) -> None:
        """
        Deposit money into wallet.
        
        Input:
            amount (float): Amount to deposit
        
        Output:
            None
        
        Description:
            Adds amount to balance and records transaction.
        """
        if amount <= 0:
            raise InvalidBetError("Deposit amount must be positive!")
        self._balance += amount
        self.transactions.append(("DEPOSIT", amount, datetime.now()))
    
    def withdraw(self, amount: float) -> None:
        """
        Withdraw money from wallet.
        
        Input:
            amount (float): Amount to withdraw
        
        Output:
            None
        
        Description:
            Subtracts amount from balance if sufficient funds exist.
        """
        if amount <= 0:
            raise InvalidBetError("Withdrawal amount must be positive!")
        if amount > self._balance:
            raise InsufficientFundsError(amount, self._balance)
        self._balance -= amount
        self.transactions.append(("WITHDRAW", amount, datetime.now()))
    
    def place_bet(self, amount: float) -> None:
        """
        Place a bet (deduct from balance).
        
        Input:
            amount (float): Bet amount
        
        Output:
            None
        
        Description:
            Validates and deducts bet from balance.
        """
        if amount <= 0:
            raise InvalidBetError("Bet must be positive!")
        if amount > self._balance:
            raise InsufficientFundsError(amount, self._balance)
        self._balance -= amount
        self.transactions.append(("BET", -amount, datetime.now()))
    
    def win_payout(self, amount: float) -> None:
        """
        Add winnings to balance.
        
        Input:
            amount (float): Winning amount
        
        Output:
            None
        
        Description:
            Adds winning amount to balance and records transaction.
        """
        if amount < 0:
            raise ValueError("Payout cannot be negative!")
        self._balance += amount
        self.transactions.append(("WIN", amount, datetime.now()))
    
    def get_statistics(self) -> Dict:
        """
        Get wallet statistics using NumPy.
        
        Input:
            None
        
        Output:
            dict: Statistics including total deposited, withdrawn, etc.
        
        Description:
            Calculates various statistics from transaction history.
            Uses NumPy for efficient computation if available.
        """
        if not self.transactions:
            return {"total_transactions": 0}
        
        deposits = [t[1] for t in self.transactions if t[0] == "DEPOSIT"]
        withdrawals = [t[1] for t in self.transactions if t[0] == "WITHDRAW"]
        wins = [t[1] for t in self.transactions if t[0] == "WIN"]
        bets = [abs(t[1]) for t in self.transactions if t[0] == "BET"]
        
        stats = {
            "total_transactions": len(self.transactions),
            "total_deposited": sum(deposits),
            "total_withdrawn": sum(withdrawals),
            "total_won": sum(wins),
            "total_bet": sum(bets),
            "net_profit": sum(wins) - sum(bets)
        }
        
        if NUMPY_AVAILABLE and bets:
            bets_array = np.array(bets)
            stats["avg_bet"] = np.mean(bets_array)
            stats["max_bet"] = np.max(bets_array)
            stats["min_bet"] = np.min(bets_array)
            stats["std_bet"] = np.std(bets_array)
        
        return stats


class Player:
    """
    Player class representing a game player.
    
    Input:
        username (str): Player's username
        hashed_password (str): Bcrypt-hashed password
        wallet (Wallet): Player's wallet instance
    
    Output:
        Player instance
    
    Description:
        Represents a player with authentication and game history.
    """
    BASE_PATH = "/Users/kung/Intro to programming_Python/Fay_Python/Tong777_V2/ID_user"
    
    def __init__(self, username: str, hashed_password: str, wallet: Optional[Wallet] = None):
        self.username = username
        self.hashed_password = hashed_password
        self.wallet = wallet or Wallet(100.0)
        self.game_history: List[Dict] = []
        self.login_time = datetime.now()
    
    @classmethod
    def create_new(cls, username: str, password: str) -> 'Player':
        """
        Factory method to create new player.
        
        Input:
            username (str): Desired username
            password (str): Plain text password
        
        Output:
            Player: New player instance
        
        Description:
            Creates new player with hashed password and initial balance.
        """
        if not username or not password:
            raise ValueError("Username and password cannot be empty!")
        
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return cls(username, hashed, Wallet(100.0))
    
    @classmethod
    def load_from_file(cls, username: str) -> Optional['Player']:
        """
        Load player from file using context manager.
        
        Input:
            username (str): Username to load
        
        Output:
            Player or None: Player instance if found
        
        Description:
            Loads player data from JSON file using context manager.
        """
        os.makedirs(cls.BASE_PATH, exist_ok=True)
        filename = os.path.join(cls.BASE_PATH, f"{username}.json")
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                wallet = Wallet(data.get('balance', 100.0))
                player = cls(
                    username=data['username'],
                    hashed_password=data['hashed_password'],
                    wallet=wallet
                )
                player.game_history = data.get('game_history', [])
                return player
        except FileNotFoundError:
            return None
        except (json.JSONDecodeError, KeyError) as e:
            raise FileOperationError("read", filename, e)
    
    def save_to_file(self) -> None:
        """
        Save player data to file using context manager.
        
        Input:
            None
        
        Output:
            None
        
        Description:
            Saves player data to JSON file using context manager.
            Includes balance and game history.
        """
        os.makedirs(self.BASE_PATH, exist_ok=True)
        filename = os.path.join(self.BASE_PATH, f"{self.username}.json")
        
        data = {
            'username': self.username,
            'hashed_password': self.hashed_password,
            'balance': self.wallet.balance,
            'game_history': self.game_history[-100:]  # Keep last 100 games
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise FileOperationError("write", filename, e)
    
    def verify_password(self, password: str) -> bool:
        """
        Verify password against stored hash.
        
        Input:
            password (str): Plain text password to verify
        
        Output:
            bool: True if password matches
        
        Description:
            Uses bcrypt to verify password securely.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))
    
    def add_game_record(self, game_name: str, bet: float, result: float) -> None:
        """
        Add game result to history.
        
        Input:
            game_name (str): Name of game played
            bet (float): Amount bet
            result (float): Win/loss amount
        
        Output:
            None
        
        Description:
            Records game result in player's history.
        """
        record = {
            'game': game_name,
            'bet': bet,
            'result': result,
            'balance_after': self.wallet.balance,
            'timestamp': datetime.now().isoformat()
        }
        self.game_history.append(record)
    
    def get_session_stats(self) -> Dict:
        """
        Get statistics for current session.
        
        Input:
            None
        
        Output:
            dict: Session statistics
        
        Description:
            Calculates win/loss stats for current session.
        """
        session_games = [g for g in self.game_history 
                        if datetime.fromisoformat(g['timestamp']) > self.login_time]
        
        if not session_games:
            return {"games_played": 0}
        
        wins = sum(1 for g in session_games if g['result'] > 0)
        losses = sum(1 for g in session_games if g['result'] < 0)
        total_won = sum(g['result'] for g in session_games if g['result'] > 0)
        total_lost = abs(sum(g['result'] for g in session_games if g['result'] < 0))
        
        return {
            "games_played": len(session_games),
            "wins": wins,
            "losses": losses,
            "win_rate": (wins / len(session_games) * 100) if session_games else 0,
            "total_won": total_won,
            "total_lost": total_lost,
            "net_profit": total_won - total_lost
        }


class Game(ABC):
    """
    Abstract base class for all casino games.
    
    Input:
        player (Player): Player instance
    
    Output:
        Game instance
    
    Description:
        Defines interface that all games must implement.
        Uses ABC (Abstract Base Class) for polymorphism.
    """
    def __init__(self, player: Player):
        self.player = player
    
    @abstractmethod
    def play(self) -> None:
        """
        Main game loop - must be implemented by subclasses.
        
        Input:
            None
        
        Output:
            None
        
        Description:
            Abstract method that each game must implement.
        """
        pass
    
    def get_valid_bet(self) -> float:
        """
        Get and validate bet from user.
        
        Input:
            None (reads from user)
        
        Output:
            float: Valid bet amount (0 to exit)
        
        Description:
            Prompts for bet and validates against balance.
            Returns 0 to exit to main menu.
        """
        while True:
            try:
                bet_str = input(f"💰 Enter bet (0 to exit) [Balance: {self.player.wallet.balance:.2f}]: ").strip()
                bet = float(bet_str)
                
                if bet == 0:
                    return 0.0
                
                if bet < 0:
                    raise InvalidBetError("Bet cannot be negative!")
                
                if bet > self.player.wallet.balance:
                    raise InsufficientFundsError(bet, self.player.wallet.balance)
                
                return round(bet, 2)
                
            except ValueError:
                print("❌ Please enter a valid number!")
            except InvalidBetError as e:
                print(f"❌ {e}")
            except InsufficientFundsError as e:
                print(f"❌ {e}")


class HighLowGame(Game):
    """
    High-Low guessing game implementation.
    
    Input:
        player (Player): Player instance
    
    Output:
        HighLowGame instance
    
    Description:
        Player guesses if next number will be higher or lower.
    """
    @log_game_action
    @validate_positive
    def play(self) -> None:
        """
        Play High-Low game.
        
        Input:
            None
        
        Output:
            None
        
        Description:
            Shows first number, player guesses higher/lower for second number.
        """
        clear_screen()
        print("🎯 High-Low Game 🎯\n")
        
        bet = self.get_valid_bet()
        if bet == 0:
            return
        
        try:
            self.player.wallet.place_bet(bet)
            
            num1 = random.randint(1, 100)
            print(f"First number: {num1}")
            
            guess = input("Will next be (h)igher or (l)ower? ").lower().strip()
            while guess not in ['h', 'l']:
                guess = input("Please enter 'h' or 'l': ").lower().strip()
            
            num2 = random.randint(1, 100)
            print(f"Next number: {num2}\n")
            
            won = (guess == 'h' and num2 > num1) or (guess == 'l' and num2 < num1)
            
            if won:
                winnings = bet * 2
                self.player.wallet.win_payout(winnings)
                self.player.add_game_record("High-Low", bet, bet)
                print(f"🎉 You won {bet:.2f}!")
            else:
                self.player.add_game_record("High-Low", bet, -bet)
                print(f"💀 You lost {bet:.2f}!")
            
            self.player.save_to_file()
            
        except GameException as e:
            print(f"❌ Error: {e}")
            press_to_continue()
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            press_to_continue()


def game_menu(player: Player) -> None:
    """
    Main game menu loop.
    
    Input:
        player (Player): Logged-in player instance
    
    Output:
        None
    
    Description:
        Shows game menu and handles user selections.
        Player can play games, manage wallet, view stats, or logout.
    """
    while True:
        clear_screen()
        print(f"Welcome, {player.username}".center(60))
        print(f"Balance: {player.wallet.balance:.2f} credits".center(60))
        print("\n🎮 GAMES:")
        print("[1] High-Low")
        print("[2] Blackjack")
        print("[3] Coin Flip")
        print("[4] Slots")
        
        print("\n💰 WALLET:")
        print("[5] Deposit")
        print("[6] Withdraw")
        
        print("\n📊 INFO:")
        print("[7] Statistics")
        print("[8] Fibonacci Bet Helper")
        
        print("\n⚙️  SYSTEM:")
        print("[9] Logout")
        print("[0] Save & Exit\n")
        
        choice = input("Select option: ").strip()
        
        try:
            if choice == '1':
                game = HighLowGame(player)
                game.play()
                press_to_continue()
            
            elif choice == '2':
                game = BlackjackGame(player)
                game.play()
                press_to_continue()
            
            elif choice == '3':
                game = CoinFlipGame(player)
                game.play()
                press_to_continue()
            
            elif choice == '4':
                game = SlotsGame(player)
                game.play()
                press_to_continue()
            
            elif choice == '5':
                deposit_menu(player)
            
            elif choice == '6':
                withdraw_menu(player)
            
            elif choice == '7':
                show_statistics(player)
                press_to_continue()
            
            elif choice == '8':
                show_fibonacci_helper(player)
                press_to_continue()
            
            elif choice == '9':
                print("🔁 Logging out...")
                player.save_to_file()
                time.sleep(1)
                return
            
            elif choice == '0':
                print("💾 Saving and exiting...")
                player.save_to_file()
                time.sleep(1)
                sys.exit()
            
            else:
                print("❌ Invalid option!")
                press_to_continue()
        
        except GameException as e:
            print(f"❌ Game error: {e}")
            press_to_continue()
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            press_to_continue()


def deposit_menu(player: Player) -> None:
    """
    Handle deposit transaction.
    
    Input:
        player (Player): Player instance
    
    Output:
        None
    
    Description:
        Prompts user for deposit amount and updates wallet.
    """
    clear_screen()
    print("💰 Deposit Credits 💰\n")
    print(f"Current balance: {player.wallet.balance:.2f}")
    
    try:
        amount_str = input("\nEnter deposit amount: ").strip()
        amount = float(amount_str)
        
        if amount <= 0:
            raise InvalidBetError("Deposit amount must be positive!")
        
        player.wallet.deposit(amount)
        player.save_to_file()
        print(f"\n✅ Successfully deposited {amount:.2f} credits!")
        print(f"New balance: {player.wallet.balance:.2f}")
        
    except ValueError:
        print("❌ Invalid amount!")
    except GameException as e:
        print(f"❌ {e}")
    
    press_to_continue()


def withdraw_menu(player: Player) -> None:
    """
    Handle withdrawal transaction.
    
    Input:
        player (Player): Player instance
    
    Output:
        None
    
    Description:
        Prompts user for withdrawal amount and updates wallet.
    """
    clear_screen()
    print("💸 Withdraw Credits 💸\n")
    print(f"Current balance: {player.wallet.balance:.2f}")
    
    try:
        amount_str = input("\nEnter withdrawal amount: ").strip()
        amount = float(amount_str)
        
        player.wallet.withdraw(amount)
        player.save_to_file()
        print(f"\n✅ Successfully withdrew {amount:.2f} credits!")
        print(f"New balance: {player.wallet.balance:.2f}")
        
    except ValueError:
        print("❌ Invalid amount!")
    except GameException as e:
        print(f"❌ {e}")
    
    press_to_continue()


def show_fibonacci_helper(player: Player) -> None:
    """
    Show Fibonacci betting sequence helper.
    
    Input:
        player (Player): Player instance
    
    Output:
        None
    
    Description:
        Displays Fibonacci sequence up to player's balance.
        Uses generator for memory efficiency.
    """
    clear_screen()
    print("🔢 Fibonacci Betting Helper 🔢\n")
    print(f"Your balance: {player.wallet.balance:.2f}\n")
    print("Suggested bet amounts (Fibonacci sequence):\n")
    
    fib_gen = fibonacci_bet_sequence(player.wallet.balance)
    bets = list(fib_gen)
    
    for i, bet in enumerate(bets[:15], 1):  # Show first 15
        print(f"  Step {i}: {bet:.2f} credits")
    
    if len(bets) > 15:
        print(f"\n  ... and {len(bets) - 15} more steps")
    
    print("\n💡 Tip: Fibonacci betting is a progressive strategy.")
    print("   Increase bet following this sequence after losses.")


class CoinFlipGame(Game):
    """
    Coin flip game implementation.
    
    Input:
        player (Player): Player instance
    
    Output:
        CoinFlipGame instance
    
    Description:
        Simple heads or tails guessing game.
    """
    @log_game_action
    @validate_positive
    def play(self) -> None:
        """
        Play coin flip game.
        
        Input:
            None
        
        Output:
            None
        
        Description:
            Player guesses heads or tails, coin is flipped randomly.
        """
        clear_screen()
        print("🪙 Coin Flip Game 🪙\n")
        
        bet = self.get_valid_bet()
        if bet == 0:
            return
        
        try:
            self.player.wallet.place_bet(bet)
            
            guess = input("Choose (h)eads or (t)ails: ").lower().strip()
            while guess not in ['h', 't']:
                guess = input("Please enter 'h' or 't': ").lower().strip()
            
            result = random.choice(['h', 't'])
            result_name = 'Heads' if result == 'h' else 'Tails'
            
            print(f"\nFlipping... 🪙")
            time.sleep(1)
            print(f"Result: {result_name}!\n")
            
            if guess == result:
                winnings = bet * 2
                self.player.wallet.win_payout(winnings)
                self.player.add_game_record("Coin Flip", bet, bet)
                print(f"🎉 You won {bet:.2f}!")
            else:
                self.player.add_game_record("Coin Flip", bet, -bet)
                print(f"💀 You lost {bet:.2f}!")
            
            self.player.save_to_file()
            
        except GameException as e:
            print(f"❌ Game error: {e}")


class SlotsGame(Game):
    """
    Slot machine game implementation.
    
    Input:
        player (Player): Player instance
    
    Output:
        SlotsGame instance
    
    Description:
        Three-reel slot machine with emoji symbols.
    """
    SYMBOLS = ['🍒', '🍋', '🍊', '🍇', '💎', '7️⃣', '🎰']
    PAYOUTS = {
        '💎': 50,
        '7️⃣': 100,
        '🎰': 250
    }
    
    @log_game_action
    @validate_positive
    def play(self) -> None:
        """
        Play slots game.
        
        Input:
            None
        
        Output:
            None
        
        Description:
            Spins three reels, pays out based on matching symbols.
        """
        clear_screen()
        print("🎰 Slot Machine 🎰\n")
        
        bet = self.get_valid_bet()
        if bet == 0:
            return
        
        try:
            self.player.wallet.place_bet(bet)
            
            print("Spinning...\n")
            
            # Spin animation
            for _ in range(5):
                reels = [random.choice(self.SYMBOLS) for _ in range(3)]
                print(f"\r| {reels[0]} | {reels[1]} | {reels[2]} |", end="", flush=True)
                time.sleep(0.2)
            
            # Final result
            final_reels = [random.choice(self.SYMBOLS) for _ in range(3)]
            print(f"\r| {final_reels[0]} | {final_reels[1]} | {final_reels[2]} |\n")
            
            # Check for win
            if final_reels[0] == final_reels[1] == final_reels[2]:
                symbol = final_reels[0]
                multiplier = self.PAYOUTS.get(symbol, 10)
                winnings = bet * multiplier
                self.player.wallet.win_payout(bet + winnings)
                self.player.add_game_record("Slots", bet, winnings)
                print(f"🎉 JACKPOT! Three {symbol}!")
                print(f"You won {winnings:.2f} credits! (x{multiplier})")
            elif final_reels[0] == final_reels[1] or final_reels[1] == final_reels[2] or final_reels[0] == final_reels[2]:
                winnings = bet * 2
                self.player.wallet.win_payout(winnings)
                self.player.add_game_record("Slots", bet, bet)
                print(f"✨ Pair! You won {bet:.2f} credits! (x2)")
            else:
                self.player.add_game_record("Slots", bet, -bet)
                print(f"💀 No match. You lost {bet:.2f} credits.")
            
            self.player.save_to_file()
            
        except GameException as e:
            print(f"❌ Game error: {e}")


# ============================================================
# NUMPY ANALYSIS UTILITIES
# ============================================================

class GameAnalytics:
    """
    Game analytics using NumPy for statistical analysis.
    
    Input:
        player (Player): Player instance
    
    Output:
        GameAnalytics instance
    
    Description:
        Provides advanced statistical analysis of game history.
        Requires NumPy to be installed.
    """
    def __init__(self, player: Player):
        self.player = player
        if not NUMPY_AVAILABLE:
            raise ImportError("NumPy is required for analytics!")
    
    def win_rate_by_game(self) -> Dict[str, float]:
        """
        Calculate win rate for each game type.
        
        Input:
            None
        
        Output:
            dict: Game name -> win rate percentage
        
        Description:
            Uses NumPy to calculate win rates efficiently.
        """
        games_dict = {}
        for record in self.player.game_history:
            game_name = record['game']
            if game_name not in games_dict:
                games_dict[game_name] = []
            games_dict[game_name].append(1 if record['result'] > 0 else 0)
        
        win_rates = {}
        for game, results in games_dict.items():
            results_array = np.array(results)
            win_rates[game] = np.mean(results_array) * 100
        
        return win_rates
    
    def calculate_volatility(self) -> float:
        """
        Calculate betting volatility (standard deviation).
        
        Input:
            None
        
        Output:
            float: Standard deviation of bet amounts
        
        Description:
            Measures how much bet sizes vary.
        """
        if not self.player.game_history:
            return 0.0
        
        bets = np.array([g['bet'] for g in self.player.game_history])
        return np.std(bets)
    
    def predict_next_balance(self) -> float:
        """
        Simple linear prediction of next balance.
        
        Input:
            None
        
        Output:
            float: Predicted balance
        
        Description:
            Uses linear regression on balance history.
            (Simplified version for demonstration)
        """
        if len(self.player.game_history) < 5:
            return self.player.wallet.balance
        
        balances = np.array([g['balance_after'] for g in self.player.game_history[-10:]])
        x = np.arange(len(balances))
        
        # Simple linear fit
        coeffs = np.polyfit(x, balances, 1)
        next_x = len(balances)
        predicted = coeffs[0] * next_x + coeffs[1]
        
        return max(0, predicted)


# ============================================================
# CONTEXT MANAGER FOR GAME SESSION
# ============================================================

class GameSession:
    """
    Context manager for game sessions.
    
    Input:
        player (Player): Player instance
    
    Output:
        GameSession instance
    
    Description:
        Ensures player data is saved even if errors occur.
        Implements context manager protocol (__enter__, __exit__).
    """
    def __init__(self, player: Player):
        self.player = player
        self.session_start = datetime.now()
    
    def __enter__(self):
        """
        Enter context - log session start.
        
        Input:
            None
        
        Output:
            self
        
        Description:
            Called when entering 'with' block.
        """
        print(f"🎮 Session started at {self.session_start.strftime('%H:%M:%S')}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit context - save player data and log session end.
        
        Input:
            exc_type: Exception type if error occurred
            exc_val: Exception value
            exc_tb: Exception traceback
        
        Output:
            bool: False to propagate exceptions
        
        Description:
            Always saves player data, even if error occurred.
        """
        session_end = datetime.now()
        duration = (session_end - self.session_start).total_seconds()
        
        try:
            self.player.save_to_file()
            print(f"\n💾 Session saved. Duration: {duration:.1f} seconds")
        except Exception as e:
            print(f"❌ Failed to save session: {e}")
        
        # Log session info
        with open("session_log.txt", "a") as f:
            f.write(f"[{self.session_start}] User: {self.player.username}, "
                   f"Duration: {duration:.1f}s, "
                   f"Final Balance: {self.player.wallet.balance:.2f}\n")
        
        return False  # Don't suppress exceptions


# ============================================================
# MAIN ENTRY POINT
# ============================================================

class BlackjackGame(Game):
    """
    Blackjack card game implementation.
    
    Input:
        player (Player): Player instance
    
    Output:
        BlackjackGame instance
    
    Description:
        Classic blackjack with hit/stand mechanics.
        Uses CardDeck iterator for dealing cards.
    """
    @log_game_action
    def play(self) -> None:
        """
        Play Blackjack game.
        
        Input:
            None
        
        Output:
            None
        
        Description:
            Player and dealer draw cards trying to reach 21.
            Player can hit or stand. Dealer must hit until 17.
        """
        clear_screen()
        print("🃏 Blackjack 🃏\n")
        
        bet = self.get_valid_bet()
        if bet == 0:
            return
        
        try:
            self.player.wallet.place_bet(bet)
            deck = CardDeck()
            
            # Deal initial cards
            player_hand = [next(deck), next(deck)]
            dealer_hand = [next(deck), next(deck)]
            
            print(f"Dealer shows: 🂠 + {dealer_hand[0]}")
            print(f"Your cards: {player_hand} (Total: {sum(player_hand)})\n")
            
            # Player turn
            busted = False
            while sum(player_hand) < 21:
                action = input("(H)it or (S)tand? ").lower().strip()
                if action == 'h':
                    player_hand.append(next(deck))
                    print(f"Your cards: {player_hand} (Total: {sum(player_hand)})")
                    if sum(player_hand) > 21:
                        busted = True
                        break
                elif action == 's':
                    break
            
            if busted:
                self.player.add_game_record("Blackjack", bet, -bet)
                print("\n💀 Bust! You lost!")
            else:
                # Dealer turn
                print(f"\nDealer's cards: {dealer_hand}")
                while sum(dealer_hand) < 17:
                    dealer_hand.append(next(deck))
                    print(f"Dealer draws: {dealer_hand[-1]} (Total: {sum(dealer_hand)})")
                
                player_total = sum(player_hand)
                dealer_total = sum(dealer_hand)
                
                if dealer_total > 21 or player_total > dealer_total:
                    winnings = bet * 2
                    self.player.wallet.win_payout(winnings)
                    self.player.add_game_record("Blackjack", bet, bet)
                    print(f"\n🎉 You won {bet:.2f}!")
                elif player_total == dealer_total:
                    self.player.wallet.win_payout(bet)  # Push
                    self.player.add_game_record("Blackjack", bet, 0)
                    print("\n😐 Push!")
                else:
                    self.player.add_game_record("Blackjack", bet, -bet)
                    print(f"\n💀 Dealer wins!")
            
            self.player.save_to_file()
            
        except GameException as e:
            print(f"❌ Game error: {e}")
        except StopIteration:
            print("❌ Deck empty! Reshuffling...")


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def clear_screen() -> None:
    """Clear terminal screen."""
    os.system('clear' if os.name != 'nt' else 'cls')


def get_char() -> str:
    """Read single character without Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def press_to_continue() -> None:
    """Pause until user presses any key."""
    print("\n\tPress any key to continue...", end="", flush=True)
    get_char()
    print()


@timing_decorator
def show_statistics(player: Player) -> None:
    """
    Display player statistics with visualization.
    
    Input:
        player (Player): Player instance
    
    Output:
        None (prints to console)
    
    Description:
        Shows wallet stats, session stats, and optionally plots history.
    """
    clear_screen()
    print("📊 Your Statistics 📊\n")
    
    # Wallet statistics
    wallet_stats = player.wallet.get_statistics()
    print("💰 Wallet Statistics:")
    for key, value in wallet_stats.items():
        if isinstance(value, float):
            print(f"  {key.replace('_', ' ').title()}: {value:.2f}")
        else:
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Session statistics
    print("\n🎮 Session Statistics:")
    session_stats = player.get_session_stats()
    for key, value in session_stats.items():
        if isinstance(value, float):
            print(f"  {key.replace('_', ' ').title()}: {value:.2f}")
        else:
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Plot history if matplotlib available
    if MATPLOTLIB_AVAILABLE and len(player.game_history) > 1:
        print("\n📈 Generating balance history chart...")
        try:
            balances = [g['balance_after'] for g in player.game_history]
            plt.figure(figsize=(10, 6))
            plt.plot(balances, marker='o', linestyle='-', linewidth=2)
            plt.title(f"{player.username}'s Balance History")
            plt.xlabel("Game Number")
            plt.ylabel("Balance (Credits)")
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(f"{player.username}_history.png")
            print(f"✅ Chart saved as {player.username}_history.png")
        except Exception as e:
            print(f"❌ Could not create chart: {e}")


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    """
    Main program entry point.
    
    Input:
        None
    
    Output:
        None
    
    Description:
        Runs the main game loop with login and game menu.
    """
    print("\n" * 10 + tong_777_pic)
    press_to_continue()
    
    # Login loop
    while True:
        clear_screen()
        print(tong_777_pic.center(60))
        print("\n[1] Login")
        print("[2] Register")
        print("[3] Exit\n")
        
        choice = input("Select option: ").strip()
        
        try:
            if choice == '1':
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                
                player = Player.load_from_file(username)
                if player and player.verify_password(password):
                    print(f"✅ Welcome back, {username}!")
                    time.sleep(1)
                    game_menu(player)
                else:
                    print("❌ Invalid username or password!")
                    press_to_continue()
            
            elif choice == '2':
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                
                if Player.load_from_file(username):
                    print("❌ Username already exists!")
                else:
                    player = Player.create_new(username, password)
                    player.save_to_file()
                    print(f"✅ Account created! You received 100 credits!")
                    press_to_continue()
            
            elif choice == '3':
                print("👋 Goodbye!")
                sys.exit()
            
        except GameException as e:
            print(f"❌")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Game interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n💥 Fatal error: {e}")
        print("Please report this error to the developers.")
        sys.exit(f"1 Game error: {e}")