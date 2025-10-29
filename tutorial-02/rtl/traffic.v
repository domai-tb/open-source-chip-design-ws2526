// traffic_light_fsm.v
module traffic_light_fsm(
    input  wire clk,
    input  wire rst,     // async high reset
    input  wire tick,    // 1-cycle pulse = "advance time"
    output reg  red,
    output reg  yellow,
    output reg  green
);
  // state encoding
  localparam S_GREEN  = 2'd0,
             S_YELLOW = 2'd1,
             S_RED    = 2'd2;

  reg [1:0] state;
  reg [3:0] timer;   // counts ticks in current state

  always @(posedge clk or posedge rst) begin
    if (rst) begin
      state  <= S_RED;
      timer  <= 4'd0;
      red    <= 1'b1; yellow <= 1'b0; green <= 1'b0;
    end else begin
      case (state)
        S_GREEN: begin
          red <= 1'b0; yellow <= 1'b0; green <= 1'b1;
          if (tick) begin
            if (timer == 4'd4) begin       // 5 ticks green
              state <= S_YELLOW; timer <= 4'd0;
            end else timer <= timer + 1'b1;
          end
        end
        S_YELLOW: begin
          red <= 1'b0; yellow <= 1'b1; green <= 1'b0;
          if (tick) begin
            if (timer == 4'd1) begin       // 2 ticks yellow
              state <= S_RED; timer <= 4'd0;
            end else timer <= timer + 1'b1;
          end
        end
        S_RED: begin
          red <= 1'b1; yellow <= 1'b0; green <= 1'b0;
          if (tick) begin
            if (timer == 4'd3) begin       // 4 ticks red
              state <= S_GREEN; timer <= 4'd0;
            end else timer <= timer + 1'b1;
          end
        end
        default: begin
          state <= S_RED; timer <= 4'd0;
          red <= 1'b1; yellow <= 1'b0; green <= 1'b0;
        end
      endcase
    end
  end
endmodule
