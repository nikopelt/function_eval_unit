/*
* Integer - Fractional seperator module
**/
module sep #(parameter INTEGER = 8, parameter FRACTIONAL = 24)(
	input logic[INTEGER + FRACTIONAL - 1:0] fixed_point,

	output logic[INTEGER-1:0] I,
	output logic[FRACTIONAL-1:0] F
);
	

	assign I = fixed_point[INTEGER + FRACTIONAL - 1: FRACTIONAL];
	assign F = fixed_point[FRACTIONAL - 1:0];

endmodule

