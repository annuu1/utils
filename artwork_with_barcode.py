import barcode
from barcode.writer import SVGWriter
import svgwrite
from io import BytesIO

def generate_barcode_with_text(code: str, vendor_code: str, product_name: str, filename: str):
    # Generate barcode in memory
    EAN = barcode.get_barcode_class('code128')  # You can change this to 'code128', 'isbn13', etc.
    ean = EAN(code, writer=SVGWriter())
    
    barcode_svg_io = BytesIO()
    ean.write(barcode_svg_io)
    
    # Write the barcode to a temporary SVG file
    barcode_filename = f"{filename}_barcode.svg"
    with open(barcode_filename, 'wb') as f:
        f.write(barcode_svg_io.getvalue())
    
    # Create a new SVG drawing
    dwg = svgwrite.Drawing(filename=f"{filename}.svg", profile='tiny', size=("70mm", "40mm"))

    # Add a black rectangle outline around the artwork
    dwg.add(dwg.rect(insert=(0, 0), size=("70mm", "40mm"), fill='none', stroke='black', stroke_width=1))

    # Embed the barcode SVG as an image within the main SVG
    dwg.add(dwg.image(href=barcode_filename, insert=(60, 50), size=("30mm", "10mm")))

    # Add vendor code text above the barcode
    dwg.add(dwg.text(vendor_code, insert=(10, 140), fill='black', font_size='14px', font_family='Arial'))
    dwg.add(dwg.text('H1-24', insert=(100, 140), fill='black', font_size='14px', font_family='Arial'))

    # Add product name text and rotate it 90 degrees
    dwg.add(dwg.text(product_name, insert=(60, 50), fill='black', font_size='14px', font_family='Arial', transform="rotate(90, 60, 20)"))

    # Save the final SVG artwork
    dwg.save()

# Usage example
generate_barcode_with_text('123456789012', 'Vendor123', 'ProductName', 'artwork')
