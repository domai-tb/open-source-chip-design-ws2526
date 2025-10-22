// traffic_light_fsm.v
module traffic_light_fsm(
    input  wire clk,
    input  wire rst,     // async high reset
    input  wire tick,    // 1-cycle pulse = "advance time"
    output reg  red,
    output reg  yellow,
    output reg  green
);



endmodule
