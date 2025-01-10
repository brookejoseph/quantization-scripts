### README: Quantized Value Mapping Script

#### **Description**
This script demonstrates how to scale and map a range of values using quantization principles. It takes four integer inputs: the original start and end range, and the new start and end range, then computes a scaled value based on these inputs.

#### **Features**
- **Input Handling**: Accepts command-line arguments for flexibility.
- **Range Mapping**: Scales and maps values from the original range to the new range.
- **Error Handling**: Includes checks for incorrect arguments and division by zero.

#### **Usage**
1. Compile the script:
   - For **C++**:
     ```bash
     g++ quantized_mapping.cpp -o quantized_mapping
     ```
   - For **C**:
     ```bash
     gcc quantized_mapping.c -o quantized_mapping
     ```
2. Run the script with four arguments:
   ```bash
   ./quantized_mapping <og_start> <og_end> <new_start> <new_end>
   ```
   Example:
   ```bash
   ./quantized_mapping 10 20 0 100
   ```

#### **Example Output**
For the input `10 20 0 100`, the script outputs:
```
Scaled Value: -1
```

#### **Error Cases**
- **Incorrect argument count**:
  ```
  Usage: ./quantized_mapping <og_start> <og_end> <new_start> <new_end>
  ```
- **Division by zero**:
  ```
  Error: Division by zero.
  ``` 

This script is a basic example of quantized value scaling, which is commonly used in tasks like mapping floating-point values to integer ranges in machine learning.
