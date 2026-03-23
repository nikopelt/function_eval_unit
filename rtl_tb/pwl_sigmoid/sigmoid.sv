/*
* System verilog module to compute the fixed point sigmoid of a fixed point input using pwl, function symmetry and linear interpolation  
**/
module sigmoid #(parameter type dtype = logic[31:0], parameter SEGMENTS = 8, 
							parameter INTEGER  = 8, parameter FRACTIONAL = 24, parameter ADDR_BITS = 3)(
	input logic clk,
	input logic rst,
	input dtype x,


	output dtype sigma_x
);
	
	dtype										k[SEGMENTS - 1:0];
	dtype										b[SEGMENTS - 1:0];
	dtype										mul_res;
	logic[ADDR_BITS - 1:0]	addr;
	logic										valid_index;
	logic										rdy;
	logic[ADDR_BITS - 1:0]	segment_index;
	dtype										x_in;
	dtype										sigma_out;


	assign x_in = x[INTEGER + FRACTIONAL - 1] ?  (~x) + 1 : x;
	
  comb_search_g #(.dtype(dtype), .SEGMENTS(SEGMENTS)) cs(.clk(clk), .rst(rst), .in_value(x_in), .segment_index(segment_index));	
	
	sgmd_mem_read #(.dtype(dtype), .SEGMENTS(SEGMENTS)) mr(.k(k), .b(b));
	sgmd_frac_mul #(.dtype(dtype), .INTEGER(INTEGER), .FRACTIONAL(FRACTIONAL)) mul(.inA(k[addr]), .inB(x_in),.out(mul_res));
	
	assign sigma_out = b[addr] + mul_res ;
	assign addr = segment_index;
	assign sigma_x = x[INTEGER + FRACTIONAL - 1] ? (1 << FRACTIONAL) + 1 + (~sigma_out) : sigma_out; 

endmodule
