#!/usr/bin/env python3
"""
Tong777 - Casino Game with Pygame GUI
Beautiful visual interface with animations and effects
"""
import os
import sys
import time
import random
import bcrypt
import pygame
from abc import ABC, abstractmethod
from typing import Optional, Tuple
from dataclasses import dataclass

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
COLOR_BG = (20, 20, 40)
COLOR_PRIMARY = (255, 215, 0)  # Gold
COLOR_SECONDARY = (138, 43, 226)  # Purple
COLOR_SUCCESS = (50, 205, 50)
COLOR_DANGER = (220, 20, 60)
COLOR_TEXT = (255, 255, 255)
COLOR_TEXT_DIM = (180, 180, 200)
COLOR_BUTTON = (70, 70, 120)
COLOR_BUTTON_HOVER = (100, 100, 160)
COLOR_CARD_BG = (40, 40, 80)

# Storage
BASE_PATH = os.path.join(os.path.expanduser("~"), ".tong777_players")
os.makedirs(BASE_PATH, exist_ok=True)

# ------------------------
# Utility Classes
# ------------------------
@dataclass
class Button:
    x: int
    y: int
    width: int
    height: int
    text: str
    color: Tuple[int, int, int] = COLOR_BUTTON
    hover_color: Tuple[int, int, int] = COLOR_BUTTON_HOVER
    text_color: Tuple[int, int, int] = COLOR_TEXT
    
    def draw(self, screen, font, mouse_pos):
        is_hover = self.is_over(mouse_pos)
        color = self.hover_color if is_hover else self.color
        
        # Draw button with gradient effect
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, COLOR_PRIMARY, (self.x, self.y, self.width, self.height), 3, border_radius=10)
        
        # Draw text
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
        screen.blit(text_surf, text_rect)
        
        return is_hover
    
    def is_over(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height

class InputBox:
    def __init__(self, x, y, width, height, font, placeholder='', password=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = COLOR_BUTTON
        self.color_active = COLOR_BUTTON_HOVER
        self.color = self.color_inactive
        self.text = ''
        self.font = font
        self.active = False
        self.placeholder = placeholder
        self.password = password
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return True
            else:
                if len(self.text) < 20:
                    self.text += event.unicode
        return False
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        pygame.draw.rect(screen, COLOR_PRIMARY, self.rect, 2, border_radius=5)
        
        display_text = self.text if not self.password else '*' * len(self.text)
        if not display_text and not self.active:
            display_text = self.placeholder
            color = COLOR_TEXT_DIM
        else:
            color = COLOR_TEXT
            
        text_surf = self.font.render(display_text, True, color)
        screen.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))
    
    def get_text(self):
        return self.text
    
    def clear(self):
        self.text = ''

# ------------------------
# Player Class
# ------------------------
class Player:
    def __init__(self, username: str, hashed_password: str, wallet: float = 0.0):
        self.username = username
        self.hashed_password = hashed_password
        self.wallet = float(wallet)
    
    @property
    def filepath(self) -> str:
        return os.path.join(BASE_PATH, f"{self.username}.txt")
    
    def save(self) -> None:
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                f.write(f"{self.username},{self.hashed_password},{self.wallet:.2f}")
        except (IOError, OSError) as e:
            print("Error saving player data:", e)
    
    @classmethod
    def load(cls, username: str) -> Optional["Player"]:
        filename = os.path.join(BASE_PATH, f"{username}.txt")
        if not os.path.exists(filename):
            return None
        try:
            with open(filename, "r", encoding="utf-8") as f:
                raw = f.read().strip()
            parts = raw.split(",")
            if len(parts) != 3:
                return None
            _, hashed_password, wallet_s = parts
            wallet = float(wallet_s)
            return cls(username=username, hashed_password=hashed_password, wallet=wallet)
        except Exception:
            return None
    
    @classmethod
    def create_new(cls, username: str, password_plain: str, starting_wallet: float = 100.0) -> "Player":
        hashed = bcrypt.hashpw(password_plain.encode("utf-8"), bcrypt.gensalt())
        hashed_s = hashed.decode("utf-8")
        player = cls(username=username, hashed_password=hashed_s, wallet=float(starting_wallet))
        player.save()
        return player
    
    def check_password(self, password_plain: str) -> bool:
        try:
            return bcrypt.checkpw(password_plain.encode("utf-8"), self.hashed_password.encode("utf-8"))
        except Exception:
            return False
    
    def update_wallet(self, amount: float) -> None:
        self.wallet = round(float(self.wallet) + float(amount), 2)
        self.save()

