// File: clk_divider_prog.v
// Simple programmable clock divider: divides clk by DIV in [2..15].
// Single synchronous process with active-high reset.
// For odd DIV, output duty is floor(DIV/2) high, ceil(DIV/2) low per period.

`timescale 1ns/1ps

module clk_divider_prog (
    input  wire       clk,     // system clock
    input  wire       rst,     // synchronous, active-high reset
    input  wire [3:0] div,     // requested divide value (1..15). <2 saturates to 2.
    output reg        clk_div  // divided clock
);

reg [3:0] cnt;
reg [3:0] div_eff;

always @(posedge clk ) begin
    if (rst) begin
        cnt <= 4'd0;
        clk_div <= 1'b0;
        div_eff <= 4'd2;
    end

    if (div < 4'd2)
        div_eff <= 4'd2;
    else
        div_eff <= div;

    if (cnt >= (div_eff-1)) 
        cnt <= 4'd0;
    else
        cnt <= cnt + 4'd1;

    if (cnt < (div_eff >> 1))
        clk_div <= 1'b1;
    else 
        clk_div <= 1'b0; 
end


endmodule

