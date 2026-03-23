import numpy as np
'''
    This is a python script to generate pwl coefficients in a range of negative numbers used for exp2 
    function implementation of a transformer, where all inputs are non positive fractional partsof an input. 

'''
# --- Configuration ---
NUM_SEGMENTS = 32       
INPUT_WIDTH = 32        
FRAC_BITS = 24          
MIN_INPUT_VAL = 1.0    

# Derived parameters
segment_width = MIN_INPUT_VAL / NUM_SEGMENTS
scale_factor = 2**FRAC_BITS

print("~~~~~~~~~~~~~~~~~~~~~~This is a script to generate pwl coefficients for the exponential function~~~~~~~~~~~~~~~~~~~~~~")
print(f"Separating [0.0, {MIN_INPUT_VAL}] in {NUM_SEGMENTS} segments")
print(f"Format: Q{INPUT_WIDTH-FRAC_BITS}.{FRAC_BITS} (Fixed Point)")

with open("exp_coeffs.mem", "w") as f:
    for i in range(NUM_SEGMENTS):
        x_start = i * segment_width
        x_end = (i + 1) * segment_width
        
        y_start = 2**(-x_start)
        y_end = 2**(-x_end)
        
        slope = (y_end - y_start) / segment_width
        intercept = y_start - slope*x_start
         

        m_fixed = int(-slope * scale_factor)
        c_fixed = int(intercept * scale_factor)
        

        f.write(f"{m_fixed:08X} {c_fixed:08X} // Seg {i}: x=[{x_start:.2f}, {x_end:.2f}]\n")

print("PWL coefficients exported to 'exp_coeffs.mem'")
