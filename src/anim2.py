import tkinter as tk
import math

class HypnoticAnimation:
    """
    A class to create a fullscreen, smooth, hypnotic animation.
    """
    def __init__(self, root):
        self.root = root
        
         
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()
        
         
        root.attributes('-fullscreen', True)
         
        root.config(cursor='none') 
        
         
        root.bind('<Escape>', self.close_app)
        
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='black')
        self.canvas.pack()
        
        self.frame = 0

    def close_app(self, event=None):
        
        self.root.destroy()

    def draw_circles(self):
        
        self.canvas.delete('all')
        
        center_x, center_y = self.width / 2, self.height / 2
         
        max_radius = min(self.width, self.height) / 2.5 
        num_circles = 35  

        for i in range(num_circles):
            oscillation = math.sin(self.frame * 0.05 + i * 0.4)
            
            radius = max_radius * ((i + 1) / num_circles) * (0.8 + 0.2 * oscillation)
            
            color_val = int(150 + 105 * oscillation)
            color = f'#{color_val:02x}{color_val:02x}{color_val:02x}' 
            
            self.canvas.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                outline=color, width=3  
            )

    def update(self):
        
        self.draw_circles()
        self.frame += 1
        
         
        self.root.after(16, self.update)

def main():
    root = tk.Tk()
     
    root.title("Hypnotic Circles Fullscreen")
    
    app = HypnoticAnimation(root)
    app.update()
    root.mainloop()

if __name__ == '__main__':
    main()
