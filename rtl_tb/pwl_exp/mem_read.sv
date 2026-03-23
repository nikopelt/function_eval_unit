/*
* Memory module that stores the outputs of a coefficients-export python script
**/
module mem_read #(parameter type dtype = logic[31:0], parameter SEGMENTS = 32)(

	output dtype k[SEGMENTS-1:0],
	output dtype b[SEGMENTS-1:0]
);


	dtype my_ram[2*SEGMENTS-1:0]; 

  initial begin
    // Read MEM for simulation
		$readmemh("exp_coeffs.mem", my_ram);
	end


	always_comb begin 
		for(int i = 0; i < 2*SEGMENTS - 1; i = i + 2) begin 
			k[i/2] = my_ram[i];
		end

		for(int i = 1; i < 2*SEGMENTS; i = i + 2) begin 
			b[i/2] = my_ram[i];
		end
	end


endmodule
