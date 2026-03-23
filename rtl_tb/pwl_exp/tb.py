import matplotlib.pyplot as plt
import numpy as np
import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Timer

"""
    Testbench to test the functionality of an exp(-x) unit for the integration to a multi-function unit of an LLM accelerator
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

@cocotb.test()
async def testbench(dut):
    
    cocotb.log.info("Testbench for the testing of exp(-x) with floating point input")
    
    cocotb.start_soon(generate_clock(dut))
    
    input_val = 0 
    
    await reset(dut);
    h = float_to_hex_fixed(input_val,8,24)
    

    await RisingEdge(dut.clk)
    dut.x.value = h;
    
    cocotb.log.info("Float Input : %f", input_val)
    cocotb.log.info("Float to Hex : 0x%X", h)
    
    cocotb.log.info("Output type : %s", type(dut.exp_x.value))


    for _ in range(100):
        await RisingEdge(dut.clk)


    cocotb.log.info("Hex to Float : %f", hex_fixed_to_float(dut.exp_x.value, 8, 24))

    points = []
    y_points = []

    for i in range(800):
        
        await RisingEdge(dut.clk)
        
        points.append(input_val)

        h = float_to_hex_fixed(input_val,8,24)
        dut.x.value = h
        y_points.append(hex_fixed_to_float(dut.exp_x.value))
        
        input_val += 0.0125

    actual_points = np.exp((-1) * np.array(points))
    plt.plot(points, y_points, 'r--', points, actual_points,'b--')
    plt.show()
    

    y_arr = np.array(y_points)
    act_arr = actual_points


    max_rel_error = 0

    for i in range(799):
        error = np.max(np.abs(y_arr[i + 1] - act_arr[i])/act_arr[i])
        if(error > max_rel_error):
            max_rel_error = error
            idx = i
    cocotb.log.info("Max Relative Error: %.3f %%, at %f: Actual value = %f, Sim value = %f", max_rel_error*100, points[idx], act_arr[idx], y_arr[idx + 1])
    
    for i in range(10):
        cocotb.log.info("Actual value = %f, Sim value = %f", act_arr[i], y_arr[i + 1])

    

    assert True
