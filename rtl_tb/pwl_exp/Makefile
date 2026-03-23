# Makefile

# defaults
SIM ?= verilator
WAVES?= 1
EXTRA_ARGS = --trace --trace-fst
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(PWD)/expu.sv
VERILOG_SOURCES += $(PWD)/mem_read.sv
VERILOG_SOURCES += $(PWD)/frac_mul.sv
VERILOG_SOURCES += $(PWD)/sep.sv
VERILOG_SOURCES += $(PWD)/log2e.sv

COCOTB_TOPLEVEL = expu 

COCOTB_TEST_MODULES = tb

include $(shell cocotb-config --makefiles)/Makefile.sim

wave:
	gtkwave dump.fst waves.gtkw > /dev/null 2>&1 &
