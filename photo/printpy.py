import requests
import tempfile
import os
import win32print
import win32ui
from PIL import Image, ImageWin

def download_image(url):
    """Download the image from the web and save it temporarily."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        with open(temp_file.name, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image downloaded to {temp_file.name}")
        return temp_file.name
    else:
        print("Failed to download image.")
        return None

def print_photo(photo_path):
    """Print the photo using win32print and Pillow."""
    # Get the default printer name
    printer_name = win32print.GetDefaultPrinter()
    print(f"Using printer: {printer_name}")

    # Load the photo using Pillow
    img = Image.open(photo_path)

    # Set up the printer device context (DC)
    printer_dc = win32ui.CreateDC()
    printer_dc.CreatePrinterDC(printer_name)

    # Get printer DPI and printable area
    printer_dpi_x = printer_dc.GetDeviceCaps(88)  # LOGPIXELSX
    printer_dpi_y = printer_dc.GetDeviceCaps(90)  # LOGPIXELSY
    printable_width = printer_dc.GetDeviceCaps(8)  # HORZRES
    printable_height = printer_dc.GetDeviceCaps(10)  # VERTRES

    # Scale the image to fit within the printable area while maintaining aspect ratio
    img_width, img_height = img.size
    scale_x = printable_width / img_width
    scale_y = printable_height / img_height
    scale = min(scale_x, scale_y)

    target_width = int(img_width * scale)
    target_height = int(img_height * scale)
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

    # Center the image
    x_offset = (printable_width - target_width) // 2
    y_offset = (printable_height - target_height) // 2
    x0, y0 = x_offset, y_offset
    x1, y1 = x0 + target_width, y0 + target_height

    # Start the print job
    printer_dc.StartDoc("Photo Print")
    printer_dc.StartPage()

    # Render the image onto the printer DC
    dib = ImageWin.Dib(img)
    dib.draw(printer_dc.GetHandleOutput(), (x0, y0, x1, y1))

    # End the print job
    printer_dc.EndPage()
    printer_dc.EndDoc()

    # Cleanup
    printer_dc.DeleteDC()
    print(f"Photo printed successfully from {photo_path}.")

