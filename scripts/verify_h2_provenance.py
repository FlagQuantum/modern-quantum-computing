#!/usr/bin/env python3
"""Independent planning audit: STO-6G integrals to the corrected H2 model.

This is verification tooling, not textbook body or a FlagQuantum API example.
Run with requirements-provenance.txt; --write records the full geometry audit.
"""
import numpy as np
from pyscf import gto,scf,ao2mo
from itertools import product
def annihilator(p):
 a=np.zeros((16,16))
 for n in range(16):
  f=[(n>>(3-i))&1 for i in range(4)]
  if f[p]:
   sign=(-1)**sum(f[:p]);f[p]=0;m=sum(v<<(3-i) for i,v in enumerate(f));a[m,n]=sign
 return a
A=[annihilator(p) for p in range(4)]
P={s:np.array(m,dtype=complex) for s,m in {'I':[[1,0],[0,1]],'X':[[0,1],[1,0]],'Y':[[0,-1j],[1j,0]],'Z':[[1,0],[0,-1]]}.items()}
B=np.zeros((16,16))
for n in range(16):
 f=[(n>>(3-i))&1 for i in range(4)];b=[f[0],f[0]^f[1],f[2],f[0]^f[1]^f[2]^f[3]];m=sum(v<<(3-i) for i,v in enumerate(b));B[m,n]=1
idx=[0,2,8,10] # b1=b3=0, active b0,b2 left to right

def build(r,basis='sto-6g'):
 mol=gto.M(atom=f'H 0 0 0; H 0 0 {r}',unit='Angstrom',basis=basis,verbose=0)
 mf=scf.RHF(mol);mf.conv_tol=1e-12;mf.kernel();assert mf.converged
 C=mf.mo_coeff.copy()
 # fix MO phases by first AO coefficient, needed for saved orbital conventions
 C*=np.where(C[0,:]<0,-1,1)
 h=C.T@mf.get_hcore()@C;eri=ao2mo.restore(1,ao2mo.kernel(mol,C),2)
 E=mol.energy_nuc();H=E*np.eye(16)
 for i,j in product(range(2),repeat=2):
  for s in range(2):H+=h[i,j]*A[2*i+s].T@A[2*j+s]
 for i,j,k,l in product(range(2),repeat=4):
  for s,t in product(range(2),repeat=2):H+=.5*eri[i,j,k,l]*A[2*i+s].T@A[2*k+t].T@A[2*l+t]@A[2*j+s]
 BK=B@H@B.T;red=BK[np.ix_(idx,idx)]
 co={u+v:float(np.trace(red@np.kron(P[u],P[v])).real/4) for u,v in product(P,repeat=2)}
 return h,eri,E,co,red,H
