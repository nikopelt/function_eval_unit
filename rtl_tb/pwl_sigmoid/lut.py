import numpy as np
'''
    This is a python script to generate pwl coefficients in a range of negative numbers used for exp2 
    function implementation of a transformer, where all inputs are non positive fractional partsof an input. 

'''


print("~~~~~~~~~~~~~~~~~~~~~~This is a script to generate pwl coefficients~~~~~~~~~~~~~~~~~~~~~~")
# --- Configuration ---
INPUT_WIDTH = 32        
FRAC_BITS = 24          
NUM_SEGMENTS = 1
# Derived parameters
scale_factor = 2**FRAC_BITS


def fun(x):
    return 1/(1 + np.exp(-x))

with open("../sim_annealing/points.txt", "r") as f:
    points = f.readlines()
    m_fixed = []
    c_fixed = []
    start_points = []
    end_points = []
    points_fixed = []
    NUM_SEGMENTS = len(points) - 1
    for i in range(1, len(points)):
        x_start = float(points[i-1]) 
        x_end = float(points[i])
        
        start_points.append(x_start)
        end_points.append(x_end)
        
        y_start = fun(x_start)
        y_end = fun(x_end)
        
        slope = (y_end - y_start) / (x_end - x_start)
        intercept = y_start - slope*x_start
        

        m_fixed.append(int(slope * scale_factor))
        c_fixed.append(int(intercept * scale_factor))
        points_fixed.append(int(x_start*scale_factor))

        
with open("coeffs.mem", "w") as f:
    for i in range(len(m_fixed)):
        f.write(f"{m_fixed[i]:08X} {c_fixed[i]:08X} // Seg {i}: x=[{start_points[i]:.2f}, {end_points[i]:.2f}]\n")

with open("segments.mem", "w") as f:
    for i in range(len(points_fixed)):
        points_fixed[i] = points_fixed[i] & 0xFFFFFFFF
        f.write(f"{points_fixed[i]:08X} // Seg {i}\n")

print(f"Separating [{start_points[0]}, {end_points[NUM_SEGMENTS - 1]} ] in {NUM_SEGMENTS} segments")
print(f"Format: Q{INPUT_WIDTH-FRAC_BITS}.{FRAC_BITS} (Fixed Point)")
print("PWL coefficients exported to 'coeffs.mem'")
