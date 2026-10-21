"""Author transfer with new targets and grid; not independent review."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
import torch
import flagquantum as fq
import examples.foundations.approximation_precision as a
inputs=[[(1,0)],[(0,1)],[ (.6,.8j) ]]
targets=[a.explicit('y',-.52) @ a.explicit('x',.19), a.explicit('z',.91), a.explicit('x',1.03) @ a.explicit('z',-.27)]
for target in targets:
    word, candidate, delta, count=a.search(target,5)
    assert count==1365
    for factors in inputs:
        v,_=a.run(a.word_circuit(word),factors)
        torch.testing.assert_close(v,candidate @ a.product_input(factors),rtol=0,atol=a.ATOL)
        assert torch.linalg.vector_norm(v-target @ a.product_input(factors)).item()<=delta+a.ATOL
rounded,h=a.quantized_angle(-1.17,7)
error=a.distance(a.explicit('z',-1.17),a.explicit('z',rounded))
assert error<=h/4+a.ATOL
for factors in inputs:
    v,_=a.run(fq.Circuit(1,dtype=a.D).rz(0,rounded),factors)
    torch.testing.assert_close(v,a.explicit('z',rounded) @ a.product_input(factors),rtol=0,atol=a.ATOL)
assert a.RUNS==12
print('12 new-target/grid transfer circuits passed; implementation residual and target approximation budget kept separate.')
