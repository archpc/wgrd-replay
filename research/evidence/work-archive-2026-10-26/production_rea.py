import subprocess,json,os,sys
base='/Users/sein/.hermes/tools/rea'
env=os.environ.copy()
env.update(GHIDRA_INSTALL_DIR='/Users/sein/.hermes/tools/ghidra/ghidra_12.1.4_PUBLIC',JAVA_HOME='/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home',GHIDRA_HEADLESS_MAXMEM='8G',REA_GHIDRA_STARTUP_TIMEOUT_MS='120000',REA_RIZIN_COMMAND='/opt/homebrew/bin/rizin',REA_KUNA_COMMAND='/Users/sein/.hermes/tools/kuna/v1.833/kuna')
log=open('/Users/sein/Code/wgrd-replay/work/rea_mcp_stderr.log','w')
p=subprocess.Popen([base+'/node_modules/.bin/rea','mcp'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=log,text=True,env=env)
def send(x):p.stdin.write(json.dumps(x)+'\n');p.stdin.flush()
def req(i,method,params):
 send(dict(jsonrpc='2.0',id=i,method=method,params=params))
 while True:
  line=p.stdout.readline()
  if not line:raise RuntimeError('MCP exited')
  v=json.loads(line)
  if v.get('id')==i:return v
req(1,'initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'wgrd-production','version':'1'}})
send(dict(jsonrpc='2.0',method='notifications/initialized'))
x=json.load(sys.stdin)
v=req(2,'tools/call',{'name':'execute_rizin_command','arguments':{'path':'/Users/sein/.hermes/artifacts/wgrd-replay/game/win64/Data/PC/59638/WarGame3.exe','command':x['command']}})
r=v.get('result',{});e=r.get('structuredContent')
if not e:e=json.loads(next(c['text'] for c in r['content'] if c['type']=='text'))
if 'evidence_id' not in e:raise RuntimeError(e)
json.dump(e,open('research/evidence/'+e['evidence_id']+'.json','w'),indent=2)
raw=e.get('raw_result',{});Path(x['output']).write_text(raw.get('stdout',''))
print(json.dumps({'evidence_id':e['evidence_id'],'exit_code':raw.get('exit_code'),'output':x['output'],'artifact_changed':raw.get('artifact_changed')}))
p.stdin.close();p.wait(timeout=30)
