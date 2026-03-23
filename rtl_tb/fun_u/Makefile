# Makefile

SIM ?= verilator
WAVES?= 1
EXTRA_ARGS = --trace --trace-fst
TOPLEVEL_LANG ?= verilog


VERILOG_SOURCES += $(PWD)/fun_u.sv

# FUNCTION DECODER - MULTIPLEXER
VERILOG_SOURCES += $(PWD)/fun_dec.sv
VERILOG_SOURCES += $(PWD)/fun_mux.sv

# SOFTMAX UNIT
VERILOG_SOURCES += $(PWD)/softmax_u.sv
VERILOG_SOURCES += $(PWD)/../pwl_exp/*.sv

# RMS UNIT
VERILOG_SOURCES += $(PWD)/rms_u.sv
VERILOG_SOURCES += $(PWD)/../log_u/*.sv

# SIGMOID UNIT
VERILOG_SOURCES += $(PWD)/sigmoid_u.sv
VERILOG_SOURCES += $(PWD)/../pwl_sigmoid/*.sv

COCOTB_TOPLEVEL = fun_u 

COCOTB_TEST_MODULES = tb_fun_u


include $(shell cocotb-config --makefiles)/Makefile.sim

wave:
	gtkwave dump.fst waves.gtkw > /dev/null 2>&1 &
