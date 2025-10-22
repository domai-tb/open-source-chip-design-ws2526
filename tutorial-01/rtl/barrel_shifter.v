module barrel_shifter (
    input  wire [3:0] data_in,
    input  wire [2:0] shift_amt,
    input  wire       direction,
    output reg  [3:0] data_out
);

    // Combinational logic using always block
    always @(*) begin
        if (direction == 1'b0) begin
            // Left shift
            case (shift_amt)
                3'b000: data_out = data_in;                    // No shift
                3'b001: data_out = {data_in[2:0], 1'b0};       // Shift left by 1
                3'b010: data_out = {data_in[1:0], 2'b00};      // Shift left by 2
                3'b011: data_out = {data_in[0], 3'b000};       // Shift left by 3
                default: data_out = 4'b0000;                   // Shifts 4-7 overflow to 0
            endcase
        end else begin
            // Right shift
            case (shift_amt)
                3'b000: data_out = data_in;                    // No shift
                3'b001: data_out = {1'b0, data_in[3:1]};       // Shift right by 1
                3'b010: data_out = {2'b00, data_in[3:2]};      // Shift right by 2
                3'b011: data_out = {3'b000, data_in[3]};       // Shift right by 3
                default: data_out = 4'b0000;                   // Shifts 4-7 overflow to 0
            endcase
        end
    end

endmodule
