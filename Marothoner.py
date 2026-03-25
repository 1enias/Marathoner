import keyboard
import mouse
import time
import threading

# --- Configuration ---
TARGET_KEY = 'space'       # The main action key
TOGGLE_KEY = 'f9'          # The key to start/pause the script
EXIT_KEY = 'esc'           # The key to kill the script
INITIAL_INTERVAL = 1.0     # The starting delay in seconds
DECAY_RATE = 0.9          # Multiplier to reduce interval by 1% each press
MIN_INTERVAL = 0.08       # Safety limit: the absolute fastest it is allowed to go
# ---------------------

is_running = False
current_interval = INITIAL_INTERVAL

def precise_sleep_until(target_time):
    while target_time - time.perf_counter() > 0.002:
        time.sleep(0.001)
    while time.perf_counter() < target_time:
        pass

def auto_presser():
    global is_running, current_interval
    
    while True:
        if is_running:
            next_run_time = time.perf_counter() + current_interval
            
            keyboard.press(TARGET_KEY)
            mouse.press(button='left')
            
            current_interval *= DECAY_RATE
            
            if current_interval < MIN_INTERVAL:
                current_interval = MIN_INTERVAL
            
            precise_sleep_until(next_run_time)
            
            keyboard.release(TARGET_KEY)
            mouse.release(button='left')
            
            precise_sleep_until(next_run_time)
        else:
            time.sleep(0.1)

def toggle_script(e):
    global is_running
    is_running = not is_running
    status = "RUNNING" if is_running else "PAUSED"
    
    print(f"[{status}] Pressing '{TARGET_KEY}' + 'Left Mouse'. Current interval is ~{current_interval:.4f}s")

if __name__ == "__main__":
    print(f"--- Marothoner Pin Helper ---")
    print(f"Target: Explicit '{TARGET_KEY}' AND Left Mouse Press/Release")
    print(f"Starts at: {INITIAL_INTERVAL}s, decreases by 1% each press.")
    print(f"Press '{TOGGLE_KEY}' to Start/Pause.")
    print(f"Press '{EXIT_KEY}' to Exit.")
    print(f"---------------------------------------------")

    keyboard.on_press_key(TOGGLE_KEY, toggle_script)

    press_thread = threading.Thread(target=auto_presser)
    press_thread.daemon = True
    press_thread.start()

    keyboard.wait(EXIT_KEY)
    print("\nExiting program...")