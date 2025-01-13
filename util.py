import string
import easyocr

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Mapping dictionaries for character conversion
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}


def write_csv(results, output_path):
    """
    Write the results to a CSV file.

    Args:
        results (dict): Dictionary containing the results.
        output_path (str): Path to the output CSV file.
    """
    with open(output_path, 'w') as f:
        f.write('{},{},{},{}\n'.format('license_plate_bbox', 'license_plate_bbox_score', 'license_number',
                                                'license_number_score'))

        if 'license_plate' in results.keys() and \
            'text' in results['license_plate'].keys():
            f.write('{},{},{},{}\n'.format('[{} {} {} {}]'.format(
                                                results['license_plate']['bbox'][0],
                                                results['license_plate']['bbox'][1],
                                                results['license_plate']['bbox'][2],
                                                results['license_plate']['bbox'][3]),
                                            results['license_plate']['bbox_score'],
                                            results['license_plate']['text'],
                                            results['license_plate']['text_score'])
                            )
        f.close()


def license_complies_format(text):
    """
    Check if the license plate text complies with the required format.

    Args:
        text (str): License plate text.

    Returns:
        bool: True if the license plate complies with the format, False otherwise.
    """
    list = [7,8,9]
    if len(text) not in list:
        return False

    if len(text) == 7:
       if (text[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
          (text[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
          (text[2] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and \
          (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
          (text[4] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
          (text[5] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
          (text[6] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()):
            return True
    elif len(text) == 8:
       if (text[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
          (text[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
          (text[2] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and \
          (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
          (text[4] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
          (text[5] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
          (text[6] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
          (text[7] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()):
            return True
    elif len(text) == 9:
       if (text[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
          (text[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
          (text[2] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and \
          (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
          (text[4] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
          (text[5] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
          (text[6] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
          (text[7] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
          (text[8] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()):
            return True
    else:
        return False


def format_license(text):
    """
    Format the license plate text by converting characters using the mapping dictionaries.

    Args:
        text (str): License plate text.

    Returns:
        str: Formatted license plate text.
    """
    license_plate_ = ''
    mapping = {0: dict_char_to_int, 1: dict_char_to_int, 3: dict_char_to_int, 4: dict_char_to_int, 5: dict_char_to_int, 6: dict_char_to_int, 7: dict_char_to_int, 8: dict_char_to_int, 
               2: dict_int_to_char}
    if len(text) == 7:
        for j in [0, 1, 2, 3, 4, 5, 6]:
            if text[j] in mapping[j].keys():
                license_plate_ += mapping[j][text[j]]
            else:
                license_plate_ += text[j]
    elif len(text) == 8:
        for j in [0, 1, 2, 3, 4, 5, 6, 7]:
            if text[j] in mapping[j].keys():
                license_plate_ += mapping[j][text[j]]
            else:
                license_plate_ += text[j]
    elif len(text) == 9:
        for j in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            if text[j] in mapping[j].keys():
                license_plate_ += mapping[j][text[j]]
            else:
                license_plate_ += text[j]

    return license_plate_


def read_license_plate(license_plate_crop):
    """
    Read the license plate text from the given cropped image.

    Args:
        license_plate_crop (PIL.Image.Image): Cropped image containing the license plate.

    Returns:
        tuple: Tuple containing the formatted license plate text and its confidence score.
    """

    detections = reader.readtext(license_plate_crop)

    text_list = []
    score_list = []

    for detection in detections:
        bbox, text_de, score_de = detection
        text_list.append(text_de)
        score_list.append(score_de)

    text = ''
    for i in text_list:
        text = text + i

    score = 0
    for i in score_list:
        score = score + i
    score = score/len(score_list)

    text = text.upper().replace(' ','')
    text = text.upper().replace('-','')
    text = text.upper().replace('.','')
    text = text.upper().replace(';','')
    text = text.upper().replace('[','')
    text = text.upper().replace(']','')
    text = text.upper().replace(',','')
    text = text.upper().replace("'",'')

    print(text)
    # print(score)

    if license_complies_format(text):
        print("Done")
        return format_license(text), score
    else:
        print("Detected license plate but unable to read the license plate")
        return None, None
