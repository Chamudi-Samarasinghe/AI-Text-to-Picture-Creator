import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import io
import threading
from huggingface_hub import InferenceClient
from datetime import datetime
import os

class TextToImageGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Text to Image Generator")
        self.root.geometry("1024x768")
        
        # Initialize Hugging Face client with API token
        self.client = InferenceClient(
            "ZB-Tech/Text-to-Image", 
            token="api_token"  
        )
        
        # Create main container with padding
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Setup UI components
        self.setup_input_section()
        self.setup_image_section()
        self.setup_status_section()
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('Big.TButton', padding=10, font=('Arial', 11))
        self.style.configure('Status.TLabel', font=('Arial', 10))
        
    def setup_input_section(self):
        # Input Frame
        input_frame = ttk.LabelFrame(self.main_frame, text="Text Prompt", padding="10")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Text input with larger font
        self.prompt_text = scrolledtext.ScrolledText(
            input_frame, 
            height=3, 
            width=50, 
            font=('Arial', 11),
            wrap=tk.WORD
        )
        self.prompt_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Generate button
        generate_button = ttk.Button(
            input_frame, 
            text="Generate Image", 
            command=self.generate_image,
            style='Big.TButton'
        )
        generate_button.pack(pady=10)
        
    def setup_image_section(self):
        # Image Display Frame
        self.image_frame = ttk.LabelFrame(self.main_frame, text="Generated Image", padding="10")
        self.image_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Image label with gray background
        self.image_label = ttk.Label(self.image_frame, background='#f0f0f0')
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Save button
        save_button = ttk.Button(
            self.image_frame, 
            text="Save Image", 
            command=self.save_image,
            style='Big.TButton'
        )
        save_button.pack(pady=10)
        
    def setup_status_section(self):
        # Status Frame
        status_frame = ttk.Frame(self.main_frame)
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.status_label = ttk.Label(
            status_frame, 
            text="Ready to generate images",
            style='Status.TLabel'
        )
        self.status_label.pack(side=tk.LEFT)
        
        self.progress_bar = ttk.Progressbar(
            status_frame, 
            mode='indeterminate', 
            length=200
        )
        self.progress_bar.pack(side=tk.RIGHT, padx=5)
        
    def generate_image(self):
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        if not prompt:
            self.status_label.config(text="Please enter a prompt")
            return
            
        self.progress_bar.start()
        self.status_label.config(text="Generating image...")
        
        # Run generation in a separate thread
        thread = threading.Thread(target=self._generate_image_thread, args=(prompt,))
        thread.daemon = True
        thread.start()
        
    def _generate_image_thread(self, prompt):
        try:
            image = self.client.text_to_image(prompt)
            self.current_image = image
            
            # Resize image to fit the window while maintaining aspect ratio
            display_size = (800, 600)
            image.thumbnail(display_size, Image.LANCZOS)
            
            # Convert PIL image to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Update UI in the main thread
            self.root.after(0, self._update_image_display, photo)
            self.root.after(0, self._update_status, "Image generated successfully")
        except Exception as e:
            self.root.after(0, self._update_status, f"Error: {str(e)}")
        finally:
            self.root.after(0, self.progress_bar.stop)
            
    def _update_image_display(self, photo):
        self.photo = photo  # Keep a reference
        self.image_label.config(image=photo)
        
    def _update_status(self, status):
        self.status_label.config(text=status)
        
    def save_image(self):
        if hasattr(self, 'current_image'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_image_{timestamp}.png"
            
            if not os.path.exists("generated_images"):
                os.makedirs("generated_images")
                
            save_path = os.path.join("generated_images", filename)
            self.current_image.save(save_path)
            self.status_label.config(text=f"Image saved as {filename}")
        else:
            self.status_label.config(text="No image to save")

def main():
    root = tk.Tk()
    
    # Make window resizable
    root.resizable(True, True)
    
    # Set minimum window size
    root.minsize(800, 600)
    
    # Configure grid weights for responsiveness
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    
    app = TextToImageGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

