import sys,itertools,json
sys.path.insert(0,'/private/tmp')
import resource_accounting as r
cases=((-0.3,.9),(.13,-.7,1.2),(.4,.2,-.8,.6))
for angles in cases:
 for mode in ('statevector','density_matrix'):
  for full in (False,True):
   _,plan,info=r.simulate(angles,31,mode,full)
   assert plan['total'].gates==2*len(angles)*31
   assert info['logical_payload_bits']==31*(len(angles)+1 if full else 1)
supports=((0,),(1,),(2,),(0,3),(1,3),(2,3));paths=[]
for k in range(1,7):
 for chain in itertools.combinations(range(6),k):
  if all(set(supports[a])&set(supports[b])for a,b in zip(chain,chain[1:])):paths.append(chain)
assert max(map(len,paths))==4==r.layers(supports,4)[1]
assert (0,3,4,5)in paths
assert r.substitute(2,3,7,50,120)['logical_gates']==1150
assert r.simulator_storage(20)['statevector_bytes']==16777216
assert r.RUNS==12
print(json.dumps(dict(native_runs=r.RUNS,angle_lists=cases,modes=['statevector','density_matrix'],selected_and_full=True,independent_path_count=len(paths),longest_path=4,resource_and_vector_output_exercise='passed'),indent=2))
