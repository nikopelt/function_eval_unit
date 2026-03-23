/*
* RMS output and Normalizer output module
**/
module rms_u #(parameter type dtype = logic[31:0], parameter BLOCK_SIZE = 64, parameter SIZE = 32, parameter INTEGER = 8, parameter FRACTIONAL = 24)(

	input logic clk,
	input logic rst,
	
	input dtype x	[BLOCK_SIZE - 1:0],

	output dtype y[BLOCK_SIZE - 1:0],
	output dtype stat
);


dtype norm;
dtype RMS		[BLOCK_SIZE - 1:0];
genvar i;
dtype south	[BLOCK_SIZE + 1];

generate 
	for(i = 0; i < BLOCK_SIZE; i++) begin
		rms #(.dtype(dtype), .SIZE(SIZE), .INTEGER(INTEGER), .FRACTIONAL(FRACTIONAL)) rmsu(.x(x[i]), .y(RMS[i]));	
		systolic_stat #(.dtype(dtype)) sys_stat(.clk(clk), .rst(rst), .north(south[i]), .west(RMS[i]), .south(south[i+1]));
	end
endgenerate

log_sqr #(.dtype(dtype), .SIZE(SIZE), .INTEGER(INTEGER), .FRACTIONAL(FRACTIONAL)) ls(.clk(clk), .x(south[BLOCK_SIZE]), .sqr_x(norm));

assign south[0] = 0;
assign stat = norm;
assign y = x;


endmodule
