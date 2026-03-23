import random
import matplotlib.pyplot as plt
import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Timer
import numpy as np
"""
    Testbench to test the functionality of an Softmax unit for the integration to a multi-function unit of an LLM accelerator
"""

# Clock task for sequential logic
async def generate_clock(dut):
    for _ in range(1000):
        dut.clk.value = 0
        await Timer(1, unit = "ns")
        dut.clk.value = 1
        await Timer(1, unit = "ns")


# Reset task for internal registers
async def reset(dut):
    dut.rst.value = 1
    
    for _ in range(5):
        await RisingEdge(dut.clk)
    
    dut.rst.value = 0
    await RisingEdge(dut.clk) 

# Function to convert floating point inputs to fixed point hex
def float_to_hex_fixed(value, integer_bits=8, fractional_bits=24):
    total_bits = integer_bits + fractional_bits
    
    scaled_int = round(value * (1 << fractional_bits))
    
    max_val = (1 << (total_bits - 1)) - 1
    min_val = -(1 << (total_bits - 1))
    
    if scaled_int > max_val: scaled_int = max_val
    if scaled_int < min_val: scaled_int = min_val
    
    if scaled_int < 0:
        scaled_int = (1 << total_bits) + scaled_int
        
    return scaled_int

# Function to convert fixed point hex to decimal float
def hex_fixed_to_float(hex_log, integer_bits=8, fractional_bits=24):
    total_bits = integer_bits + fractional_bits
    
    int_val = int(hex_log)
    
    if int_val & (1 << (total_bits - 1)):
        int_val -= (1 << total_bits)
        
    return int_val / (1 << fractional_bits)


def softmax(x):
    exps = 0
    out = x
    for i in range(len(x)):
        x[i] = np.exp(-x[i])
        exps += x[i]
    for i in range(len(x)):
        out[i] = x[i]/exps
    return out


def rms(x):
    RMS = 0
    out = x
    for i in range(len(x)):
        RMS += (x[i]*x[i])
    for i in range(len(x)):
        out[i] = x[i]/np.sqrt(RMS)
    return out

def sigmoid(x):
    return 1/(1 + np.exp(-x))

@cocotb.test()
async def testbench(dut):
    
    cocotb.log.info("Testbench for the testing of Softmax(x) with fixed point input")
    
    cocotb.start_soon(generate_clock(dut))
    
    BLOCK_SIZE = 64
    input_val = 0.001
    sfmx_x_s = []

    await reset(dut);
#============================================================================    
# SOFTMAX TEST
#============================================================================    

    cocotb.log.info("=========================================")
    cocotb.log.info("SOFTMAX TEST")
    cocotb.log.info("=========================================")

    await RisingEdge(dut.clk)
    dut.en_sfmx.value = 1

    await RisingEdge(dut.clk)
    for i in range(BLOCK_SIZE):
        input_val = random.uniform(0.01, 2)
        h = float_to_hex_fixed(input_val,8,24)
        sfmx_x_s.append(input_val);
        dut.x[i].value = h;
    
    sfmx_x_s = np.array(sfmx_x_s, dtype = np.float64)
    cocotb.log.info("Float Input : %f", input_val)
    cocotb.log.info("Float to Hex : 0x%X", h)
    
    cocotb.log.info("Output type : %s", type(dut.sfmx_stat.value))


    for _ in range(BLOCK_SIZE + 1):
        await RisingEdge(dut.clk)


    cocotb.log.info("Output expontent value of element 0 : %f", hex_fixed_to_float(dut.fun_u_out[0].value, 8, 24))
    cocotb.log.info("Systolic Running Stat : %f", hex_fixed_to_float(dut.sfmx_stat.value, 8, 24))
    cocotb.log.info("System Verilog Softmax : %f",(hex_fixed_to_float(dut.fun_u_out[0].value, 8, 24)/hex_fixed_to_float(dut.sfmx_stat.value, 8, 24)))
    cocotb.log.info("Numpy SoftMax : %f", softmax(sfmx_x_s)[0])
   
    dut_value = []
    actual_value = []
    points = []
    sum_of_sfmx = 0

    for i in range(BLOCK_SIZE):
        dut_value.append((hex_fixed_to_float(dut.fun_u_out[i].value, 8, 24)/hex_fixed_to_float(dut.sfmx_stat.value, 8, 24)))
        actual_value.append(sfmx_x_s[i])
        points.append(i)
        sum_of_sfmx += (hex_fixed_to_float(dut.fun_u_out[i].value, 8, 24)/hex_fixed_to_float(dut.sfmx_stat.value, 8, 24))
    
    
    cocotb.log.info("Sum of Softmax Outputs : %f", sum_of_sfmx)
    
    y_arr = np.array(dut_value)
    act_arr = actual_value


    max_rel_error = 0

    for i in range(BLOCK_SIZE):
        error = np.max(np.abs(y_arr[i] - act_arr[i])/act_arr[i])
        if(error > max_rel_error):
            max_rel_error = error
            idx = i
    cocotb.log.info("Max Relative Error: %.3f %%, at %d: Actual value = %f, Sim value = %f", max_rel_error*100, points[idx], act_arr[idx], y_arr[idx])

