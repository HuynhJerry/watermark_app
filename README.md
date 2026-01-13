# 📸 NH Photography Watermark Tool

A lightweight, Python-based desktop application designed for photographers to batch watermark images efficiently. Features a modern dark-themed UI, drag-and-drop functionality, and smart scaling for both portrait and landscape orientations.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

* **Drag & Drop Interface:** Easily drag multiple images directly into the application window.
* **Batch Processing:** Watermark hundreds of photos in seconds.
* **Smart Scaling:** Automatically detects image orientation (Portrait vs. Landscape) and adjusts watermark size accordingly.
* **Position Control:** Choose between **Left**, **Center**, or **Right** alignment for your logo.
* **Format Support:** Supports `.jpg`, `.jpeg`, `.png`, and `.webp`.
* **Non-Destructive:** Saves new copies with `_wm` suffix, preserving your original files.
* **High-DPI Support:** Optimized for 2K/4K monitors on Windows.

## 🛠️ Prerequisites

To run this tool, you need **Python 3.6+** installed.

You also need the following dependencies:
* **Pillow** (Image processing)
* **tkinterdnd2** (Drag-and-drop support for GUI)

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/watermark-tool.git](https://github.com/yourusername/watermark-tool.git)
    cd watermark-tool
    ```

2.  **Install dependencies:**
    ```bash
    pip install Pillow tkinterdnd2
    ```

## ⚙️ Setup (Crucial Step)

Before running the app, you must place your transparent watermark logo files in the project root directory.

The application expects **three specific files** to exist in the same folder as the script:
1.  `watermark_left.png`
2.  `watermark_center.png`
3.  `watermark_right.png`

> **Tip:** You can use the same image file for all three, just copy and rename them. Ensure they are PNGs with transparent backgrounds.

## 🚀 Usage

1.  **Run the script:**
    ```bash
    python main.py
    ```
2.  **Add Images:** Drag and drop your photos into the dark grey zone, or click the **"➕ Add Images"** button.
3.  **Select Output Folder:** By default, it saves to a `Watermarked` folder on your Desktop. You can change this by clicking **"📂 Select Output Folder"**.
4.  **Choose Position:** Select **Left**, **Center**, or **Right**.
5.  **Apply:** Click **"✨ Apply Watermark"** and watch the progress bar!

## 📂 Project Structure

```text
watermark_app/
├── README.md
├── watermark.gui                # Main folder
    ├── watermark_gui.py         # The application source code
    ├── watermark_left.png       # (Required) Logo for left position
    ├── watermark_center.png     # (Required) Logo for center position
    ├── watermark_right.png      # (Required) Logo for right position
├── watermarked                  # Suggested export folder or you can choose any other folder to export
