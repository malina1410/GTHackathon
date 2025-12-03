import os
import io
import time
import logging
import zipfile
from pathlib import Path
from typing import List, Tuple

from dotenv import load_dotenv
from PIL import Image
from rembg import remove as remove_background

# Google Cloud Imports
import vertexai
from vertexai.generative_models import GenerativeModel, Part, Image as VertexImage
from vertexai.preview.vision_models import ImageGenerationModel

# Import Config
import config

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
load_dotenv()

# Setup Directories
BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "inputs"
OUTPUT_DIR = BASE_DIR / "outputs"
ASSETS_DIR = BASE_DIR / "assets"

def init_google_cloud():
    """Initializes Vertex AI SDK."""
    try:
        vertexai.init(project=config.PROJECT_ID, location=config.LOCATION)
        logging.info(f"✅ Google Cloud Vertex AI initialized: {config.PROJECT_ID}")
    except Exception as e:
        logging.error(f"❌ Failed to init Vertex AI. Run 'gcloud auth application-default login'. Error: {e}")
        exit(1)

def clean_product_image(image_path: Path) -> Image.Image:
    """
    Uses 'rembg' to strip the background from the product image.
    Returns a PIL Image with transparent background.
    """
    logging.info(f"🧹 Removing background from: {image_path.name}...")
    with open(image_path, "rb") as f:
        input_data = f.read()
    
    # Remove background using U2Net (standard robust model)
    output_data = remove_background(input_data)
    img = Image.open(io.BytesIO(output_data)).convert("RGBA")
    return img

def generate_prompt_with_gemini(product_img: Image.Image, theme: dict) -> str:
    """
    Sends the product image to Gemini 1.5 Flash to write a perfect prompt
    based on the requested theme.
    """
    logging.info(f"🧠 Asking Gemini to write a prompt for theme: '{theme['theme']}'...")
    
    # Convert PIL image to bytes for Vertex AI
    img_byte_arr = io.BytesIO()
    product_img.save(img_byte_arr, format='PNG')
    img_bytes = img_byte_arr.getvalue()
    
    model = GenerativeModel("gemini-1.5-flash-002")
    
    # Construct the multimodal request
    prompt_request = f"Theme: {theme['theme']}\nMood: {theme['mood']}"
    
    response = model.generate_content(
        [
            Part.from_image(VertexImage.from_bytes(img_bytes)),
            config.PROMPT_GENERATION_INSTRUCTIONS,
            prompt_request
        ]
    )
    
    generated_prompt = response.text.strip()
    logging.info(f"📝 Prompt Generated: \"{generated_prompt[:60]}...\"")
    return generated_prompt

def generate_background_with_imagen(prompt: str) -> Image.Image:
    """
    Calls Imagen 3 to generate the background scene.
    Note: We generate the SCENE, then composite the product on top.
    """
    logging.info("🎨 Generating background with Imagen 3...")
    model = ImageGenerationModel.from_pretrained(config.IMAGEN_MODEL)
    
    response = model.generate_images(
        prompt=prompt,
        number_of_images=1,
        aspect_ratio=config.ASPECT_RATIO,
        safety_filter_level="block_some",
        person_generation="allow_adult"
    )
    
    # Convert Vertex output to PIL Image
    # response.images[0] is a Vertex Image object
    return response[0]._pil_image

def composite_images(background: Image.Image, product: Image.Image) -> Image.Image:
    """
    Smartly places the product onto the background.
    """
    # Resize background to target (e.g., 1024x1024)
    target_size = (1024, 1024)
    background = background.resize(target_size, Image.Resampling.LANCZOS).convert("RGBA")
    
    # Calculate Product Size (e.g., 60% of canvas height)
    scale_factor = 0.6
    aspect_ratio = product.width / product.height
    new_height = int(target_size[1] * scale_factor)
    new_width = int(new_height * aspect_ratio)
    
    product_resized = product.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Center the product
    x_pos = (target_size[0] - new_width) // 2
    y_pos = (target_size[1] - new_height) // 2 + 50 # Slightly lower for "grounded" look
    
    # Composite
    final_image = Image.new("RGBA", target_size)
    final_image.paste(background, (0,0))
    final_image.paste(product_resized, (x_pos, y_pos), product_resized)
    
    return final_image.convert("RGB")

def main():
    print("="*50)
    print("   GOOGLE VERTEX AI CREATIVE STUDIO")
    print("="*50)
    
    init_google_cloud()
    
    # Setup folders
    OUTPUT_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(exist_ok=True)
    
    # Check for assets
    input_files = list(ASSETS_DIR.glob("*.*"))
    if not input_files:
        logging.error(f"❌ No images found in {ASSETS_DIR}. Please add a product photo.")
        return

    # Process just the first image found for this demo
    product_path = input_files[0]
    logging.info(f"📸 Processing Product: {product_path.name}")
    
    # Step 1: Clean the Product (Remove Background)
    clean_product = clean_product_image(product_path)
    
    captions = []
    
    # Step 2: Loop through Themes
    for i, theme in enumerate(config.CAMPAIGN_THEMES):
        logging.info(f"\n🚀 Job {i+1}: {theme['theme']}")
        
        # A. Get Creative Prompt from Gemini
        prompt = generate_prompt_with_gemini(clean_product, theme)
        
        # B. Generate Background with Imagen
        try:
            background_img = generate_background_with_imagen(prompt)
            
            # C. Composite
            final_asset = composite_images(background_img, clean_product)
            
            # Save
            filename = f"output_{i}_{theme['marketing_angle']}.png"
            save_path = OUTPUT_DIR / filename
            final_asset.save(save_path)
            
            captions.append(f"FILE: {filename}\nPROMPT: {prompt}\n")
            logging.info(f"✅ Saved: {filename}")
            
        except Exception as e:
            logging.error(f"❌ Generation failed for {theme['theme']}: {e}")

    # Final Summary
    with open(OUTPUT_DIR / "manifest.txt", "w") as f:
        f.write("\n".join(captions))
        
    print(f"\n🎉 Done! Check the '{OUTPUT_DIR}' folder.")

if __name__ == "__main__":
    main()