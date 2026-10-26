import hashlib,json,pathlib,subprocess,sys,copy
root=pathlib.Path.cwd();base='06d1351a8d62efbd4ea7952fdf4ed0187b8c1fd9'
baseline=root/'work/public-baseline-wgrd_replay.py';baseline.write_bytes(subprocess.check_output(['git','show',base+':wgrd_replay.py']))
previous=json.loads((root/'research/entity-cli-validation.json').read_text())
previous={s['sample']:s['timeline_sha256'] for s in previous['samples']}
rows=[]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for sample in json.loads((root/'samples/manifest.json').read_text())['samples']:
 name=sample['file'];source=pathlib.Path('/Users/sein/.hermes/artifacts/wgrd-replay/samples/raw')/name
 assert digest(source)==sample['sha256']
 paths={k:root/'work'/(name+'.public-'+k+'.json') for k in ['old','default','plain','enriched0','enriched1']}
 for mode,p in paths.items():
  script=baseline if mode=='old' else root/'wgrd_replay.py'
  args=['--timeline'] if mode=='plain' else ['--timeline','--unit-data',str(root/'work/public-units/wargame-data')] if mode.startswith('enriched') else []
  with p.open('wb') as f:subprocess.run([sys.executable,'-B',str(script),str(source)]+args,stdout=f,check=True)
 assert digest(paths['old'])==digest(paths['default'])
 assert digest(paths['plain'])==previous[name]
 assert digest(paths['enriched0'])==digest(paths['enriched1'])
 plain=json.loads(paths['plain'].read_text());enriched=json.loads(paths['enriched0'].read_text())
 restored=copy.deepcopy(enriched);cat=restored['entity_references'];cat.pop('descriptor_data')
 for entry in cat['entries']:entry.pop('static_descriptor');entry.pop('descriptor_match_status')
 assert restored==plain
 assert digest(source)==sample['sha256']
 rows.append({'sample':name,'sample_unchanged':True,'default_matches_starting_commit':True,
              'plain_timeline_matches_starting_commit':True,'enriched_two_runs_identical':True,
              'enriched_sha256':digest(paths['enriched0']),'only_reference_catalog_annotated':True,
              'events':len(enriched['events']),'matched_references':enriched['entity_references']['descriptor_data']['matched_references']})
report={'starting_commit':base,'samples':rows}
(root/'research/public-unit-cli-validation.json').write_text(json.dumps(report,indent=1,sort_keys=True)+'\n');print(json.dumps(report))
