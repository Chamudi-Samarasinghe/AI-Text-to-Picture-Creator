# Text to Image Generator

A Python-based AI-powered Text to Image Generator that allows users to input text prompts and generate images using Hugging Face's Inference API. This application utilizes Tkinter for the graphical user interface and supports image generation and saving functionality.

## Features

- **Text-to-Image Generation:** Enter a text prompt and generate a corresponding image.
- **Image Display:** Display generated images directly in the app window.
- **Save Image:** Option to save generated images to your local storage.
- **Progress Bar:** A progress bar indicating the image generation status.

## Requirements

- Python 3.7+
- Tkinter (usually comes with Python)
- Pillow (for image handling)
- Hugging Face Inference API (`huggingface_hub`)

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/text-to-image-generator.git
    ```

2. Navigate into the project folder:

    ```bash
    cd text-to-image-generator
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Obtain an API token from Hugging Face and replace `"your_api_token_here"` in the code with your actual token.

## Usage

1. Run the application:

    ```bash
    python main.py
    ```

2. Enter a text prompt in the provided text box.
3. Click **Generate Image** to create an image.
4. Once the image is generated, it will be displayed in the app window.
5. Click **Save Image** to save the generated image to your local storage.

## Folder Structure


