module adder_8bit (
    input  wire [7:0] a,
    input  wire [7:0] b,
    input  wire       cin,
    output wire [7:0] sum,
    output wire       cout
);

    // Internal carry chain: carry[0] = cin, carry[8] = cout
    wire [8:0] carry;

    // Connect first carry in
    assign carry[0] = cin;

    // Connect final carry out
    assign cout = carry[8];

    // Generate 8 full adder instances using a loop
    genvar i;
    generate
        for (i = 0; i < 8; i = i + 1) begin : adder_stage
            full_adder fa (
                .a(a[i]),
                .b(b[i]),
                .cin(carry[i]),
                .sum(sum[i]),
                .cout(carry[i+1])
            );
        end
    endgenerate

endmodule
