import random
import os
import sys
import tty
import termios
import time
import bcrypt

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
# Utility Functions
# ============================================================

# ===== Function Clear Terminal =====
def clear_screen() -> None:
    """
    Clear the terminal screen.

    Input:
        None

    Output:
        None

    Description:
        Uses the OS-specific command to clear the terminal for macOS/Linux/Windows.
    """
    os.system('clear' if os.name != 'nt' else 'cls')


# ===== Functiom Press Key and No Enter =====
def get_char() -> str:
    """
    Read and return a single character from input (no Enter required).

    Input:
        None

    Output:
        str: a single character typed by the user

    Description:
        Works on Unix-like systems by switching terminal to raw mode for a single character read.
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


# ===== Functiom Press Any Key to Continue =====
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


# ===== Loading Screen =====
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


# ===== Check Valid Two Decimal =====
def is_positive_number(text: str) -> bool:
    """
    Check if the given string represents a positive number with up to 2 decimal places.

    Input:
        text (str): string to test

    Output:
        bool: True if the string is numeric and has at most 2 decimal places, else False

    Description:
        - Allows only positive numbers (integer or decimal).
        - Accepts up to 2 digits after the decimal point.
        - Rejects empty strings, symbols, or more than 2 decimal places.
    """
    stripped = text.strip()
    if stripped == "" or stripped == ".":
        return False
    if stripped.count(".") > 1:
        return False
    if not stripped.replace(".", "", 1).isdigit():
        return False
    if "." in stripped:
        decimals = stripped.split(".")[1]
        if len(decimals) > 2:
            return False
    return True


# ===== Check Valid Bet =====
def get_valid_bet(current_money: float) -> float:
    """
    Ask the player to enter a bet amount and ensure it is valid.

    Input:
        current_money (float): The player's current wallet balance.

    Output:
        float:
            - Returns a valid float bet (rounded to 2 decimals).
            - Returns 0.0 if the player enters 0 to exit.

    Description:
        This function ensures:
            - The bet is numeric, positive, and has at most 2 decimal places.
            - The bet does not exceed the current balance.
            - Entering 0 exits the game and returns 0.0.
    """
    while True:
        amount = input(f"💰 Enter your bet (0 to exit): ").strip()

        # Check numeric validity
        if not is_positive_number(amount):
            print(
                "❌ Invalid input. Please enter a positive number with up to 2 decimal places.")
            continue

        # Convert safely (no try/except)
        if '.' in amount:
            integer_part, decimal_part = amount.split('.', 1)
            if decimal_part == '':
                decimal_part = '0'
            fval = float(integer_part + '.' + decimal_part)
        else:
            fval = float(amount)

        # Handle exit
        if fval == 0:
            return 0.0

        # Check against balance
        if fval > current_money:
            print(
                f"❌ You cannot bet more than your balance ({current_money:.2f}).")
            continue

        # Passed all checks
        return round(fval, 2)


# ============================================================
# Player Data Management
# ============================================================

# ===== Path for ID User =====
BASE_PATH = "/Users/kung/Intro to programming_Python/Fay_Python/Tong777/ID_user"
os.makedirs(BASE_PATH, exist_ok=True)

# ===== Load Player =====
def load_player(username: str) -> tuple[str, float]:
    """
    Load player data from file.

    Input:
        username (str): player's username (file is <username>.txt)

    Output:
        tuple or None:
            - If exists and valid: (hashed_password (str), wallet (float))
            - If not found or file invalid: None

    Description:
        Reads CSV format: username,hashed_password,wallet
    """
    filename = os.path.join(BASE_PATH, f"{username}.txt")
    if not os.path.exists(filename):
        return None
    with open(filename, "r") as file:
        data = file.read().strip().split(",")
        if len(data) != 3:
            return None
        _, hashed_password, wallet = data
        return hashed_password, float(wallet)


# ===== Save Player =====
def save_player(username: str, hashed_password: str, wallet: float) -> None:
    """
    Save player data to file.

    Input:
        username (str): player's username
        hashed_password (str): bcrypt-hashed password (utf-8 string)
        wallet (float): wallet balance to save

    Output:
        None

    Description:
        Writes CSV format: username,hashed_password,wallet to BASE_PATH/<username>.txt
    """
    filename = os.path.join(BASE_PATH, f"{username}.txt")
    with open(filename, "w") as file:
        file.write(f"{username},{hashed_password},{wallet:.2f}")


# ============================================================
# Login / Register System with Password Hash
# ============================================================

# ===== Login or Register =====
def login_or_register() -> tuple[str, str, float]:
    """
    Login or register menu.

    Input:
        None (interacts with user via prompts)

    Output:
        tuple:
            (username (str), hashed_password (str), wallet (float)) on successful login or new registration

    Description:
        Offers options: Login, Register, Forgot Password, Exit.
        Validates inputs and uses bcrypt to check/store hashed passwords.
    """
    while True:
        clear_screen()
        print(tong_777_pic)
        print(login_pic)

        choice = input("Select option (1-3): ").strip()
        if choice not in ['1', '2', '3', '4']:
            print("Please select 1-3.")
            press_to_continue()
            continue

        if choice == '1':
            username = input("Enter username: ").strip()
            if username == "":
                print("Username cannot be empty.")
                press_to_continue()
                continue
            player_data = load_player(username)

            if player_data is not None:
                hashed_password, wallet = player_data
                password = input("Enter password: ").strip()
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    print(f"Welcome back, {username}!")
                    press_to_continue()
                    return username, hashed_password, wallet
                else:
                    print("❌ Incorrect password.")
                    press_to_continue()
                    continue
            else:
                print("❌ User not found.")
                press_to_continue()
                continue

        elif choice == '2':
            username = input("Enter username: ").strip()
            if username == "":
                print("Username cannot be empty.")
                press_to_continue()
                continue
            if load_player(username):
                print("⚠️ Username already exists.")
                press_to_continue()
                continue
            password = input("Set your password: ").strip()
            while password == "":
                password = input(
                    "Password cannot be empty. Set your password: ").strip()
            hashed_password = bcrypt.hashpw(password.encode(
                'utf-8'), bcrypt.gensalt()).decode('utf-8')
            wallet = 100.00
            save_player(username, hashed_password, wallet)
            print(f"✅ Account '{username}' created successfully!")
            print("🎁 You received 100.00 credits as a new player bonus 🎁")
            press_to_continue()
            return username, hashed_password, wallet

        elif choice == '3':
            print("👋 Goodbye!")
            sys.exit()


# ============================================================
# Deposit / Withdraw
# ============================================================

# ===== Deposit =====
def deposit(wallet: float) -> float:
    """
    Deposit function.

    Input:
        wallet (float): current wallet balance

    Output:
        float: amount deposited (positive)

    Description:
        Shows QR placeholder and asks user for deposit amount. Validates numeric input.
    """
    clear_screen()
    print("----[Deposit Funds]----\n")
    print(f"You have {wallet:.2f} credits.")

    while True:
        amount = input(
            "How much would you like to deposit [credits]: ").strip()
        if not is_positive_number(amount):
            print("❌ Invalid input. Please enter a number (max 2 decimals).")
            continue

        deposit_value = float(amount)
        if deposit_value <= 0:
            print("❌ Amount must be greater than 0.")
            continue

        break

    print(qr_promptpay_pic)
    transaction_ID = input("Please enter Transaction ID: ").strip()

    time.sleep(0.5)
    print(f"✅ Successfully added {deposit_value:.2f} credits to your wallet.")
    return round(deposit_value, 2)


# ===== Withdraw =====
def withdraw(wallet: float) -> float:
    """
    Withdraw function.

    Input:
        wallet (float): current wallet balance

    Output:
        float: amount withdrawn (positive)

    Description:
        Prompts user to input an amount to withdraw, validates numeric input and sufficient funds.
    """
    clear_screen()
    print("----[Withdraw Funds]----\n")
    print(f"You have {wallet:.2f} credits.")

    while True:
        amount = input(
            "How much would you like to withdraw [credits]: ").strip()
        if not is_positive_number(amount):
            print("❌ Invalid input. Please enter a number (max 2 decimals).")
            continue

        withdraw_value = float(amount)
        if withdraw_value <= 0:
            print("❌ Amount must be greater than 0.")
            continue
        if withdraw_value > wallet:
            print("❌ Not enough balance! Enter a smaller amount.")
            continue

        break

    time.sleep(0.5)
    print(f"✅ Successfully withdrew {withdraw_value:.2f} credits.")
    return withdraw_value


# ============================================================
# Game Logic
# ============================================================

# ===== Game High-Low =====
def game_high_low(current_money: float) -> float:
    """
    High-Low game.

    Input:
        current_money (float): player's current balance

    Output:
        float: change in money (positive if win, negative if lose, 0 if invalid)

    Description:
        Player bets an amount and guesses whether the next random number (1-100) will be higher or lower.
    """

    clear_screen()
    print("🎯 High-Low Game 🎯")
    print(f"You have {current_money:.2f} credits.")

    bet_input = get_valid_bet(current_money)
    bet = float(bet_input)
    if bet <= 0 or bet > current_money:
        print("Invalid bet amount!")
        return 0.0

    num1 = random.randint(1, 100)
    print(f"First number: {num1}")
    guess = input(
        "Will the next number be (h)igher or (l)ower? ").lower().strip()
    while guess not in ['h', 'l']:
        guess = input("Please enter 'h' or 'l': ").lower().strip()

    num2 = random.randint(1, 100)
    print(f"Next number: {num2}")

    if (guess == 'h' and num2 > num1) or (guess == 'l' and num2 < num1):
        print(f"🎉 You won {bet:.2f}!")
        return bet
    else:
        print(f"💀 You lost {bet:.2f}.")
        return -bet


# ===== Game Coin Flib =====
def game_coin_flip(current_money: float) -> float:
    """
    Coin flip game.

    Input:
        current_money (float): player's current balance

    Output:
        float: change in money (positive if win, negative if lose, 0 if invalid)

    Description:
        Player bets an amount and chooses heads (h) or tails (t). Coin is flipped randomly.
    """
    clear_screen()
    print("🪙 Coin Flip (h/t) 🪙")
    print(f"You have {current_money:.2f} credits.")

    bet_input = get_valid_bet(current_money)
    bet = float(bet_input)
    if bet <= 0 or bet > current_money:
        print("Invalid bet amount!")
        return 0.0

    guess = input("Choose (h)eads or (t)ails: ").lower().strip()
    while guess not in ['h', 't']:
        guess = input("Please enter 'h' or 't': ").lower().strip()

    result = random.choice(['h', 't'])

    if guess == result:
        print(f"🎉 You won! It was {'heads' if result == 'h' else 'tails'}.")
        return bet
    else:
        print(f"💀 You lost! It was {'heads' if result == 'h' else 'tails'}.")
        return -bet


# ===== Game Backjack =====
def game_blackjack(current_money: float) -> float:
    """
    Blackjack game with dealing effect.

    Input:
        current_money (float): player's current balance

    Output:
        float: net change to player's balance across the blackjack session (positive for net win, negative for net loss)

    Description:
        Plays rounds of blackjack. Player can enter 0 as bet to return to main menu.
        This function calculates wins/losses as net change but does not directly modify external wallet.
        Paying rules:
          - Blackjack (21 on initial hand): wins 1.5x bet (i.e., get bet + 1.5*bet)
          - Regular win: player wins equal to bet (i.e., get bet + bet)
          - Push: no change
          - Loss: lose bet
    """
    total_change = 0.0

    def hand_total(hand):
        return sum(hand)

    def deal_card_animation(to_whom: str, card_value: int) -> None:
        """
        Deal card animation

        Input:
            to_whom (str): Dealing a card to
            card_value (int): Number on card

        Output:
            None

        Description:
            Deal card animation with delay
        """
        print(f"Dealing a card to {to_whom}...", end="", flush=True)
        time.sleep(0.4)
        print(" 🂠", end="", flush=True)
        time.sleep(0.4)
        print(f" → {card_value}")
        time.sleep(0.3)

    while True:
        clear_screen()
        print("🃏 Blackjack 🃏")
        print("Enter 0 to return to the main menu.")
        wallet = current_money + total_change
        print(f"💰 Balance: {wallet:.2f}\n")

        bet_input = get_valid_bet(current_money)
        bet = float(bet_input)
        if bet == 0:
            print("\nReturning to main menu...")
            time.sleep(0.8)
            return total_change

        if bet < 0 or bet > wallet:
            print("Invalid bet amount!")
            press_to_continue()
            continue

        # Deal initial cards
        dealer_cards = []
        player_cards = []

        print("\n🎴 Dealing cards...\n")
        time.sleep(0.4)
        for _ in range(2):
            dealer_card = random.randint(1, 11)
            player_card = random.randint(1, 11)
            deal_card_animation("Dealer", dealer_card)
            dealer_cards.append(dealer_card)
            deal_card_animation("You", player_card)
            player_cards.append(player_card)
            print()
            time.sleep(0.2)

        print(f"\nDealer shows: 🂠 + {dealer_cards[0]}")
        print(
            f"Your cards: {player_cards} (Total: {hand_total(player_cards)})")

        # Player turn
        player_busted = False
        while True:
            if hand_total(player_cards) == 21 and len(player_cards) == 2:
                win = bet * 2.5
                total_change += win
                print(f"🎉 Blackjack! You won {win:.2f} (x2.5) credits!")
                break
            if hand_total(player_cards) > 21:
                print("💀 Bust! You went over 21.")
                total_change -= bet
                player_busted = True
                break

            move = input("Do you want to (H)it or (S)tand? ").lower().strip()
            while move not in ['h', 's']:
                move = input("❌ Please enter H or S only: ").lower().strip()
            if move == 'h':
                new_card = random.randint(1, 11)
                deal_card_animation("You", new_card)
                player_cards.append(new_card)
                print(f"Your total: {hand_total(player_cards)}")
            else:
                print("\nYou chose to stand.")
                break

        # Dealer turn and determine outcome (if player not busted)
        if not player_busted:
            print("\nDealer's turn...")
            time.sleep(0.3)
            print(
                f"Dealer's cards: {dealer_cards} (Total: {hand_total(dealer_cards)})")
            while hand_total(dealer_cards) < 17:
                new_card = random.randint(1, 11)
                deal_card_animation("Dealer", new_card)
                dealer_cards.append(new_card)
                print(f"Dealer's total: {hand_total(dealer_cards)}")
                time.sleep(0.2)

            player_total = hand_total(player_cards)
            dealer_total = hand_total(dealer_cards)

            print("\n--------------------------------")
            print(f"Dealer: {dealer_total} | You: {player_total}")
            print("--------------------------------")

            win_amount = bet * 2
            if dealer_total > 21:
                print(
                    f"🎉 Dealer busts! You won {win_amount:.2f} credits (x2)!")
                total_change += bet
            elif player_total > dealer_total:
                print(f"🎯 You won {win_amount:.2f} credits (x2)!")
                total_change += bet
            elif player_total == dealer_total:
                print("😐 Push! You get your bet back.")
                # no change
            else:
                print("💀 Dealer wins!")
                total_change -= bet

        # print(f"\nRound result (net change so far): {total_change:.2f}")
        result_wallet = wallet + total_change

        print(f"💰 Balance: {result_wallet:.2f}")
        press_to_continue()


# ===== Game Slots =====
def game_cute_emoji(current_money: float) -> float:
    """
    Cute Emoji Slot Machine.

    Input:
        current_money (float): player's current balance

    Output:
        float: net change in balance from playing slots this session (positive if win, negative if loss)

    Description:
        Player can play repeated slot spins. Enter bet=0 to return to main menu.
        Each spin shows three random emojis. Matching pairs/triples of the 'special' emoji yield multiplier wins.
    """
    list_slots = ['ʕっ•ᴥ•ʔっ',
                  ' (⇀‸↼‶)  ',
                  ' (・3・) ',
                  ' (︶︹︶)',
                  '( º﹃º ) '
                  ]
    multipliers = [5, 10, 25, 50, 100]
    total_change = 0.0

    while True:
        clear_screen()
        print("🎰 Cute Emoji Slot Machine 🎰")
        print("Enter 0 to return to main menu.\n")
        wallet = current_money + total_change
        print(f"💰 You have: {wallet:.2f} credits\n")

        bet_input = get_valid_bet(current_money)
        bet = float(bet_input)
        if bet == 0:
            print("\nReturning to main menu...")
            time.sleep(0.8)
            return total_change

        if bet < 0 or bet > wallet:
            print("Invalid bet amount!")
            press_to_continue()
            continue

        # Spin animation
        clear_screen()
        print("Spinning...\n")
        time.sleep(0.8)
        result1 = result2 = result3 = None
        for _ in range(6):  # show a few roll frames
            result1 = random.choice(list_slots)
            result2 = random.choice(list_slots)
            result3 = random.choice(list_slots)
            print(f"|  {result1}  |  {result2}  |  {result3}  |")
            time.sleep(0.2)
        print()

        win_amount = 0.0
        special = 'ʕっ•ᴥ•ʔっ'

        if result1 == result2 == result3 == special:
            multiplier = random.choice(multipliers)
            win_amount = bet * multiplier
            print(
                f"🎉 JACKPOT! You won {win_amount:.2f} credits (x{multiplier})!")
        elif (result1 == special and result2 == special) or \
             (result1 == special and result3 == special) or \
             (result2 == special and result3 == special):
            multiplier = random.choice(multipliers[:3])
            win_amount = bet * multiplier
            print(
                f"✨ You got a pair! You won {win_amount:.2f} credits (x{multiplier})!")
        else:
            print("😢 Too bad! You lost this round.")
            win_amount = -bet

        total_change += win_amount
        result_wallet = wallet + win_amount

        print(f"💰 Balance: {result_wallet:.2f}")
        press_to_continue()

# ============================================================
# Main Game Menu
# ============================================================

def main():
    """
    Main program entry point.

    Input:
        None (runs interactive terminal UI)

    Output:
        None (exits when user selects Exit)

    Description:
        Shows loading screen, then runs login/register loop, then main menu loop.
        All games and wallet changes update player file on exit or on save.
    """
    print(
        f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n{tong_777_pic}\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    press_to_continue()
    clear_screen()
    loading_screen()

    while True:
        username, hashed_password, wallet = login_or_register()

        while True:
            clear_screen()
            print(tong_777_pic)
            print(f"Player: {username}")
            print(f"Balance: {wallet:.2f} credits")
            print(menu_pic)

            choice = input("Select menu (1-8): ").strip()

            if choice == '1':
                change = game_high_low(wallet)
                wallet += change
                save_player(username, hashed_password, wallet)
                press_to_continue()

            elif choice == '2':
                change = game_coin_flip(wallet)
                wallet += change
                save_player(username, hashed_password, wallet)
                press_to_continue()

            elif choice == '3':
                change = game_blackjack(wallet)
                wallet += change
                save_player(username, hashed_password, wallet)
                press_to_continue()

            elif choice == '4':
                change = game_cute_emoji(wallet)
                wallet += change
                save_player(username, hashed_password, wallet)
                press_to_continue()

            elif choice == '5':
                amount = deposit(wallet)
                wallet += amount
                save_player(username, hashed_password, wallet)
                press_to_continue()

            elif choice == '6':
                amount = withdraw(wallet)
                wallet -= amount
                save_player(username, hashed_password, wallet)
                press_to_continue()

            elif choice == '7':
                print("🔁 Logging out...")
                time.sleep(1)
                break  # back to login/register

            elif choice == '8':
                print("💾 Saving data and exiting game...")
                save_player(username, hashed_password, wallet)
                time.sleep(1)
                sys.exit()  # exit code no return

            else:
                print("Please select 1-8 only.")
                press_to_continue()

# ============================================================
# Start Game
# ============================================================

if __name__ == "__main__":
    main()
