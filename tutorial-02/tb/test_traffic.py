# test_traffic_light_fsm.py
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

async def apply_tick(dut):
    """Apply a single tick pulse: high for 1 cycle, low for 1 cycle, then wait for outputs to settle."""
    dut.tick.value = 1
    await RisingEdge(dut.clk)
    dut.tick.value = 0
    await RisingEdge(dut.clk)
    # Extra clock cycle to ensure outputs have fully updated after any state transition
    await RisingEdge(dut.clk)

async def check_state(dut, expected_red, expected_yellow, expected_green, msg=""):
    """Check that outputs match expected values and are one-hot encoded."""
    r = int(dut.red.value)
    y = int(dut.yellow.value)
    g = int(dut.green.value)

    # Verify one-hot encoding
    assert (r + y + g) == 1, f"{msg}: Not one-hot - R={r}, Y={y}, G={g}"

    # Verify expected state
    assert (r, y, g) == (expected_red, expected_yellow, expected_green), (
        f"{msg}: Expected R={expected_red}, Y={expected_yellow}, G={expected_green} "
        f"but got R={r}, Y={y}, G={g}"
    )
    dut._log.info(f"{msg}: OK - R={r}, Y={y}, G={g}")

@cocotb.test()
async def test_traffic_light_cycle(dut):
    """Verify RED->GREEN->YELLOW->RED sequence with correct tick durations."""

    # Start clock (fix deprecation warning)
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    # Reset
    dut.tick.value = 0
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)

    # After reset: should be in RED
    await check_state(dut, 1, 0, 0, "After reset")

    # RED state: 4 ticks total before transition to GREEN
    # Ticks 1-3: stay in RED
    await apply_tick(dut)
    await check_state(dut, 1, 0, 0, "RED - tick 1/4")

    await apply_tick(dut)
    await check_state(dut, 1, 0, 0, "RED - tick 2/4")

    await apply_tick(dut)
    await check_state(dut, 1, 0, 0, "RED - tick 3/4")

    # Tick 4: transition to GREEN
    await apply_tick(dut)
    await check_state(dut, 0, 0, 1, "RED->GREEN transition (tick 4/4)")

    # GREEN state: 5 ticks total before transition to YELLOW
    # Ticks 1-4: stay in GREEN
    await apply_tick(dut)
    await check_state(dut, 0, 0, 1, "GREEN - tick 1/5")

    await apply_tick(dut)
    await check_state(dut, 0, 0, 1, "GREEN - tick 2/5")

    await apply_tick(dut)
    await check_state(dut, 0, 0, 1, "GREEN - tick 3/5")

    await apply_tick(dut)
    await check_state(dut, 0, 0, 1, "GREEN - tick 4/5")

    # Tick 5: transition to YELLOW
    await apply_tick(dut)
    await check_state(dut, 0, 1, 0, "GREEN->YELLOW transition (tick 5/5)")

    # YELLOW state: 2 ticks total before transition to RED
    # Tick 1: stay in YELLOW
    await apply_tick(dut)
    await check_state(dut, 0, 1, 0, "YELLOW - tick 1/2")

    # Tick 2: transition back to RED (complete the cycle)
    await apply_tick(dut)
    await check_state(dut, 1, 0, 0, "YELLOW->RED transition (tick 2/2)")

    dut._log.info("Traffic light FSM passed full cycle test!")
