import os

# OOP
if __name__ == "__main__":
    # main()
    print(__name__)


# press any
if os.name == "nt":
    import msvcrt

    def clear_screen() -> None:
        # Use clear console command
        os.system("cls")

    def get_char() -> str:
        # Output 1 character then user type without echo and waiting for enter
        return chr(msvcrt.getch()[0])

else:
    import tty
    import termios
    import sys

    def clear_screen() -> None:
        os.system("clear")

    def get_char() -> str:
        # Gets the file descriptor (an integer handle) for standard input
        file_descriptor = sys.stdin.fileno()

        # Saves the current terminal settings
        old_settings = termios.tcgetattr(file_descriptor)

        # Puts the terminal in raw mode (No echo)
        tty.setraw(file_descriptor)

        # Reads 1 character from the terminal
        character = sys.stdin.read(1)

        # Restores the original terminal settings
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)

        # return character
        return character


lane1 = ['Bonus Bomb', 'Grapes', 'Banana', 'Lemon', 'Pear', 'Strawberry']
lane1 = ['ʕっ•ᴥ•ʔっ', '(ㆆ _ ㆆ)', '(˵ ͡° ͜ʖ ͡°˵)',
         '( ͡° ᴥ ͡°)', 'ԅ(≖‿≖ԅ)', 'Strawberry']

x = r"""
    x⸑x
    (˵ ͡° ͜ʖ ͡°˵)
    ԅ(≖‿≖ԅ)
    (͠≖ ͜ʖ͠≖)
    (◞థ౪థ)ᴖ
    (˶‾᷄ ⁻̫ ‾᷅˵)

-`ღ´-

"""

lane1 = ['!! ʕっ•ᴥ•ʔっ !!', '(⇀‸↼‶)', '(⇀‸↼‶)', '(・3・)', '(︶︹︶)', '( º﹃º )']

lane2 = ['!! ʕ •́؈•̀) !!', '(੭*ˊᵕˋ)੭', '(ღ˘⌣˘ღ)', '(っˆڡˆς)', '(ㆆ _ ㆆ)', '( ͡° ᴥ ͡°)']

lane3 = ['!! ༼ಠ益ಠ༽ !!', '(⌐■_■)', '(≧︿≦)', 'ᕦ(⩾﹏⩽)ᕥ', '(҂◡_◡) ᕤ', 'ψ(｀∇´)ψ']

x2 = """
ʕっ•ᴥ•ʔっ
ʕ •́؈•̀)

(⇀‸↼‶)
(⇀‸↼‶)
(・3・)
(︶︹︶)
( º﹃º )

(੭*ˊᵕˋ)੭
(ღ˘⌣˘ღ)
(っˆڡˆς)
(ㆆ _ ㆆ)
( ͡° ᴥ ͡°)


༼ಠ益ಠ༽
꒰ ꒡⌓꒡꒱

(ง •̀_•́)ง

(⌐■_■)
(≧︿≦)
ᕦ(⩾﹏⩽)ᕥ
(҂◡_◡) ᕤ
ψ(｀∇´)ψ

(ಡ_ಡ)☞
(ಠ_ಠ)
(ʘ‿ʘ)╯
(❍ᴥ❍ʋ)
✌(-‿-)✌
"""

