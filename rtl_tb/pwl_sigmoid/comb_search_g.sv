/*
* Combinational module for search of the segment that the input is located
**/

module comb_search_g #(parameter type dtype = logic[31:0], parameter SIZE = 32,parameter SEGMENTS = 8)(
	input logic clk,
	input logic rst,
	input dtype in_value,
	
	output logic[$clog2(SEGMENTS) - 1:0] segment_index
);

dtype value[SEGMENTS - 1:0];

logic [SEGMENTS-1 : 0] cmp;
logic [SEGMENTS-1 : 0] one_hot;

initial begin
  // Read MEM for simulation
	$readmemh("segments.mem", value);
end

// Parallel Comparators
genvar i;

generate	
	for(i = 0; i < SEGMENTS; i++) begin
		comp #(.SIZE(SIZE)) cmp_u(.in_a(in_value), .in_b(value[i]), .cmp(cmp[i]));
	end
endgenerate

// XOR for One-hot
always_comb begin
	for(int i = 0; i < SEGMENTS - 1; i++) begin
		one_hot[i] = cmp[i] ^ cmp[i+1];		
	end
	one_hot[SEGMENTS - 1] = cmp[SEGMENTS - 1];
end

// One-hot to Binary conversion
always_comb begin

  segment_index = '0; 
	
	for(int i = 0; i < $clog2(SEGMENTS); i++) begin
    for(int j = 0; j < SEGMENTS; j++) begin
      if ((j % (2**(i+1))) >= (2**i)) begin
        segment_index[i] |= one_hot[j];
      end
    end
  end

end

endmodule
