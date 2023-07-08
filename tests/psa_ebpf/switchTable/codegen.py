import sys

sys.path.append('../../../src')

from p4rrot.generator_tools import *
from p4rrot.known_types import *
from p4rrot.standard_fields import *
from p4rrot.core.commands import *

# from p4rrot.core.stateful import *

fp = FlowProcessor(
            istruct = [('x',uint8_t)],
            locals  = [('l',bool_t)],
            ostruct = [('y', uint8_t)]
        )

(
fp
.add(SwitchTable(['x']))
    .Case([5])
        .add(AssignConst('y',7))
    .Case([9])
        .add(AssignConst('y',5))
    .Case([11])
        .add(AssignConst('y',11))
    .Default()
        .add(AssignConst('y',9))
.EndSwitch()
.add(SendBack())
)  

fs = FlowSelector(
    'IPV4_UDP',
    # 8 becasue its the length of the UDP header, seems a little unnecessary
    # for me or at least mythic to put a 8 there and not some sort of constant
    [(UdpDstPort, 5555), (UdpLen, 8 + hdr_len(fp.istruct))],
    fp
)

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('template')
