import serial
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import PIL.ImageChops
import PIL.ImageOps
from time import sleep
import struct


COM_PORT = "COM11"
BAUDRATE = 9600
PRINTER_WIDTH = 384


def initialize_printer(soc):
    soc.write(b"\x1b\x40")


def get_printer_status(soc):
    soc.write(b"\x1e\x47\x03")
    return soc.read(38)


def get_printer_serial_number(soc):
    soc.write(b"\x1D\x67\x39")
    return soc.read(21)


def get_printer_product_info(soc):
    soc.write(b"\x1d\x67\x69")
    return soc.read(16)


def send_start_print_sequence(soc):
    soc.write(b"\x1d\x49\xf0\x19")


def send_end_print_sequence(soc):
    soc.write(b"\x0a\x0a\x0a\x0a")


def trim_image(im):
    bg = PIL.Image.new(im.mode, im.size, (255, 255, 255))
    diff = PIL.ImageChops.difference(im, bg)
    diff = PIL.ImageChops.add(diff, diff, 2.0)
    bbox = diff.getbbox()

    if bbox:
        return im.crop((bbox[0], bbox[1], bbox[2], bbox[3] + 10))

    return im


def get_wrapped_text(text, font, line_length):
    lines = [""]

    for word in text.split():
        line = f"{lines[-1]} {word}".strip()

        if font.getlength(line) <= line_length:
            lines[-1] = line
        else:
            lines.append(word)

    return "\n".join(lines)


def create_text(text, font_name="arial.ttf", font_size=32):
    img = PIL.Image.new("RGB", (PRINTER_WIDTH, 5000), color=(255, 255, 255))

    try:
        font = PIL.ImageFont.truetype(font_name, font_size)
    except:
        font = PIL.ImageFont.load_default()

    d = PIL.ImageDraw.Draw(img)

    lines = []
    for line in text.splitlines():
        lines.append(get_wrapped_text(line, font, PRINTER_WIDTH))

    lines = "\n".join(lines)
    d.text((0, 0), lines, fill=(0, 0, 0), font=font)

    return trim_image(img)


def print_image(soc, im):
    if im.width > PRINTER_WIDTH:
        height = int(im.height * (PRINTER_WIDTH / im.width))
        im = im.resize((PRINTER_WIDTH, height))

    if im.width < PRINTER_WIDTH:
        padded_image = PIL.Image.new("1", (PRINTER_WIDTH, im.height), 1)
        padded_image.paste(im)
        im = padded_image

    im = im.rotate(180)

    if im.mode != "1":
        im = im.convert("1")

    if im.size[0] % 8:
        im2 = PIL.Image.new(
            "1",
            (im.size[0] + 8 - im.size[0] % 8, im.size[1]),
            "white"
        )
        im2.paste(im, (0, 0))
        im = im2

    im = PIL.ImageOps.invert(im.convert("L"))
    im = im.convert("1")

    buf = b"".join((
        bytearray(b"\x1d\x76\x30\x00"),
        struct.pack("2B", int(im.size[0] / 8 % 256), int(im.size[0] / 8 / 256)),
        struct.pack("2B", int(im.size[1] % 256), int(im.size[1] / 256)),
        im.tobytes()
    ))

    initialize_printer(soc)
    sleep(0.5)

    send_start_print_sequence(soc)
    sleep(0.5)

    soc.write(buf)
    sleep(0.5)

    send_end_print_sequence(soc)
    sleep(0.5)


def main():
    print("Verbinde mit Drucker auf", COM_PORT)

    with serial.Serial(COM_PORT, baudrate=BAUDRATE, timeout=2) as s:
        sleep(1)

        print("Status:", get_printer_status(s))
        sleep(0.5)

        print("Serial:", get_printer_serial_number(s))
        sleep(0.5)

        print("Info:", get_printer_product_info(s))
        sleep(0.5)

        # Bild drucken
        # img = PIL.Image.open("Turtle.jpg")

        # Text drucken
        img = create_text(
            "YHK / TEDi Thermodrucker\nWindows Testdruck\nCOM11 funktioniert!",
            font_size=36
        )

        print_image(s, img)

    print("Fertig.")


if __name__ == "__main__":
    main()