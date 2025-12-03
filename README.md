# 🎨🤖 The AI Creative Studio (Auto-Creative Engine)

> **Turn one product shot + one logo into a full ad campaign in seconds.**

The **Auto-Creative Engine** is an automated AI-powered marketing creative generator.
Feed it a product photo and brand logo, and it builds a full multi-variation ad campaign—complete with imagery, captions, and export-ready bundles.

---

## 1. 🌍 Overview

Creative fatigue is the #1 killer of digital ad performance.
Brands need **fresh, on-brand visuals every single day**, but:

* Designers spend *80 percent of their time* on repetitive tasks.
* Creative teams become bottlenecks in performance marketing.
* Scaling experiments across platforms, geos, and audiences becomes painfully slow.

**This engine fixes that.**

You provide:

* **Product image** (shoe, watch, perfume, gadget, anything)
* **Brand logo**

The system automatically generates:

* **10+ high-definition ad creatives**
* **Consistent logo placement across all images**
* **Punchy AI-written captions**
* **A ready-to-upload `campaign_output.zip`**

---

## 2. 📦 What the User Gets

### **Input**

A folder containing:

```
product.jpg
logo.png   (transparent recommended)
```

### **Action**

Run:

```bash
python main.py
```

### **Output**

A single zipped campaign package:

```
campaign_output.zip
├── creatives/        (10+ unique HD ads)
├── captions.txt      (1 caption per creative)
└── metadata.json     (optional — concept → image → caption mapping)
```

Creatives include variations such as:

* Neon cyberpunk cityscapes
* Mars surface sci-fi scenes
* Luxury marble podiums
* Minimal studio shots
* Streetwear alley aesthetics

**Compatible with:**

* Meta Ads (FB/IG)
* Google Display
* TikTok / X / LinkedIn
* Landing pages, banners, email headers

---

## 3. 🧠 System Design & Approach

The architecture follows one principle:

> **AI handles creativity. Code ensures brand consistency.**

Pure image models are unreliable for logo fidelity—so the system uses a hybrid **GenAI + deterministic pipeline**.

---

### 3.1 🔺 High-Level Flow

#### **1. Creative Director (LLM – Gemini 1.5 Flash)**

* Takes product + brand vibe
* Brainstorms ~10 visual concepts
* Outputs structured prompts

**Example prompts:**

* “Futuristic Neon City at Night”
* “Mars Surface With Dust Storm”
* “Luxury Marble Podium With Soft Studio Light”

---

#### **2. The Artist (Imagen 3.0 / Gemini 2.0 Flash Experimental)**

Generates images from the prompts.
Output: Base creative images (no logo).

---

#### **3. The Enforcer (Python + Pillow)**

The model is *not* asked to draw the logo.
Instead, Python:

* Resizes logo
* Positions it consistently
* Applies transparency, margins, styling
* Overlays pixel-perfect logo on all creatives

Ensures **brand integrity** across all outputs.

---

#### **4. The Copywriter (LLM)**

For each creative:

* Generates a short, punchy ad caption
* Outputs `captions.txt`

---

#### **5. The Packager (Zip Orchestrator)**

Bundles everything into:

```
campaign_output.zip
```

---

## 4. 🧩 Tech Stack

**Language:**

* Python 3.12

**GenAI SDK:**

* `google-genai` (v1alpha/v1beta)

**Models:**

* **Gemini 1.5 Flash** — concept generation, copywriting
* **Imagen 3.0** — primary image generation
* **Gemini 2.0 Flash (Experimental)** — fallback generator

**Image Processing:**

* Pillow (PIL)

**Packaging:**

* Python `zipfile`, `os`, `pathlib`

---

## 5. 🔒 Reliability & Brand Safety

### 5.1 Model Quotas & Availability

**Problem:**
Imagen APIs may hit:

* Quota limits
* Temporary downtime
* Billing restrictions during demos

**Solution:**
Automatic fallbacks:

1. Try Imagen 3.0
2. If it fails → use Gemini 2.0 Flash Experimental image generator

Ensures the engine **never hard-crashes**.

---

### 5.2 Brand Integrity (The Garbled Logo Problem)

**Problem:**
LLMs and image models distort logos:

* warped shapes
* wrong symbols
* unreadable marks

**Solution:**
Never ask the model to draw the logo.

**AI handles art.
Python handles the brand.**

This split is essential for production marketing use cases.

---

## 6. 📁 Suggested Folder Structure

```
.
├── main.py
├── prompts.py
├── generators/
│   ├── concepts.py
│   ├── images.py
│   └── captions.py
├── utils/
│   ├── logo_overlay.py
│   └── packaging.py
├── assets/
│   ├── product.jpg
│   └── logo.png
└── output/
    └── campaign_output.zip
```

Your repo may differ — this is the recommended clean layout.

---

## 7. 🚀 How to Run

### 7.1 Clone the Repo

```bash
git clone https://github.com/malina1410/GTHackathon.git
cd GTHackathon
```

### 7.2 Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
```

### 7.3 Install Dependencies

```bash
pip install google-genai pillow
```

Or:

```bash
pip install -r requirements.txt
```

### 7.4 Configure API Key

Get from Google AI Studio.

**Environment variable (recommended):**

```bash
export GOOGLE_API_KEY="your_key_here"
# Windows:
set GOOGLE_API_KEY="your_key_here"
```

Or hardcode inside `main.py`:

```python
GOOGLE_API_KEY = "your_key_here"
```

Place product and logo images in `assets/`.

---

### 7.5 Run the Engine

```bash
python main.py
```

You’ll see logs like:

```
[Creative Director] Generated 10 visual concepts.
[Artist] Creating variation 1/10 ...
[Enforcer] Logo applied to variation_1.png
[Copywriter] Writing caption 1/10 ...
[Packager] campaign_output.zip created ✓
```

Final output inside `output/`.

---

## 8. 🖼️ Visual Proof (Add Your Screenshots)

Replace this section once you have assets.

Suggested screenshots:

1. **Product + Logo input**
2. **Terminal logs during generation**
3. **Grid of 10 creatives with logo overlays**
4. **Excerpt from captions.txt**

---

## 9. 🚧 Future Improvements

Potential extensions:

* Auto-resizing for multiple platforms (1:1, 4:5, 9:16, 1.91:1)
* A/B variant generator around a single theme
* Palette matching with brand colors
* Web UI (Streamlit / React) for marketers
* Bulk product batch generation
