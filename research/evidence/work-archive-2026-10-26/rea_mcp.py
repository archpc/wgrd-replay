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
print(json.dumps(req(1,'initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'wgrd-readonly','version':'1'}})),flush=True)
send(dict(jsonrpc='2.0',method='notifications/initialized'))
tools=req(2,'tools/list',{})['result']['tools']
print('REA MCP connected; schemas retained',flush=True)
json.dump(tools,open('/Users/sein/Code/wgrd-replay/work/rea-tool-schemas.json','w'))
for i,line in enumerate(sys.stdin,3):
 try:
  x=json.loads(line)
  if x.get('method')=='exit':break
  v=req(i,x.get('method','tools/call'),x.get('params',x))
  out='/Users/sein/Code/wgrd-replay/work/rea-mcp-'+str(i)+'.json'
  json.dump(v,open(out,'w'),indent=2)
  r=v.get('result',{})
  e=r.get('structuredContent')
  if not e:
   texts=[c['text'] for c in r.get('content',[]) if c.get('type')=='text']
   e=json.loads(texts[0]) if texts else r
  if 'evidence_id' in e:
   print(json.dumps({k:e.get(k) for k in ['evidence_id','provider']}),flush=True)
   json.dump(e,open('research/evidence/'+e['evidence_id']+'.json','w'),indent=2)
   raw=e.get('raw_result',{})
   if isinstance(raw,dict) and 'stdout' in raw:
    print(raw['stdout'],flush=True)
    print(json.dumps({k:raw.get(k) for k in ['exit_code','completion_status','artifact_changed']}),flush=True)
   else:print(json.dumps(e.get('normalized_result')),flush=True)
  else: print(json.dumps(e),flush=True)
  print('saved:',out,flush=True)
 except Exception as e:print(json.dumps({'client_error':str(e)}),flush=True)
p.stdin.close();p.wait(timeout=30)
