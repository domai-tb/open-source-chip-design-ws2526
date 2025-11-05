import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock


@cocotb.test()
async def test_crc5_basic(dut):
    """Test CRC-5 with a simple data pattern"""

    # Start the clock (10ns period = 100 MHz)
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    # Reset the module
    dut.rst.value = 1
    dut.en.value = 0
    dut.din.value = 0
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)

    # Verify CRC is initialized to 0
    assert dut.crc.value == 0, f"CRC should be 0 after reset, got {dut.crc.value}"
    dut._log.info(f"After reset: CRC = {int(dut.crc.value):05b}")

    # Test data: 8 bits = 0xA5 = 10100101 (MSB-first)
    test_data = [1, 0, 1, 0, 0, 1, 0, 1]

    # Feed data bits one by one
    dut.en.value = 1
    for i, bit in enumerate(test_data):
        dut.din.value = bit
        await RisingEdge(dut.clk)
        dut._log.info(f"Bit {i}: din={bit}, CRC = {int(dut.crc.value):05b} (0x{int(dut.crc.value):02X})")

    # Clock one more cycle to allow final CRC to settle
    await RisingEdge(dut.clk)
    dut._log.info(f"After final clock: CRC = {int(dut.crc.value):05b} (0x{int(dut.crc.value):02X})")

    # Expected CRC-5 value for 0xA5 with polynomial 0x25
    # Calculated using standard CRC-5 algorithm
    expected_crc = 0x0E  # This is 0b01110

    # Check final CRC value
    actual_crc = int(dut.crc.value)
    dut._log.info(f"Final CRC: expected={expected_crc:05b}, actual={actual_crc:05b}")
    assert actual_crc == expected_crc, f"CRC mismatch: expected {expected_crc:05b}, got {actual_crc:05b}"

    dut._log.info("Test passed!")