def main():
 import argparse,csv,hashlib,json,platform
 from pathlib import Path
 import pyscf,scipy,h5py
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--write',action='store_true')
 args=parser.parse_args()
 root=Path(__file__).resolve().parents[1]
 path=root/'examples/omalley2016/h2-table.csv'
 rows=list(csv.DictReader(path.open()))
 # BSE STO-6G H version 1: compare primitives, not merely the basis name.
 expected=np.array([[35.52322122,.009163596281],[6.513143725,.04936149294],
                    [1.822142904,.1685383049],[.6259552659,.3705627997],
                    [.2430767471,.4164915298],[.1001124280,.1303340841]])
 assert np.allclose(gto.basis.load('sto-6g','H')[0][1:],expected,rtol=0,atol=2e-10)
 paulis=['II','ZI','IZ','ZZ','XX','YY'];out=[]
 for row in rows:
  r=float(row['R_angstrom']);h,e,enn,c,red,full=build(r)
  # Independent closed-form coefficient bridge from the six unique integrals.
  a,b=h.diagonal();u,v,w,k=e[0,0,0,0],e[1,1,1,1],e[0,0,1,1],e[0,1,0,1]
  analytic=[enn+a+b+(u+v)/2+w-k/2,-a-u/2-w+k/2,
            -b-v/2-w+k/2,w-k/2,k/2,k/2]
  assert np.allclose([c[x] for x in paulis],analytic,atol=1e-12,rtol=0)
  assert all(abs(v)<1e-12 for x,v in c.items() if x not in paulis)
  assert np.allclose(full,full.T,atol=1e-12,rtol=0)
  bk=B@full@B.T
  # O'Malley Eq. A5 / Seeley Eq. 79: compare every four-qubit term,
  # before projecting or combining any coefficient. Add E_NN only to f0.
  f0=enn+a+b+(u+v)/4+w-k/2
  f1=-a/2-u/4-w/2+k/4;f2=u/4
  f3=-b/2-v/4-w/2+k/4;f4=(w-k)/4
  f5=v/4;f6=k/4;f7=w/4
  terms=[('IIII',f0),('ZIII',f1),('IZII',f2),('IIZI',f3),
         ('ZZII',f1),('ZIZI',f4),('IZIZ',f5),('XZXI',f6),
         ('YZYI',f6),('ZZZI',f7),('ZIZZ',f4),('IZZZ',f3),
         ('XZXZ',f6),('YZYZ',f6),('ZZZZ',f7)]
  a5=np.zeros((16,16),complex)
  for labels,value in terms:
   op=np.array([[1.]])
   for label in labels:op=np.kron(op,P[label])
   a5+=value*op
  assert np.max(abs(bk-a5))<1e-12
  for bit in [1,3]:
   z=np.diag([(-1)**((n>>(3-bit))&1) for n in range(16)])
   assert np.max(abs(bk@z-z@bk))<1e-12
  odd=red[np.ix_([1,2],[1,2])]
  # Correct two-electron Fock block; exclude vacuum and fully occupied states.
  n2=[n for n in range(16) if bin(n).count('1')==2]
  e2=float(np.linalg.eigvalsh(full[np.ix_(n2,n2)])[0])
  eo=float(np.linalg.eigvalsh(odd)[0])
  assert abs(eo-e2)<1e-10
  delta=max(abs(c[x]-float(row[x])) for x in paulis)
  assert delta <= .00005+1e-10,(r,delta)
  rounded=sum(float(row[x])*np.kron(P[x[0]],P[x[1]]) for x in paulis)
  table_e=float(np.linalg.eigvalsh(rounded[np.ix_([1,2],[1,2])])[0])
  # Operator perturbation bound for rounded coefficients.
  assert abs(eo-table_e)<=sum(abs(c[x]-float(row[x])) for x in paulis)+1e-12
  out.append(dict(R_angstrom=r,coefficients={x:c[x] for x in paulis},
                  max_coefficient_residual_hartree=delta,nuclear_repulsion_hartree=enn,
                  exact_two_electron_energy_hartree=eo,rounded_table_energy_hartree=table_e))
 assert len(out)==54
 # Seeley Table III is a distinct historical integral fixture (STO-3G numerically).
 h,e,_,_,_,_=build(1.401*.52917721092,'sto-3g')
 fixture=[h[0,0],h[1,1],e[0,0,0,0],e[1,1,1,1],e[0,0,1,1],e[0,1,0,1]]
 assert np.max(abs(np.array(fixture)-[-1.252477,-.475934,.674493,.697397,.663472,.181287]))<1e-6
 counter=build(.75,'sto-3g')[3]
 at_075=next(row for row in rows if float(row['R_angstrom'])==.75)
 assert max(abs(counter[x]-float(at_075[x])) for x in paulis)>.007
 report=dict(scope='Independent regeneration to published four-decimal precision; original author integral files not recovered; no hardware claim',
   checked='2026-10-20',environment=dict(python=platform.python_version(),pyscf=pyscf.__version__,numpy=np.__version__,scipy=scipy.__version__,h5py=h5py.__version__,platform=platform.platform()),
   input_table_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
   basis='STO-6G hydrogen; built-in primitives checked against Basis Set Exchange version 1 within 2e-10 absolute',
   orbital_order=['g_alpha','g_beta','u_alpha','u_beta'],bk_bits=['f0','f0 xor f1','f2','f0 xor f1 xor f2 xor f3'],fixed_bk_z={'1':1,'3':1},
   active_qubits=[0,2],two_qubit_basis=['vacuum','u_alpha u_beta','g_alpha g_beta','fully occupied'],
   electron_sector='Z0 Z1 = -1',coefficient_count=6*len(out),
   tolerance_hartree=.00005,max_coefficient_residual_hartree=max(x['max_coefficient_residual_hartree'] for x in out),
   seeley_table_III_independent_fixture=fixture,rows=out)
 if args.write:
  target=root/'book/verification/h2-provenance.json';target.parent.mkdir(exist_ok=True)
  target.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['coefficient_count','max_coefficient_residual_hartree','tolerance_hartree']}))
if __name__=='__main__':main()
