from flask import Flask, request, send_file, render_template
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    uid = request.form['uid']
    ios_version = request.form['ios_version']
    amount = request.form['amount']
    product_name = request.form['product_name']

    # Create base image (375x600)
    img = Image.new('RGB', (375, 600), color=(10, 10, 10))  # dark gray background
    draw = ImageDraw.Draw(img)

    # Add gradient effect
    # for y in range(600):
    #     r = int(10 + y * 0.1)
    #     g = int(10 + y * 0.05)
    #     b = int(10 + y * 0.1)
    #     draw.line([(0, y), (375, y)], fill=(r, g, b))

    # Load and paste logo
    logo = Image.open('logo.png').convert("RGBA").resize((100, 100))
    img.paste(logo, (135, 20), logo)

    # Load font
    font_main = ImageFont.truetype("arial.ttf", 22)
    font_title = ImageFont.truetype("arial.ttf", 26)
    font_small = ImageFont.truetype("arial.ttf", 16)

    # Add Title
    draw.text((50, 120), "PURCHASE RECEIPT", font=font_title, fill="white")  # Moved 50px left

    # Draw a box around the info
    draw.rectangle((20, 170, 355, 420), outline="white", width=2)

    # Draw horizontal lines inside the box
    draw.line((25, 215, 350, 215), fill="white", width=1)
    draw.line((25, 265, 350, 265), fill="white", width=1)
    draw.line((25, 315, 350, 315), fill="white", width=1)

    # Write data
    draw.text((30, 180), f"UID: {uid}", font=font_main, fill='white')
    draw.text((30, 230), f"iOS Version: {ios_version}", font=font_main, fill='white')
    draw.text((30, 280), f"Amount Paid: ₦{amount}", font=font_main, fill='white')
    draw.text((30, 330), f"Item: {product_name}", font=font_main, fill='white')

    # Add footer
    draw.text((85, 450), "Thank you for your support!", font=font_small, fill='white')
    draw.text((85, 480), "Follow on tiktok @liamiosff", font=font_small, fill='gray')
    draw.text((85, 510), "Whatsapp +2349037933681", font=font_small, fill='gray')
    draw.text((95, 550), "LIAM H4X TEAM", font=font_main, fill='white')

    # Save to BytesIO
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='liamsale.png')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port))
