import cv2
import os
import sys
import shutil
import time
import platform

# For cross-platform non-blocking keyboard input
if platform.system() == 'Windows':
    import msvcrt
else:
    import termios
    import tty
    import select

ASCII = " .'`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

# ==========================
# Configuration
# ==========================
WIDTH = 300
CHAR_ASPECT = 0.5
MENU_ITEMS = ["Test Print", "Option 2", "Exit"]
MENU_ROWS = 3   # 1: hint, 2: menu, 3: status

def terminal_size():
    cols, rows = shutil.get_terminal_size((120, 40))
    return cols, rows

def frame_to_ascii(frame, width, target_height=None):
    h, w = frame.shape[:2]
    aspect = h / w
    if target_height is None:
        height = max(1, int(width * aspect * CHAR_ASPECT))
    else:
        height = target_height
    frame = cv2.resize(frame, (width, height))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    output = []
    for y in range(height):
        line = ""
        for x in range(width):
            b, g, r = frame[y, x]
            value = gray[y, x]
            char = ASCII[int(value / 255 * (len(ASCII) - 1))]
            line += f"\033[38;2;{r};{g};{b}m{char}"
        output.append(line)
    return "\n".join(output) + "\033[0m"

def get_key_windows():
    """Non-blocking key reader for Windows using msvcrt."""
    if not msvcrt.kbhit():
        return None
    ch = msvcrt.getch()
    if ch == b'\r':          # Enter
        return 'ENTER'
    if ch == b'q':
        return 'q'
    if ch in (b'\x00', b'\xe0'):   # Arrow keys start with these
        arrow = msvcrt.getch()
        if arrow == b'H':
            return 'UP'
        elif arrow == b'P':
            return 'DOWN'
    return None

def get_key_unix(timeout=0.05):
    """Non-blocking key reader for Unix using select."""
    if select.select([sys.stdin], [], [], timeout)[0]:
        ch = os.read(sys.stdin.fileno(), 1)
        if ch == b'\x1b':          # escape sequence
            if select.select([sys.stdin], [], [], 0.01)[0]:
                seq = os.read(sys.stdin.fileno(), 2)
                if seq == b'[A':
                    return 'UP'
                elif seq == b'[B':
                    return 'DOWN'
        elif ch in (b'\r', b'\n'):
            return 'ENTER'
        elif ch == b'q':
            return 'q'
    return None

# Unified get_key
if platform.system() == 'Windows':
    get_key = get_key_windows
else:
    get_key = get_key_unix

def main():
    if len(sys.argv) != 2:
        print("Usage: python ascii_video_menu.py video.mp4")
        return

    cap = cv2.VideoCapture(sys.argv[1])
    if not cap.isOpened():
        print("Cannot open video.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 1:
        fps = 30
    delay = 1.0 / fps

    # Prepare terminal
    print("\033[?25l", end="", flush=True)  # hide cursor (works on modern terminals)
    if platform.system() != 'Windows':
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())

    try:
        print("\033[2J", end="", flush=True)  # clear screen

        selected = 0
        status_text = ""

        while True:
            start = time.time()

            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            cols, rows = terminal_size()
            video_height = max(1, rows - MENU_ROWS)
            width = cols

            ascii_frame = frame_to_ascii(frame, width, target_height=video_height)

            # --- Draw video area ---
            print("\033[H", end="")
            print(ascii_frame, end="", flush=True)

            # --- Draw menu area ---
            # Line 1: hint
            print(f"\033[{video_height+1};1H\033[2K", end="")
            print("Use ↑↓ to move, Enter to select, 'q' to quit.", end="")
            # Line 2: menu items
            print(f"\033[{video_height+2};1H\033[2K", end="")
            menu_line = ""
            for i, item in enumerate(MENU_ITEMS):
                if i == selected:
                    menu_line += f"\033[7m[{item}]\033[0m  "
                else:
                    menu_line += f"[{item}]  "
            print(menu_line, end="")
            # Line 3: status
            print(f"\033[{video_height+3};1H\033[2K", end="")
            print(f"Status: {status_text}", end="", flush=True)

            # --- Timing and input handling ---
            elapsed = time.time() - start
            remaining = delay - elapsed

            while remaining > 0:
                timeout = min(remaining, 0.05)
                if platform.system() == 'Windows':
                    key = get_key()  # already non-blocking
                    # Simulate a small sleep so we don't hammer the CPU, but not exactly timeout
                    # Actually we can just sleep a tiny bit and then check again
                    time.sleep(0.01)
                    # recalc remaining
                    elapsed = time.time() - start
                    remaining = delay - elapsed
                else:
                    key = get_key(timeout)
                    elapsed = time.time() - start
                    remaining = delay - elapsed

                if key == 'UP':
                    selected = (selected - 1) % len(MENU_ITEMS)
                elif key == 'DOWN':
                    selected = (selected + 1) % len(MENU_ITEMS)
                elif key == 'ENTER':
                    if selected == 0:
                        status_text = "Test action triggered! This is a test print."
                    elif selected == 1:
                        status_text = "Option 2 selected."
                    elif selected == 2:
                        raise StopIteration
                elif key == 'q':
                    raise StopIteration

    except (StopIteration, KeyboardInterrupt):
        pass
    finally:
        print("\033[?25h", end="")      # show cursor
        if platform.system() != 'Windows':
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        print("\033[2J\033[H", end="")
        cap.release()
        print("Goodbye!")

if __name__ == "__main__":
    main()