import sys
sys.path.append('../../../src')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.standard_fields import *
from p4rrot.core.commands import *

UID.reset()
fp = FlowProcessor(
        istruct = [('i_uint8', uint8_t)],
        mstruct = [('true_bool_t', bool_t),('false_bool_t', bool_t)],
        ostruct = [('o_uint8_0', uint8_t),('o_uint8_1', uint8_t)]
)



(
fp
.add(AssignConst('true_bool_t', 1))
.add(AssignConst('false_bool_t', 0))
.add(If('true_bool_t',
        fp.get_env(),
        then_block=Block(env=fp.get_env()).add(AssignConst('o_uint8_0', 0x54)),
        else_block=Block(env=fp.get_env()).add(AssignConst('o_uint8_0', 0x46))))
.add(If('false_bool_t',
        fp.get_env(),
        then_block=Block(env=fp.get_env()).add(AssignConst('o_uint8_1', 0x54)),
        else_block=Block(env=fp.get_env()).add(AssignConst('o_uint8_1', 0x46))))
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
