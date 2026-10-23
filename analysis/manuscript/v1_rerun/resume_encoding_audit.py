from pathlib import Path
import ast,json,unicodedata
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT/'apc-brainstorm-publish';D=Path(__file__).resolve().parent
scripts=list(REPO.rglob('*.py'))+list(D.glob('*.py'))
audit=[]
for p in scripts:
    s=p.read_text(encoding='utf-8');b=s.encode('utf-8')
    for offset,byte in enumerate(b):
        if byte==0x9d:
            context=b[max(0,offset-24):offset+24].decode('utf-8',errors='replace')
            audit.append({'path':str(p),'byte_offset':offset,'byte_hex':'9d','context':context})
    tree=ast.parse(s);lines=s.splitlines(keepends=True);positions=[];start=[0]
    for line in lines:start.append(start[-1]+len(line))
    for n in ast.walk(tree):
        if not isinstance(n,ast.Call):continue
        f=n.func;name=f.attr if isinstance(f,ast.Attribute) else f.id if isinstance(f,ast.Name) else ''
        if name not in ['read_text','write_text','open','check_output','run']:continue
        if any(k.arg=='encoding' for k in n.keywords):continue
        needs=name in ['read_text','write_text']
        if name=='open':
            mode=n.args[0] if isinstance(f,ast.Attribute) and n.args else n.args[1] if len(n.args)>1 else None
            mode_kw=next((k.value for k in n.keywords if k.arg=='mode'),None)
            if mode_kw is not None:mode=mode_kw
            needs=mode is None or (isinstance(mode,ast.Constant) and isinstance(mode.value,str) and 'b' not in mode.value)
        if name in ['check_output','run']:
            needs=any(k.arg in ['text','universal_newlines'] and isinstance(k.value,ast.Constant) and k.value.value is True for k in n.keywords)
        if needs:
            # AST columns are UTF-8 byte offsets, whereas string offsets are characters.
            row=lines[n.end_lineno-1];col=len(row.encode('utf-8')[:n.end_col_offset].decode('utf-8'))
            positions.append(start[n.end_lineno-1]+col-1)
    for pos in sorted(positions,reverse=True):s=s[:pos]+',encoding="utf-8"'+s[pos:]
    if positions:p.write_text(s,encoding='utf-8')
mapping={'\u2013':'-','\u2014':'--','\u2018':"'",'\u2019':"'",'\u201c':'"','\u201d':'"','\u00b1':'+/-','\u00d7':'*','\u2264':'<=','\u2265':'>=','\u2212':'-','\u03c0':'pi','\u03c6':'phi','\u03b8':'theta','\u00b0':' degrees','\u2026':'...','\u00b2':'^2','\u00b3':'^3','\u03bc':'u','\u03c3':'sigma','\u2192':'->','\u0394':'Delta','\u03b4':'delta','\u00a0':' '}
matlab=[]
for p in REPO.rglob('*.m'):
    s=p.read_text(encoding='utf-8-sig');chars=sorted(set(c for c in s if ord(c)>127))
    if not chars:continue
    matlab.append({'path':str(p),'characters':[{'character':c,'codepoint':f'U+{ord(c):04X}'} for c in chars]})
    for c in chars:
        replacement=mapping.get(c,unicodedata.normalize('NFKD',c).encode('ascii','ignore').decode('ascii'))
        if not replacement:replacement='[U+%04X]'%ord(c)
        s=s.replace(c,replacement)
    assert s.isascii();p.write_text(s,encoding='utf-8')
(D/'encoding_audit.json').write_text(json.dumps({'python_9d_occurrences':audit,'ascii_matlab_edits':matlab,'python_scripts_scanned':[str(p) for p in scripts]},indent=2),encoding='utf-8')
old=D/'RESULTS_v1.md';preserved=D/'RESULTS_v1_stopped_before_resume.md'
if old.exists() and not preserved.exists():preserved.write_bytes(old.read_bytes())
print(json.dumps({'byte_9d_occurrences':audit,'matlab_files_converted':len(matlab),'python_scripts_scanned':len(scripts)},ensure_ascii=True))
