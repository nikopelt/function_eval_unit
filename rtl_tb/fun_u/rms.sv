/*
* RMS x^2 output module
**/
module rms #(parameter type dtype = logic[31:0], parameter SIZE = 32, parameter INTEGER = 8, parameter FRACTIONAL = 24)(
	input dtype x,
	
	output dtype y
);

dtype mul_x;

assign mul_x = x[SIZE - 1] ? (~x + 1) : x;

fixed_mul #(.dtype(dtype), .INTEGER(INTEGER), .FRACTIONAL(FRACTIONAL)) fm(.inA(mul_x), .inB(mul_x), .out(y));

endmodule
