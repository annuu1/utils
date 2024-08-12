import barcode
from barcode.writer import SVGWriter
import svgwrite
from io import BytesIO

def generate_barcode_with_text(code: str, text: str, filename: str):
    # Generate barcode in memory
    EAN = barcode.get_barcode_class('ean13')  # You can change this to 'code128', 'isbn13', etc.
    ean = EAN(code, writer=SVGWriter())
    
    barcode_svg_io = BytesIO()
    ean.write(barcode_svg_io)
    
    # Write the barcode to a temporary SVG file
    barcode_filename = f"{filename}_barcode.svg"
    with open(barcode_filename, 'wb') as f:
        f.write(barcode_svg_io.getvalue())
    
    # Create a new SVG drawing
    dwg = svgwrite.Drawing(filename=f"{filename}.svg", profile='tiny')
    
    # Embed the barcode SVG as an image within the main SVG
    dwg.add(dwg.image(href=barcode_filename, insert=(10, 10), size=("150px", "50px")))
    
    # Add text below the barcode
    dwg.add(dwg.text(text, insert=(10, 100), fill='black', font_size='20px', font_family='Arial'))

    # Save the final SVG artwork
    dwg.save()

# Usage example
generate_barcode_with_text('123456789012', 'My Artwork Text', 'artwork')
