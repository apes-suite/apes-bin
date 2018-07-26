import sys
from waflib import Logs
try:
   import subprocess # If subprocess is available and provides check_output
   # This is working with Python > 2.7.
   # The check on check_output is necessary, because 2.6 provides subprocess
   # put without check_output.
   if getattr(subprocess, 'check_output'):
     use_subproc = True
   else:
     use_subproc = False
except:
   import commands
   use_subproc = False
import datetime
from waflib import Utils

def options(opt):
  opt.add_option('--revision_string', action='store',
                 help='Set the revision string instead of trying to obtain it automatically.')

def configure(conf):
  """ The revision string may be set during configuration. """
  if conf.options.revision_string:
    conf.env.revision_string = conf.options.revision_string

def revision_module_file(bld, projectdir):
  """ Define a revision module describing the project revision and the
      compilation information.

      The revision information is attempted to be taken from mercurial
      in the provided projectdir, but it may be overwritten on the
      command line by explicitly setting it with the option
      --revision_string.
  """

  # Try to find a revision string of the application.
  if bld.env.revision_string:
    solver_rev = bld.env.revision_string
  else:
    solver_rev = 'UNKNOWN'

  # The default revision string may be overwritten by the --revision_string option
  # during the build step.
  if bld.options.revision_string:
    solver_rev = bld.options.revision_string

  if solver_rev == 'UNKNOWN':
    if use_subproc:
      try:
        hg_stat = 0
        hg_out = subprocess.check_output(['hg', 'id', '-i'], cwd=projectdir)
      except subprocess.CalledProcessError as e:
        hg_stat = e.returncode
        hg_out = e.output
      except OSError:
        hg_stat = 1
    else:
      (hg_stat, hg_out) = commands.getstatusoutput('hg id -i', cwd=projectdir)

    if hg_stat == 0:
      if sys.version_info[0] > 2:
        solver_rev = hg_out.split()[-1].decode('ascii')
      else:
        solver_rev = hg_out.split()[-1]
    else:
      # There is no hg, or hg did not find a proper revision.
      # Try to use the node information from .hg_archival.
      import os
      archfile = os.path.join(projectdir, '.hg_archival.txt')
      if os.path.isfile(archpath):
        import re
        arfile = open(archfile, 'r')
        hgnodeline = re.compile('^node:')
        for line in arfile:
          if hgnodeline.match(line):
            solver_rev = line[6:18]
            break
        arfile.close()

  fc_name_str = "".join(bld.env['FC_NAME'])
  fc_version_str = ".".join(bld.env['FC_VERSION'])
  fc_flags_str = " ".join(bld.env['FCFLAGS'])
  link_flags_str = " ".join(bld.env['LINKFLAGS'])
  builddate = datetime.datetime.now().strftime("%Y-%m-%d")

  Logs.warn('Compiler: '+fc_name_str)
  Logs.warn('Version : '+fc_version_str)
  Logs.warn('Flags   : '+fc_flags_str)

  flaglen = len(fc_flags_str)
  nFlagLines = max((flaglen+71) // 72, 1)

  revmod = bld.path.find_or_declare('source/soi_revision_module.f90')

  modtext = """!> SOIL module for holding the revision of the solver
!!
!! This information will be written by soi_world_init.
!! This source file is generated during compilation!
! *************************************************************************** !
! WARNING: Do NOT change this file, as it will be overwritten during
!          compilation.
!          See bin/revision_module.py for the generating script.
!          (in the apes build infrastructure project)
! *************************************************************************** !

module soi_revision_module
  implicit none
  !> The HG revision of the application used for this executable.
  character(len=13), parameter :: soi_solver_revision &
    &                            = '%s'

  !> Name of the compiler.
  character(len=32), parameter :: soi_FC_name &
    &                            = '%s'

  !> The compilation command that was used to build this executable.
  character(len=32), parameter :: soi_FC_command &
    &                            = '%s'

  !> The version of the Fortran compiler used in the compilation of this
  !! executable.
  character(len=32), parameter :: soi_FC_version &
    &                            = '%s'

  !> Number of lines needed to represent the compiler flags
  integer, parameter :: soi_FC_nFlagLines = %i

  !> The Fortran compiler flags used to compile this executable.
  character(len=72), parameter :: soi_FC_flags(soi_FC_nFlagLines) &
""" % (solver_rev, fc_name_str, " ".join(bld.env.FC), fc_version_str,
       nFlagLines)
  tempstr = fc_flags_str[0:72]
  tempstr = tempstr + ' '*(72-len(tempstr))
  modtext = modtext + """    & = [ '%s'""" % (tempstr[0:72])
  for line in range(2,nFlagLines+1):
     tempstr = fc_flags_str[(line-1)*72:line*72]
     tempstr = tempstr + ' '*(72-len(tempstr))
     modtext = modtext + """, &
  &     '%s'""" % (tempstr)
  modtext = modtext + """ ]

  !> The date when this executable was built.
  character(len=10), parameter :: soi_build_date &
    &                            = '%s'
end module soi_revision_module
""" % (builddate)

  revmod.write(modtext)
  revmod.sig = Utils.h_file(revmod.abspath())
  return(revmod)
