import tkinter as tk
import math

class HypnoticAnimation:
    """
    A class to create a fullscreen, smooth, hypnotic animation.
    """
    def __init__(self, root):
        self.root = root
        
        # --- CHANGE: Get screen dimensions automatically ---
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()
        
        # --- CHANGE: Set the window to be truly fullscreen ---
        root.attributes('-fullscreen', True)
        # --- NEW: Hide the mouse cursor for better immersion ---
        root.config(cursor='none') 
        
        # --- NEW: Bind the Escape key to close the program ---
        root.bind('<Escape>', self.close_app)
        
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='black')
        self.canvas.pack()
        
        self.frame = 0

    def close_app(self, event=None):
        """ A function to close the window. """
        self.root.destroy()

    def draw_circles(self):
        """
        Draws one frame of the animation.
        """
        self.canvas.delete('all')
        
        center_x, center_y = self.width / 2, self.height / 2
        # --- CHANGE: Radius is now based on the smaller screen dimension ---
        max_radius = min(self.width, self.height) / 2.5 
        num_circles = 35 # Increased circles for a fuller look on a large screen

        for i in range(num_circles):
            oscillation = math.sin(self.frame * 0.05 + i * 0.4)
            
            radius = max_radius * ((i + 1) / num_circles) * (0.8 + 0.2 * oscillation)
            
            color_val = int(150 + 105 * oscillation)
            color = f'#{color_val:02x}{color_val:02x}{color_val:02x}'
            
            self.canvas.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                outline=color, width=3 # Slightly thicker lines
            )

    def update(self):
        """
        Updates the animation state and schedules the next frame.
        """
        self.draw_circles()
        self.frame += 1
        
        # --- CHANGE: Update every 16ms for ~60 FPS (1000ms / 16ms ≈ 62.5 FPS) ---
        self.root.after(16, self.update)

def main():
    root = tk.Tk()
    # Title is not visible in fullscreen, but good practice to have it
    root.title("Hypnotic Circles Fullscreen")
    
    app = HypnoticAnimation(root)
    app.update()
    root.mainloop()

if __name__ == '__main__':
    main()
