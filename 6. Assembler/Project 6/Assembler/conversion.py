def decimal_to_binary(decimal_num, length=None):
    """
    Convert a decimal number to binary string with specified length
    
    Args:
        decimal_num (int): Decimal number to convert
        length (int): Desired length of binary string (default: None)
        
    Returns:
        str: Binary representation as string, padded with zeros if length specified
    """
    if decimal_num == 0:
        binary = "0"
    else:
        binary = ""
        num = abs(decimal_num)
        
        while num > 0:
            binary = str(num % 2) + binary
            num //= 2
            
        if decimal_num < 0:
            binary = "-" + binary
    
    if length is not None:
        # Remove negative sign for padding if present
        is_negative = binary.startswith('-')
        if is_negative:
            binary = binary[1:]
            
        # Pad with zeros
        binary = binary.zfill(length)
        
        # Add back negative sign if needed
        if is_negative:
            binary = "-" + binary
            
    return binary

def binary_to_decimal(binary_str):
    """
    Convert a binary string to decimal number
    
    Args:
        binary_str (str): Binary number as string
        
    Returns:
        int: Decimal representation
    """
    # Handle negative binary numbers
    is_negative = binary_str.startswith('-')
    if is_negative:
        binary_str = binary_str[1:]
        
    decimal = 0
    power = 0
    
    # Convert from right to left
    for digit in binary_str[::-1]:
        if digit == '1':
            decimal += 2 ** power
        elif digit != '0':
            raise ValueError("Invalid binary string")
        power += 1
        
    return -decimal if is_negative else decimal