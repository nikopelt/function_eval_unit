/*
*	Module to perform multiplication with constant value log2e by shift-and-add
**/
module log2e #(parameter type dtype = logic[31:0])(
	input dtype x,

	output dtype y

);

assign y = x + (x>>1) - (x>>4); 


endmodule
