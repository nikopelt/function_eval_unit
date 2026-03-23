/*
*	Comparator Module to compare positive inputs 
*/

module comp #(parameter SIZE = 32) (
	input logic[SIZE - 1:0] in_a,
	input logic[SIZE - 1:0] in_b,

	output logic cmp
);

assign cmp = in_a > in_b; 

endmodule
