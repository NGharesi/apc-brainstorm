from pathlib import Path
import sys,json
ROOT=Path(r'C:\Users\nghare\.brainstorm\process');OUT=ROOT/'revision_checks/rodent_multi';sys.path.insert(0,str(ROOT/'pydeps'))
from PIL import Image,ImageOps,ImageDraw,PngImagePlugin
info=json.loads((OUT/'regional_figures.json').read_text(encoding='utf-8'))
canvas=Image.new('RGB',(1600,5*490),'white');draw=ImageDraw.Draw(canvas)
for i,f in enumerate(info['figures']):
    picture=Image.open(f['png']).convert('RGB');picture.thumbnail((790,450));x=(i%2)*800+(800-picture.width)//2;y=(i//2)*490+28
    canvas.paste(picture,(x,y));draw.text(((i%2)*800+12,(i//2)*490+5),f['stem'],fill='black')
pngmeta=PngImagePlugin.PngInfo();pngmeta.add_text('Description',json.dumps(info))
canvas.save(OUT/'regional_QA_contact.png',pnginfo=pngmeta)
print(str(OUT/'regional_QA_contact.png'))
