import sys
sys.path.append('../../../src')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.standard_fields import *
from p4rrot.core.commands import *  

UID.reset()
fp = FlowProcessor(
        istruct = [('i_uint8', uint8_t)],
        ostruct = [('o_uint8', uint8_t)]
)



(
fp
.add(StrictAssignVar('o_uint8', 'i_uint8'))
.add(LeftShift('o_uint8', 1))
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
solution.get_generated_code().dump('template')
