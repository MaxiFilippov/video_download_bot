from PIL import Image, ImageDraw, ImageFont
import textwrap
import aiohttp

def draw_multiple_line_text(image, text, font, text_color, text_start_height):
    
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=17)
    for line in lines:
        line_width = font.getsize(line)[0]
        line_height = 100
        draw.text(((image_width - line_width) / 2, y_text), 
                  line, font=font, fill=text_color)
        y_text += line_height


def make_thumbnail(title):
    
    image = Image.new('RGB', (600, 600), color = (0, 0, 0))
    fontsize = 60  # starting font size
    font = ImageFont.truetype("NotoSerifKR-Black.otf", fontsize)
    text = title  
    print(len(text))
    if len(text) > 69:
        text = text[:69] + "..."
    text_color = (255, 255, 255)
    text_start_height = 0
    draw_multiple_line_text(image, text, font, text_color, text_start_height)
    #draw_multiple_line_text(image, text2, font, text_color, 400)
    image.save(f'{title}.jpeg')
    return f'{title}.jpeg'
  

async def make_ydl_thumbnail(url, title):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                img =  await resp.read()
                with open(f"{title}.jpeg", "wb") as f:
                    f.write(img)
                return f"{title}.jpeg"
            else:
                return None    