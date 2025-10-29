# File: test_clk_divider_prog.py
# cocotb 2.0 testbench for clk_divider_prog
# Run with: make SIM=icarus (or verilator), see Makefile snippet below.

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles

CLK_PERIOD_NS = 10  # 100 MHz clock for simulation convenience

async def sync_reset(dut):
    """Synchronous, active-high reset for 2 cycles."""
    dut.rst.value = 1
    await ClockCycles(dut.clk, 2)
    dut.rst.value = 0
    # Give one extra cycle for everything to settle
    await ClockCycles(dut.clk, 1)

async def measure_one_period(dut):
    """
    Measure one full output period in units of input clock cycles.
    Returns (period_cycles, high_cycles, low_cycles).
    """
    # Align to a rising edge of the divided clock
    # Wait until it is low, then catch a rising edge to start a fresh period.
    # (This avoids corner cases right after reset or DIV changes.)
    # Guard: ensure we sample on clock edges (registered signals).
    while int(dut.clk_div.value) != 0:
        await RisingEdge(dut.clk)
    # Start at the rising edge that begins our period
    # (clk_div updates on clk's posedge, so monitoring the signal directly is OK)
    while True:
        await RisingEdge(dut.clk)
        if int(dut.clk_div.value) == 1:
            break

    # Measure high phase
    high_cycles = 1  # Count the cycle where clk_div just became high
    while True:
        await RisingEdge(dut.clk)
        if int(dut.clk_div.value) == 1:
            high_cycles += 1
        else:
            break

    # Measure low phase
    low_cycles = 1  # Count the cycle where clk_div just became low
    while True:
        await RisingEdge(dut.clk)
        if int(dut.clk_div.value) == 0:
            low_cycles += 1
        else:
            break

    period_cycles = high_cycles + low_cycles
    return period_cycles, high_cycles, low_cycles

@cocotb.test()
async def test_all_divisors(dut):
    """Sweep DIV = 0..15 (with 0/1 saturating to 2) and verify period & duty."""
    # Create and start the input clock
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_NS, unit="ns").start())

    await sync_reset(dut)

    test_values = list(range(0, 16))  # 0..15, covers saturation and normal range

    for raw_div in test_values:
        dut.div.value = raw_div

        # Allow a couple of cycles for the new DIV to take effect cleanly
        await ClockCycles(dut.clk, 3)

        # Effective divisor (hardware saturates values <2 to 2)
        div_eff = raw_div if raw_div >= 2 else 2

        # Measure a few consecutive periods to be safe/stable
        for _ in range(2):
            period, high_cyc, low_cyc = await measure_one_period(dut)

            assert period == div_eff, (
                f"DIV={raw_div} (eff {div_eff}): expected period {div_eff}, got {period}"
            )

            expected_high = div_eff // 2
            expected_low  = div_eff - expected_high

            assert high_cyc == expected_high, (
                f"DIV={raw_div} (eff {div_eff}): expected high {expected_high}, got {high_cyc}"
            )
            assert low_cyc == expected_low, (
                f"DIV={raw_div} (eff {div_eff}): expected low {expected_low}, got {low_cyc}"
            )

@cocotb.test()
async def test_dynamic_change(dut):
    """Change DIV on the fly and ensure the new period takes effect."""
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_NS, unit="ns").start())
    await sync_reset(dut)

    # Start at DIV=6 (even)
    dut.div.value = 6
    await ClockCycles(dut.clk, 5)
    p1, _, _ = await measure_one_period(dut)
    assert p1 == 6

    # Change to DIV=9 (odd)
    dut.div.value = 9
    await ClockCycles(dut.clk, 5)
    p2, h2, l2 = await measure_one_period(dut)
    assert p2 == 9
    assert h2 == 9 // 2 and l2 == 9 - (9 // 2)

