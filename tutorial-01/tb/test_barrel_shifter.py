import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test_barrel_shifter(dut):
    """Test barrel shifter with comprehensive test cases"""

    # Test vectors: (data_in, shift_amt, direction, expected_out, description)
    # direction: 0=left, 1=right
    test_vectors = [
        # Left shifts with 0b1111
        (0b1111, 0, 0, 0b1111, "0b1111 << 0"),
        (0b1111, 1, 0, 0b1110, "0b1111 << 1"),
        (0b1111, 2, 0, 0b1100, "0b1111 << 2"),
        (0b1111, 3, 0, 0b1000, "0b1111 << 3"),

        # Right shifts with 0b1111
        (0b1111, 0, 1, 0b1111, "0b1111 >> 0"),
        (0b1111, 1, 1, 0b0111, "0b1111 >> 1"),
        (0b1111, 2, 1, 0b0011, "0b1111 >> 2"),
        (0b1111, 3, 1, 0b0001, "0b1111 >> 3"),

        # Left shifts with 0b1010
        (0b1010, 0, 0, 0b1010, "0b1010 << 0"),
        (0b1010, 1, 0, 0b0100, "0b1010 << 1"),
        (0b1010, 2, 0, 0b1000, "0b1010 << 2"),
        (0b1010, 3, 0, 0b0000, "0b1010 << 3"),

        # Right shifts with 0b1010
        (0b1010, 0, 1, 0b1010, "0b1010 >> 0"),
        (0b1010, 1, 1, 0b0101, "0b1010 >> 1"),
        (0b1010, 2, 1, 0b0010, "0b1010 >> 2"),
        (0b1010, 3, 1, 0b0001, "0b1010 >> 3"),

        # Overflow: Left shifts >= 4 with 0b1111 (should output 0b0000)
        (0b1111, 4, 0, 0b0000, "0b1111 << 4 (overflow)"),
        (0b1111, 5, 0, 0b0000, "0b1111 << 5 (overflow)"),
        (0b1111, 6, 0, 0b0000, "0b1111 << 6 (overflow)"),
        (0b1111, 7, 0, 0b0000, "0b1111 << 7 (overflow)"),

        # Overflow: Right shifts >= 4 with 0b1111 (should output 0b0000)
        (0b1111, 4, 1, 0b0000, "0b1111 >> 4 (overflow)"),
        (0b1111, 5, 1, 0b0000, "0b1111 >> 5 (overflow)"),
        (0b1111, 6, 1, 0b0000, "0b1111 >> 6 (overflow)"),
        (0b1111, 7, 1, 0b0000, "0b1111 >> 7 (overflow)"),

        # Overflow: Additional pattern tests with 0b1010
        (0b1010, 4, 0, 0b0000, "0b1010 << 4 (overflow)"),
        (0b1010, 7, 0, 0b0000, "0b1010 << 7 (overflow)"),
        (0b1010, 4, 1, 0b0000, "0b1010 >> 4 (overflow)"),
        (0b1010, 7, 1, 0b0000, "0b1010 >> 7 (overflow)"),
    ]

    for i, (data_in, shift_amt, direction, expected_out, desc) in enumerate(test_vectors):
        # Apply inputs
        dut.data_in.value = data_in
        dut.shift_amt.value = shift_amt
        dut.direction.value = direction

        # Wait for combinatorial logic to settle
        await Timer(1, unit='ns')

        # Check output
        actual_out = int(dut.data_out.value)

        # Direction string for logging
        dir_str = "left" if direction == 0 else "right"

        # Log test case
        dut._log.info(
            f"Test {i+1}: {desc} = 0b{actual_out:04b} "
            f"(shift {dir_str} by {shift_amt})"
        )

        # Assert correct output
        assert actual_out == expected_out, \
            f"Output mismatch: expected 0b{expected_out:04b}, got 0b{actual_out:04b}"

        # Waveform spacing
        await Timer(5, unit='ns')

    dut._log.info("All test cases passed!")
