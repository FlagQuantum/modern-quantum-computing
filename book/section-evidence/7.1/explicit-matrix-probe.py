import sys,math,torch
sys.path.insert(0,'.')
import examples.foundations.product_entanglement as e
import flagquantum as fq
x=1e-14
U=torch.tensor([[math.sqrt(1-x*x),-x],[x,math.sqrt(1-x*x)]],dtype=e.D)
v,_=e.query(fq.Circuit(2,dtype=e.D).unitary(0,unitary=U).cx(0,1))
print(repr(v.tolist())); assert v[3].real.item()==x
