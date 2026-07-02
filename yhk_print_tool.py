import serial
import struct
from time import sleep
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops
import qrcode

COM_PORT = "COM11"
BAUDRATE = 9600
PRINTER_WIDTH = 384


def trim_image(im):
    bg = Image.new(im.mode, im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        return im.crop((bbox[0], bbox[1], bbox[2], bbox[3] + 20))
    return im


def create_text_image(text, font_size=32):
    img = Image.new("RGB", (PRINTER_WIDTH, 3000), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    y = 0

    for raw_line in text.splitlines():
        line = ""

        for word in raw_line.split():
            test = (line + " " + word).strip()

            if draw.textlength(test, font=font) < PRINTER_WIDTH:
                line = test
            else:
                draw.text((0, y), line, fill="black", font=font)
                y += font_size + 8
                line = word

        draw.text((0, y), line, fill="black", font=font)
        y += font_size + 10

    return trim_image(img)


def create_qr_image(text):
    qr = qrcode.QRCode(
        version=1,
        box_size=8,
        border=2
    )

    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img = img.resize((300, 300))

    canvas = Image.new("RGB", (PRINTER_WIDTH, 340), "white")
    canvas.paste(img, ((PRINTER_WIDTH - img.width) // 2, 10))

    return canvas


def print_image(im):
    if im.width > PRINTER_WIDTH:
        h = int(im.height * (PRINTER_WIDTH / im.width))
        im = im.resize((PRINTER_WIDTH, h))

    if im.width < PRINTER_WIDTH:
        padded = Image.new("RGB", (PRINTER_WIDTH, im.height), "white")
        padded.paste(im, ((PRINTER_WIDTH - im.width) // 2, 0))
        im = padded

    im = im.rotate(180)
    im = im.convert("1")
    im = ImageOps.invert(im.convert("L")).convert("1")

    buf = b"".join((
        b"\x1d\x76\x30\x00",
        struct.pack("2B", int(im.width / 8 % 256), int(im.width / 8 / 256)),
        struct.pack("2B", int(im.height % 256), int(im.height / 256)),
        im.tobytes()
    ))

    with serial.Serial(COM_PORT, baudrate=BAUDRATE, timeout=2) as s:
        sleep(1)
        s.write(b"\x1b\x40")
        sleep(0.3)
        s.write(b"\x1d\x49\xf0\x19")
        sleep(0.3)
        s.write(buf)
        sleep(0.3)
        s.write(b"\x0a\x0a\x0a\x0a")
        sleep(0.3)


def get_input():
    text = input_box.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning("Fehler", "Bitte Text eingeben.")
        return None

    return text


def print_text():
    text = get_input()

    if text:
        print_image(create_text_image(text))
        messagebox.showinfo("Fertig", "Text gedruckt.")


def print_qr():
    text = get_input()

    if text:
        print_image(create_qr_image(text))
        messagebox.showinfo("Fertig", "QR-Code gedruckt.")


root = tk.Tk()
root.title("YHK / TEDi Print Tool")
root.geometry("420x310")

tk.Label(root, text="Text / QR-Code Inhalt:").pack(pady=8)

input_box = tk.Text(root, height=8, width=45)
input_box.pack(padx=10)

tk.Button(root, text="Text drucken", command=print_text, height=2).pack(fill="x", padx=20, pady=5)
tk.Button(root, text="QR-Code drucken", command=print_qr, height=2).pack(fill="x", padx=20, pady=5)

tk.Label(root, text=f"Drucker-Port: {COM_PORT}").pack(pady=8)

root.mainloop()