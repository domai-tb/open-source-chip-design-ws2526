import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test_full_adder(dut):
    """Test full adder with all possible input combinations"""

    # Test vectors: (a, b, cin, expected_sum, expected_cout)
    test_vectors = [
        (0, 0, 0, 0, 0),
        (0, 0, 1, 1, 0),
        (0, 1, 0, 1, 0),
        (0, 1, 1, 0, 1),
        (1, 0, 0, 1, 0),
        (1, 0, 1, 0, 1),
        (1, 1, 0, 0, 1),
        (1, 1, 1, 1, 1),
    ]

    for i, (a, b, cin, expected_sum, expected_cout) in enumerate(test_vectors):
        # Apply inputs
        dut.a.value = a
        dut.b.value = b
        dut.cin.value = cin

        # Wait for combinatorial logic to settle
        await Timer(1, unit='ns')

        # Check outputs
        actual_sum = dut.sum.value
        actual_cout = dut.cout.value

        # Log the test case
        dut._log.info(f"Test {i+1}: a={a}, b={b}, cin={cin} -> sum={actual_sum}, cout={actual_cout}")

        # Assert correct outputs
        assert actual_sum == expected_sum, f"Sum mismatch: expected {expected_sum}, got {actual_sum}"
        assert actual_cout == expected_cout, f"Carry out mismatch: expected {expected_cout}, got {actual_cout}"

        # Wait a bit more for waveform clarity
        await Timer(5, unit='ns')

    dut._log.info("All test cases passed!")