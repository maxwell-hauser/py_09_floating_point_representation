# Chapter 9: Floating-Point Representation (IEEE 754)

## Overview

This chapter explores how computers represent real numbers (numbers with fractional parts) using the IEEE 754 floating-point standard. This format enables representation of very large and very small numbers with fractional precision.

## Key Concepts

### Why Floating-Point?

**Problem:** Fixed-point binary can only represent a limited range with fixed precision.

**Solution:** Floating-point uses scientific notation in binary!

```
Decimal scientific notation: 6.022 × 10²³
Binary floating-point:      1.101 × 2⁵
```

### Floating-Point Components

Three parts make up a floating-point number:

```
[Sign] [Exponent] [Mantissa/Significand]
  ±        E            M

Value = (-1)^Sign × (1.M) × 2^(E-Bias)
```

## IEEE 754 Single Precision (32-bit)

### Format Layout

```
Bit 31    Bits 30-23      Bits 22-0
[Sign]    [Exponent]      [Mantissa]
  1 bit    8 bits          23 bits
```

### Components

#### 1. Sign Bit (1 bit)
- **0** = Positive
- **1** = Negative

#### 2. Exponent (8 bits)
- **Biased representation:** Actual exponent + 127
- **Range:** 0 to 255
- **Bias:** 127
- **Actual exponent:** Stored value - 127
- **Range:** -126 to +127 (excluding special cases)

**Why biased?** Makes comparison easier (treat as unsigned integer)

#### 3. Mantissa/Significand (23 bits)
- **Fractional part** after the binary point
- **Implicit leading 1:** Always 1.xxxxx (normalized)
- **23 bits store:** The fractional part after "1."
- **Effective precision:** 24 bits (1 implicit + 23 stored)

### Value Calculation

```
Value = (-1)^Sign × (1.Mantissa) × 2^(Exponent-127)
```

### Example: Representing 5.75

**Step 1: Convert to binary**
```
5.75₁₀ = 101.11₂
       = 1.0111 × 2²  (normalized)
```

**Step 2: Extract components**
```
Sign:      0 (positive)
Exponent:  2 + 127 = 129 = 10000001₂
Mantissa:  0111 0000 0000 0000 0000 000
           (fractional part after "1.")
```

**Step 3: Combine**
```
0 10000001 01110000000000000000000
│ └──┬──┘  └──────────┬──────────┘
│    │              Mantissa (23)
│  Exponent (8)
Sign (1)

Hex: 0x40B80000
```

**Verification:**
```
(-1)⁰ × (1.0111) × 2^(129-127)
= 1 × 1.4375 × 2²
= 1.4375 × 4
= 5.75 ✓
```

## Normalized vs Denormalized Numbers

### Normalized Numbers (Standard)
- **Exponent:** 1 to 254 (not 0 or 255)
- **Form:** 1.M × 2^(E-127)
- **Implicit leading 1:** Always present

### Denormalized Numbers (Special)
- **Exponent:** 0 (all zeros)
- **Form:** 0.M × 2^(-126)
- **No implicit leading 1:** Allows very small numbers near zero
- **Purpose:** Gradual underflow, represents numbers closer to zero

## Special Values

### Zero
```
Positive zero: 0 00000000 00000000000000000000000
Negative zero: 1 00000000 00000000000000000000000
```

**Note:** +0 and -0 exist but are equal in comparisons

### Infinity
```
Positive infinity: 0 11111111 00000000000000000000000
Negative infinity: 1 11111111 00000000000000000000000
```

**Caused by:** Division by zero, overflow

### NaN (Not a Number)
```
Exponent = 255, Mantissa ≠ 0
Example: 0 11111111 10000000000000000000000
```

**Caused by:** Invalid operations like 0/0, ∞-∞, √(-1)

### Summary Table

| Exponent | Mantissa | Meaning |
|----------|----------|---------|
| 0 | 0 | Zero (±0) |
| 0 | ≠0 | Denormalized number |
| 1-254 | Any | Normalized number |
| 255 | 0 | Infinity (±∞) |
| 255 | ≠0 | NaN (Not a Number) |

## Range and Precision

### Single Precision (32-bit)

**Range:**
- **Smallest positive normalized:** ~1.18 × 10⁻³⁸
- **Largest positive:** ~3.40 × 10³⁸
- **Precision:** ~7 decimal digits

