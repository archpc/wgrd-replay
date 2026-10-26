import hashlib
import json
from pathlib import Path
import subprocess
import sys

root=Path.cwd()
base='5be10ad11cdf1d1c8c4dd31206886100852a0d5a'
baseline=root/'work/baseline_wgrd_replay.py'
baseline.write_bytes(subprocess.check_output(['git','show',base+':wgrd_replay.py']))
manifest=json.loads((root/'samples/manifest.json').read_text())
results=[]
for sample in manifest['samples']:
    name=sample['file']
    source=Path('/Users/sein/.hermes/artifacts/wgrd-replay/samples/raw')/name
    digest=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    assert digest(source)==sample['sha256']
    old=root/'work'/('baseline-'+name+'.json')
    default=root/'work'/('default-'+name+'.json')
    timelines=[root/'work'/(name+'.timeline-'+str(i)+'.json') for i in range(2)]
    for script,out,args in [(baseline,old,[]),(root/'wgrd_replay.py',default,[])] + [(root/'wgrd_replay.py',p,['--timeline']) for p in timelines]:
        with out.open('wb') as f:
            subprocess.run([sys.executable,'-B',str(script),str(source)]+args,stdout=f,check=True)
    assert digest(old)==digest(default), name+' default output changed'
    assert digest(timelines[0])==digest(timelines[1]), name+' timeline nondeterministic'
    timeline=json.loads(timelines[0].read_text())
    assert timeline['header']['digest_valid']
    assert digest(source)==sample['sha256']
    results.append({'sample':name,'default_matches_starting_commit':True,
                    'timeline_two_cli_runs_identical':True,
                    'timeline_sha256':digest(timelines[0]),'events':len(timeline['events']),
                    'sample_unchanged':True})
    if name.startswith('koppeltar-Sample1'):
        e=next(e for e in timeline['events'] if e['frame']==131 and e['player_slot']==2 and e['opcode']==8)
        print(json.dumps({'authentic_example':{k:e[k] for k in ['frame','player_slot','command_order','opcode','interpretation','source']}},sort_keys=True))
report={'starting_commit':base,'samples':results}
(root/'research/timeline-cli-validation.json').write_text(json.dumps(report,indent=1,sort_keys=True)+'\n')
print(json.dumps(report,sort_keys=True))
