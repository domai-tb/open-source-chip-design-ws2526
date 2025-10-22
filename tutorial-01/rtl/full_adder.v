module full_adder (
    input  wire a,
    input  wire b,
    input  wire cin,
    output wire sum,
    output wire cout
);

    // Internal wires for connecting the two half adders
    wire sum_temp;
    wire carry1;
    wire carry2;

    // First half adder: adds a and b
    half_adder ha1 (
        .a(a),
        .b(b),
        .sum(sum_temp),
        .carry(carry1)
    );

    // Second half adder: adds sum_temp and cin
    half_adder ha2 (
        .a(cin),
        .b(sum_temp),
        .sum(sum),
        .carry(carry2)
    );

    // Final carry out is OR of both carries
    assign cout = carry1 | carry2;

endmodule