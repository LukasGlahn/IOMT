def decimal_to_5bit_list(number):
    """
    Funktion der konverterer et base 10 tal (0-31) til en 5-bit binær 
    værdi i en liste, så pilledispenseren kan styres. 

    Argumenter:
        En integer der skal konverteres. Skal være mellem 0 og 31.
    
    Returnerer:
        En liste med en binær værdi. 
    
    Fejlhåndtering:
        'ValueError' hvis tallet ikke er mellem 0 og 31.
    """
    if number < 0 or number > 31:
        raise ValueError("Tallet skal være mellem 0 og 31.")

    # Konverter tallet til binær og fyld op til 5 bit
    binary_str = bin(number)[2:].zfill(5)

    # Lav en liste af binære værdier
    binary_list = [int(digit) for digit in binary_str]

    return binary_list

# TEST!!! - Eksempel på brug. Slettes når scripts samles til et program:
if __name__ == "__main__":
    # Test med forskellige tal fra 1 til 32
    for test_number in [1, 16, 31]:
        result = decimal_to_5bit_list(test_number)
        print(f"{test_number} -> {result}")
