module counter_8bit (
    input  wire       clk,
    input  wire       reset,
    input  wire       enable,
    output reg  [7:0] count
);

wire [7:0] adder_out;

adder_8bit adder (
    .a(count),
    .b(8'd1), // 8 bit number one
    .cin(1'b0),
    .sum(adder_out),
    .cout()
);

// Important to add the posedge
always @(posedge clk) begin
    if(reset) 
        count <= 8'd0;
    else if (enable)
        count <= adder_out; 
end

endmodule
