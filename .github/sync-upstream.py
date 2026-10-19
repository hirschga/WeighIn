from pathlib import Path
import re
import subprocess as s

def run(*args):
 s.run(args, check=True)

upstream = '4f266c5e8d5a98de7e83e80ebe4a1475ec1bbe0f'
run('git', 'config', 'user.name', 'github-actions[bot]')
run('git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com')
run('git', 'fetch', 'https://github.com/WeighInNG/WeighIn.git', upstream)
run('git', 'merge', '--no-commit', '--no-ff', '-X', 'ours', upstream)
p = Path('src/action.ts')
t = p.read_text()
assert 'class RpcCompatibilityError' not in t
anchor = '// ---------------------------------------------------------------------------\n// RPC health check'
assert anchor in t
t = t.replace(anchor, 'class RpcCompatibilityError extends Error {}\n\n' + anchor, 1)
t = t.replace('  validatedDiffJson = null;\n', '').replace('    validatedDiffJson = JSON.stringify(diff);\n', ')
assert 'validatedDiffJson' not in t
assert 'validateBaseRef(headWorkspace, baseRef)' in t
p.write_text(t)
p = Path('tests/support/action-unit-hook.cjs')
t = p.read_text()
old = '(mode === "summary-write-once" || mode === "summary-write-always")'
assert old in t
p.write_text(t.replace(old, old[:-1] + ' || mode === "summary-delivery-failure")))
p = Path('tests/fail-closed.test.cjs')
t = p.read_text()
t, count = re.subn(r'\nfunction lastActionOutput\(output, name\) \{.*?\n\}\n', '\n', t, flags=re.S)
assert count == 1 and 'function outputValue(' in t
p.write_text(t.replace('lastActionOutput(', 'outputValue('))
p = Path('README.md')
t = p.read_text()
t, count = re.subn(r'An unsuccessful comparison emits `fail` and `\{\}`\. A valid comparison with policy\nviolations.*?retaining the computed diff\.', 'A valid comparison with policy violations emits its real diff, writes the\nreport, then fails the Action.', t, flags=re.S)
assert count == 1
p.write_text(t)
run('npx', 'prettier', '--write', 'src/action.ts', 'src/build.ts', 'src/network.ts')
for command in ['lint', 'typecheck', 'test', 'build', 'bundle', 'provenance']:
    run('npm', 'run', command)
run('npm', 'audit', '--audit-level=moderate')
run('git', 'diff', '--check')
run('git', 'add', '-u')
run('git', 'commit', '-m', 'fix: reconcile validation repairs with current upstream')
run('npm', 'run', 'bundle')
run('npm', 'run', 'provenance')
run('git', 'diff', '--exit-code')
assert not s.check_output(['git', 'status', '--porcelain']).strip()
run('git', 'push', 'origin', 'HEAD:fix/report-delivery-diff')
run('git', 'rev-parse', 'HEAD')
