from pathlib import Path
import struct,json,hashlib
p=Path('/Users/sein/.hermes/artifacts/wgrd-replay/game/win64/.DepotDownloader/251062_7569342467126442184.manifest')
b=p.read_bytes()
def var(b,p):
 v=0;s=0
 while True:
  c=b[p];p+=1;v|=(c&127)<<s
  if c<128:return v,p
  s+=7
  if s>63:raise ValueError('varint')
def fields(b):
 p=0
 while p<len(b):
  tag,p=var(b,p);n=tag>>3;t=tag&7
  if t==0:v,p=var(b,p)
  elif t==2:
   z,p=var(b,p);v=b[p:p+z];assert len(v)==z;p+=z
  elif t in (1,5):
   z=8 if t==1 else 4;v=b[p:p+z];p+=z
  else:raise ValueError(t)
  yield n,v
magic,n=struct.unpack_from('<II',b);assert magic==0x71f617d0
payload=b[8:8+n];magic,n2=struct.unpack_from('<II',b,8+n);assert magic==0x1f4812be
meta=dict(fields(b[16+n:16+n+n2]));assert meta[1]==251062 and meta[2]==7569342467126442184 and not meta[4]
for field,v in fields(payload):
 if field!=1:continue
 f=list(fields(v));d={k:v for k,v in f if k!=6}
 name=d[1].decode().rstrip('\0')
 if name.endswith('ZZ_Win.dat'):
  chunks=[dict(fields(v)) for k,v in f if k==6]
  assert sum(c[4] for c in chunks)==d[2]
  print(json.dumps({'app':251060,'depot':meta[1],'manifest':str(meta[2]),'manifest_sha256':hashlib.sha256(b).hexdigest(),'path':name.replace('\\','/'),'size':d[2],'content_sha1':d[5].hex(),'chunk_count':len(chunks),'compressed_chunk_bytes':sum(c[5] for c in chunks),'manifest_creation_unix':meta[3],'file_cached':False},indent=1))