**Bit breakdown:**
```
Sign:      1 bit
Exponent:  8 bits
Mantissa:  23 bits
Total:     32 bits (4 bytes)
```

### Double Precision (64-bit)

**Range:**
- **Smallest positive normalized:** ~2.23 × 10⁻³⁰⁸
- **Largest positive:** ~1.80 × 10³⁰⁸
- **Precision:** ~15-16 decimal digits

**Bit breakdown:**
```
Sign:      1 bit
Exponent:  11 bits (bias = 1023)
Mantissa:  52 bits
Total:     64 bits (8 bytes)
```

## Limitations of Floating-Point

### 1. Limited Precision

```python
0.1 + 0.2 = 0.30000000000000004  # Not exactly 0.3!
```

**Why?** 0.1 and 0.2 cannot be exactly represented in binary

### 2. Rounding Errors

Small errors accumulate over many operations:
```
sum = 0.0
for i in range(1000000):
    sum += 0.1
# sum might not equal exactly 100000.0
```

### 3. Comparison Issues

```python
a = 0.1 + 0.2
b = 0.3
a == b  # Might be False!

# Better:
abs(a - b) < epsilon  # Use threshold for equality
```

### 4. Loss of Significance

Adding small and large numbers:
```
1.0e20 + 1.0  # Result might still be 1.0e20
              # The 1.0 is too small relative to 1.0e20
```

## Converting Decimal to IEEE 754

### Algorithm

1. **Determine sign bit** (0 for +, 1 for -)
2. **Convert to binary**
3. **Normalize:** Get form 1.xxx × 2^E
4. **Calculate biased exponent:** E + 127
5. **Extract mantissa:** Fractional part after "1."
6. **Assemble:** Sign | Exponent | Mantissa

### Example: Convert -6.5

**Step 1:** Sign = 1 (negative)

**Step 2:** Convert 6.5 to binary
```
6₁₀ = 110₂
0.5₁₀ = 0.1₂
6.5₁₀ = 110.1₂
```

**Step 3:** Normalize
```
110.1₂ = 1.101 × 2²
```

**Step 4:** Biased exponent
```
E = 2
Biased = 2 + 127 = 129 = 10000001₂
```

**Step 5:** Mantissa
```
1.101 → fractional part = 101
Pad to 23 bits: 101 00000000000000000000
```

**Step 6:** Assemble
```
1 10000001 10100000000000000000000

Hex: 0xC0D00000
```

## Converting IEEE 754 to Decimal

### Algorithm

1. **Extract sign, exponent, mantissa**
2. **Check for special values** (0, ∞, NaN)
3. **Calculate actual exponent:** Biased - 127
4. **Reconstruct value:** (-1)^S × (1.M) × 2^E
5. **Convert to decimal**

### Example: Decode 0x40400000

**Step 1:** Convert to binary
```
0x40400000 = 01000000010000000000000000000000
```

**Step 2:** Extract components
```
Sign:     0
Exponent: 10000000 = 128
Mantissa: 10000000000000000000000
```

**Step 3:** Actual exponent
```
128 - 127 = 1
```

**Step 4:** Reconstruct
```
(-1)⁰ × (1.1) × 2¹
= 1 × 1.5 × 2
= 3.0
```

## Learning Objectives

By the end of this chapter, you should be able to:
- Understand the IEEE 754 floating-point format
- Identify sign, exponent, and mantissa components
- Convert decimal numbers to IEEE 754 single precision
- Convert IEEE 754 representation back to decimal
- Recognize special values (zero, infinity, NaN)
- Understand normalized and denormalized numbers
- Explain limitations of floating-point arithmetic
- Compare single and double precision formats

## Python Example

Run the interactive example:

```bash
python ch09_floating_point.py
```

### What the Example Demonstrates

1. **IEEE 754 Breakdown:** Dissecting 32-bit float representation
2. **Manual Conversion:** Converting decimal to IEEE 754 step-by-step
3. **Special Values:** Zero, infinity, and NaN representations
4. **Precision Limits:** Demonstrating rounding errors
5. **Range Examples:** Very large and very small numbers
6. **Comparison Issues:** Why exact equality fails
7. **Python struct Module:** Using built-in IEEE 754 conversion

### Sample Output

