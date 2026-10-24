"""Research-only matching59638 NDF analysis. Writes ignored work/ndf59638/ only.
No replay decoder changes, archive repacking, or runtime state reconstruction.
Published format source revisions: research/ndf59638-format-sources.json.
"""
import json,collections,hashlib,sys,os
from pathlib import Path
objs=json.load(open('work/ndf59638/objects.json'))
def resolve(ref):
 if ref is None or ref.get('null_kind') or ref.get('ref_index')==ref.get('ref_class_id')==0xffffffff:return None
 assert 'ref_index' in ref,ref
 obj=objs[ref['ref_index']];assert obj['class_id']==ref['ref_class_id'];return obj

def guid(obj):
 x=obj['properties'].get('DescriptorId');assert x and x['ndf_type']==26 and len(bytes.fromhex(x['raw_hex']))==16;return x['raw_hex']

def record(obj):return {'object_index':obj['index'],'ndf_class':obj['class'],'descriptor_guid_hex':guid(obj),'debug_name':obj['properties'].get('ClassNameForDebug'),'name_in_menu_token':obj['properties'].get('NameInMenuToken'),'alias_name':obj['properties'].get('AliasName'),'object_file_offset':obj['offset']+40}

units=[o for o in objs if o['class'] in ('TUniteAuSolDescriptor','TUniteDescriptor')]
byguid=collections.defaultdict(list)
for u in units:byguid[guid(u)].append(u)
# Retain duplicate descriptor GUIDs as candidate source objects, never last-wins.
inverse=collections.defaultdict(list);paths=[];unresolved=[];selection=[]
for u in units:
 slots=[x for x in u['properties'].get('Modules',[]) if x['key']=='CompanyUnit']
 if not slots:continue
 assert len(slots)==1
 node=resolve(slots[0]['value']);assert node is not None
 if node['class']=='TModuleSelector':
  selector=node
  if node['properties'].get('Selection'):selection.append({'unit':record(u),'selector':node})
  node=resolve(node['properties'].get('Default'))
 else:selector=None
 if node is None:unresolved.append({'unit':record(u),'reason':'null selector default'});continue
 assert node['class']=='TCompanyUnitModuleDescriptor',node['class']
 company=resolve(node['properties'].get('CompanyDescriptor'))
 if company is None:unresolved.append({'unit':record(u),'reason':'null CompanyDescriptor'});continue
 assert company['class']=='TUniteDescriptor',company['class']
 path={'unit':record(u),'company':record(company),'selector_object_index':selector['index'] if selector else None,'company_module_object_index':node['index'],'selector_filters':[{'filter_object_index':f['ref_index'],'filter_class':resolve(f)['class'],'condition':resolve(resolve(f)['properties'].get('Condition'))} for f in selector['properties'].get('Selection',[])] if selector else [],'condition_evaluated':False}
 inverse[guid(company)].append(path);paths.append(path)
for item in selection:
 for ref in item['selector']['properties']['Selection']:
  filt=resolve(ref);assert filt['class']=='TModuleSelectorFilter' and set(filt['properties'])=={'Condition'}
  cond=resolve(filt['properties']['Condition']);assert cond['class']=='TModuleSelectorCondition_ParamEquals_Integer'
  assert cond['properties']=={'ParamId':11,'ParamValue':1}
report={'unit_descriptors':len(units),'unique_guid_count':len(byguid),'duplicate_descriptor_guid_count':sum(len(v)>1 for v in byguid.values()),'company_unit_static_paths':len(paths),'inverse_companies':len(inverse),'inverse_cardinalities':dict(collections.Counter(len(v) for v in inverse.values())),'unresolved_links':unresolved,'selectors_with_condition_filters':len(selection)}
root=Path('work/ndf59638');(root/'bridge-paths.json').write_text(json.dumps(paths,indent=1)+'\n');(root/'bridge-report.json').write_text(json.dumps(report,indent=1)+'\n');(root/'company-selector-alternatives.json').write_text(json.dumps(selection,indent=1)+'\n')
sys.path.insert(0,str(Path.cwd()));from wgrd_replay import parse_replay;from wgrd_timeline import build_timeline
samples=Path(os.environ.get('WGRD_SAMPLES_DIR',str(Path.home()/'.hermes/artifacts/wgrd-replay/samples/raw')));rows=[];details=[]
for sample in json.load(open('samples/manifest.json'))['samples']:
 b=(samples/sample['file']).read_bytes();assert hashlib.sha256(b).hexdigest()==sample['sha256']
 refs=build_timeline(parse_replay(b))['entity_references']['entries'];counts=collections.Counter();candidate_counts=collections.Counter();candidate_set=set();matched_guids=set()
 for ref in refs:
  g=ref['validation_guid_hex'];source=byguid.get(g,[])
  candidates=list(inverse.get(g,[]))+[{'unit':record(obj),'company':None} for obj in source if obj['class']=='TUniteAuSolDescriptor']
  if len(candidates)>1:status='ambiguous_static_unit_types'
  elif candidates:status='direct_unit_descriptor' if candidates[0]['company'] is None else 'unique_configured_static_unit_type'
  else:status='unmapped'
  counts[status]+=1;candidate_counts[len(candidates)]+=1;candidate_set.update(x['unit']['descriptor_guid_hex'] for x in candidates);matched_guids.add(g)
  details.append({'sample':sample['file'],'reference_id':ref['reference_id'],'status':status,'evidence_status':'matching_build_59638' if sample['game_version']=='59638' else 'inferred_mismatched_build','source_descriptors':[record(obj) for obj in source],'candidate_paths':candidates,'occurrences':ref['occurrences']})
 rows.append({'sample':sample['file'],'sha256':sample['sha256'],'game_version':sample['game_version'],'references':len(refs),'distinct_descriptor_guids':len(matched_guids),'status':dict(counts),'candidate_cardinalities':dict(candidate_counts),'distinct_candidate_unit_types':len(candidate_set),'references_with_source_alias':sum(bool(v['candidate_paths'][0]['unit']['alias_name']) for v in details if v['sample']==sample['file'] and len(v['candidate_paths'])==1)})
(root/'replay-bridge-details.json').write_text(json.dumps(details,indent=1)+'\n');report['samples']=rows
(root/'bridge-report.json').write_text(json.dumps(report,indent=1)+'\n')
print(json.dumps(report,indent=1))
