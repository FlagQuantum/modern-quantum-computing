import json,pathlib,math,subprocess,time
root=pathlib.Path(__file__).resolve().parent.parent
out=root/'outputs'
t=json.loads((root/'tasks.json').read_text())[0]
q=dict(t['data']);q['angle_unit']='radian';q['phase_radians']=[math.radians(x) for x in t['data']['phase_radians']];q['readout']={'type':'phase-h','delta_radians':math.radians(0)}
(out/'C1.clarification.json').write_text(json.dumps({'question':'Are the original scan values 30 and 75 degrees or radians?','answer':'The scan values 30 and 75 are in degrees, and the analyzer delta is zero degrees. Convert them explicitly to radians before using the helper and retain the original values in the record.','source':'parent relayed caller clarification','source_scan_values':t['data']['phase_radians'],'source_angle_unit':'degree','source_analyzer_delta':0,'conversion':'radians = degrees * pi / 180','converted_phase_radians':q['phase_radians']},indent=2))
req=json.dumps(q,indent=2);(out/'C1.request.json').write_text(req)
args=['/private/tmp/mqc-writing-venv/bin/python',str(root/'skills/reproduce-qubit-interference/scripts/interference.py')]
start=time.perf_counter();r=subprocess.run(args,input=req,text=True,capture_output=True,cwd=root)
(out/'C1.helper.stdout').write_text(r.stdout);(out/'C1.helper.stderr').write_text(r.stderr)
(out/'C1.helper.execution.json').write_text(json.dumps({'argv':args,'exit_code':r.returncode,'runtime_seconds':time.perf_counter()-start},indent=2))
