"""Research-only matching59638 NDF analysis. Writes ignored work/ndf59638/ only.
No replay decoder changes, archive repacking, or runtime state reconstruction.
Published format source revisions: research/ndf59638-format-sources.json.
"""
from pathlib import Path
import struct,json,collections
b=Path('work/ndf59638/everything.expanded.ndfbin').read_bytes()
assert b[:4]==b'EUG0';toc=struct.unpack_from('<I',b,16)[0];assert b[toc:toc+4]==b'TOC0';n=struct.unpack_from('<I',b,toc+4)[0]
blocks={}
for i in range(n):
 p=toc+8+24*i;name=b[p:p+4].decode();off,size=struct.unpack_from('<QQ',b,p+8);assert off+size<=toc;blocks[name]=(off,size)
assert toc+8+n*24==len(b)
end=40
for off,size in sorted(blocks.values()):
 assert off==end;end=off+size
assert end==toc
class Reader:
 def __init__(self,data):self.b=data;self.p=0
 def take(self,n):
  assert 0<=n<=len(self.b)-self.p,(self.p,n,len(self.b));x=self.b[self.p:self.p+n];self.p+=n;return x
 def num(self,fmt):return struct.unpack(fmt,self.take(struct.calcsize(fmt)))[0]
 def u32(self):return self.num('<I')
 def string(self):return self.take(self.u32()).decode('latin1')
def block(k):o,z=blocks[k];return Reader(b[o:o+z])
def strings(k):
 r=block(k);x=[]
 while r.p<len(r.b):x.append(r.string())
 return x
classes=strings('CLAS');strs=strings('STRG');trans=strings('TRAN');r=block('PROP');props=[]
while r.p<len(r.b):props.append((r.string(),r.u32()))
counts=collections.Counter();typecounts=collections.Counter();refs=[]
def value(r,depth=0):
 assert depth<64
 t=r.u32();typecounts[t]+=1
 if t==9:return value(r,depth+1)
 if t in (0xffffffff,0xeeeeeeee):return {'null_kind':hex(t)}
 if t==0xbbbbbbbb:
  ref={'ref_index':r.u32(),'ref_class_id':r.u32()};refs.append(ref);return ref
 if t==0xaaaaaaaa:
  ix=r.u32();assert ix<len(trans);return {'import_path_index':ix}
 if t==17:return [value(r,depth+1) for _ in range(r.u32())]
 if t==18:return [{'key':value(r,depth+1),'value':value(r,depth+1)} for _ in range(r.u32())]
 if t==34:return {'key':value(r,depth+1),'value':value(r,depth+1)}
 if t==8:return r.take(r.u32()).decode('utf-16-le')
 if t in (7,28):
  ix=r.u32();assert ix<len(strs);return strs[ix]
 if t in (12,26,29):return {'raw_hex':r.take({12:16,26:16,29:8}[t]).hex(),'ndf_type':t}
 if t in (11,33):return struct.unpack('<'+'f'*(3 if t==11 else 2),r.take(12 if t==11 else 8))
 if t==31:return struct.unpack('<ii',r.take(8))
 if t==13:return {'raw_hex':r.take(4).hex(),'ndf_type':t}
 fmt={0:'<?',1:'<B',2:'<i',3:'<I',5:'<f',6:'<d',24:'<h',25:'<H'}.get(t)
 if fmt:return r.num(fmt)
 raise ValueError('Unknown value type %x at OBJE+%x object=%s property=%s next=%s'%(t,r.p-4,(obj['index'],obj['class']),name,r.b[r.p:r.p+48].hex()))
r=block('OBJE');objects=[]
while r.p<len(r.b):
 start=r.p;cid=r.u32();assert cid<len(classes),(len(objects),hex(start),cid);obj={'index':len(objects),'class_id':cid,'class':classes[cid],'offset':start,'properties':{}}
 while True:
  pid=r.u32()
  if pid==0xabababab:break
  assert pid<len(props),(len(objects),hex(r.p-4),pid)
  name,owner=props[pid];assert name not in obj['properties'],(len(objects),name)
  obj['properties'][name]=value(r)
 counts[obj['class']]+=1;objects.append(obj)
assert r.p==len(r.b)
chunk=block('CHNK'); assert chunk.u32()==0; expected=chunk.u32(); assert expected==len(objects),(expected,len(objects))
null_refs=0
for ref in refs:
 if ref['ref_index']==ref['ref_class_id']==0xffffffff:
  null_refs+=1;continue
 assert ref['ref_index']<len(objects),ref
 assert objects[ref['ref_index']]['class_id']==ref['ref_class_id'],(ref,objects[ref['ref_index']]['class'])
out=Path('work/ndf59638');(out/'objects.json').write_text(json.dumps(objects,ensure_ascii=True,separators=(',',':')))
report={'blocks':blocks,'class_count':len(classes),'property_count':len(props),'string_count':len(strs),'import_path_count':len(trans),'objects':len(objects),'object_bytes_consumed':r.p,'non_null_object_references_class_checked':len(refs)-null_refs,'null_object_references':null_refs,'value_types':{hex(k):v for k,v in typecounts.items()},'selected_classes':{k:v for k,v in counts.items() if k in ['TUniteDescriptor','TUniteAuSolDescriptor','TCompanyUnitModuleDescriptor','TModuleSelector','TUnitListCompanyModuleDescriptor']}}
(out/'parse.json').write_text(json.dumps(report,indent=1)+'\n');print(json.dumps(report))
