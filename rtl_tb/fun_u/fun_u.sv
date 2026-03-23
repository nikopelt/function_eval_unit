/*
* Function unit with selected function output
**/
module fun_u #(parameter type dtype = logic[31:0], parameter BLOCK_SIZE = 64, parameter SIZE = 32,parameter SOFTMAX_SEGMENTS = 32, parameter INTEGER = 8, parameter FRACTIONAL = 24)(
	input logic clk,
	input logic rst,

	input logic en_sfmx,
	input logic en_rms,
	input logic en_sgmd,
	input dtype x						[BLOCK_SIZE - 1:0],

	output dtype fun_u_out	[BLOCK_SIZE - 1:0]
);

dtype identity_x	[BLOCK_SIZE - 1:0];
dtype sfmx_x			[BLOCK_SIZE - 1:0];
dtype rms_x				[BLOCK_SIZE - 1:0];
dtype sigmoid_x		[BLOCK_SIZE - 1:0];

dtype sfmx_y			[BLOCK_SIZE - 1:0];
dtype rms_y				[BLOCK_SIZE - 1:0];
dtype sigmoid_y		[BLOCK_SIZE - 1:0];

dtype sfmx_stat;
dtype rms_stat;

fun_dec #(.dtype(dtype), .BLOCK_SIZE(BLOCK_SIZE)) fd(.clk(clk), .rst(rst), .x(x), .en_sfmx(en_sfmx), .en_rms(en_rms), .en_sgmd(en_sgmd), .identity_x(identity_x), .softmax_x(sfmx_x), .RMS_x(rms_x), .sigmoid_x(sigmoid_x));

softmax_u #(.dtype(dtype), .BLOCK_SIZE(BLOCK_SIZE), .SEGMENTS(SOFTMAX_SEGMENTS), .INTEGER(INTEGER), .FRACTIONAL(FRACTIONAL), .ADDR_BITS($clog2(SOFTMAX_SEGMENTS))) sfmx_unit(.clk(clk), .rst(rst), .x(sfmx_x), .y(sfmx_y), .stat(sfmx_stat));
rms_u #(.dtype(dtype), .BLOCK_SIZE(BLOCK_SIZE), .SIZE(SIZE), .INTEGER(INTEGER), .FRACTIONAL(FRACTIONAL)) rms_unit(.clk(clk), .rst(rst), .x(rms_x), .y(rms_y), .stat(rms_stat));
sigmoid_u #(.dtype(dtype), .BLOCK_SIZE(BLOCK_SIZE), .INTEGER(INTEGER), .FRACTIONAL(FRACTIONAL)) sigmoid_unit(.clk(clk), .rst(rst), .x(sigmoid_x), .sigma_x(sigmoid_y));

fun_mux #(.dtype(dtype) , .BLOCK_SIZE(BLOCK_SIZE)) fm(.clk(clk), .rst(rst), .en_sfmx(en_sfmx), .en_rms(en_rms), .en_sgmd(en_sgmd), .identity_y(identity_x), .softmax_y(sfmx_y), .RMS_y(rms_y), .sigmoid_y(sigmoid_y), .fun_u_out(fun_u_out));


endmodule
