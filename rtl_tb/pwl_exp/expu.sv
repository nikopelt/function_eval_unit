/*
* System verilog module to compute the fixed point exponential of a fixed point input using pwl  
**/
module expu #(parameter type dtype = logic[31:0], parameter SEGMENTS = 32, 
							parameter INTEGER  = 8, parameter FRACTIONAL = 24, parameter ADDR_BITS = 5)(
	input logic clk,
	input logic rst,
	input dtype x,


	output dtype exp_x
);
	
	dtype k[SEGMENTS - 1:0];
	dtype b[SEGMENTS - 1:0];
	dtype y;
	dtype mul_res;
	dtype f_inter;
	logic[ADDR_BITS - 1:0] addr;
	logic[INTEGER-1:0] I;
	logic[FRACTIONAL - 1:0] F;

	
	mem_read #(.dtype(dtype), .SEGMENTS(SEGMENTS)) mr(.k(k), .b(b));
	log2e #(.dtype(dtype)) l2e(.x(x), .y(y));	
	frac_mul #(.dtype(dtype), .INTEGER(INTEGER), .FRACTIONAL(FRACTIONAL)) mul(.inA(k[addr]), .inB(f_inter),.out(mul_res));
	sep #(.INTEGER(INTEGER), .FRACTIONAL(FRACTIONAL)) sp(.fixed_point(y), .I(I), .F(F));
	
	assign f_inter[FRACTIONAL - 1:0] = F;
	assign addr = F[FRACTIONAL - 1: FRACTIONAL - ADDR_BITS];
	assign exp_x = (b[addr] - mul_res) >> I;
	

endmodule
