#! /usr/bin/env python
# encoding: utf-8
# Harald Klimach 2018

import sys
import os

def append_modpaths(ctx):
    ''' Add directories with Python modules for waf to sys.path. '''
    myabspath = ctx.path.abspath()
    extabspath = os.path.join(myabspath, 'external', 'fypp')
    if not myabspath in sys.path:
        sys.path.append(myabspath)
    if not extabspath in sys.path:
        sys.path.append(extabspath)


def options(opt):
    ''' Additional modules when loading options. '''
    append_modpaths(opt)


def preconfigure(conf):
    ''' Some settings that commonly neeed to be applied before configuration. '''
    append_modpaths(conf)

    # Recompilation if any of these change
    conf.vars = ['FC_NAME', 'FC_VERSION', 'FCFLAGS']


def postconfigure(conf):
    ''' Common settings that need to be applied after configuration. '''
    from fortran_compiler import set_fc_flags

    osfcflags = conf.env.FCFLAGS

    # Flags for the default (production) variant
    set_fc_flags(conf, ['optimize', 'warn'], osfcflags)

    # Set flags for the debug variant
    conf.setenv('debug',conf.env)
    set_fc_flags(conf, ['standard', 'warn', 'w2e', 'debug'],
                 osfcflags)


def build(bld):
    ''' Make additional modules available during build and enable
        pretty printed commands available.
    '''
    append_modpaths(bld)

    if bld.options.print_cmds:
        import waflib.extras.print_commands
    if bld.cmd == 'docu':
        bld.env.FYPP_LINENUM_FLAG = []


from waflib.Build import BuildContext
class ford(BuildContext):
   "Build FORD documentation"
   cmd     = 'docu'
   variant = 'ford'
   fun     = 'build'
