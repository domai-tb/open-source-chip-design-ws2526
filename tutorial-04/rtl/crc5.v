// CRC-5 with polynomial 0x25 (x^5 + x^2 + 1), MSB-first, initial value 0.
// Feed one data bit per cycle on din (MSB first).
module crc5_0x25_msb (
    input  wire       clk,
    input  wire       rst,   // active-low async reset
    input  wire       en,      // advance by one bit when high
    input  wire       din,     // incoming data bit (MSB-first)
    output reg  [4:0] crc      // current CRC value
);
  
  wire fb;
  assign fb = crc[4] ^ din;

  always @(posedge clk) begin
    if(rst) begin
        crc <= 0; // seed value
    end else if(en) begin
        /* verilator lint_off WIDTHEXPAND */
        crc <= {
            // Bit by Bit describtion
            crc[3],
            crc[2] ^ fb,
            crc[1],
            fb
        };
    end
  end

endmodule
