/*
*	Exponent output and Softmax normalizer output module
**/
module softmax_u #(parameter type dtype = logic[31:0], parameter BLOCK_SIZE = 64, parameter SEGMENTS = 32,
									 parameter INTEGER = 8, parameter FRACTIONAL = 24, parameter ADDR_BITS = 5)(
	input logic clk,
	input logic rst,
	
	input dtype x	[BLOCK_SIZE - 1:0],


	output dtype y[BLOCK_SIZE - 1:0],
	output dtype stat
);

dtype south[BLOCK_SIZE - 1:0];
genvar i;
generate
	for(i = 0; i < BLOCK_SIZE; i++) begin 
		expu #(.dtype(dtype), .SEGMENTS(SEGMENTS), .INTEGER(INTEGER), .FRACTIONAL(FRACTIONAL), .ADDR_BITS(ADDR_BITS)) eu(.clk(clk), .rst(rst), .x(x[i]), .exp_x(y[i]));
		if (i == 0) begin
			systolic_stat #(.dtype(dtype)) sys_stat(.clk(clk), .rst(rst), .north('0), .west(y[i]), .south(south[i]));
		end else begin
			systolic_stat #(.dtype(dtype)) sys_stat(.clk(clk), .rst(rst), .north(south[i-1]), .west(y[i]), .south(south[i]));
		end
	end
endgenerate

assign stat = south[BLOCK_SIZE - 1];

endmodule
