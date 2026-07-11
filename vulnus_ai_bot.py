import cv2
import numpy as np
import mss
import keyboard
import time
import ctypes
import win32gui, win32api, win32con, win32process

# DPI Tudatosság beállítása
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    ctypes.windll.user32.SetProcessDPIAware()

pid = win32api.GetCurrentProcessId()
handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
win32process.SetPriorityClass(handle, win32process.REALTIME_PRIORITY_CLASS)

class VulnusGhostBot:
    def __init__(self):
        self.active = False
        self.sct = mss.mss()
        self.hwnd = None
        self.sl, self.st = 0, 0
        self.width, self.height = 0, 0
        
        # --- SOKKAL ENGEDÉKENYEBB SZÍNTARTOMÁNYOK ---
        # Blue: vilagosabb kék is belefér
        self.LOWER_BLUE = np.array([80, 50, 50])
        self.UPPER_BLUE = np.array([140, 255, 255])
        # Pink: tágabb tartomány
        self.LOWER_PINK = np.array([130, 50, 50])
        self.UPPER_PINK = np.array([179, 255, 255])

    def teleport_mouse(self, tx, ty):
        """Alacsony szintű egér teleportálás abszolút koordinátákkal"""
        # A Windows mouse_event 0-65535 közötti skálát használ az egész képernyőre
        screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        
        # Normalizálás
        nx = int(tx * (65535 / screen_width))
        ny = int(ty * (65535 / screen_height))
        
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_MOVE, nx, ny, 0, 0)

    def find_rhythia(self):
        # Megpróbáljuk több néven is, hátha változott
        for title in ["Rhythia", "Vulnus"]:
            hwnd = win32gui.FindWindow(None, title)
            if hwnd:
                cl_rect = win32gui.GetClientRect(hwnd)
                self.sl, self.st = win32gui.ClientToScreen(hwnd, (0, 0))
                self.width, self.height = cl_rect[2], cl_rect[3]
                return hwnd
        return None

    def run(self):
        print("\n--- VULNUS GHOST-BOT v31 ---")
        print("Mód: Teleportálás (Debug móddal)")
        print("CTRL+W: Start/Stop")
        
        keyboard.add_hotkey('ctrl+w', self.toggle)
        
        last_debug_time = time.time()

        while True:
            if keyboard.is_pressed('esc'): break
            
            if not self.hwnd or not win32gui.IsWindow(self.hwnd):
                self.hwnd = self.find_rhythia()
                if not self.hwnd:
                    time.sleep(1)
                    continue

            if self.active:
                try:
                    rect = {"top": self.st, "left": self.sl, "width": self.width, "height": self.height}
                    sct_img = self.sct.grab(rect)
                    
                    frame = np.array(sct_img)[:,:,:3]
                    # Kisebb downscale a pontosságért (csak 25%-os csökkentés)
                    small = cv2.resize(frame, (0,0), fx=0.75, fy=0.75, interpolation=cv2.INTER_NEAREST)
                    
                    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
                    mask = cv2.bitwise_or(
                        cv2.inRange(hsv, self.LOWER_BLUE, self.UPPER_BLUE),
                        cv2.inRange(hsv, self.LOWER_PINK, self.UPPER_PINK)
                    )
                    
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    
                    best_target = None
                    max_y = -1

                    # DEBUG: Kiírjuk ha látunk kontúrokat egyáltalán
                    if time.time() - last_debug_time > 2:
                        if len(contours) > 0:
                            print(f"Látok valamit! Kontúrok száma: {len(contours)}")
                        last_debug_time = time.time()

                    for cnt in contours:
                        # Kerület alapú szűrés - sokkal tágabb határok
                        perimeter = cv2.arcLength(cnt, True)
                        
                        # Ha a kerület > 30 pixel (ez már egy apró kocka is)
                        if perimeter > 30:
                            M = cv2.moments(cnt)
                            if M["m00"] != 0:
                                # Visszaszámítás az eredeti felbontásra (/0.75)
                                tx = self.sl + int((M["m10"] / M["m00"]) / 0.75)
                                ty = self.st + int((M["m01"] / M["m00"]) / 0.75)
                                
                                if ty > max_y:
                                    max_y = ty
                                    best_target = (tx, ty)

                    if best_target:
                        self.teleport_mouse(best_target[0], best_target[1])
                    
                except Exception as e:
                    # print(f"Hiba: {e}")
                    continue
            else:
                time.sleep(0.1)

    def toggle(self):
        self.active = not self.active
        print("\nBOT: " + ("AKTÍV" if self.active else "KIKAPCSOLVA"))
        if self.active:
            # Frissítjük az ablak pozícióját aktiváláskor
            self.hwnd = self.find_rhythia()

if __name__ == "__main__":
    bot = VulnusGhostBot()
    bot.run()
