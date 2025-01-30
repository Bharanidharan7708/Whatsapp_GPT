from PIL import Image

# Open the image
image = Image.open("twilio.jpg")

# Resize while maintaining aspect ratio
new_size = (image.width // 2, image.height // 2)  # Adjust factor as needed
resized_image = image.resize(new_size, Image.ANTIALIAS)

# Save the resized image
resized_image.save("screenshot_resized.png")