#============================================================================    
# RMS TEST
#============================================================================    
   
    cocotb.log.info("=========================================")
    cocotb.log.info("RMS TEST")
    cocotb.log.info("=========================================")

    rms_x_s = []
    await RisingEdge(dut.clk)
    dut.en_sfmx.value = 0
    dut.en_rms.value = 1
    

    await RisingEdge(dut.clk)
    for i in range(BLOCK_SIZE):
        input_val = random.uniform(-2, 2)
        h = float_to_hex_fixed(input_val,8,24)
        rms_x_s.append(input_val);
        dut.x[i].value = h;
    
    cocotb.log.info("Float Input : %f", input_val)
    cocotb.log.info("Float to Hex : 0x%X", h)
    
    rms_x_s = np.array(rms_x_s, dtype = np.float64)   


    for _ in range(BLOCK_SIZE + 1):
        await RisingEdge(dut.clk)

    cocotb.log.info("Output value of element 0 : %f", hex_fixed_to_float(dut.fun_u_out[0].value, 8, 24))
    cocotb.log.info("Systolic Running Stat : %f", hex_fixed_to_float(dut.rms_stat.value, 8, 24))
    cocotb.log.info("System Verilog RMS : %f",(hex_fixed_to_float(dut.fun_u_out[0].value, 8, 24)/hex_fixed_to_float(dut.rms_stat.value, 8, 24)))
    cocotb.log.info("Numpy RMS : %f", rms(rms_x_s)[0])
    
    rms_dut_value = []
    rms_actual_value = []

    for i in range(BLOCK_SIZE):
        rms_dut_value.append((hex_fixed_to_float(dut.fun_u_out[i].value, 8, 24)/hex_fixed_to_float(dut.rms_stat.value, 8, 24)))
        rms_actual_value.append(rms_x_s[i])
    
    
    
    y_arr = np.array(rms_dut_value)
    act_arr = rms_actual_value


    max_rel_error = 0

    for i in range(BLOCK_SIZE):
        error = np.max(np.abs(y_arr[i] - act_arr[i])/act_arr[i])
        if(error > max_rel_error):
            max_rel_error = error
            idx = i
    cocotb.log.info("RMS Max Relative Error: %.3f %%, at %d: Actual value = %f, Sim value = %f", max_rel_error*100, points[idx], act_arr[idx], y_arr[idx])
   

#============================================================================    
# SIGMOID TEST
#============================================================================    

    cocotb.log.info("=========================================")
    cocotb.log.info("SIGMOID TEST")
    cocotb.log.info("=========================================")

    sigmoid_x_s = []
    await RisingEdge(dut.clk)
    dut.en_rms.value = 0
    dut.en_sgmd.value = 1
    

    await RisingEdge(dut.clk)
    for i in range(BLOCK_SIZE):
        input_val = random.uniform(-4, 4)
        h = float_to_hex_fixed(input_val,8,24)
        sigmoid_x_s.append(input_val);
        dut.x[i].value = h;
    
    await RisingEdge(dut.clk)

    cocotb.log.info("Float Input : %f", input_val)
    cocotb.log.info("Float to Hex : 0x%X", h)
    
    sigmoid_x_s = np.array(sigmoid_x_s, dtype = np.float64)   


    cocotb.log.info("Output value of element 0 : %f", hex_fixed_to_float(dut.fun_u_out[0].value, 8, 24))
    cocotb.log.info("System Verilog Sigmoid : %f",(hex_fixed_to_float(dut.fun_u_out[0].value, 8, 24)))
    cocotb.log.info("Numpy Sigmoid : %f", sigmoid(sigmoid_x_s)[0])
    
    sigmoid_dut_value = []
    sigmoid_actual_value = []

    for i in range(BLOCK_SIZE):
        sigmoid_dut_value.append((hex_fixed_to_float(dut.fun_u_out[i].value, 8, 24)))
        sigmoid_actual_value.append(sigmoid(sigmoid_x_s[i]))
    
    
    
    y_arr = np.array(sigmoid_dut_value)
    act_arr = sigmoid_actual_value


    max_rel_error = 0

    for i in range(BLOCK_SIZE):
        error = np.max(np.abs(y_arr[i] - act_arr[i])/act_arr[i])
        if(error > max_rel_error):
            max_rel_error = error
            idx = i
    cocotb.log.info("Sigmoid Max Relative Error: %.3f %%, at %d: Actual value = %f, Sim value = %f", max_rel_error*100, points[idx], act_arr[idx], y_arr[idx])
    

    fig, axs = plt.subplots(3)
    fig.suptitle('Function Unit Output')
    axs[0].set_title("Softmax Output")
    axs[0].plot(points, actual_value,'b--', points, dut_value, 'r--')
    
    axs[1].set_title("RMS Output")
    axs[1].plot(points, rms_actual_value,'b--', points, rms_dut_value, 'r--')
    
    axs[2].set_title("Sigmoid Output")
    axs[2].plot(points, sigmoid_actual_value,'b--', points, sigmoid_dut_value, 'r--')
    plt.show()



    assert True
