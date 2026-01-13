import os
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image

# ---------- PATH SETUP ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- CONFIG ----------
WATERMARKS = {
    "left": os.path.join(BASE_DIR, "watermark_left.png"),
    "center": os.path.join(BASE_DIR, "watermark_center.png"),
    "right": os.path.join(BASE_DIR, "watermark_right.png")
}

MARGIN = 40
LANDSCAPE_SCALE = 0.06   # smaller, professional size
PORTRAIT_SCALE = 0.08
# ----------------------------

selected_images = []
last_opened_dir = None


# Default export folder
output_dir = r"D:\Code\watermark_app\watermarked"
os.makedirs(output_dir, exist_ok=True)


# ---------- FUNCTIONS ----------
def reset_app():
    selected_images.clear()
    update_status()


def drop_files(event):
    files = root.tk.splitlist(event.data)
    for f in files:
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            selected_images.append(f)
    update_status()


def select_images():
    global last_opened_dir

    files = filedialog.askopenfilenames(
        title="Select Images",
        initialdir=last_opened_dir,
        filetypes=[("Images", "*.jpg *.jpeg *.png")]
    )

    if files:
        last_opened_dir = os.path.dirname(files[0])
        selected_images.extend(files)
        update_status()


def select_output_folder():
    global output_dir
    output_dir = filedialog.askdirectory(
        title="Select Output Folder",
        initialdir=output_dir
    )
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        output_label.config(text=f"📁 {output_dir}")


def update_status():
    count = len(set(selected_images))
    status_label.config(text=f"🖼 {count} images ready")


def add_watermark(image_path, position):
    portrait_scale = PORTRAIT_SCALE
    landscape_scale = LANDSCAPE_SCALE
    base = Image.open(image_path).convert("RGBA")
    watermark = Image.open(WATERMARKS[position]).convert("RGBA")

    if position == "left" or position == "right":
        portrait_scale = portrait_scale * 1.2
        landscape_scale = landscape_scale * 1.2

    scale = portrait_scale if base.height > base.width else landscape_scale

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

    position = watermark_position.get()
    images = list(set(selected_images))
    total = len(images)

    progress["value"] = 0
    progress["maximum"] = total
    root.update_idletasks()

    processed = 0

    for i, img in enumerate(images, start=1):
        try:
            result = add_watermark(img, position)
            filename = os.path.basename(img)
            name, ext = os.path.splitext(filename)

            save_path = os.path.join(output_dir, f"{name}_wm{ext}")
            result.save(save_path, quality=95)

            processed += 1
            progress["value"] = i
            root.update_idletasks()

        except Exception as e:
            messagebox.showerror("Watermark Error", f"{img}\n\n{e}")
            return

    messagebox.showinfo(
        "Watermark Complete ✔",
        f"Successfully watermarked {processed} images.\n\nSaved to:\n{output_dir}"
    )

    # Open export folder (Windows)
    try:
        os.startfile(output_dir)
    except:
        pass

    reset_app()


# ---------- UI ----------
root = TkinterDnD.Tk()
root.title("NH Photography – Watermark Tool")
root.geometry("520x560")
root.configure(bg="#111111")
root.resizable(False, True)

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

output_label = Label(root, text=f"📁 {output_dir}",
                     fg="#aaaaaa", bg="#111111", wraplength=450)
output_label.pack()

Label(root, text="Watermark Position",
      fg="white", bg="#111111",
      font=("Segoe UI", 11, "bold")).pack(pady=10)

watermark_position = StringVar(value="center")
frame_pos = Frame(root, bg="#111111")
frame_pos.pack()

for text, value in [("Left", "left"), ("Center", "center"), ("Right", "right")]:
    Radiobutton(
        frame_pos, text=text, value=value,
        variable=watermark_position,
        fg="white", bg="#111111",
        selectcolor="#333333",
        activebackground="#111111"
    ).pack(side=LEFT, padx=15)

progress = ttk.Progressbar(
    root,
    orient="horizontal",
    length=420,
    mode="determinate"
)
progress.pack(pady=12)

Button(
    root,
    text="✨ Apply Watermark",
    width=25,
    height=2,
    bg="#ffffff",
    fg="#000000",
    font=("Segoe UI", 10, "bold"),
    command=apply_watermark
).pack(pady=15)

root.mainloop()
