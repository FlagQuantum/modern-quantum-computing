import torch
from examples.foundations.tensor_reshaping import axis_order,undo_order,apply_local,execute,DTYPE,ATOL
from examples.foundations.ordered_supports import controlled_flip,scalar_scatter
S=(3,1);order=axis_order(4,S);assert order==(3,1,0,2) and undo_order(order)==(2,1,3,0)
x=torch.zeros(16,dtype=DTYPE);x[11]=1
packed=x.reshape((2,)*4).permute(order).reshape(4,4);assert packed[2,3]==1
U=controlled_flip();expected=apply_local(x,U,4,S)
scalar=torch.tensor(scalar_scatter(U,x.tolist(),4,S),dtype=DTYPE)
a,p=execute(U,4,S,[(0,1),(1,0),(0,1),(0,1)])
assert torch.allclose(a,expected,rtol=0,atol=ATOL) and torch.allclose(a,scalar,rtol=0,atol=ATOL)
assert a[15]==1 and torch.allclose(p,a.abs().square(),rtol=0,atol=ATOL)
markers=torch.arange(8).reshape(2,2,2);o=(2,0,1)
assert markers[1,0,0]==4 and markers.permute(o).permute(o)[1,0,0]==2
print('Separate4qubit transfer:1011,index11 -> packed row2,column3; controlled support(3,1) ->1111,index15.')
print('Inverse-axis answer checked; repeating order(2,0,1) yields marker2 instead of4.')
