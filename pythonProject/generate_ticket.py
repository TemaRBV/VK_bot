from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
import random
import bs4
import requests

image_path = 'Files/Ticket.png'
font_path = 'Files/Roboto-Regular.ttf'


def generate_ticket(name, email):
    # get an image
    with Image.open(image_path).convert("RGBA") as base:
        # get a font
        font_1 = ImageFont.truetype(font_path, 40)
        font_2 = ImageFont.truetype(font_path, 30)
        # get a drawing context
        draw = ImageDraw.Draw(base)

        # draw text
        draw.text((1100, 100), name, font=font_1, fill=(42, 47, 60, 255))
        draw.text((1100, 430), email, font=font_2, fill=(42, 47, 60, 255))

        html = requests.get('https://avatarzo.ru/tag/animals/').text
        bs_html = bs4.BeautifulSoup(html, features='html.parser')
        list_of_tags = bs_html.find_all('img')
        list_of_tags.pop(-1)
        list_of_res = []
        for tag in list_of_tags:
            res = tag.get('srcset')
            list_res = res.split(' ')
            res = list_res[-2]
            list_of_res.append(res)

        response = random.choice(list_of_res)
        res_get = requests.get(response)
        avatar_file = BytesIO(res_get.content)
        avatar = Image.open(avatar_file)
        base.paste(avatar, (173, 40))

        temp = BytesIO()
        base.save(temp, 'png')
        temp.seek(0)

        return temp




