import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test_adder_8bit(dut):
    """Test 8-bit adder with directed test cases"""

    # Test vectors: (a, b, cin, expected_sum, expected_cout)
    test_vectors = [
        (0x00, 0x00, 0, 0x00, 0),  # All zeros
        (0x01, 0x01, 0, 0x02, 0),  # Simple addition
        (0x0F, 0x01, 0, 0x10, 0),  # Carry propagation across nibble
        (0xFF, 0x00, 0, 0xFF, 0),  # Maximum value
        (0xFF, 0x01, 0, 0x00, 1),  # Overflow case
        (0xFF, 0xFF, 0, 0xFE, 1),  # Full carry chain
        (0xFF, 0xFF, 1, 0xFF, 1),  # With carry in
        (0xAA, 0x55, 0, 0xFF, 0),  # Alternating bits pattern
        (0x12, 0x34, 0, 0x46, 0),  # Random test case
        (0x80, 0x80, 0, 0x00, 1),  # Signed overflow demonstration
    ]

    for i, (a, b, cin, expected_sum, expected_cout) in enumerate(test_vectors):
        # Apply inputs
        dut.a.value = a
        dut.b.value = b
        dut.cin.value = cin

        # Wait for combinatorial logic to settle
        await Timer(1, unit='ns')

        # Check outputs
        actual_sum = int(dut.sum.value)
        actual_cout = int(dut.cout.value)

        # Log the test case with hex formatting
        dut._log.info(
            f"Test {i+1}: 0x{a:02X} + 0x{b:02X} + {cin} = 0x{actual_sum:02X}, cout={actual_cout}"
        )

        # Assert correct outputs
        assert actual_sum == expected_sum, \
            f"Sum mismatch: expected 0x{expected_sum:02X}, got 0x{actual_sum:02X}"
        assert actual_cout == expected_cout, \
            f"Carry out mismatch: expected {expected_cout}, got {actual_cout}"

        # Wait a bit more for waveform clarity
        await Timer(5, unit='ns')

    dut._log.info("All test cases passed!")