```
============================================================
CHAPTER 9: Floating-Point Representation (IEEE 754)
============================================================

--- Example 1: IEEE 754 Single Precision Breakdown ---
Value: 5.75
Binary: 01000000101110000000000000000000
Hex:    0x40B80000

Sign bit:      0 (positive)
Exponent:      10000001 (129) → 129 - 127 = 2
Mantissa:      01110000000000000000000
Implied:       1.01110000000000000000000

Calculation: (-1)^0 × 1.4375 × 2^2 = 5.75
...
```

## Real-World Applications

### Scientific Computing
- **Physics Simulations:** Large/small values (10⁻³⁰ to 10³⁰)
- **Astronomy:** Distances, masses, energies
- **Chemistry:** Molecular calculations
- **Engineering:** Complex calculations with wide ranges

### Graphics and Gaming
- **3D Coordinates:** Vertex positions, vectors
- **Colors:** RGB values (often 0.0 to 1.0)
- **Transformations:** Matrix operations
- **Physics Engines:** Collision detection, forces

### Machine Learning
- **Neural Networks:** Weights and activations
- **Training:** Gradient calculations
- **Inference:** Forward propagation
- **Mixed Precision:** Using both float32 and float16

### Financial Systems
- **Note:** Usually avoided for money (use fixed-point or decimal types)
- **Used for:** Statistical analysis, risk calculations, modeling
- **Not for:** Exact currency amounts (rounding errors unacceptable)

## Common Questions

**Q: Why can't 0.1 be represented exactly in binary floating-point?**  
A: Just like 1/3 can't be written exactly in decimal (0.333...), 0.1 is a repeating fraction in binary (0.0001100110011...).

**Q: When should I use float vs double?**  
A: Use double for most applications requiring precision. Use float when memory is critical (graphics, large arrays) and lower precision is acceptable.

**Q: Why are there +0 and -0?**  
A: The sign bit creates both. They compare as equal but can affect certain operations (like 1/+0 = +∞, 1/-0 = -∞).

**Q: What is NaN used for?**  
A: Indicates invalid operations. NaN propagates through calculations, making it easy to detect errors.

**Q: How do I compare floating-point numbers?**  
A: Use a threshold (epsilon): `abs(a - b) < 1e-9` instead of `a == b`.

## Best Practices

### ✅ DO
- Use double precision for general purposes
- Compare with epsilon tolerance
- Be aware of precision limits
- Test edge cases (very large, very small, zero)
- Use specialized libraries for critical precision needs

### ❌ DON'T
- Use floats for money (use decimal types or integers)
- Compare floats with == or !=
- Assume arithmetic is exact
- Ignore NaN and infinity in calculations
- Perform many operations without considering accumulated error

## Key Takeaways

- IEEE 754 is the universal standard for floating-point representation
- Format: [Sign 1 bit] [Exponent 8 bits] [Mantissa 23 bits] for single precision
- Biased exponent (add 127) simplifies comparison
- Normalized form: 1.M × 2^E (implicit leading 1)
- Special values: ±0, ±∞, NaN
- Limited precision causes rounding errors
- 📏 Single: ~7 digits, Double: ~15-16 digits precision
- 💰 Never use for exact financial calculations

## Practice Exercises

1. Convert 12.625₁₀ to IEEE 754 single precision (show all steps)
2. Decode 0xC1200000 to decimal
3. What is the IEEE 754 representation of -1.0?
4. Represent positive infinity in IEEE 754
5. What is the smallest positive normalized number in single precision?
6. Explain why 0.1 + 0.2 ≠ 0.3 in floating-point
7. Convert 0.15625₁₀ to binary, then to IEEE 754
8. What happens when you divide 1.0 by 0.0?
9. Identify if 0x7F800001 is zero, infinity, or NaN
10. Calculate the value of: 0 10000010 10010000000000000000000

## Further Study

- Learn about double and extended precision formats
- Study floating-point arithmetic algorithms
- Explore decimal floating-point (IEEE 754-2008)
- Investigate numerical stability in algorithms
- Learn about GPU half-precision (float16) formats

---

**Course Navigation:**  
← Previous: [Chapter 8 - Binary Arithmetic](../ch8_binary_addition_subtraction/) | Next: [Chapter 10 - Binary Coded Decimal](../ch10_binary_coded_decimals/) →

---
<!-- License moved to dedicated LICENSE file -->
