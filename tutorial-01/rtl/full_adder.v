module full_adder (
    input  wire a,
    input  wire b,
    input  wire cin,
    output wire sum,
    output wire cout
);

// We could actually do:
//  assign sum = a + b;
// The problem with that is, that we
// don't have any control of the chip design.

wire sum_tmp;
wire carry_tmp;
wire carry2_tmp;

half_adder ha1(
    .a(a),
    .b(b),
    .sum(sum_tmp),
    .carry(carry_tmp)
);

half_adder ha2(
    .a(cin),
    .b(sum_tmp),
    .sum(),
    .carry(carry2_tmp)
);

assign cout = carry2_tmp | carry_tmp;

endmodule