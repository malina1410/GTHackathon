"""
Configuration & Creative Strategy
---------------------------------
This file defines the 'Creative Director' persona for Gemini.
"""
import os

# Google Cloud Settings
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

# Image Generation Settings
IMAGEN_MODEL = "imagen-3.0-generate-001" 
ASPECT_RATIO = "1:1"

# Creative Strategy
# Gemini will use these themes to invent specific prompts for your uploaded product.
CAMPAIGN_THEMES = [
    {
        "theme": "Neo-Tokyo Cyberpunk",
        "mood": "Futuristic, Neon, High Contrast, Wet Surface reflections",
        "marketing_angle": "Innovation"
    },
    {
        "theme": "Organic Minimalism",
        "mood": "Soft sunlight, beige stone textures, Japandi style, shadows",
        "marketing_angle": "Simplicity"
    },
    {
        "theme": "Midnight Luxury",
        "mood": "Black marble, gold rim lighting, floating, expensive, bokeh",
        "marketing_angle": "Exclusivity"
    }
]

# The System Instruction for Gemini (The "Prompt Engineer" Persona)
PROMPT_GENERATION_INSTRUCTIONS = """
You are an expert AI Prompt Engineer for product photography. 
Your goal is to write a structured prompt for a text-to-image model (Imagen 3).
I will give you an image of a product and a 'Theme'.

You must output ONLY the prompt text. Follow this structure:
"[Subject Description], [Environment/Background], [Lighting], [Camera Angle], [Style/Render Engine]"

Rules:
1. Keep the subject description minimal (e.g., "The perfume bottle").
2. Focus heavily on the environment and lighting to match the requested Theme.
3. Use keywords like "8k", "photorealistic", "octane render", "softbox lighting".
4. Do not include introductory text like "Here is the prompt".
"""
