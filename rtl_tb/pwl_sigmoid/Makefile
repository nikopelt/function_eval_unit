# Makefile

# defaults
SIM ?= verilator
WAVES?= 1
EXTRA_ARGS = --trace --trace-fst
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(PWD)/sigmoid.sv
VERILOG_SOURCES += $(PWD)/comb_search.sv
VERILOG_SOURCES += $(PWD)/b_search.sv
VERILOG_SOURCES += $(PWD)/sgmd_mem_read.sv
VERILOG_SOURCES += $(PWD)/sgmd_frac_mul.sv
VERILOG_SOURCES += $(PWD)/comp.sv
# use VHDL_SOURCES for VHDL files

# COCOTB_TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
COCOTB_TOPLEVEL = sigmoid	 

# COCOTB_TEST_MODULES is the basename of the Python test file(s)
COCOTB_TEST_MODULES = tb
# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim

wave:
	gtkwave dump.fst waves.gtkw > /dev/null 2>&1 &

coeffs:
	python3 lut.py
