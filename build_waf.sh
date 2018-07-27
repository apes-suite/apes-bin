set -x
UTESTS=$PWD/tools/utest_results.py
SEQF=$PWD/tools/command_sequence.py
bindir=$PWD

TOOLS=c_bgxlc,c_nec,doxygen,eclipse,fc_nag,fc_nec,fc_bgxlf,fc_cray,fc_open64,fc_pgfortran,fc_solstudio,fc_xlf,print_commands,$UTESTS,$SEQF
cd external/waf-1.9.15 && ./waf-light --make-waf --prelude='' --tools=$TOOLS && cp waf $bindir && cd -
