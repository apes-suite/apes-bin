set -x
UTESTS=$PWD/tools/utest_results.py
SEQF=$PWD/tools/command_sequence.py
FORD=$PWD/tools/make_fordoc.py
bindir=$PWD

TOOLS=c_bgxlc,c_nec,doxygen,eclipse,fc_nag,fc_nec,fc_nfort,fc_bgxlf,fc_cray,fc_open64,fc_pgfortran,fc_solstudio,fc_xlf,print_commands,$UTESTS,$SEQF,$FORD
cd external/waf-2.0.14 && ./waf-light --make-waf --prelude='' --tools=$TOOLS && cp waf $bindir && cd -
