module sgmd_frac_mul #(parameter type dtype = logic[31:0], parameter INTEGER = 8, parameter FRACTIONAL = 24)(
	input dtype inA,
	input dtype inB,
	
	output dtype out
);

logic[2*(INTEGER + FRACTIONAL) - 1:0] result;

assign result = inA*inB; 

assign out = result[2*FRACTIONAL + INTEGER - 1:FRACTIONAL];


endmodule
