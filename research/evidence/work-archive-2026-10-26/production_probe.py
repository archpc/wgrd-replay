import json,struct,collections,gzip,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from wgrd_replay import parse_replay
index=json.load(gzip.open('research/unit-data/build59638-v1.json.gz'))
def decode(f):
 b=bytes.fromhex(f['serializer_payload_hex']);p=0
 def take(n):
  nonlocal p
  assert n>=0 and p+n<=len(b),(p,n,len(b));out=b[p:p+n];p+=n;return out
 def u():return int.from_bytes(take(4),'little')
 def scope():
  h,n=u(),u();return h,take(n)
 h,base=scope();a={'base':int.from_bytes(base,'little'),'player':u()}
 h,refs=scope();assert len(refs)==52
 a['refs']=[refs[i:i+16].hex() for i in (0,16,32)];a['ref_extra']=int.from_bytes(refs[48:],'little')
 if f['variant_u32']==2:a['scalars']=[u(),u(),u()]
 else:
  n=u();a['positions']=[struct.unpack('<3fI',take(16)) for _ in range(n)]
  a['obj68']=u();a['obj6c']=u();a['obj70']=u()
  n=u();a['counts']=[u() for _ in range(n)];a['obj90']=u();a['flags']=list(take(2))
  n=u();a['nested']=[[u() for _ in range(u())] for _ in range(n)];a['flag96']=take(1)[0]
 assert p==len(b),(p,len(b),a)
 return a
if __name__=='__main__':
 for s in json.load(open('samples/manifest.json'))['samples']:
  r=parse_replay(Path(s['stored_at']).expanduser().read_bytes());out=[]
  for rec in r['commands']:
   for c in rec['command_decode']['commands']:
    if c['opcode']==13:out.append({'frame':rec['frame'],'slot':rec['slot'],'variant':c['fields']['variant_u32'],**decode(c['fields'])})
  Path('work/production-'+s['file']+'.json').write_text(json.dumps(out,indent=2))
  print(s['file'],len(out),collections.Counter(a['base'] for a in out));print(out[:2])
