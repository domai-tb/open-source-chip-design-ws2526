// CRC-5 with polynomial 0x25 (x^5 + x^2 + 1), MSB-first, initial value 0.
// Feed one data bit per cycle on din (MSB first).
module crc5_0x25_msb (
    input  wire       clk,
    input  wire       rst,   // active-low async reset
    input  wire       en,      // advance by one bit when high
    input  wire       din,     // incoming data bit (MSB-first)
    output reg  [4:0] crc      // current CRC value
);
  

endmodule
