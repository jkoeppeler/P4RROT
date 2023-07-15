from p4rrot.known_types import KnownType
from typing import Dict, List, Tuple
from p4rrot.standard_fields import *
from p4rrot.generator_tools import *
from p4rrot.checks import *
import random

class AssignRandomValue(Command):

    def __init__(self, vname, min_value, max_value, env=None):
        self.env = env
        self.vname=vname
        self.min_value = min_value
        self.max_value = max_value

        
        if self.env != None:
            self.check()


    def check(self):
        var_exists(self.vname, self.env)
        assert self.env.get_varinfo(self.vname)['type'] in [ uint8_t, uint16_t ,uint32_t, uint64_t ], 'Not supported random generation'
        target_type = self.env.get_varinfo(self.vname)['type']
        is_writeable(self.vname,self.env)


    def get_generated_code(self):
        gc = GeneratedCode()
        rng_name = "rng_"+UID.get()
        target_type = self.env.get_varinfo(self.vname)['type']
        rng_type = target_type.get_p4_type()
        vi  = self.env.get_varinfo(self.vname)
        gc.get_decl().writeln('Random< {} >(({}){},({}){}) {};'.format(
            rng_type,
            rng_type,
            self.min_value,
            rng_type,
            self.max_value,
            rng_name
        ))
        gc.get_apply().writeln('{} = {}.read();'.format(vi['handle'], rng_name))
        return gc


    def execute(self, test_env):
        target_type = self.env.get_varinfo(self.vname)['type']
        test_env[self.vname] = random.randint(target_type.cast_value(min_value),target_type.cast_value(max_value))


class AssignHash(Command):
    def __init__(self, t_name, s_name, hash_name, env=None):
        self.env = env
        self.t_name = t_name
        self.s_name = s_name
        self.hash_name = hash_name

        if self.env != None:
            self.check()

    def check(self):
        var_exists(self.t_name, self.env)
        var_exists(self.s_name, self.env)
        var_exists(self.hash_name, self.env)
        is_writeable(self.t_name, self.env)

    def get_generated_code(self):
        gc = GeneratedCode()
        target = self.env.get_varinfo(self.t_name)
        source = self.env.get_varinfo(self.s_name)
        gc.get_apply().writeln('{} = {}.get_hash({});'.format(target['handle'], self.hash_name, source['handle']))
        return gc


class GetTimestamp(Command):
    def __init__(self, vname, env=None):
        self.env = env
        self.vname = vname

        if self.env != None:
            self.check()

    
    def check(self):
        var_exists(self.vname, self.env)
        assert self.env.get_varinfo(self.vname)['type'] == uint64_t
        is_writeable(self.vname, self.env)


    def get_generated_code(self):
        gc = GeneratedCode()
        vi = self.env.get_varinfo(self.vname)
        gc.get_apply().writeln('{} = (bit<64>) istd.ingress_timestamp;'.format(vi['handle']))
        return gc

    
    def execute(self, test_env):
        pass


class Digest(Command):
    def __init__(self, values, keys, env=None):
        self.values=values
        self.keys=keys
        self.env = env


    def check(self):
        pass


    def get_generated_code(self):
        self.values = [(self.env.get_varinfo(value)["handle"], self.env.get_varinfo(value)["type"]) for value in self.values]
        gc = GeneratedCode()
        names = [
            (name.split(".")[-1] + "_" + str(UID.get()), given_type)
            for name, given_type, in self.values
        ]
        self.digest_name, digest_code = gen_struct(names, "generated_digest")
        self.digest_metadata_name = f"digest_matadata_{UID.get()}"
        self.digest_instance_name = "Instance_"+self.digest_name
        print(self.digest_name)
        gc.get_or_create("deparser_declaration").writeln(
            "Digest<{}>() {};".format(self.digest_name, self.digest_instance_name)
        )
        gc.get_headers().write(digest_code)
        gc.get_headers().write('#define DIGEST')
        gc.get_or_create("metadata").writeln(f"{self.digest_name} {self.digest_metadata_name};")
        gc.get_or_create("metadata").writeln(f"bool digest;")
        gc.get_or_create("deparser_apply").writeln("if (meta.digest) {")
        gc.get_or_create("deparser_apply").writeln(
            "{}.pack(meta.{});".format(self.digest_instance_name, self.digest_metadata_name)
        )
        gc.get_or_create("deparser_apply").writeln("}")



        return gc