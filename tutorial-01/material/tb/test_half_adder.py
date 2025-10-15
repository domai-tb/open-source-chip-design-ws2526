import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test_half_adder(dut):
    """Test half adder with all possible input combinations"""

    # Test vectors: (a, b, expected_sum, expected_carry)
    test_vectors = [
        (0, 0, 0, 0),
        (0, 1, 1, 0),
        (1, 0, 1, 0),
        (1, 1, 0, 1),
    ]

    for i, (a, b, expected_sum, expected_carry) in enumerate(test_vectors):
        # Apply inputs
        dut.a.value = a
        dut.b.value = b

        # Wait for combinatorial logic to settle
        await Timer(1, unit='ns')

        # Check outputs
        actual_sum = dut.sum.value
        actual_carry = dut.carry.value

        # Log the test case
        dut._log.info(f"Test {i+1}: a={a}, b={b} -> sum={actual_sum}, carry={actual_carry}")

        # Assert correct outputs
        assert actual_sum == expected_sum, f"Sum mismatch: expected {expected_sum}, got {actual_sum}"
        assert actual_carry == expected_carry, f"Carry mismatch: expected {expected_carry}, got {actual_carry}"

        # Wait a bit more for waveform clarity
        await Timer(5, unit='ns')

    dut._log.info("All test cases passed!")
