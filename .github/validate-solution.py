import pathlib,re,gzip,base64,hashlib,subprocess,json
p=pathlib.Path
out=p('validation-output');out.mkdir(exist_ok=True)
results={}
def run(name,args,expected=False):
 r=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 (out/(name+'.log')).write_text(r.stdout)
 results[name]=r.returncode
 print(name,r.returncode,r.stdout[-5000:],flush=True)
 if not expected: assert r.returncode==0,name
 return r

def failures(r):
 names=re.findall(r'^not ok \d+ - (.+)$',r.stdout,re.M)
 assert r.returncode==0 or names,'Failure outside behavior tests'
 return sorted(names)

s=p('.github/workflows/solution-validation.yml').read_text()
b=re.search("echo '([^']+)'",s)[1].replace('OUYuTzBNukkoxeney7','OUYuTzBNpukkoxeney7')
s=gzip.decompress(base64.b64decode(b))
assert hashlib.sha256(s).hexdigest()=='5af1a89596e3707afae998be808f60a420df32d609a974dc134964668d0765c2'
b=re.search("echo '([^']+)'",s.decode())[1]
p('/tmp/solution.patch').write_bytes(gzip.decompress(base64.b64decode(b)))
before=run('baseline-test',['npm','test'],True)
run('apply',['git','apply','/tmp/solution.patch'])
run('format',['npx','--no-install','prettier','--write','src/action.ts','test/npm-audit-policy.test.ts'])
for name in ['lint','typecheck','build']:
 run(name,['npm','run',name])
after=run('candidate-test',['npm','test'],True)
assert failures(before)==failures(after),'New test failure'
print('BASELINE_FAILURES='+json.dumps(failures(before)),flush=True)
run('focused',['node','--test','tests/fail-closed.test.cjs'])
run('vitest',['npm','run','test:vitest'])
run('bundle',['npm','run','bundle'])
run('diff-check',['git','diff','--check'])
run('audit',['npm','audit','--audit-level=moderate'])
(out/'results.json').write_text(json.dumps({'exits':results,'baseline_failures':failures(before)},indent=2))
print('VALIDATION_RESULTS='+json.dumps(results),flush=True)
