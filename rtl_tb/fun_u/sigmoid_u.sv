module sigmoid_u #(parameter type dtype = logic[31:0], parameter BLOCK_SIZE = 64,parameter SEGMENTS = 8, parameter INTEGER = 8, parameter FRACTIONAL = 24)(
	input logic clk,
	input logic rst,
	input dtype x					[BLOCK_SIZE - 1:0],

	output dtype sigma_x	[BLOCK_SIZE - 1:0]
);

genvar i;

generate
	for(i = 0; i < BLOCK_SIZE; i++) begin 
		sigmoid #(.dtype(dtype), .SEGMENTS(SEGMENTS), .INTEGER(INTEGER), .FRACTIONAL(FRACTIONAL), .ADDR_BITS($clog2(SEGMENTS))) sgmd(.clk(clk), .rst(rst), .x(x[i]), .sigma_x(sigma_x[i]));
	end
endgenerate

endmodule
