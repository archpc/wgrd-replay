"""Research-only matching59638 NDF analysis. Writes ignored work/ndf59638/ only.
No replay decoder changes, archive repacking, or runtime state reconstruction.
Published format source revisions: research/ndf59638-format-sources.json.
"""
from pathlib import Path
import hashlib,json,struct,zlib
source=Path('/Users/sein/.hermes/artifacts/wgrd-replay/game/win64/Data/WarGame/PC/59638/NDF_Win.dat')
b=source.read_bytes();target=json.load(open('research/matching-ndf-target.json'))
assert len(b)==target['size'] and hashlib.sha1(b).hexdigest()==target['content_sha1']
assert b[:8]==b'edat\x02\0\0\0'
doff,dsize,boff,bsize=struct.unpack_from('<4I',b,25);sector=struct.unpack_from('<I',b,45)[0]
assert doff+dsize<=len(b) and boff+bsize<=len(b)
assert hashlib.md5(b[doff:doff+dsize]).digest()==b[49:65]
assert b[doff:doff+10]==b'\x0a\0\0\0'+b'\0'*6
entries={}
def walk(p,end,prefix):
 while p<end:
  start=p; span,total=struct.unpack_from('<2I',b,p);p+=8
  stop=start+total if total else end
  assert p<=stop<=end
  if span:
   z=b.index(b'\0',p,stop);part=b[p:z].decode();p=z+1+(z+1-p)%2
   assert p==start+span
   walk(p,stop,prefix+part);p=stop
  else:
   off,pad,size,pad2=struct.unpack_from('<4I',b,p);md5=b[p+16:p+32];p+=32
   assert pad==pad2==0
   z=b.index(b'\0',p,stop);part=b[p:z].decode();p=z+1+(z+1-p)%2
   assert p==stop
   path=prefix+part;assert path not in entries and boff+off+size<=len(b)
   entries[path]={'offset':boff+off,'size':size,'md5':md5.hex()}
 assert p==end
walk(doff+10,doff+dsize,'')
hits=[p for p in entries if p.lower().endswith('everything.ndfbin')];assert len(hits)==1,hits
path=hits[0];e=entries[path];raw=b[e['offset']:e['offset']+e['size']];assert hashlib.md5(raw).hexdigest()==e['md5']
out=Path('work/ndf59638');out.mkdir(exist_ok=True);(out/'everything.ndfbin').write_bytes(raw)
assert raw[:4]==b'EUG0' and raw[8:12]==b'CNDF'
flag=struct.unpack_from('<I',raw,12)[0];assert flag in (0,128)
if flag:
 dec=zlib.decompressobj();body=dec.decompress(raw[44:])+dec.flush();assert not dec.unused_data and not dec.unconsumed_tail
 assert len(body)==struct.unpack_from('<I',raw,40)[0]
else:body=raw[40:]
# Preserve source header in scratch; do not repair/repack it.
expanded=raw[:40]+body;(out/'everything.expanded.ndfbin').write_bytes(expanded)
report={'archive_sha1':hashlib.sha1(b).hexdigest(),'archive_sha256':hashlib.sha256(b).hexdigest(),'archive_size':len(b),'dictionary_md5_valid':True,'archive_entries':len(entries),'dictionary_offset':doff,'dictionary_size':dsize,'entry':{'path':path,**e,'md5_valid':True,'sha256':hashlib.sha256(raw).hexdigest()},'expanded_size':len(expanded),'expanded_sha256':hashlib.sha256(expanded).hexdigest(),'source_header_hex':raw[:44].hex(),'zlib_eof_marker_present':dec.eof if flag else None,'expanded_declared_size_valid':len(expanded)==struct.unpack_from('<I',raw,32)[0]}
(out/'unpack.json').write_text(json.dumps(report,indent=1)+'\n');(out/'entries.json').write_text(json.dumps(entries,indent=1)+'\n');print(json.dumps(report))
