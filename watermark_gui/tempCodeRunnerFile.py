import os
from tkinter import *
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image

# ---------- CONFIG ----------
WATERMARKS = {
    "left": "watermark_left.png",
    "center": "watermark_center.png",
    "right": "watermark_right.png"
}

MARGIN = 40
LANDSCAPE_SCALE = 0.18
PORTRAIT_SCALE = 0.25
# ----------------------------

selected_images = []
output_dir = ""


def drop_files(event):
    files = root.tk.splitlist(event.data)
    for f in files:
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            selected_images.append(f)
    update_status()


def select_images():
    files = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Images", "*.jpg *.jpeg *.png")]
    )
    selected_images.extend(files)
    update_status()


def select_output_folder():
    global output_dir
    output_dir = filedialog.askdirectory(title="Select Output Folder")
    output_label.config(text=f"📁 {output_dir}" if output_dir else "No output folder selected")


def update_status():
    count = len(set(selected_images))
    status_label.config(text=f"🖼 {count} images ready")


def add_watermark(image_path, position):
    base = Image.open(image_path).convert("RGBA")
    watermark = Image.open(WATERMARKS[position]).convert("RGBA")

    # Auto-detect orientation
    scale = PORTRAIT_SCALE if base.height > base.width else LANDSCAPE_SCALE

    wm_width = int(base.width * scale)
    ratio = wm_width / watermark.width
    wm_height = int(watermark.height * ratio)
    watermark = watermark.resize((wm_width, wm_height), Image.LANCZOS)

    if position == "left":
        x = MARGIN
    elif position == "center":
        x = (base.width - wm_width) // 2
    else:
        x = base.width - wm_width - MARGIN

    y = base.height - wm_height - MARGIN

    layer = Image.new("RGBA", base.size)
    layer.paste(base, (0, 0))
    layer.paste(watermark, (x, y), watermark)

    return layer.convert("RGB")


def apply_watermark():
    if not selected_images:
        messagebox.showerror("Error", "No images selected")
        return

    if not output_dir:
        messagebox.showerror("Error", "Please select an output folder")
        return

    position = watermark_position.get()
    processed = 0

    for img in set(selected_images):
        result = add_watermark(img, position)
        filename = os.path.basename(img)
        result.save(os.path.join(output_dir, filename), quality=95)
        processed += 1

    messagebox.showinfo(
        "Watermark Complete ✔",
        f"Successfully watermarked {processed} images."
    )


# ---------- UI ----------
root = TkinterDnD.Tk()
root.title("NH Photography – Watermark Tool")
root.geometry("520x420")
root.configure(bg="#111111")
root.resizable(False, False)

FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_TEXT = ("Segoe UI", 10)

Label(root, text="NH Photography Watermark Tool",
      fg="white", bg="#111111", font=FONT_TITLE).pack(pady=15)

drop_zone = Label(
    root,
    text="Drag & Drop Images Here\nor click 'Add Images'",
    fg="#cccccc",
    bg="#1c1c1c",
    font=FONT_TEXT,
    width=45,
    height=6,
    relief="ridge"
)
drop_zone.pack(pady=10)
drop_zone.drop_target_register(DND_FILES)
drop_zone.dnd_bind("<<Drop>>", drop_files)

Button(root, text="➕ Add Images",
       width=20, command=select_images).pack(pady=5)

status_label = Label(root, text="No images selected",
                     fg="#aaaaaa", bg="#111111")
status_label.pack(pady=5)

Button(root, text="📂 Select Output Folder",
       width=25, command=select_output_folder).pack(pady=8)

output_label = Label(root, text="No output folder selected",
                     fg="#aaaaaa", bg="#111111", wraplength=450)
output_label.pack()

Label(root, text="Watermark Position",
      fg="white", bg="#111111", font=("Segoe UI", 11, "bold")).pack(pady=10)

watermark_position = StringVar(value="center")
frame_pos = Frame(root, bg="#111111")
frame_pos.pack()

for text, value in [("Left", "left"), ("Center", "center"), ("Right", "right")]:
    Radiobutton(frame_pos, text=text, value=value,
                variable=watermark_position,
                fg="white", bg="#111111",
                selectcolor="#333333",
                activebackground="#111111").pack(side=LEFT, padx=15)

Button(root, text="✨ Apply Watermark",
       width=25, height=2,
       bg="#ffffff", fg="#000000",
       font=("Segoe UI", 10, "bold"),
       command=apply_watermark).pack(pady=20)

root.mainloop()
