def get_numbers_from_string(string):
    numbers_from_string = []
    is_part_of_number = False
    current_number = ""
    for char in string:
        if char.isdigit():
            if not is_part_of_number:
                is_part_of_number = True
            current_number += char
        else:
            if is_part_of_number:
                is_part_of_number = False
                numbers_from_string.append(current_number)
                current_number = ""
    return numbers_from_string