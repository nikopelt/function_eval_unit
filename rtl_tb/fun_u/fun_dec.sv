/*
* Function Input Decoder Module
**/
module fun_dec #(parameter type dtype = logic[31:0], parameter BLOCK_SIZE = 64) (
	input logic clk,
	input logic rst,
	
	input dtype x						[BLOCK_SIZE - 1:0],

	input logic en_sfmx,
	input logic en_rms,
	input logic en_sgmd,
	
	output dtype identity_x	[BLOCK_SIZE - 1:0], 
	output dtype softmax_x	[BLOCK_SIZE - 1:0], 
	output dtype RMS_x			[BLOCK_SIZE - 1:0], 
	output dtype sigmoid_x	[BLOCK_SIZE - 1:0] 

);

dtype z[BLOCK_SIZE - 1:0];

always_comb begin
	for(int i = 0; i < BLOCK_SIZE; i++) begin
		z[i] = '0;
	end
end

assign identity_x = ((~en_sfmx) & (~en_rms) & (~en_sgmd)) ? x : z;
assign softmax_x  =	 (en_sfmx   & (~en_rms) & (~en_sgmd)) ? x : z;
assign RMS_x      = ((~en_sfmx) &   en_rms  & (~en_sgmd)) ? x : z;
assign sigmoid_x  = ((~en_sfmx) & (~en_rms) &	 en_sgmd )  ? x : z;


endmodule 
