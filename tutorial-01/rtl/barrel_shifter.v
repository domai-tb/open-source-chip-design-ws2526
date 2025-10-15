module barrel_shifter (
    input  wire [3:0] data_in,
    input  wire [2:0] shift_amt,
    input  wire       direction,
    output reg  [3:0] data_out
);

// check solution from moodle

always @(*) begin
    if (direction == 1'b0) begin
        // Left shift
        case (shift_amt)
            3'b000: data_out = data_in;
            3'b001: data_out = {data_in[2:0], 1'b0};
            // ...  
            default: data_out = 4'b0000; 
        endcase
    end else begin
        // Right shift
        // ...
    end
end

endmodule
