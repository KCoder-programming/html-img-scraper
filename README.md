# Download Images – Image to PDF Scraper
A Python utility to fetch images from a webpage, preview them in a GUI, and export them as a single PDF.

This project is a lightweight Image-to-PDF scraper that lets you paste a webpage URL, automatically fetch all images, preview them inside the app, and save them either individually or combined into a single PDF.

It’s designed for students and professionals who want to download notes, diagrams, or slides quickly and organize them neatly.

## Features
- 🔗 Fetch all images from a web page.
- 🖼️ Preview downloaded images inside the GUI.
- 📂 Save images locally.
- 📑 Export all images into a single PDF.
- 🎨 Clean and modern UI (using ttkbootstrap).

---

## Installation
- Clone the repository or download the source code.
  ```bash
  git clone https://github.com/KCoder-programming/html-img-scraper.git
  cd html-img-scraper
  ```

- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Run the app:
```bash
python download_images.py
```

## Requirements
- beautifulsoup4
- requests
- Pillow
- tqdm
- ttkbootstrap
- python 3.x

(given in [requirements.txt](https://github.com/KCoder-programming/html-img-scraper/blob/main/requirements.txt))

## Usage
1. Enter the URL of a page containing images.

2. Click Fetch Images → the images will be listed and previewed.

3. Select images you want to save/export.

4. Choose Export as PDF to create a clean PDF document.

---

## License:
[MIT License](https://github.com/KCoder-programming/html-img-scraper/blob/main/LICENSE)

Copyright (c) 2025 KCoder-programming
