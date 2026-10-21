import json,pathlib,subprocess,time
out=pathlib.Path('/private/tmp/mqc-algebra-blind-r1/c/outputs')
command=['/private/tmp/mqc-writing-venv/bin/python',str(out/'independent_verify.py')]
start=time.perf_counter();cp=subprocess.run(command,capture_output=True,text=True);elapsed=time.perf_counter()-start
(out/'independent_stdout.json').write_text(cp.stdout);(out/'independent_stderr.txt').write_text(cp.stderr)
(out/'independent_execution.json').write_text(json.dumps({'command':command,'exit_code':cp.returncode,'wall_seconds':elapsed},indent=2)+'\n')
print(cp.stdout)
