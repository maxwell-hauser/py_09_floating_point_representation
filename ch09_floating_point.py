#!/usr/bin/env python3
"""
Chapter 9: Floating Point Representation (IEEE 754)
Demonstrates single and double precision floating point format
"""

import struct

def decimal_to_ieee754_single(decimal_num):
    """Convert decimal to IEEE 754 single precision (32-bit)"""
    # Use Python's struct module for actual conversion
    packed = struct.pack('f', decimal_num)
    ieee_bits = ''.join(f'{byte:08b}' for byte in packed)
    
    # Parse components
    sign_bit = ieee_bits[0]
    exponent = ieee_bits[1:9]
    mantissa = ieee_bits[9:32]
    
    return {
        'full': ieee_bits,
        'sign': sign_bit,
        'exponent': exponent,
        'mantissa': mantissa,
        'sign_val': '-' if sign_bit == '1' else '+',
        'exponent_val': int(exponent, 2) - 127,
        'exponent_biased': int(exponent, 2)
    }

def ieee754_single_to_decimal(ieee_bits):
    """Convert IEEE 754 single precision to decimal"""
    # Convert binary string to bytes
    bytes_array = bytearray()
    for i in range(0, 32, 8):
        byte = int(ieee_bits[i:i+8], 2)
        bytes_array.append(byte)
    
    # Unpack as float
    return struct.unpack('f', bytes_array)[0]

def manual_float_conversion(decimal_num):
    """Manually show steps of floating point conversion"""
    print(f"\nConverting {decimal_num} to IEEE 754 Single Precision:")
    
    # Step 1: Sign bit
    sign = 0 if decimal_num >= 0 else 1
    abs_num = abs(decimal_num)
    print(f"\n1. Sign bit: {sign} ({'positive' if sign == 0 else 'negative'})")
    
    # Step 2: Convert to binary
    integer_part = int(abs_num)
    fractional_part = abs_num - integer_part
    
    # Integer to binary
    int_binary = bin(integer_part)[2:] if integer_part > 0 else '0'
    
    # Fractional to binary
    frac_binary = ""
    temp = fractional_part
    for _ in range(23):  # Enough for single precision
        temp *= 2
        bit = int(temp)
        frac_binary += str(bit)
        temp -= bit
        if temp == 0:
            break
    
    print(f"\n2. Binary representation:")
    print(f"   Integer part:    {int_binary}")
    print(f"   Fractional part: 0.{frac_binary}")
    print(f"   Combined: {int_binary}.{frac_binary}")
    
    # Step 3: Normalize
    if integer_part > 0:
        # Find position of first 1 in integer part
        exponent = len(int_binary) - 1
        mantissa = int_binary[1:] + frac_binary
    else:
        # Find position of first 1 in fractional part
        first_one = frac_binary.index('1')
        exponent = -(first_one + 1)
        mantissa = frac_binary[first_one + 1:]
    
    print(f"\n3. Normalize to 1.xxxxx × 2^exponent:")
    print(f"   Exponent: {exponent}")
    print(f"   Mantissa: 1.{mantissa[:23]}")
    
    # Step 4: Bias exponent
    biased_exponent = exponent + 127
    exponent_binary = format(biased_exponent, '08b')
    print(f"\n4. Biased exponent: {exponent} + 127 = {biased_exponent}")
    print(f"   Binary: {exponent_binary}")
    
    # Step 5: Mantissa (23 bits)
    mantissa_binary = mantissa[:23].ljust(23, '0')
    print(f"\n5. Mantissa (23 bits): {mantissa_binary}")
    
    # Final format
    sign_bit = str(sign)
    final = sign_bit + exponent_binary + mantissa_binary
    
    print(f"\n6. Final IEEE 754 format:")
    print(f"   Sign | Exponent | Mantissa")
    print(f"    {sign_bit}   | {exponent_binary} | {mantissa_binary}")
    print(f"\n   Complete: {final}")
    
    return final

def main():
    print("=" * 60)
    print("CHAPTER 9: Floating Point Representation (IEEE 754)")
    print("=" * 60)
    
    # Example 1: IEEE 754 Format Structure
    print("\n--- Example 1: IEEE 754 Single Precision Format ---")
    print("\n32 bits total:")
    print("  Bit 31:    Sign bit (0=positive, 1=negative)")
    print("  Bits 30-23: Exponent (8 bits, biased by 127)")
    print("  Bits 22-0:  Mantissa/Significand (23 bits)")
    print("\nFormula: (-1)^sign × 1.mantissa × 2^(exponent-127)")
    
    # Example 2: Convert decimal to IEEE 754
    print("\n--- Example 2: Decimal to IEEE 754 ---")
    test_num = 12.375
    result = decimal_to_ieee754_single(test_num)
    
    print(f"\nNumber: {test_num}")
    print(f"IEEE 754 representation:")
    print(f"  Sign:     {result['sign']} ({result['sign_val']})")
    print(f"  Exponent: {result['exponent']} (biased: {result['exponent_biased']}, actual: {result['exponent_val']})")
    print(f"  Mantissa: {result['mantissa']}")
    print(f"\n  Complete: {result['full']}")
    
    # Verify
    back = ieee754_single_to_decimal(result['full'])
    print(f"\nVerification: {back}")
    
    # Example 3: Manual conversion steps
    print("\n--- Example 3: Manual Conversion Steps ---")
    manual_float_conversion(6.5)
    
    # Example 4: Special values
    print("\n--- Example 4: Special IEEE 754 Values ---")
    special_values = [
        (0.0, "Zero"),
        (-0.0, "Negative Zero"),
        (float('inf'), "Positive Infinity"),
        (float('-inf'), "Negative Infinity"),
        (1.0, "One"),
        (-1.0, "Negative One")
    ]
    
    print("\nValue          | Sign | Exponent | Mantissa (first 8 bits)")
    print("---------------|------|----------|------------------------")
    for val, desc in special_values:
        try:
            result = decimal_to_ieee754_single(val)
            print(f"{desc:14s} | {result['sign']:^4s} | {result['exponent']} | {result['mantissa'][:8]}...")
        except:
            print(f"{desc:14s} | (special case)")
    
    # Example 5: Precision demonstration
    print("\n--- Example 5: Precision and Range ---")
    print("\nSingle Precision (32-bit):")
    print("  Significant digits: ~7 decimal digits")
    print("  Range: ±1.18 × 10^-38 to ±3.40 × 10^38")
    print("  Exponent bias: 127")
    
    print("\nDouble Precision (64-bit):")
    print("  Significant digits: ~16 decimal digits")
    print("  Range: ±2.23 × 10^-308 to ±1.80 × 10^308")
    print("  Exponent bias: 1023")
    print("  Format: 1 sign + 11 exponent + 52 mantissa bits")
    
    # Example 6: Common floating point numbers
    print("\n--- Example 6: Common Numbers in IEEE 754 ---")
    test_numbers = [0.5, 1.0, 2.0, 0.1, -0.15625]
    
    for num in test_numbers:
        result = decimal_to_ieee754_single(num)
        print(f"\n{num:8.5f}: {result['full']}")
        print(f"  Exponent: 2^{result['exponent_val']}")
    
    print("\n" + "=" * 60)
    print("Key Concepts:")
    print("- IEEE 754: Standard for floating point representation")
    print("- Format: Sign + Exponent + Mantissa")
    print("- Normalized form: 1.xxx × 2^exp")
    print("- Single precision: 32 bits (1+8+23)")
    print("- Double precision: 64 bits (1+11+52)")
    print("=" * 60)

if __name__ == "__main__":
    main()
