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


def configure(conf):
    ''' Make additional modules available during config. '''

    append_modpaths(conf)

    # Recompilation if any of these change
    conf.vars = ['FC_NAME', 'FC_VERSION', 'FCFLAGS']


def build(bld):
    ''' Make additional modules available during build and enable
        pretty printed commands available.
    '''
    append_modpaths(bld)
    if bld.options.print_cmds:
        import waflib.extras.print_commands
