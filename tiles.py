from PIL import Image

names = [
    'ud', 'rl', 'rd', 'ur', 'dl', 'ul', 
    'b', 'w', 'a', 
    'urd', 'udl', 'url', 'rdl',
    'r', 'l', 'd', 'u',
]

tiles = []

for i in names:
    img = Image.new('RGB', (64, 64), (255, 255, 255, 0))
    hLine = Image.new('RGB', (64, 5), (0, 0, 0, 0))
    vLine = Image.new('RGB', (5, 64), (0, 0, 0, 0))
    if 'u' in i:
        img.paste(hLine, (0, 0))
    if 'd' in i:
        img.paste(hLine, (0, 59))
    if 'l' in i:
        img.paste(vLine, (0, 0))
    if 'r' in i:
        img.paste(vLine, (59, 0))
    if 'a' in i:
        img.paste(Image.new('RGB', (64, 64), (0, 0, 0, 0)), (0, 0))
    img.save(f"assets/{i}.png")
    tiles.append(img)
    