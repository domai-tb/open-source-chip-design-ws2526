# Cocotb-driven build configuration for Verilator simulations

# ============================================================================
# Phony targets
# ============================================================================
.PHONY: all clk_div clean help

# ============================================================================
# User-facing targets (using recursive make to pass variables correctly)
# ============================================================================

# Default target
all: clk_div

# Barrel shifter test: clean then simulate with proper variables
clk_div:
	@$(MAKE) clean > /dev/null 2>&1
	@$(MAKE) sim TOPLEVEL=clk_divider_prog TEST=test_clk_div \
		VERILOG_SOURCES="$(PWD)/rtl/clk_div.v"

# ============================================================================
# Simulation configuration
# ============================================================================

TOPLEVEL_LANG ?= verilog
SIM ?= verilator
COCOTB_TEST_MODULES ?= $(TEST)

# Verilator configuration
# VERILATOR_ROOT = /path/to/verilator
# VERILATOR_BIN_DIR = $(VERILATOR_ROOT)/bin
# PATH := $(VERILATOR_ROOT)/bin:$(PATH)

# Export variables for cocotb
# export VERILATOR_ROOT
# export VERILATOR_BIN_DIR
# export PATH

# Make the testbench package visible
export PYTHONPATH := $(PWD)/tb:$(PYTHONPATH)

# Enable FST waveform tracing for Verilator
ifeq ($(SIM),verilator)
    TRACE_OUTPUT ?= $(PWD)/dump.fst
    COMPILE_ARGS += --trace --trace-structs --trace-fst
    SIM_ARGS += --trace --trace-file $(TRACE_OUTPUT)
endif

# ============================================================================
# Include cocotb's makefile
# ============================================================================

COCOTB_MAKEFILE_DIR := $(shell cocotb-config --makefiles)
ifeq ($(strip $(COCOTB_MAKEFILE_DIR)),)
    $(error Unable to locate cocotb makefiles; ensure cocotb is installed and cocotb-config is on PATH)
endif

include $(COCOTB_MAKEFILE_DIR)/Makefile.sim

# ============================================================================
# Help target
# ============================================================================

help::
	@echo "================================================================"
	@echo "  Chip Design Lecture - Makefile Targets"
	@echo "================================================================"
	@echo ""
	@echo "Available targets:"
	@echo "  make                - Run full adder testbench (default)"
	@echo "  make full_adder     - Run full adder testbench"
	@echo "  make half_adder     - Run half adder testbench"
	@echo "  make adder_8bit     - Run 8-bit adder testbench"
	@echo "  make barrel_shifter - Run barrel shifter testbench"
	@echo "  make counter_8bit   - Run 8-bit counter testbench"
	@echo "  make clean          - Clean build artifacts and waveforms"
	@echo "  make help           - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make half_adder     # Test the half_adder module"
	@echo "  make full_adder     # Test the full_adder module"
	@echo "  make adder_8bit     # Test the 8-bit adder module"
	@echo "  make barrel_shifter # Test the barrel shifter module"
	@echo "  make counter_8bit   # Test the 8-bit counter module"
	@echo ""
	@echo "Output:"
	@echo "  - Test results displayed in console"
	@echo "  - Waveform saved to dump.fst (view with GTKWave)"
	@echo "================================================================"
