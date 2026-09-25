import os
from PIL import Image, ImageDraw, ImageFont

def generate_assets():
    size = 1024
    
    # 1. Base image for favicons (squircle with transparent background)
    img_squircle = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw_sq = ImageDraw.Draw(img_squircle)
    radius = int(size * 0.22)
    bg_color = (17, 17, 17, 255)
    border_color = (51, 51, 56, 255)
    draw_sq.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=bg_color)
    draw_sq.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, outline=border_color, width=4)
    
    # 2. Base image for Apple Touch Icon (full bleed square background - iOS applies its own squircle mask)
    img_apple = Image.new("RGBA", (size, size), bg_color)
    draw_apple = ImageDraw.Draw(img_apple)
    
    font_path = "/System/Library/Fonts/Menlo.ttc"
    font_size = int(size * 0.50)
    font = ImageFont.truetype(font_path, font_size, index=1) # Menlo Bold
    
    text = "TK"
    bbox = draw_sq.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (size - text_w) / 2 - bbox[0]
    y = (size - text_h) / 2 - bbox[1]
    
    # Draw white text on both
    draw_sq.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    draw_apple.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    
    # Save standard raster sizes
    targets_squircle = {
        "favicon-512x512.png": 512,
        "favicon-192x192.png": 192,
        "favicon-96x96.png": 96,
        "favicon-48x48.png": 48,
        "favicon-32x32.png": 32,
        "favicon-16x16.png": 16,
    }
    
    for filename, s in targets_squircle.items():
        resized = img_squircle.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(filename, "PNG", optimize=True)
        print(f"Generated {filename} ({s}x{s})")
        
    # Apple Touch Icon: 180x180 full bleed
    apple_resized = img_apple.resize((180, 180), Image.Resampling.LANCZOS)
    apple_resized.save("apple-touch-icon.png", "PNG", optimize=True)
    print("Generated apple-touch-icon.png (180x180 full bleed)")
        
    # Multi-resolution favicon.ico containing 16x16, 32x32, 48x48
    ico_sizes = [(16, 16), (32, 32), (48, 48)]
    img_squircle.save("favicon.ico", format="ICO", sizes=ico_sizes)
    print("Generated favicon.ico (16, 32, 48)")

    # Vector favicon.svg
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="28" fill="#111111"/>
  <rect x="0.5" y="0.5" width="127" height="127" rx="27.5" fill="none" stroke="#333338" stroke-width="1"/>
  <text x="64" y="67" dominant-baseline="central" text-anchor="middle" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace" font-size="62" font-weight="700" fill="#ffffff" letter-spacing="-1">TK</text>
</svg>
"""
    with open("favicon.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("Generated favicon.svg")

    # site.webmanifest
    manifest_content = """{
  "name": "Tyler 'TK' Koshakow",
  "short_name": "TK",
  "icons": [
    {
      "src": "/favicon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/favicon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "theme_color": "#111111",
  "background_color": "#111111",
  "display": "standalone"
}
"""
    with open("site.webmanifest", "w", encoding="utf-8") as f:
        f.write(manifest_content)
    print("Generated site.webmanifest")

if __name__ == "__main__":
    generate_assets()
