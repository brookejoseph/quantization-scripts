
#### **Description**
This was built in an effort to better understand how weights are changed in a Neural Network when a model is quantized to fit on a smaller chip. 


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
