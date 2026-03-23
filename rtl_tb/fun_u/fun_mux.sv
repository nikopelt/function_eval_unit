/*
* Function output multiplexer
**/
module fun_mux #(parameter type dtype = logic[31:0], parameter BLOCK_SIZE = 64)(
	input logic clk,
	input logic rst,
	
	input logic en_sfmx,
	input logic en_rms,
	input logic en_sgmd,

	input dtype identity_y	[BLOCK_SIZE - 1:0],
	input dtype softmax_y		[BLOCK_SIZE - 1:0],
	input dtype RMS_y				[BLOCK_SIZE - 1:0],
	input dtype sigmoid_y		[BLOCK_SIZE - 1:0],
	
	output dtype fun_u_out	[BLOCK_SIZE - 1:0]
);


dtype z[BLOCK_SIZE - 1:0];
always_comb begin
	for(int i = 0; i < BLOCK_SIZE; i ++) begin
		z[i] = '0;
	end
end

assign fun_u_out = ((~en_sfmx) & (~en_rms) & (~en_sgmd)) ? identity_y : 
									 (  en_sfmx  & (~en_rms) & (~en_sgmd)) ? softmax_y :
									 ((~en_sfmx) &   en_rms  & (~en_sgmd)) ? RMS_y :
									 ((~en_sfmx) & (~en_rms) &   en_sgmd ) ? sigmoid_y : z;

endmodule
