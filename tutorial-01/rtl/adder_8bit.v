module adder_8bit (
    input  wire [7:0] a,
    input  wire [7:0] b,
    input  wire       cin,
    output wire [7:0] sum,
    output wire       cout
);

// 9-value wire
wire [8:0] carry;

// In = First, Out = Last
assign carry[0] = cin;
assign carry[8] = cout;

genvar i;
generate
    for (i = 0; i < 8; i += 1) begin : adder_stage
        full_adder fa(
            .a(a[i]),
            .b(b[i]),
            .cin(carry[i]),
            .sum(sum[i]),
            .cout(carry[i+1])
        );
    end
endgenerate

endmodule
