import os
import sys
import time
import random
import bcrypt
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Generator
import subprocess
import platform
import tty
import termios

# ------------------------
# Banner
# ------------------------

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

# ------------------------
# Utility
# ------------------------


def get_char(prompt: str = "") -> str:
    """
    Read and return a single character from input (no Enter required).

    Input:
        None

    Output:
        str: A single character typed by the user

    Description:
        Works on Unix-like systems (macOS, Linux) by switching terminal to raw mode 
        for a single character read. On Windows, uses msvcrt.getch().
    """
    if prompt:
        print(prompt, end="", flush=True)

    if platform.system() == 'Windows':
        import msvcrt
        return msvcrt.getch().decode('utf-8')
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def press_to_continue() -> None:
    """
    Pause execution until the user presses any key.

    Input:
        None

    Output:
        None

    Description:
        Shows a prompt and uses get_char to wait for one key press.
    """
    print("\n\n\tPress any key to continue...", end="", flush=True)
    get_char()
    print()


def clear_screen() -> None:
    """
    Clear terminal (cross-platform).

    Input:
        None

    Output:
        None

    Description:
        Clear terminal screen using 'cls' command on Windows or 'clear' on Unix-like systems.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def loading_screen() -> None:
    """
    Show the loading animation with card suit symbols.

    Input:
        None

    Output:
        None

    Description:
        Displays a sequence of suit symbols with small delays to simulate loading.
    """
    symbols = ["♠︎ ♤ ♣︎ ♧", "♤ ♣︎ ♧ ♥︎", "♣︎ ♧ ♥︎ ♡", "♧ ♥︎ ♡ ♦︎",
               "♥︎ ♡ ♦︎ ♢", "♡ ♦︎ ♢ ♠", "♦︎ ♢ ♠︎ ♤", "♢ ♦︎ ♤ ♣︎"]
    time.sleep(0.4)
    for symbol in symbols:
        clear_screen()
        print(tong_777_pic)
        print(loading_pic)
        print(
            f"\n\n                                                     {symbol}\n")
        time.sleep(0.4)
    clear_screen()
    print(tong_777_pic)
    time.sleep(0.4)


def open_image(image_path: str) -> bool:
    """
    Open image with default viewer (Cross-platform).

    Input:
        image_path (str): Full path to the image file.

    Output:
        bool: True if the attempt to open the image was successful, False otherwise.

    Description:
        Attempts to open an image file using the operating system's default viewer.
        Handles different commands for macOS, Windows, and Linux.
    """
    if not os.path.exists(image_path):
        return False
    try:
        if platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', image_path])
        elif platform.system() == 'Windows':
            os.startfile(image_path)
        else:  # Linux
            subprocess.run(['xdg-open', image_path])
        return True
    except:
        return False


# ------------------------
# Storage path
# ------------------------

BASE_PATH = os.path.join(os.path.expanduser("~"), ".tong777_players")
os.makedirs(BASE_PATH, exist_ok=True)

# ------------------------
# Player Class
# ------------------------


class Player:
    def __init__(self, username: str, hashed_password: str, wallet: float = 0.0) -> None:
        """
        Initialize a Player instance.

        Input:
            username (str): The player's username.
            hashed_password (str): The bcrypt-hashed password as a string.
            wallet (float): The player's starting balance (default: 0.0).

        Output:
            None

        Description:
            Creates a new Player object with username, hashed password, and wallet balance.
        """
        self.username = username
        self.hashed_password = hashed_password  # stored as decoded str
        self.wallet = float(wallet)

    @property
    def filepath(self) -> str:
        """
        Get the file path for this player's data file.

        Input:
            None

        Output:
            str: Full path to the player's data file.

        Description:
            Constructs the file path by combining BASE_PATH with the username and .txt extension.
        """
        return os.path.join(BASE_PATH, f"{self.username}.txt")

    def save(self) -> None:
        """
        Save player data to file.

        Input:
            None

        Output:
            None

        Description:
            Writes player data (username, hashed_password, wallet) to a text file using context manager
            (with open). Handles IOError and OSError exceptions by printing error messages.
        """
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                f.write(
                    f"{self.username},{self.hashed_password},{self.wallet:.2f}")
        except (IOError, OSError) as e:
            print("❌ Error saving player data:", e)

    @classmethod
    def load(cls, username: str) -> Optional["Player"]:
        """
        Load player data from file.

        Input:
            username (str): The username to load.

        Output:
            Optional[Player]: Player object if found and valid, None otherwise.

        Description:
            Reads player data from file, parses it, and creates a Player instance.
            Returns None if file doesn't exist or data is invalid. Handles I/O and parsing errors.
        """
        filename = os.path.join(BASE_PATH, f"{username}.txt")
        if not os.path.exists(filename):
            return None
        try:
            with open(filename, "r", encoding="utf-8") as f:
                raw = f.read().strip()
        except (IOError, OSError) as e:
            print("❌ Error reading player file:", e)
            return None

        try:
            parts = raw.split(",")
            if len(parts) != 3:
                raise ValueError("Invalid player file format")
            _, hashed_password, wallet_s = parts
            wallet = float(wallet_s)
            return cls(username=username, hashed_password=hashed_password, wallet=wallet)
        except (ValueError, TypeError) as e:
            print("❌ Error parsing player file:", e)
            return None

    @classmethod
    def create_new(cls, username: str, password_plain: str, starting_wallet: float = 100.0) -> "Player":
        """
        Create a new player with hashed password.

        Input:
            username (str): The desired username.
            password_plain (str): The plaintext password to hash.
            starting_wallet (float): Initial wallet balance (default: 100.0).

        Output:
            Player: A new Player instance with hashed password.

        Description:
            Creates a new player by hashing the password with bcrypt (using String Encodings), 
            initializing the wallet, and immediately saving to file.
        """
        hashed = bcrypt.hashpw(
            password_plain.encode("utf-8"), bcrypt.gensalt())
        hashed_s = hashed.decode("utf-8")
        player = cls(username=username, hashed_password=hashed_s,
                     wallet=float(starting_wallet))
        player.save()
        return player

    def check_password(self, password_plain: str) -> bool:
        """
        Verify a plaintext password against stored hash.

        Input:
            password_plain (str): The plaintext password to check.

        Output:
            bool: True if password matches, False otherwise.

        Description:
            Uses bcrypt to compare the plaintext password (encoded to bytes) with the stored hash (also bytes).
            Returns False if any exception occurs during verification.
        """
        try:
            return bcrypt.checkpw(password_plain.encode("utf-8"), self.hashed_password.encode("utf-8"))
        except Exception:
            return False

    # Wallet operations with validation + try/except for user input
    def update_wallet(self, amount: float) -> None:
        """
        Update wallet balance by adding or subtracting an amount.

        Input:
            amount (float): Amount to add (positive) or subtract (negative).

        Output:
            None

        Description:
            Adds the specified amount to the wallet, rounds the new balance to 2 decimal places, 
            and handles potential conversion errors (ValueError, TypeError).
        """
        try:
            new_balance = float(self.wallet) + float(amount)
        except (ValueError, TypeError):
            print("❌ Invalid amount to update wallet.")
            return
        self.wallet = round(new_balance, 2)

    def deposit_interactive(self) -> None:
        """
        Interactive deposit interface for adding funds.

        Input:
            None

        Output:
            None

        Description:
            Prompts user to enter deposit amount and transaction ID, validates input (non-negative float),
            updates wallet, and saves player data. Includes a placeholder for QR code display.
        """
        qr_path = "/Users/kung/Intro to programming_Python/Fay_Python/Module 5/Tong777_V2/images/QR_PromptPay.png"

        clear_screen()
        print("----[ Deposit Funds ]----")
        print(f"Current balance: {self.wallet:.2f}")
        print("\n(Placeholder) Please transfer funds and enter transaction ID when done.")

        while True:
            amt = input("Amount to deposit (0 to cancel): ").strip()
            try:
                if amt == "":
                    print("Please enter a number.")
                    continue
                amt_f = float(amt)
                if amt_f < 0:
                    print("Enter positive amount.")
                    continue
                if amt_f == 0:
                    print("Deposit cancelled.")
                    return
                break
            except ValueError:
                print("❌ Invalid number, try again.")

        # Open QR Code
        print("\n📱 Opening PromptPay QR Code...")
        if open_image(qr_path):
            print("✅ QR Code opened!")
        else:
            print("⚠️  Could not open QR Code")

        tx = input("\nTransaction ID: ").strip()
        # in real app, validate tx
        self.update_wallet(amt_f)
        self.save()
        print(f"✅ Deposited {amt_f:.2f}. New balance: {self.wallet:.2f}")
        time.sleep(1)

    def withdraw_interactive(self) -> None:
        """
        Interactive withdrawal interface for removing funds.

        Input:
            None

        Output:
            None

        Description:
            Prompts user to enter withdrawal amount and destination. Validates that the amount
            is non-negative and does not exceed the current balance. Updates wallet and saves.
        """
        clear_screen()
        print("----[ Withdraw Funds ]----")
        print(f"Current balance: {self.wallet:.2f}")
        while True:
            amt = input("Amount to withdraw (0 to cancel): ").strip()
            try:
                if amt == "":
                    print("Please enter a number.")
                    continue
                amt_f = float(amt)
                if amt_f < 0:
                    print("Enter positive amount.")
                    continue
                if amt_f == 0:
                    print("Withdrawal cancelled.")
                    return
                if amt_f > self.wallet:
                    print("❌ Not enough balance.")
                    continue
                break
            except ValueError:
                print("❌ Invalid number, try again.")
        dest = input("Enter destination (placeholder): ").strip()
        self.update_wallet(-amt_f)
        self.save()
        print(f"✅ Withdrew {amt_f:.2f}. New balance: {self.wallet:.2f}")
        time.sleep(1)


# ------------------------
# Input helpers
# ------------------------
def is_positive_number(text: str) -> bool:
    """
    Validate if a string represents a positive number with max 2 decimals.

    Input:
        text (str): String to validate.

    Output:
        bool: True if valid positive number (including zero), False otherwise.

    Description:
        Checks format validity (max 2 decimals, allows optional leading +) and ensures
        the parsed float value is non-negative. Uses try/except for robust parsing.
    """
    try:
        s = text.strip()
        if s == "" or s == ".":
            return False
        if s.count(".") > 1:
            return False
        if s[0] == "+":
            s = s[1:]
        if not s.replace(".", "", 1).isdigit():
            return False
        if "." in s:
            decimals = s.split(".", 1)[1]
            if len(decimals) > 2:
                return False
        return float(s) >= 0
    except Exception:
        return False


def get_valid_bet(current_money: float) -> float:
    """
    Prompt user for a valid bet amount.

    Input:
        current_money (float): Player's current balance.

    Output:
        float: Valid bet amount (rounded to 2 decimals), or 0.0 if user cancels.

    Description:
        Repeatedly prompts until user enters a valid, non-negative bet amount 
        that does not exceed their available balance.
    """
    while True:
        ans = input(f"💰 Enter your bet (0 to cancel): ").strip()
        try:
            if not is_positive_number(ans):
                raise ValueError("Invalid number format")
            val = float(ans)
            val = round(val, 2)
            if val < 0:
                raise ValueError("Negative bet")
            if val == 0:
                return 0.0
            if val > current_money:
                print(
                    f"❌ You cannot bet more than your balance ({current_money:.2f}).")
                continue
            return val
        except ValueError:
            print("❌ Please enter a valid positive number (max 2 decimals).")


# ------------------------
# Decorator: game_session
# ------------------------
def game_session(game_name: str):
    """
    Decorator for game play_round methods.

    Input:
        game_name (str): Display name of the game for the header.

    Output:
        function: Decorated function wrapper (Callable[[BaseGame, Player, ...], float])

    Description:
        Provides core functionality wrapping game rounds:
        1. Prints game header and player balance.
        2. Handles exceptions during the game logic (try/except).
        3. Updates the player's wallet with the net change (float).
        4. Auto-saves player data.
        5. Prompts user to continue after the round ends.
    """
    def decorator(func):
        def wrapper(self, player: Player, *args, **kwargs):
            clear_screen()
            print(tong_777_pic)
            print(f"----[ {game_name} ]----")
            print(
                f"Player: {player.username} | Balance: {player.wallet:.2f}\n")
            try:
                # Calls the original game logic (play_round)
                net_change = func(self, player, *args, **kwargs)
            except Exception as e:
                print("❌ An error occurred during the game:", e)
                net_change = 0.0
            # net_change may be None or float
            try:
                if isinstance(net_change, (int, float)):
                    if net_change != 0:
                        player.update_wallet(net_change)
                    player.save()
                    print(f"\n💰 New balance: {player.wallet:.2f}")
                else:
                    # if function handled wallet update itself
                    player.save()
            except Exception as e:
                print("❌ Error updating player wallet:", e)
            press_to_continue()
            return net_change
        return wrapper
    return decorator


# ------------------------
# Base Game and Subclasses
# ------------------------
class BaseGame(ABC):
    """
    Abstract base class for games (Interface).

    Input:
        None

    Output:
        None

    Description:
        Defines the mandatory interface (contract) for all game classes using ABC 
        and an abstract play_round method that must be implemented by concrete subclasses.
    """
    name: str = "BaseGame"

    @abstractmethod
    def play_round(self, player: Player) -> float:
        """
        Play a single round or session of the game. (Abstract Method)

        Input:
            player (Player): The player object.

        Output:
            float: Net change to player's wallet (positive for wins, negative for losses).

        Description:
            Abstract method that must be implemented by subclasses to define specific game logic.
            The return value is processed by the @game_session decorator.
        """
        pass


class HighLow(BaseGame):
    """
    High-Low number guessing game with animation.

    Input:
        None

    Output:
        None

    Description:
        Player guesses if the next random number (1-100) will be higher or lower
        than the first number shown. Includes complex animation and visual feedback.
    """
    name = "High-Low"

    def __init__(self):
        """
        Initialize High-Low game parameters.

        Input:
            None

        Output:
            None

        Description:
            Sets the minimum and maximum range for the numbers used in the game (1 to 100).
        """
        self.min_num = 1
        self.max_num = 100

    def _number_reveal_animation(self, final_number: int, frames: int = 15) -> Generator[Tuple[int, float], None, None]:
        """
        Generator for number reveal animation.

        Input:
            final_number (int): The final number to reveal.
            frames (int): Number of animation frames (default: 15).

        Output:
            Generator[Tuple[int, float], None, None]: Yields (number, delay) for each frame.

        Description:
            Creates suspense by yielding random numbers with progressive delays that slow down 
            before revealing the final number. Uses time-based seeding for randomness.
        """
        for i in range(frames):
            # Progressive delay - starts fast, slows down dramatically
            delay = 0.04 + (i * 0.03)

            # Add time-based randomization
            random.seed(int(time.time() * 1000000) + i)

            # Show random numbers, but get closer to final as we approach the end
            if i < frames - 3:
                num = random.randint(self.min_num, self.max_num)
            else:
                # Last few frames hint at the final number
                num = final_number + random.randint(-5, 5)
                num = max(self.min_num, min(self.max_num, num))

            yield (num, delay)

    def _display_number_box(self, number: int, label: str = "NUMBER") -> None:
        """
        Display a number in a decorative box.

        Input:
            number (int): The number to display.
            label (str): Label above the number (default: "NUMBER").

        Output:
            None

        Description:
            Shows the number in an ASCII art box for visual emphasis and formatting.
        """
        print(f"\n    ╔═══════════╗")
        print(f"    ║  {label:^7}  ║")
        print(f"    ║           ║")
        print(f"    ║    {number:3d}    ║")
        print(f"    ║           ║")
        print(f"    ╚═══════════╝\n")

    def _spinning_numbers(self, final_number: int, position: str = "FIRST") -> None:
        """
        Show animated number reveal.

        Input:
            final_number (int): The number to reveal.
            position (str): Label for the number position (default: "FIRST").

        Output:
            None

        Description:
            Displays animated countdown effect using the _number_reveal_animation generator,
            showing random numbers before revealing the final number.
        """
        print("\n" + "="*40)
        print(f"🎲 REVEALING {position} NUMBER... 🎲".center(40))
        print("="*40 + "\n")

        # Spinning effect
        for (num, delay) in self._number_reveal_animation(final_number, frames=18):
            print(f"        ▶  {num:3d}  ◀        ", end="\r", flush=True)
            time.sleep(delay)

        print()  # newline

        # Dramatic pause before reveal
        time.sleep(0.3)

        # Show final number in box
        self._display_number_box(final_number, position)
        time.sleep(0.5)

    def _compare_visual(self, num1: int, num2: int, guess: str) -> None:
        """
        Show visual comparison of the two numbers.

        Input:
            num1 (int): First number.
            num2 (int): Second number.
            guess (str): Player's guess ('h' or 'l') (used for context, not logic).

        Output:
            None

        Description:
            Displays both numbers side by side with visual indicators (arrows) 
            showing the relationship between them.
        """
        print("\n" + "="*40)
        print("📊 COMPARISON 📊".center(40))
        print("="*40 + "\n")

        # Determine relationship
        if num2 > num1:
            symbol = "↗️"
            relation = "HIGHER"
        elif num2 < num1:
            symbol = "↘️"
            relation = "LOWER"
        else:
            symbol = "➡️"
            relation = "EQUAL"

        # Display comparison
        print(f"    {num1:3d}   {symbol}   {num2:3d}")
        print(f"          {relation}          \n")

        time.sleep(0.5)

    def _get_difficulty_hint(self, num: int) -> str:
        """
        Provide a hint about the difficulty based on the number.

        Input:
            num (int): The first number.

        Output:
            str: Difficulty hint message.

        Description:
            Returns a hint message based on how close the number is to the extremes (1 or 100).
            Numbers closer to the middle (45-55) are considered harder to predict.
        """
        if num <= 20:
            return "💡 Tip: Very low number - likely to go higher!"
        elif num >= 80:
            return "💡 Tip: Very high number - likely to go lower!"
        elif 45 <= num <= 55:
            return "💡 Tip: Middle range - 50/50 chance!"
        elif num < 50:
            return "💡 Tip: Below middle - slight bias upward"
        else:
            return "💡 Tip: Above middle - slight bias downward"

    @game_session("High-Low 🎲")
    def play_round(self, player: Player) -> float:
        """
        Play one round of High-Low with enhanced animations.

        Input:
            player (Player): The player object.

        Output:
            float: Bet amount if win, negative bet if loss, 0 if cancelled.

        Description:
            Implements the main game logic: animated reveal of first number, prompts 
            for higher/lower guess, animated reveal of second number, and determines 
            the final result.
        """
        while True:
            print("\n╔═════════════════════════════════════╗")
            print("║            HIGH-LOW GAME            ║")
            print("╚═════════════════════════════════════╝")
            print("\n📋 Rules:")
            print("  • A number from 1-100 will be shown")
            print("  • Guess if the next number is Higher or Lower")
            print("  • Correct guess = Win 1x your bet")
            print("  • Wrong guess = Lose your bet")
            print("  • Equal numbers = You lose")
            print("\nEnter 0 to return to main menu.")

            bet = get_valid_bet(player.wallet)
            if bet == 0:
                print("💼 Returning to menu...")
                time.sleep(0.5)
                return 0.0

            print(f"\n💰 Betting: {bet:.2f}")
            time.sleep(0.5)

            # Generate first number with time-based seed
            random.seed(int(time.time() * 1000000))
            num1 = random.randint(self.min_num, self.max_num)

            # Show first number with animation
            self._spinning_numbers(num1, "FIRST")

            # Show difficulty hint
            hint = self._get_difficulty_hint(num1)
            print(hint)
            print()

            # Get player's guess with better prompts
            print("─"*40)
            print("Make your prediction:")
            print("  [H] Higher - Next number will be > " + str(num1))
            print("  [L] Lower  - Next number will be < " + str(num1))
            print("─"*40)

            guess = get_char("\n🎯 Your choice (h/l): ").lower().strip()
            while guess not in ('h', 'l'):
                guess = get_char("❌ Please enter 'h' or 'l': ").lower().strip()

            choice_name = 'HIGHER' if guess == 'h' else 'LOWER'
            print(f"\n✅ You predicted: {choice_name}")

            time.sleep(1)

            # Generate second number with new time-based seed
            random.seed(int(time.time() * 1000000))
            num2 = random.randint(self.min_num, self.max_num)

            # Dramatic pause
            print("\n🎲 Drawing next number...")
            time.sleep(0.8)

            # Show second number with animation
            self._spinning_numbers(num2, "SECOND")

            # Show comparison
            self._compare_visual(num1, num2, guess)

            # Determine result
            print("="*40)

            # Check for win/loss
            won = False
            if num2 == num1:
                print("😐 EQUAL NUMBERS 😐".center(40))
                print("="*40)
                print(f"\n🔄 Both numbers are {num1}!")
                print(f"💸 You lost {bet:.2f} (House rule: Equal = Loss)")
            elif (guess == 'h' and num2 > num1) or (guess == 'l' and num2 < num1):
                won = True
                print("🎉 YOU WIN! 🎉".center(40))
                print("="*40)
                print(f"\n✨ You guessed correctly!")
                print(f"💰 You won {bet:.2f}!")

                # Victory animation
                time.sleep(0.3)
                print("\n" + "🎊 " * 10)
                time.sleep(0.3)
            else:
                print("💀 YOU LOSE 💀".center(40))
                print("="*40)
                print(f"\n😔 Your guess was wrong...")
                print(f"💸 You lost {bet:.2f}.")

            time.sleep(1)

            return bet if won else -bet


class CoinFlip(BaseGame):
    """
    Coin flip betting game with realistic animation.

    Input:
        None

    Output:
        None

    Description:
        Player chooses heads or tails and wins if they guess correctly.
        Features realistic coin flipping animation with time-based effects.
    """
    name = "Coin Flip"

    def __init__(self):
        """
        Initialize Coin Flip game.

        Input:
            None

        Output:
            None

        Description:
            Sets up coin symbols for animation and ASCII art representation of Heads/Tails faces.
        """
        # Coin symbols for animation
        self.coin_frames = [
            "◯",  # Spinning
            "◐",
            "●",
            "◑",
            "◯",
            "◓",
            "●",
            "◒"
        ]

        # Final coin faces
        self.heads = """
        ╔═══════╗
        ║       ║
        ║   H   ║
        ║ HEADS ║
        ║       ║
        ╚═══════╝
        """
        self.tails = """
        ╔═══════╗
        ║       ║
        ║   T   ║
        ║ TAILS ║
        ║       ║
        ╚═══════╝
        """

    def _flip_animation(self, frames: int = 20) -> Generator[Tuple[str, float], None, None]:
        """
        Generator for coin flipping animation.

        Input:
            frames (int): Number of animation frames (default: 20).

        Output:
            Generator[Tuple[str, float], None, None]: Yields (coin_symbol, delay) for each frame.

        Description:
            Creates realistic flipping effect with variable delays that slow down
            over time, simulating a coin losing momentum.
        """
        for i in range(frames):
            # Progressive delay - starts fast, slows down
            delay = 0.03 + (i * 0.015)

            # Add time-based randomization
            random.seed(int(time.time() * 1000000) + i)

            # Cycle through coin frames
            frame = self.coin_frames[i % len(self.coin_frames)]

            yield (frame, delay)

    def _display_result(self, result: str) -> None:
        """
        Display the final coin result with visual effect.

        Input:
            result (str): 'h' for heads or 't' for tails.

        Output:
            None

        Description:
            Shows the final coin face using appropriate ASCII art and a brief pause for effect.
        """
        print("\n" + "="*40)
        print("🪙 COIN LANDED! 🪙".center(40))
        print("="*40)

        if result == 'h':
            print(self.heads)
        else:
            print(self.tails)

        time.sleep(0.5)

    def _spinning_effect(self) -> None:
        """
        Show coin spinning animation.

        Input:
            None

        Output:
            None

        Description:
            Displays animated coin flip with progressive slowdown effect
            using the _flip_animation generator for realistic physics simulation.
        """
        print("\n" + "="*40)
        print("🪙 FLIPPING COIN... 🪙".center(40))
        print("="*40 + "\n")

        for (frame, delay) in self._flip_animation(frames=25):
            # Create spinning effect with multiple frames on one line
            print(f"        {frame} {frame} {frame}        ",
                  end="\r", flush=True)
            time.sleep(delay)

        print()  # newline after animation

    @game_session("Coin Flip 🪙")
    def play_round(self, player: Player) -> float:
        """
        Play one round of Coin Flip with animation.

        Input:
            player (Player): The player object.

        Output:
            float: Bet amount if win, negative bet if loss, 0 if cancelled.

        Description:
            Player chooses heads or tails, watches realistic coin flip animation,
            and wins if their choice matches the result.
        """
        while True:
            print("\n╔══════════════════════════════════════╗")
            print("║            COIN FLIP GAME            ║")
            print("╚══════════════════════════════════════╝")
            print("\n📋 Rules:")
            print("  • Choose Heads (H) or Tails (T)")
            print("  • Correct guess = Win 1x your bet")
            print("  • Wrong guess = Lose your bet")
            print("  • 50/50 chance!")
            print("\nEnter 0 to return to main menu.")

            bet = get_valid_bet(player.wallet)
            if bet == 0:
                print("💼 Returning to menu...")
                time.sleep(0.5)
                return 0.0

            # Get player's choice with better prompts
            print("\n" + "─"*40)
            print("Choose your side:")
            print("  [H] Heads")
            print("  [T] Tails")
            print("─"*40)

            guess = get_char("\n🎯 Your choice (h/t): ").lower().strip()
            while guess not in ('h', 't'):
                guess = get_char("❌ Please enter 'h' or 't': ").lower().strip()

            choice_name = 'HEADS' if guess == 'h' else 'TAILS'
            print(f"\n✅ You chose: {choice_name}")
            print(f"💰 Betting: {bet:.2f}")

            time.sleep(0.8)

            # Coin flip with animation
            self._spinning_effect()

            # Determine result with time-based randomization
            random.seed(int(time.time() * 1000000))
            result = random.choice(['h', 't'])

            # Show result
            self._display_result(result)

            result_name = 'HEADS' if result == 'h' else 'TAILS'

            # Determine win/loss
            print("\n" + "="*40)
            if guess == result:
                print("🎉 YOU WIN! 🎉".center(40))
                print("="*40)
                print(f"\n✨ The coin landed on {result_name}!")
                print(f"💰 You won {bet:.2f}!")

                # Victory animation
                time.sleep(0.3)
                print("\n" + "🎊 " * 10)
                time.sleep(0.3)

                return bet
            else:
                print("💀 YOU LOSE 💀".center(40))
                print("="*40)
                print(f"\n😔 The coin landed on {result_name}...")
                print(f"💸 You lost {bet:.2f}.")

                time.sleep(0.5)
                return -bet


class Blackjack(BaseGame):
    """
    Realistic Blackjack card game with standard 52-card deck.

    Input:
        None

    Output:
        None

    Description:
        Simulates real blackjack with 52-card deck. Player tries to get closer to 21 than dealer.
        Supports multiple rounds in one session.
    """
    name = "Blackjack"

    def __init__(self):
        """
        Initialize Blackjack game.

        Input:
            None

        Output:
            None

        Description:
            Sets up card suits and ranks for a standard 52-card deck. Initializes an empty deck list.
        """
        self.suits = ['♠', '♥', '♦', '♣']
        self.ranks = ['A', '2', '3', '4', '5', '6',
                      '7', '8', '9', '10', 'J', 'Q', 'K']
        self.deck = []

    def _create_deck(self) -> None:
        """
        Create a fresh 52-card deck and shuffle it.

        Input:
            None

        Output:
            None

        Description:
            Creates a standard deck with 4 suits × 13 ranks = 52 cards, each represented as a tuple 
            of (rank, suit). The deck is immediately shuffled.
        """
        self.deck = [(rank, suit)
                     for suit in self.suits for rank in self.ranks]
        random.shuffle(self.deck)

    def _draw_card(self) -> Tuple[str, str]:
        """
        Draw one card from the deck.

        Input:
            None

        Output:
            Tuple[str, str]: (rank, suit) of the drawn card.

        Description:
            Removes and returns the top card from the deck. Creates a new deck if the current one is empty.
        """
        if len(self.deck) == 0:
            self._create_deck()
        return self.deck.pop()

    def _card_value(self, card: Tuple[str, str]) -> int:
        """
        Get numeric value of a card.

        Input:
            card (Tuple[str, str]): Card as (rank, suit).

        Output:
            int: Card value (A=11, J/Q/K=10, others=face value).

        Description:
            Returns the blackjack value of a card. Ace returns 11 initially. Face cards return 10.
        """
        rank = card[0]
        if rank == 'A':
            return 11
        elif rank in ['J', 'Q', 'K']:
            return 10
        else:
            return int(rank)

    def _format_card(self, card: Tuple[str, str]) -> str:
        """
        Format card for display.

        Input:
            card (Tuple[str, str]): Card as (rank, suit).

        Output:
            str: Formatted card string (e.g., "A♠" or "10♥").

        Description:
            Creates a visual representation of the card with rank and suit symbol.
        """
        return f"{card[0]}{card[1]}"

    def _hand_value(self, hand: List[Tuple[str, str]]) -> int:
        """
        Calculate total value of a hand with Ace adjustment.

        Input:
            hand (List[Tuple[str, str]]): List of cards.

        Output:
            int: Best possible hand value (not exceeding 21 if possible).

        Description:
            Sums card values and adjusts Aces from 11 to 1 if the total exceeds 21 
            (to prevent busting when possible).
        """
        total = sum(self._card_value(card) for card in hand)
        aces = sum(1 for card in hand if card[0] == 'A')

        # Adjust Aces from 11 to 1 if busting
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def _display_hand(self, hand: List[Tuple[str, str]], name: str = "Hand", hide_first: bool = False) -> None:
        """
        Display a hand of cards with visual formatting.

        Input:
            hand (List[Tuple[str, str]]): List of cards.
            name (str): Name to display (default: "Hand").
            hide_first (bool): Whether to hide the first card (hole card) (default: False).

        Output:
            None

        Description:
            Prints cards in a row with proper formatting and calculated total value. If hide_first 
            is True, the first card is shown as face-down (🂠).
        """
        if hide_first and len(hand) > 0:
            cards_str = "🂠  " + "  ".join(self._format_card(card)
                                          for card in hand[1:])
            visible_value = sum(self._card_value(card) for card in hand[1:])
            print(f"{name}: {cards_str} (Showing: {visible_value})")
        else:
            cards_str = "  ".join(self._format_card(card) for card in hand)
            total = self._hand_value(hand)
            print(f"{name}: {cards_str} (Total: {total})")

    def _deal_animation(self, card: Tuple[str, str], recipient: str) -> None:
        """
        Animated card dealing effect.

        Input:
            card (Tuple[str, str]): Card being dealt.
            recipient (str): Who receives the card ("Player" or "Dealer").

        Output:
            None

        Description:
            Shows a quick animation of a card being dealt with brief delays for visual effect.
        """
        symbols = ['🂠', '🃏', '🎴', '🂡']
        for i in range(4):
            random.seed(int(time.time() * 1000000) + i)
            print(
                f"Dealing to {recipient}... {random.choice(symbols)}", end="\r", flush=True)
            time.sleep(0.1)
        print(f"Dealt to {recipient}: {self._format_card(card)}    ")
        time.sleep(0.3)

    @game_session("Blackjack ♠♥♦♣")
    def play_round(self, player: Player) -> float:
        """
        Play Blackjack session with multiple rounds using real deck.

        Input:
            player (Player): The player object.

        Output:
            float: Total net change across all rounds in the session.

        Description:
            Implements the main Blackjack game loop, including betting, card dealing, 
            player/dealer turns, Ace adjustment, and result calculation (Blackjack pays 3:2).
            Returns cumulative net change when the player decides to quit the session.
        """
        total_change = 0.0
        self._create_deck()  # Create initial deck

        while True:
            print("\n╔══════════════════════════════════════╗")
            print("║           BLACKJACK TABLE           ║")
            print("╚══════════════════════════════════════╝")
            print("\n📋 Rules:")
            print("  • Goal: Get closer to 21 than dealer")
            print("  • Dealer hits on 16, stands on 17")
            print("  • Blackjack (A + 10/J/Q/K) pays 3:2")
            print("  • Aces count as 1 or 11")
            print(f"\n💰 Session Balance: {player.wallet + total_change:.2f}")
            print("\nEnter 0 to return to main menu.")

            bet = get_valid_bet(player.wallet + total_change)
            if bet == 0:
                print("💼 Cashing out from Blackjack table...")
                time.sleep(0.5)
                return total_change

            # Check if deck needs reshuffling
            if len(self.deck) < 15:
                print("\n🔄 Shuffling new deck...")
                time.sleep(0.8)
                self._create_deck()

            print("\n" + "="*40)
            print("🎴 DEALING CARDS 🎴".center(40))
            print("="*40 + "\n")

            # Initial deal - 2 cards each
            player_hand = []
            dealer_hand = []

            # Deal with animation
            time.sleep(0.3)
            card = self._draw_card()
            self._deal_animation(card, "Player")
            player_hand.append(card)

            card = self._draw_card()
            self._deal_animation(card, "Dealer")
            dealer_hand.append(card)

            card = self._draw_card()
            self._deal_animation(card, "Player")
            player_hand.append(card)

            card = self._draw_card()
            print("Dealing to Dealer... 🂠 (Face Down)")
            dealer_hand.append(card)
            time.sleep(0.5)

            # Display initial hands
            print("\n" + "="*40)
            self._display_hand(dealer_hand, "Dealer", hide_first=True)
            self._display_hand(player_hand, "Your Hand")
            print("="*40 + "\n")

            player_value = self._hand_value(player_hand)
            dealer_value = self._hand_value(dealer_hand)

            # Check for natural blackjack
            player_blackjack = (player_value == 21 and len(player_hand) == 2)
            dealer_blackjack = (dealer_value == 21 and len(dealer_hand) == 2)

            if player_blackjack and dealer_blackjack:
                print("🤝 Both have Blackjack! Push!")
                self._display_hand(dealer_hand, "Dealer's Hand")
                time.sleep(1)
                continue

            if player_blackjack:
                win = bet * 1.5
                print("🎉 BLACKJACK! You win " + f"{win:.2f}! 🎉")
                print("💎 Paid 3:2 💎")
                total_change += win
                time.sleep(1.5)

                print(f"\n💰 Session net: {total_change:+.2f}")

                cont = get_char(
                    "\n♠ Play another hand? (y/n): ").lower().strip()
                if cont != 'y':
                    return total_change
                continue

            if dealer_blackjack:
                print("💀 Dealer has Blackjack! You lose.")
                self._display_hand(dealer_hand, "Dealer's Hand")
                total_change -= bet
                time.sleep(1.5)

                print(f"\n💰 Session net: {total_change:+.2f}")

                cont = get_char(
                    "\n♠ Play another hand? (y/n): ").lower().strip()
                if cont != 'y':
                    return total_change
                continue

            # Player's turn
            busted = False
            while True:
                player_value = self._hand_value(player_hand)

                if player_value > 21:
                    print("\n💀 BUST! You went over 21!")
                    total_change -= bet
                    busted = True
                    time.sleep(1)
                    break

                move = get_char("\n🎯 (H)it or (S)tand? ").lower().strip()
                while move not in ('h', 's'):
                    move = get_char(
                        "Please enter 'h' or 's': ").lower().strip()

                if move == 'h':
                    card = self._draw_card()
                    print(f"\n🎴 You drew: {self._format_card(card)}")
                    player_hand.append(card)
                    time.sleep(0.5)
                    self._display_hand(player_hand, "Your Hand")
                else:
                    print(f"\n✋ You stand with {player_value}")
                    time.sleep(0.8)
                    break

            if busted:
                print(f"\n💸 Lost: {bet:.2f}")
                print(f"💰 Session net: {total_change:+.2f}")

                cont = get_char(
                    "\n♠ Play another hand? (y/n): ").lower().strip()
                if cont != 'y':
                    return total_change
                continue

            # Dealer's turn
            print("\n" + "="*40)
            print("🎴 DEALER'S TURN 🎴".center(40))
            print("="*40 + "\n")

            time.sleep(0.8)
            print("Revealing dealer's hole card...")
            time.sleep(0.8)
            self._display_hand(dealer_hand, "Dealer's Hand")
            time.sleep(1)

            # Dealer hits on 16 or less
            while self._hand_value(dealer_hand) < 17:
                print("\nDealer hits...")
                time.sleep(0.8)
                card = self._draw_card()
                dealer_hand.append(card)
                print(f"🎴 Dealer drew: {self._format_card(card)}")
                time.sleep(0.5)
                self._display_hand(dealer_hand, "Dealer's Hand")
                time.sleep(0.8)

            dealer_value = self._hand_value(dealer_hand)

            if dealer_value > 21:
                print("\n💥 Dealer BUSTS!")
                time.sleep(0.5)

            # Final comparison
            print("\n" + "="*40)
            print("🏁 FINAL RESULT 🏁".center(40))
            print("="*40 + "\n")

            self._display_hand(dealer_hand, "Dealer")
            self._display_hand(player_hand, "You")
            print()

            player_value = self._hand_value(player_hand)
            dealer_value = self._hand_value(dealer_hand)

            if dealer_value > 21:
                print(f"🎉 Dealer busts! You win {bet:.2f}! 🎉")
                total_change += bet
            elif player_value > dealer_value:
                print(f"🎊 You win {bet:.2f}! 🎊")
                total_change += bet
            elif player_value == dealer_value:
                print("🤝 Push! Bet returned.")
            else:
                print(f"💀 Dealer wins. You lose {bet:.2f}.")
                total_change -= bet

            time.sleep(1)
            print(f"\n💵 Bet: {bet:.2f}")
            print(f"💰 Session net: {total_change:+.2f}")

            cont = get_char("\n♠ Play another hand? (y/n): ").lower().strip()
            if cont != 'y':
                print("\n💼 Leaving Blackjack table...")
                time.sleep(0.5)
                return total_change


class Slots(BaseGame):
    """
    Emoji-themed slot machine game.

    Input:
        None

    Output:
        None

    Description:
        Three-reel slot machine with cute emoji symbols and various multipliers
        for matching symbols. Uses a weighted random selection for more realistic odds.
    """
    name = "Cute Slots"

    def __init__(self) -> None:
        """
        Initialize Slots game with symbols and their weights.

        Input:
            None

        Output:
            None

        Description:
            Sets up symbols list and probability weights. Special symbol (bear) has
            much lower probability (5%) compared to other symbols (23.75% each).
        """
        self.symbols = [
            'ʕっ•ᴥ•ʔっ',   # Special - rare (5% chance)
            ' (⇀‸↼‶)  ',  # Common (23.75% each)
            ' (・3・) ',
            ' (︶︹︶)',
            '( º﹃º ) '
        ]

        self.weights = [5, 23.75, 23.75, 23.75, 23.75]

        self.multipliers = {
            3: 100,  # 3 specials = jackpot
            2: 25,   # 2 specials = big win
            1: 5     # 1 special = small win
        }

    def _weighted_choice(self) -> str:
        """
        Choose a random symbol based on weighted probabilities.

        Input:
            None

        Output:
            str: Selected emoji symbol.

        Description:
            Uses random.choices with weights to make special symbol appear less frequently.
        """
        return random.choices(self.symbols, weights=self.weights, k=1)[0]

    def _spin_generator(self, frames: int = 15) -> Generator[Tuple[str, str, str, float], None, None]:
        """
        Generator for enhanced slot machine spin animation.

        Input:
            frames (int): Number of animation frames (default: 15).

        Output:
            Generator[Tuple[str, str, str, float], None, None]: Yields tuple of (r1, r2, r3, delay) for each frame.

        Description:
            Creates realistic spinning effect with variable delays that slow down
            over time. Uses time-based randomization for more realistic feel.
            Uses weighted choice for final symbols.
        """
        for i in range(frames):
            # Progressive delay - starts fast, slows down
            delay = 0.05 + (i * 0.02)

            # Add time-based seed variation for more randomness
            random.seed(int(time.time() * 1000000) + i)

            r1 = random.choice(self.symbols)
            r2 = random.choice(self.symbols)
            r3 = random.choice(self.symbols)

            yield (r1, r2, r3, delay)

    def _calculate_win(self, r1: str, r2: str, r3: str, bet: float) -> Tuple[float, str, int]:
        """
        Calculate winnings based on special symbol count.

        Input:
            r1 (str): First reel symbol.
            r2 (str): Second reel symbol.
            r3 (str): Third reel symbol.
            bet (float): Bet amount.

        Output:
            Tuple[float, str, int]: (win_amount, message, special_count).

        Description:
            Counts special symbols (bear emoji) and returns appropriate winnings and message 
            based on fixed multipliers. Checks for triple match of regular symbols as a minor win.
        """
        special = 'ʕっ•ᴥ•ʔっ'
        special_count = [r1, r2, r3].count(special)

        if special_count == 3:
            multiplier = self.multipliers[3]
            win = bet * multiplier
            return win, f"💎 MEGA JACKPOT! 3 Specials x{multiplier} => Won {win:.2f}! 💎", 3

        elif special_count == 2:
            multiplier = self.multipliers[2]
            win = bet * multiplier
            return win, f"✨ BIG WIN! 2 Specials x{multiplier} => Won {win:.2f}! ✨", 2

        elif special_count == 1:
            multiplier = self.multipliers[1]
            win = bet * multiplier
            return win, f"🌟 Lucky! 1 Special x{multiplier} => Won {win:.2f}!", 1

        else:
            # Check for three matching regular symbols
            if r1 == r2 == r3:
                win = bet * 2
                return win, f"🎊 Triple Match! x2 => Won {win:.2f}!", 0
            else:
                return -bet, "😢 No win this spin.", 0

    @game_session("Cute Emoji Slots")
    def play_round(self, player: Player) -> float:
        """
        Play one round of enhanced Slots.

        Input:
            player (Player): The player object.

        Output:
            float: Winnings (positive) or loss (negative), 0 if cancelled.

        Description:
            Implements the main slot machine game loop, including betting, 
            animated spinning using the _spin_generator, result calculation, and visual feedback.
        """
        total_change = 0.0

        while True:
            print("\n╔═════════════════════════════════════╗")
            print("║          CUTE EMOJI SLOTS           ║")
            print("╚═════════════════════════════════════╝")
            print("\n💰 Prize Table:")
            print("  3x ʕっ•ᴥ•ʔっ  = x100 (MEGA JACKPOT!)")
            print("  2x ʕっ•ᴥ•ʔっ  = x25  (BIG WIN!)")
            print("  1x ʕっ•ᴥ•ʔっ  = x5   (Lucky!)")
            print("  3x Same   = x2   (Triple Match)")
            print("\nʕっ•ᴥ•ʔっ is RARE - Good luck!\n")
            print(f"💰 Session Balance: {player.wallet + total_change:.2f}\n")
            print("Enter 0 to return to main menu.")

            bet = get_valid_bet(player.wallet + total_change)
            if bet == 0:
                print("💼 Cashing out from Cute emoji slots...")
                time.sleep(0.5)
                return total_change

            # Enhanced spinning animation with visual effects
            print("\n" + "="*40)
            print("🎰 SPINNING... 🎰".center(40))
            print("="*40 + "\n")

            # Show spinning animation with progressive slowdown
            for (r1, r2, r3, delay) in self._spin_generator(frames=20):
                print(f"║ {r1} ║ {r2} ║ {r3} ║", end="\r", flush=True)
                time.sleep(delay)

            print()  # newline after animation

            # Final result using weighted selection
            r1 = self._weighted_choice()
            r2 = self._weighted_choice()
            r3 = self._weighted_choice()

            # Display final result with visual emphasis
            print("\n" + "="*40)
            print("🎯 FINAL RESULT 🎯".center(40))
            print("="*40)
            print(f"\n    ║ {r1} ║ {r2} ║ {r3} ║\n")
            print("="*40 + "\n")

            # Calculate and display winnings
            win, message, special_count = self._calculate_win(r1, r2, r3, bet)

            # Show result with appropriate animation
            if win > 0:
                print(message)
                if special_count >= 2:
                    # Extra celebration for big wins
                    time.sleep(0.3)
                    print("\n" + "🎉" * 20)
                    time.sleep(0.3)
            else:
                print(message)

            # Show statistics
            print(f"\n💵 Bet: {bet:.2f}")
            if win > 0:
                print(f"💰 Won: {win:.2f}")
            else:
                print(f"💸 Lost: {abs(win):.2f}")

            total_change += win

            print(f"\n💰 Session net: {total_change:+.2f}")

            cont = get_char("\n♠ Spin more? (y/n): ").lower().strip()
            if cont != 'y':
                print("\n💼 Leaving Emoji Slots...")
                time.sleep(0.5)
                return total_change


# ------------------------
# Login / Register System
# ------------------------
def login_or_register_loop() -> "Player":
    """
    Handle user login or registration.

    Input:
        None

    Output:
        Player: A logged-in Player instance.

    Description:
        Displays login menu and handles user authentication (login) or new account creation (register).
        Loops until user successfully logs in, registers, or chooses to exit the program.
    """
    while True:
        clear_screen()
        print(tong_777_pic)
        print(login_pic)
        choice = get_char("Choose: ").strip()
        if choice == '1':
            clear_screen()
            print(tong_777_pic)
            print(login_pic)
            username = input("Username: ").strip()
            if username == "":
                print("Username cannot be empty.")
                time.sleep(1)
                continue
            p = Player.load(username)
            if p is None:
                print("❌ User not found.")
                time.sleep(1)
                continue
            pw = input("Password: ").strip()
            if p.check_password(pw):
                print(f"✅ Welcome back, {username}!")
                time.sleep(1)
                return p
            else:
                print("❌ Incorrect password.")
                time.sleep(1)
                continue

        elif choice == '2':
            clear_screen()
            print(tong_777_pic)
            print(login_pic)
            username = input("Choose username: ").strip()
            if username == "":
                print("Username cannot be empty.")
                time.sleep(1)
                continue
            if Player.load(username) is not None:
                print("⚠️ Username already exists.")
                time.sleep(1)
                continue
            pw = input("Set password: ").strip()
            while pw == "":
                pw = input("Password cannot be empty. Set password: ").strip()
            p = Player.create_new(
                username=username, password_plain=pw, starting_wallet=100.0)
            print(
                f"✅ Account '{username}' created. Bonus 100.00 credits added.")
            time.sleep(1)
            return p

        elif choice == '3':
            clear_screen()
            print(tong_777_pic)
            print(login_pic)
            print("Goodbye.")
            sys.exit(0)
        else:
            print("Please choose 1-3.")
            time.sleep(1)


# ------------------------
# Main menu
# ------------------------
def main() -> None:
    """
    Main program entry point.

    Input:
        None

    Output:
        None

    Description:
        Initializes the system, shows the loading screen, and enters the main game loop. 
        Manages the user session by handling login/register, menu display, and processing 
        all game and financial choices.
    """
    loading_screen()

    games = {
        "1": HighLow(),
        "2": CoinFlip(),
        "3": Blackjack(),
        "4": Slots()
    }

    while True:
        player = login_or_register_loop()
        # main menu loop
        while True:
            clear_screen()
            print(tong_777_pic)
            print(
                f"Player: {player.username} | Balance: {player.wallet:.2f}\n")
            print(menu_pic)
            choice = get_char("Select option (1-8): ").strip()
            if choice in ("1", "2", "3", "4"):
                game = games[choice]
                # decorator handles wallet update and save
                game.play_round(player)
            elif choice == "5":
                player.deposit_interactive()
            elif choice == "6":
                player.withdraw_interactive()
            elif choice == "7":
                print("Logging out...")
                time.sleep(0.7)
                break  # back to login/register loop
            elif choice == "8":
                print("Saving and exiting...")
                player.save()
                time.sleep(0.8)
                sys.exit(0)
            else:
                print("Please select 1-8 only.")
                time.sleep(1)


if __name__ == "__main__":
    main()
