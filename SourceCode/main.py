# --- main.py ---
from process import r_file, loop_playing, create_game,  , close
from var import menu_start, menu_load
import os

def main():
    screen = create_game('Chicken Invader')
    while True:
        # Kiểm tra file lưu để hiển thị menu
        if os.path.exists('../Data/save/save.txt'):
            select_start = create_menu(screen, menu_load())
            if select_start == 1:
                load_inf = r_file()  # tiếp tục từ level lưu
                loop_playing(screen, load_inf)
            elif select_start == 2:
                os.remove('../Data/save/save.txt')
                loop_playing(screen)
        else:
            select_start = create_menu(screen, menu_start())
            if select_start == 1:
                loop_playing(screen)
            elif select_start == 2:
                close()

if __name__ == "__main__":
    main()