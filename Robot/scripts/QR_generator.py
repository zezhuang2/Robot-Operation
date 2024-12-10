#!/usr/bin/env python
import qrcode
from PIL import Image, ImageDraw, ImageFont

# Data to encode in the QR code
name = "PCBA Mount"
data = f"{name}.script\n9.5\n3\n86.75"

# Create a QR code instance
qr = qrcode.QRCode(
    version=1,  # controls the size of the QR code
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # controls error correction used
    box_size=10,  # size of each box in the QR code grid
    border=1.5,  # thickness of the border
)

# Add the data to the QR code
qr.add_data(data)
qr.make(fit=True)

# Create an image from the QR code
img = qr.make_image(fill="black", back_color=(173, 216, 230))
text = data

# Load a font
# You can use ImageFont.truetype() to load custom fonts if desired
font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf",size=20)

# Calculate the size of the image with the text included
qr_width, qr_height = img.size
bbox = font.getbbox(text)
font_width = bbox[2] - bbox[0]-80
font_height = bbox[3] - bbox[1]
total_height = qr_height + font_height + 60  # Adding some padding (10px)
combined_img = Image.new("RGB", (qr_width, total_height), (173, 216, 230))
combined_img.paste(img, (0, 0))
draw = ImageDraw.Draw(combined_img)
text_position = ((qr_width - font_width) // 2, qr_height - 10)  # Center the text
draw.text(text_position, text, font=font, fill="black")
combined_img.save(f"C:\\Users\\ZeZhuang\\UR3\\QRCode\\{name}.png")
#combined_img.show()
