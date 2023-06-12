import sys
sys.path.append('../../../src')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.standard_fields import *
from p4rrot.core.commands import *  

UID.reset()
fp = FlowProcessor(
        istruct = [],
        ostruct = [('uint64', uint64_t),('uint32',uint32_t), ('uint16', uint16_t), ('uint8', uint8_t)]
    )



(
fp
.add(AssignConst('uint64',1122))
.add(AssignConst('uint32',3344))
.add(AssignConst('uint16',66))
.add(AssignConst('uint8',77))
.add(SendBack())
)  



fs = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,5555)],
        fp
    )


solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('test.p4app')