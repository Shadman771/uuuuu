import qrcode

# Bangla text
bangla_text = "Shilon Bangla QR Created __ (শিলন বাংলা কিউআর তৈরি করা হয়েছে)"

# Create QR code instance
qr = qrcode.QRCode(
    version=1,  # controls the size of the QR Code
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Add data to the QR code
qr.add_data(bangla_text)
qr.make(fit=True)

# Create an image from the QR Code instance
img = qr.make_image(fill='black', back_color='white')

# Save the image
img.save("bangla_qr_code.png")

print("QR code generated and saved as 'bangla_qr_code.png'")