# ------------------------
# Game Classes
# ------------------------
class BaseGame(ABC):
    name: str = "BaseGame"
    
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self.running = True
    
    @abstractmethod
    def run(self, player: Player) -> bool:
        """Run game, return True to continue, False to exit"""
        pass
    
    def draw_header(self, player: Player, title: str):
        # Draw gradient background
        for i in range(0, 150, 5):
            color = (20 + i//3, 20 + i//3, 40 + i//2)
            pygame.draw.rect(self.screen, color, (0, i, SCREEN_WIDTH, 5))
        
        # Title
        title_text = self.fonts['title'].render(title, True, COLOR_PRIMARY)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Player info
        info_text = f"{player.username} | Balance: ${player.wallet:.2f}"
        info_surf = self.fonts['medium'].render(info_text, True, COLOR_TEXT)
        info_rect = info_surf.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(info_surf, info_rect)

class HighLowGame(BaseGame):
    name = "High-Low"
    
    def run(self, player: Player) -> bool:
        bet_input = InputBox(SCREEN_WIDTH//2 - 150, 300, 300, 50, self.fonts['medium'], 'Enter bet amount')
        back_button = Button(SCREEN_WIDTH//2 - 100, 700, 200, 50, "Back to Menu")
        
        state = "betting"  # betting, guessing, result
        bet_amount = 0
        first_num = 0
        second_num = 0
        result_msg = ""
        result_color = COLOR_TEXT
        
        clock = pygame.time.Clock()
        
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                if state == "betting":
                    if bet_input.handle_event(event):
                        try:
                            bet_amount = float(bet_input.get_text())
                            if 0 < bet_amount <= player.wallet:
                                first_num = random.randint(1, 100)
                                state = "guessing"
                            else:
                                result_msg = "Invalid bet amount!"
                                result_color = COLOR_DANGER
                        except ValueError:
                            result_msg = "Please enter a valid number!"
                            result_color = COLOR_DANGER
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_over(mouse_pos):
                        return True
                    
                    if state == "guessing":
                        # Higher button area
                        if 300 < mouse_pos[0] < 500 and 400 < mouse_pos[1] < 500:
                            second_num = random.randint(1, 100)
                            if second_num > first_num:
                                player.update_wallet(bet_amount)
                                result_msg = f"WIN! +${bet_amount:.2f}"
                                result_color = COLOR_SUCCESS
                            else:
                                player.update_wallet(-bet_amount)
                                result_msg = f"LOSE! -${bet_amount:.2f}"
                                result_color = COLOR_DANGER
                            state = "result"
                        
                        # Lower button area
                        elif 700 < mouse_pos[0] < 900 and 400 < mouse_pos[1] < 500:
                            second_num = random.randint(1, 100)
                            if second_num < first_num:
                                player.update_wallet(bet_amount)
                                result_msg = f"WIN! +${bet_amount:.2f}"
                                result_color = COLOR_SUCCESS
                            else:
                                player.update_wallet(-bet_amount)
                                result_msg = f"LOSE! -${bet_amount:.2f}"
                                result_color = COLOR_DANGER
                            state = "result"
                    
                    elif state == "result":
                        # Play again area
                        if SCREEN_WIDTH//2 - 100 < mouse_pos[0] < SCREEN_WIDTH//2 + 100 and 600 < mouse_pos[1] < 650:
                            bet_input.clear()
                            state = "betting"
                            result_msg = ""
            
            # Draw
            self.screen.fill(COLOR_BG)
            self.draw_header(player, "🎲 High-Low Game")
            
            if state == "betting":
                bet_input.draw(self.screen)
                instruction = self.fonts['medium'].render("Enter your bet and press Enter", True, COLOR_TEXT)
                self.screen.blit(instruction, (SCREEN_WIDTH//2 - 200, 250))
            
            elif state == "guessing":
                # Show first number
                num_text = self.fonts['huge'].render(str(first_num), True, COLOR_PRIMARY)
                num_rect = num_text.get_rect(center=(SCREEN_WIDTH//2, 300))
                self.screen.blit(num_text, num_rect)
                
                # Draw buttons
                higher_btn = Button(300, 400, 200, 100, "HIGHER", COLOR_SUCCESS, COLOR_SUCCESS)
                lower_btn = Button(700, 400, 200, 100, "LOWER", COLOR_DANGER, COLOR_DANGER)
                higher_btn.draw(self.screen, self.fonts['large'], mouse_pos)
                lower_btn.draw(self.screen, self.fonts['large'], mouse_pos)
                
                bet_text = self.fonts['medium'].render(f"Bet: ${bet_amount:.2f}", True, COLOR_PRIMARY)
                self.screen.blit(bet_text, (SCREEN_WIDTH//2 - 80, 550))
            
            elif state == "result":
                # Show both numbers
                nums_text = self.fonts['huge'].render(f"{first_num} → {second_num}", True, COLOR_PRIMARY)
                nums_rect = nums_text.get_rect(center=(SCREEN_WIDTH//2, 300))
                self.screen.blit(nums_text, nums_rect)
                
                # Show result
                result_surf = self.fonts['large'].render(result_msg, True, result_color)
                result_rect = result_surf.get_rect(center=(SCREEN_WIDTH//2, 450))
                self.screen.blit(result_surf, result_rect)
                
                # Play again button
                play_again_btn = Button(SCREEN_WIDTH//2 - 100, 600, 200, 50, "Play Again")
                play_again_btn.draw(self.screen, self.fonts['medium'], mouse_pos)
            
            if result_msg and state == "betting":
                msg_surf = self.fonts['medium'].render(result_msg, True, result_color)
                msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH//2, 400))
                self.screen.blit(msg_surf, msg_rect)
            
            back_button.draw(self.screen, self.fonts['medium'], mouse_pos)
            
            pygame.display.flip()
            clock.tick(FPS)
        
        return True

class SlotsGame(BaseGame):
    name = "Slots"
    
    def run(self, player: Player) -> bool:
        symbols = ['🐻', '🎮', '🎨', '🎪', '🍰']
        bet_input = InputBox(SCREEN_WIDTH//2 - 150, 250, 300, 50, self.fonts['medium'], 'Enter bet amount')
        back_button = Button(SCREEN_WIDTH//2 - 100, 700, 200, 50, "Back to Menu")
        spin_button = Button(SCREEN_WIDTH//2 - 100, 600, 200, 60, "SPIN!", COLOR_SUCCESS, COLOR_SUCCESS)
        
        state = "betting"  # betting, spinning, result
        bet_amount = 0
        reels = ['🐻', '🐻', '🐻']
        spin_frame = 0
        result_msg = ""
        result_color = COLOR_TEXT
        
        clock = pygame.time.Clock()
        
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                if state == "betting":
                    bet_input.handle_event(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_over(mouse_pos):
                        return True
                    
                    if state == "betting" and spin_button.is_over(mouse_pos):
                        try:
                            bet_amount = float(bet_input.get_text())
                            if 0 < bet_amount <= player.wallet:
                                state = "spinning"
                                spin_frame = 0
                            else:
                                result_msg = "Invalid bet amount!"
                                result_color = COLOR_DANGER
                        except ValueError:
                            result_msg = "Please enter a valid number!"
                            result_color = COLOR_DANGER
                    
                    elif state == "result":
                        bet_input.clear()
                        state = "betting"
                        result_msg = ""
            
            # Spinning animation
            if state == "spinning":
                spin_frame += 1
                if spin_frame < 60:
                    reels = [random.choice(symbols) for _ in range(3)]
                else:
                    # Final result
                    reels = [random.choice(symbols) for _ in range(3)]
                    state = "result"
                    
                    # Calculate win
                    if reels[0] == reels[1] == reels[2]:
                        win = bet_amount * 10
                        player.update_wallet(win)
                        result_msg = f"JACKPOT! +${win:.2f}"
                        result_color = COLOR_PRIMARY
                    elif reels[0] == reels[1] or reels[1] == reels[2] or reels[0] == reels[2]:
                        win = bet_amount * 2
                        player.update_wallet(win)
                        result_msg = f"WIN! +${win:.2f}"
                        result_color = COLOR_SUCCESS
                    else:
                        player.update_wallet(-bet_amount)
                        result_msg = f"LOSE! -${bet_amount:.2f}"
                        result_color = COLOR_DANGER
            
            # Draw
            self.screen.fill(COLOR_BG)
            self.draw_header(player, "🎰 Slots Machine")
            
            # Draw reels
            for i, symbol in enumerate(reels):
                x = 300 + i * 200
                y = 350
                pygame.draw.rect(self.screen, COLOR_CARD_BG, (x, y, 150, 150), border_radius=10)
                pygame.draw.rect(self.screen, COLOR_PRIMARY, (x, y, 150, 150), 3, border_radius=10)
                
                symbol_text = self.fonts['huge'].render(symbol, True, COLOR_TEXT)
                symbol_rect = symbol_text.get_rect(center=(x + 75, y + 75))
                self.screen.blit(symbol_text, symbol_rect)
            
            if state == "betting":
                bet_input.draw(self.screen)
                spin_button.draw(self.screen, self.fonts['large'], mouse_pos)
            
            if result_msg:
                result_surf = self.fonts['large'].render(result_msg, True, result_color)
                result_rect = result_surf.get_rect(center=(SCREEN_WIDTH//2, 550))
                self.screen.blit(result_surf, result_rect)
            
            back_button.draw(self.screen, self.fonts['medium'], mouse_pos)
            
            pygame.display.flip()
            clock.tick(FPS)
        
        return True

# ------------------------
# Main Game Application
# ------------------------
class CasinoApp:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎰 Tong777 Casino")
        
        # Fonts
        self.fonts = {
            'huge': pygame.font.Font(None, 120),
            'title': pygame.font.Font(None, 72),
            'large': pygame.font.Font(None, 48),
            'medium': pygame.font.Font(None, 36),
            'small': pygame.font.Font(None, 24)
        }
        
        self.player = None
        self.running = True
    
    def show_login_screen(self):
        username_input = InputBox(SCREEN_WIDTH//2 - 200, 300, 400, 50, self.fonts['medium'], 'Username')
        password_input = InputBox(SCREEN_WIDTH//2 - 200, 380, 400, 50, self.fonts['medium'], 'Password', password=True)
        
        login_button = Button(SCREEN_WIDTH//2 - 250, 500, 200, 60, "Login")
        register_button = Button(SCREEN_WIDTH//2 + 50, 500, 200, 60, "Register")
        
        message = ""
        message_color = COLOR_TEXT
        
        clock = pygame.time.Clock()
        
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return None
                
                username_input.handle_event(event)
                password_input.handle_event(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if login_button.is_over(mouse_pos):
                        username = username_input.get_text()
                        password = password_input.get_text()
                        
                        if username and password:
                            player = Player.load(username)
                            if player and player.check_password(password):
                                message = f"Welcome back, {username}!"
                                message_color = COLOR_SUCCESS
                                pygame.display.flip()
                                pygame.time.wait(1000)
                                return player
                            else:
                                message = "Invalid username or password!"
                                message_color = COLOR_DANGER
                        else:
                            message = "Please fill all fields!"
                            message_color = COLOR_DANGER
                    
                    elif register_button.is_over(mouse_pos):
                        username = username_input.get_text()
                        password = password_input.get_text()
                        
                        if username and password:
                            if Player.load(username):
                                message = "Username already exists!"
                                message_color = COLOR_DANGER
                            else:
                                player = Player.create_new(username, password, 100.0)
                                message = f"Account created! Welcome, {username}!"
                                message_color = COLOR_SUCCESS
                                pygame.display.flip()
                                pygame.time.wait(1000)
                                return player
                        else:
                            message = "Please fill all fields!"
                            message_color = COLOR_DANGER
            
            # Draw
            self.screen.fill(COLOR_BG)
            
            # Title
            title = self.fonts['title'].render("🎰 TONG777 CASINO", True, COLOR_PRIMARY)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
            self.screen.blit(title, title_rect)
            
            subtitle = self.fonts['medium'].render("Welcome! Please login or register", True, COLOR_TEXT_DIM)
            subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 220))
            self.screen.blit(subtitle, subtitle_rect)
            
            username_input.draw(self.screen)
            password_input.draw(self.screen)
            login_button.draw(self.screen, self.fonts['medium'], mouse_pos)
            register_button.draw(self.screen, self.fonts['medium'], mouse_pos)
            
            if message:
                msg_surf = self.fonts['medium'].render(message, True, message_color)
                msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH//2, 620))
                self.screen.blit(msg_surf, msg_rect)
            
            pygame.display.flip()
            clock.tick(FPS)
        
        return None
    
    def show_main_menu(self):
        buttons = [
            Button(SCREEN_WIDTH//2 - 250, 250, 200, 80, "🎲 High-Low"),
            Button(SCREEN_WIDTH//2 + 50, 250, 200, 80, "🎰 Slots"),
            Button(SCREEN_WIDTH//2 - 250, 370, 200, 80, "💰 Deposit"),
            Button(SCREEN_WIDTH//2 + 50, 370, 200, 80, "💳 Withdraw"),
            Button(SCREEN_WIDTH//2 - 100, 500, 200, 60, "🚪 Logout")
        ]
        
        clock = pygame.time.Clock()
        
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return None
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons[0].is_over(mouse_pos):  # High-Low
                        game = HighLowGame(self.screen, self.fonts)
                        if not game.run(self.player):
                            self.running = False
                            return None
                    elif buttons[1].is_over(mouse_pos):  # Slots
                        game = SlotsGame(self.screen, self.fonts)
                        if not game.run(self.player):
                            self.running = False
                            return None
                    elif buttons[2].is_over(mouse_pos):  # Deposit
                        self.show_deposit_screen()
                    elif buttons[3].is_over(mouse_pos):  # Withdraw
                        self.show_withdraw_screen()
                    elif buttons[4].is_over(mouse_pos):  # Logout
                        return "logout"
            
            # Draw
            self.screen.fill(COLOR_BG)
            
            # Title
            title = self.fonts['title'].render("🎰 TONG777 CASINO", True, COLOR_PRIMARY)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 80))
            self.screen.blit(title, title_rect)
            
            # Player info
            info = f"{self.player.username} | Balance: ${self.player.wallet:.2f}"
            info_surf = self.fonts['large'].render(info, True, COLOR_TEXT)
            info_rect = info_surf.get_rect(center=(SCREEN_WIDTH//2, 160))
            self.screen.blit(info_surf, info_rect)
            
            # Draw buttons
            for button in buttons:
                button.draw(self.screen, self.fonts['medium'], mouse_pos)
            
            pygame.display.flip()
            clock.tick(FPS)
        
        return None
    
    def show_deposit_screen(self):
        amount_input = InputBox(SCREEN_WIDTH//2 - 200, 350, 400, 50, self.fonts['medium'], 'Amount to deposit')
        confirm_button = Button(SCREEN_WIDTH//2 - 100, 500, 200, 60, "Confirm")
        back_button = Button(SCREEN_WIDTH//2 - 100, 600, 200, 50, "Back")
        
        message = ""
        message_color = COLOR_TEXT
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                
                amount_input.handle_event(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if confirm_button.is_over(mouse_pos):
                        try:
                            amount = float(amount_input.get_text())
                            if amount > 0:
                                self.player.update_wallet(amount)
                                message = f"Deposited ${amount:.2f} successfully!"
                                message_color = COLOR_SUCCESS
                                pygame.display.flip()
                                pygame.time.wait(1500)
                                return
                            else:
                                message = "Please enter a positive amount!"
                                message_color = COLOR_DANGER
                        except ValueError:
                            message = "Please enter a valid number!"
                            message_color = COLOR_DANGER
                    
                    elif back_button.is_over(mouse_pos):
                        return
            
            # Draw
            self.screen.fill(COLOR_BG)
            
            title = self.fonts['title'].render("💰 Deposit Funds", True, COLOR_PRIMARY)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
            self.screen.blit(title, title_rect)
            
            balance_text = f"Current Balance: ${self.player.wallet:.2f}"
            balance_surf = self.fonts['medium'].render(balance_text, True, COLOR_TEXT_DIM)
            balance_rect = balance_surf.get_rect(center=(SCREEN_WIDTH//2, 250))
            self.screen.blit(balance_surf, balance_rect)
            
            amount_input.draw(self.screen)
            confirm_button.draw(self.screen, self.fonts['medium'], mouse_pos)
            back_button.draw(self.screen, self.fonts['medium'], mouse_pos)
            
            if message:
                msg_surf = self.fonts['medium'].render(message, True, message_color)
                msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH//2, 680))
                self.screen.blit(msg_surf, msg_rect)
            
            pygame.display.flip()
            clock.tick(FPS)
    
    def show_withdraw_screen(self):
        amount_input = InputBox(SCREEN_WIDTH//2 - 200, 350, 400, 50, self.fonts['medium'], 'Amount to withdraw')
        confirm_button = Button(SCREEN_WIDTH//2 - 100, 500, 200, 60, "Confirm")
        back_button = Button(SCREEN_WIDTH//2 - 100, 600, 200, 50, "Back")
        
        message = ""
        message_color = COLOR_TEXT
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                
                amount_input.handle_event(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if confirm_button.is_over(mouse_pos):
                        try:
                            amount = float(amount_input.get_text())
                            if amount > 0:
                                if amount <= self.player.wallet:
                                    self.player.update_wallet(-amount)
                                    message = f"Withdrew ${amount:.2f} successfully!"
                                    message_color = COLOR_SUCCESS
                                    pygame.display.flip()
                                    pygame.time.wait(1500)
                                    return
                                else:
                                    message = "Insufficient balance!"
                                    message_color = COLOR_DANGER
                            else:
                                message = "Please enter a positive amount!"
                                message_color = COLOR_DANGER
                        except ValueError:
                            message = "Please enter a valid number!"
                            message_color = COLOR_DANGER
                    
                    elif back_button.is_over(mouse_pos):
                        return
            
            # Draw
            self.screen.fill(COLOR_BG)
            
            title = self.fonts['title'].render("💳 Withdraw Funds", True, COLOR_PRIMARY)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
            self.screen.blit(title, title_rect)
            
            balance_text = f"Current Balance: ${self.player.wallet:.2f}"
            balance_surf = self.fonts['medium'].render(balance_text, True, COLOR_TEXT_DIM)
            balance_rect = balance_surf.get_rect(center=(SCREEN_WIDTH//2, 250))
            self.screen.blit(balance_surf, balance_rect)
            
            amount_input.draw(self.screen)
            confirm_button.draw(self.screen, self.fonts['medium'], mouse_pos)
            back_button.draw(self.screen, self.fonts['medium'], mouse_pos)
            
            if message:
                msg_surf = self.fonts['medium'].render(message, True, message_color)
                msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH//2, 680))
                self.screen.blit(msg_surf, msg_rect)
            
            pygame.display.flip()
            clock.tick(FPS)
    
    def run(self):
        while self.running:
            # Login screen
            self.player = self.show_login_screen()
            if not self.player or not self.running:
                break
            
            # Main menu
            while self.running:
                result = self.show_main_menu()
                if result == "logout":
                    break
                elif result is None:
                    self.running = False
                    break
        
        pygame.quit()
        sys.exit()

# ------------------------
# Main Entry Point
# ------------------------
def main():
    try:
        app = CasinoApp()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()