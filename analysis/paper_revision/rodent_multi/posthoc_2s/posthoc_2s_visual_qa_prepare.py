"""POST HOC scientific-figure contact sheet for visual QA only."""
from pathlib import Path
import sys,json,math
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent.parent;sys.path.insert(0,str(ROOT/'pydeps'))
from PIL import Image,ImageDraw,PngImagePlugin
info=json.loads((OUT/'posthoc_2s_figures.json').read_text(encoding='utf-8'));n=len(info['figures']);cols=3;rows=math.ceil(n/cols)
canvas=Image.new('RGB',(2400,rows*620),'white');draw=ImageDraw.Draw(canvas)
for i,f in enumerate(info['figures']):
    im=Image.open(f['png']).convert('RGB');im.thumbnail((790,580));x=(i%cols)*800+(800-im.width)//2;y=(i//cols)*620+30
    canvas.paste(im,(x,y));draw.text(((i%cols)*800+8,(i//cols)*620+5),'POST HOC '+f['stem'],fill='black')
metadata=PngImagePlugin.PngInfo();metadata.add_text('Description',json.dumps(info));canvas.save(OUT/'posthoc_2s_QA_contact.png',pnginfo=metadata)
print('POST HOC figure contact sheet: '+str(OUT/'posthoc_2s_QA_contact.png'))
