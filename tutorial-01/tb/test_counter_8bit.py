import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock


@cocotb.test()
async def test_counter_8bit(dut):
    """Test 8-bit counter with reset, enable, and wrap-around"""

    # Start clock (10ns period = 100MHz)
    clock = Clock(dut.clk, 10, unit='ns')
    cocotb.start_soon(clock.start())

    # Test 1: Reset on startup
    dut.reset.value = 1
    dut.enable.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, unit='ns')
    assert dut.count.value == 0, f"Reset failed: count = {dut.count.value}"
    dut._log.info("Test 1: Reset to 0 ✓")

    # Test 2: Count with enable (0 -> 1 -> 2 -> ... -> 9)
    dut.reset.value = 0
    dut.enable.value = 1

    for expected in range(1, 10):
        await RisingEdge(dut.clk)
        await Timer(1, unit='ns')
        actual = int(dut.count.value)
        assert actual == expected, f"Count mismatch: expected {expected}, got {actual}"
        dut._log.info(f"Test 2: Count = {actual} ✓")

    # Test 3: Hold when enable is low
    current_count = int(dut.count.value)
    dut.enable.value = 0

    for _ in range(5):
        await RisingEdge(dut.clk)
        await Timer(1, unit='ns')
        actual = int(dut.count.value)
        assert actual == current_count, f"Hold failed: count changed from {current_count} to {actual}"

    dut._log.info(f"Test 3: Hold at {current_count} for 5 cycles ✓")

    # Test 4: Resume counting
    dut.enable.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, unit='ns')
    actual = int(dut.count.value)
    expected = current_count + 1
    assert actual == expected, f"Resume failed: expected {expected}, got {actual}"
    dut._log.info(f"Test 4: Resume counting from {current_count} to {actual} ✓")

    # Test 5: Reset during operation
    dut.reset.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, unit='ns')
    assert dut.count.value == 0, f"Mid-operation reset failed"
    dut._log.info("Test 5: Reset during operation ✓")

    # Test 6: Wrap-around from 255 to 0
    # Reset and count up to 254
    dut.reset.value = 1
    await RisingEdge(dut.clk)
    dut.reset.value = 0
    dut.enable.value = 1

    # Fast forward to 254
    for i in range(1, 255):
        await RisingEdge(dut.clk)
    await Timer(1, unit='ns')
    assert dut.count.value == 254, f"Expected 254, got {dut.count.value}"
    dut._log.info("Test 6a: Count = 254 ✓")

    # 254 -> 255
    await RisingEdge(dut.clk)
    await Timer(1, unit='ns')
    assert dut.count.value == 255, f"Expected 255, got {dut.count.value}"
    dut._log.info("Test 6b: Count = 255 ✓")

    # 255 -> 0 (wrap-around)
    await RisingEdge(dut.clk)
    await Timer(1, unit='ns')
    assert dut.count.value == 0, f"Wrap-around failed: expected 0, got {dut.count.value}"
    dut._log.info("Test 6c: Wrap-around 255 -> 0 ✓")

    # 0 -> 1
    await RisingEdge(dut.clk)
    await Timer(1, unit='ns')
    assert dut.count.value == 1, f"Post-wrap failed: expected 1, got {dut.count.value}"
    dut._log.info("Test 6d: After wrap: 0 -> 1 ✓")

    dut._log.info("All tests passed!")
