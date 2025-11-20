#!/usr/bin/env python3
"""
Tong777 - Refactored Casino Terminal (OOP, File Handling, Decorator, Generator)
Requirements implemented:
 - Player class with load/save (with open), hashed password, wallet
 - BaseGame abstract class + subclasses for games
 - game_session decorator to handle printing, auto-save and wallet updates
 - try/except for input and file I/O
 - slots uses a generator for spinning animation
 - removed get_char() and press_to_continue()
"""

import os
import sys
import time
import random
import bcrypt
from abc import ABC, abstractmethod
from typing import Optional

# ------------------------
# Banner (kept tong_777_pic)
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
def clear_screen() -> None:
    """Clear terminal (cross-platform)."""
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
               "♥︎ ♡ ♦︎ ♢", "♡ ♦︎ ♢ ♠", "♦︎ ♢ ♠︎ ♤", "♢ ♠︎ ♤ ♣︎"]
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

# ------------------------
# Storage path
# ------------------------
BASE_PATH = os.path.join(os.path.expanduser("~"), ".tong777_players")
os.makedirs(BASE_PATH, exist_ok=True)


# ------------------------
# Player Class
# ------------------------
class Player:
    """
    Player object with username, hashed_password (string), wallet (float).
    Responsible for loading/saving own data.
    File format: username,hashed_password,wallet
    """
    def __init__(self, username: str, hashed_password: str, wallet: float = 0.0):
        self.username = username
        self.hashed_password = hashed_password  # stored as decoded str
        self.wallet = float(wallet)

    @property
    def filepath(self) -> str:
        return os.path.join(BASE_PATH, f"{self.username}.txt")

    def save(self) -> None:
        """Save player to file using context manager; handle I/O errors."""
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                f.write(f"{self.username},{self.hashed_password},{self.wallet:.2f}")
        except (IOError, OSError) as e:
            print("❌ Error saving player data:", e)

    @classmethod
    def load(cls, username: str) -> Optional["Player"]:
        """Load player data, return Player or None. Handles I/O and parse errors."""
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
        """Create new player (hash password) and save immediately."""
        hashed = bcrypt.hashpw(password_plain.encode("utf-8"), bcrypt.gensalt())
        hashed_s = hashed.decode("utf-8")
        player = cls(username=username, hashed_password=hashed_s, wallet=float(starting_wallet))
        player.save()
        return player

    def check_password(self, password_plain: str) -> bool:
        """Check plaintext password against stored hash."""
        try:
            return bcrypt.checkpw(password_plain.encode("utf-8"), self.hashed_password.encode("utf-8"))
        except Exception:
            return False

    # Wallet operations with validation + try/except for user input
    def update_wallet(self, amount: float) -> None:
        """Increment/decrement wallet by amount (can be negative)."""
        try:
            new_balance = float(self.wallet) + float(amount)
        except (ValueError, TypeError):
            print("❌ Invalid amount to update wallet.")
            return
        self.wallet = round(new_balance, 2)

    def deposit_interactive(self) -> None:
        """Ask user to deposit funds (simplified QR placeholder)."""
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
        tx = input("Transaction ID (any text): ").strip()
        # in real app, validate tx
        self.update_wallet(amt_f)
        self.save()
        print(f"✅ Deposited {amt_f:.2f}. New balance: {self.wallet:.2f}")
        time.sleep(1)

    def withdraw_interactive(self) -> None:
        """Withdraw funds interactively with validation."""
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
    """Same validation: positive number with up to 2 decimals."""
    try:
        s = text.strip()
        if s == "" or s == ".":
            return False
        if s.count(".") > 1:
            return False
        # allow leading plus
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
    Ask player to enter bet; uses try/except to parse and validate.
    Returns a rounded float (2 decimals). Return 0.0 when user chooses to exit from betting.
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
                print(f"❌ You cannot bet more than your balance ({current_money:.2f}).")
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
    The wrapped function should accept (self, player) and return net_change (float).
    Decorator will:
     - print game header
     - show starting balance
     - call play_round
     - update player wallet and auto-save
    """
    def decorator(func):
        def wrapper(self, player: Player, *args, **kwargs):
            clear_screen()
            print(tong_777_pic)
            print(f"----[ {game_name} ]----")
            print(f"Player: {player.username} | Balance: {player.wallet:.2f}\n")
            try:
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
            input("\nPress Enter to continue...")
            return net_change
        return wrapper
    return decorator


# ------------------------
# Base Game and Subclasses
# ------------------------
class BaseGame(ABC):
    """Abstract base class for games."""

    name: str = "BaseGame"

    @abstractmethod
    def play_round(self, player: Player) -> float:
        """
        Should implement a round / session and return net change to player's wallet.
        (positive for wins, negative for losses, 0 for no-change)
        """
        pass


class HighLow(BaseGame):
    name = "High-Low"

    @game_session("High-Low")
    def play_round(self, player: Player) -> float:
        """Single round High-Low: returns +bet or -bet or 0 (if cancelled)"""
        print("Guess whether the next number will be higher or lower (1-100).")
        bet = get_valid_bet(player.wallet)
        if bet == 0:
            print("Returning to menu.")
            return 0.0
        num1 = random.randint(1, 100)
        print(f"First number: {num1}")
        guess = input("Will the next be (h)igher or (l)ower? ").lower().strip()
        while guess not in ('h', 'l'):
            guess = input("Please enter 'h' or 'l': ").lower().strip()
        num2 = random.randint(1, 100)
        print(f"Next number: {num2}")
        if (guess == 'h' and num2 > num1) or (guess == 'l' and num2 < num1):
            print(f"🎉 You won {bet:.2f}!")
            return bet
        else:
            print(f"💀 You lost {bet:.2f}.")
            return -bet


class CoinFlip(BaseGame):
    name = "Coin Flip"

    @game_session("Coin Flip")
    def play_round(self, player: Player) -> float:
        bet = get_valid_bet(player.wallet)
        if bet == 0:
            print("Returning to menu.")
            return 0.0
        print("Choose heads (h) or tails (t).")
        guess = input("Your choice (h/t): ").lower().strip()
        while guess not in ('h', 't'):
            guess = input("Please enter 'h' or 't': ").lower().strip()
        result = random.choice(['h', 't'])
        print(f"Result: {'heads' if result == 'h' else 'tails'}")
        if guess == result:
            print(f"🎉 You won {bet:.2f}!")
            return bet
        else:
            print(f"💀 You lost {bet:.2f}.")
            return -bet


class Blackjack(BaseGame):
    name = "Blackjack"

    @game_session("Blackjack")
    def play_round(self, player: Player) -> float:
        """
        Simple blackjack session: multiple hits/stands allowed.
        Returns net change across the session (can be multiple rounds until user cancels by betting 0).
        """
        total_change = 0.0

        def hand_total(hand):
            return sum(hand)

        while True:
            print("Enter 0 to return to main menu.")
            print(f"Current session balance: {player.wallet + total_change:.2f}")
            bet = get_valid_bet(player.wallet + total_change)
            if bet == 0:
                print("Exiting Blackjack session.")
                return total_change

            # initial deal
            dealer = [random.randint(1, 11)]
            player_hand = [random.randint(1, 11), random.randint(1, 11)]
            print(f"Dealer shows: 🂠 + {dealer[0]}")
            print(f"Your hand: {player_hand} (Total: {hand_total(player_hand)})")

            # player turn
            busted = False
            while True:
                total = hand_total(player_hand)
                if total == 21 and len(player_hand) == 2:
                    win = bet * 1.5
                    print(f"BLACKJACK! You win {win:.2f}.")
                    total_change += win
                    break
                if total > 21:
                    print("💀 Bust!")
                    total_change -= bet
                    busted = True
                    break
                move = input("Hit or Stand? (h/s): ").lower().strip()
                while move not in ('h', 's'):
                    move = input("Enter h or s: ").lower().strip()
                if move == 'h':
                    newcard = random.randint(1, 11)
                    player_hand.append(newcard)
                    print(f"You drew {newcard}. New total: {hand_total(player_hand)}")
                else:
                    break

            if busted:
                continue

            # dealer turn
            dealer.append(random.randint(1, 11))
            while hand_total(dealer) < 17:
                dealer.append(random.randint(1, 11))

            print(f"Dealer: {dealer} (Total: {hand_total(dealer)})")
            print(f"You: {player_hand} (Total: {hand_total(player_hand)})")

            p_total = hand_total(player_hand)
            d_total = hand_total(dealer)

            if d_total > 21 or p_total > d_total:
                print(f"🎉 You win {bet:.2f}!")
                total_change += bet
            elif p_total == d_total:
                print("😐 Push! No change.")
            else:
                print(f"💀 You lose {bet:.2f}.")
                total_change -= bet

            print(f"Session net change so far: {total_change:.2f}\n")
            cont = input("Play another Blackjack round? (y/n): ").lower().strip()
            if cont != 'y':
                return total_change


class Slots(BaseGame):
    name = "Cute Slots"

    def _spin_generator(self, symbols, frames=6):
        """Generator yields (r1, r2, r3) for each frame to simulate spin."""
        for _ in range(frames):
            yield (random.choice(symbols), random.choice(symbols), random.choice(symbols))

    @game_session("Cute Emoji Slots")
    def play_round(self, player: Player) -> float:
        symbols = ['ʕっ•ᴥ•ʔっ', '(⇀‸↼‶)', '(・3・)', '(︶︹︶)', '( º﹃º )']
        multipliers = [5, 10, 25, 50, 100]

        while True:
            print("Enter 0 to return to main menu.")
            bet = get_valid_bet(player.wallet)
            if bet == 0:
                return 0.0
            # spin with generator animation
            print("\nSpinning...\n")
            for (r1, r2, r3) in self._spin_generator(symbols, frames=8):
                print(f"| {r1} | {r2} | {r3} |", end="\r", flush=True)
                time.sleep(0.18)
            # final
            print()  # newline
            r1 = random.choice(symbols)
            r2 = random.choice(symbols)
            r3 = random.choice(symbols)
            print(f"| {r1} | {r2} | {r3} |")

            special = 'ʕっ•ᴥ•ʔっ'
            win = 0.0
            if r1 == r2 == r3 == special:
                mul = random.choice(multipliers)
                win = bet * mul
                print(f"🎉 JACKPOT! x{mul} => Won {win:.2f}")
            elif (r1 == special and r2 == special) or (r1 == special and r3 == special) or (r2 == special and r3 == special):
                mul = random.choice(multipliers[:3])
                win = bet * mul
                print(f"✨ Pair of special! x{mul} => Won {win:.2f}")
            else:
                win = -bet
                print("😢 No win this spin.")

            return win


# ------------------------
# Login / Register System
# ------------------------
def login_or_register_loop() -> Player:
    """Return a logged-in Player instance (or exits program)."""
    while True:
        clear_screen()
        print(tong_777_pic)
        print(login_pic)
        choice = input("Choose: ").strip()
        if choice == '1':
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
            p = Player.create_new(username=username, password_plain=pw, starting_wallet=100.0)
            print(f"✅ Account '{username}' created. Bonus 100.00 credits added.")
            time.sleep(1)
            return p
        elif choice == '3':
            print("Goodbye.")
            sys.exit(0)
        else:
            print("Please choose 1-3.")
            time.sleep(1)


# ------------------------
# Main menu
# ------------------------
def main():
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
            print(f"Player: {player.username} | Balance: {player.wallet:.2f}\n")
            print(menu_pic)
            choice = input("Select option (1-8): ").strip()
            if choice in ("1", "2", "3", "4"):
                game = games[choice]
                game.play_round(player)  # decorator handles wallet update and save
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
