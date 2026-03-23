/*
* Systolic module that performs Normalizer accumulation using a 1D-systolic grid
**/
module systolic_stat #(parameter type dtype = logic[31:0])( 
	input logic clk,
	input logic rst,
	input dtype north,
	input dtype west,

	output dtype south
);

always_ff @(posedge clk) begin
	if(rst) begin
		south <= 0;
	end else begin
		south <= north + west;
	end
end

endmodule
