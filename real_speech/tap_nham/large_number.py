from normalize_input.vietnam_number_custom.number2word.hundreds import n2w_hundreds
from normalize_input.vietnam_number_custom.number2word.utils.base import chunks
import random

def n2w_large_number(numbers: str):
    """Hàm chuyển đổi các số có giá trị lớn.

    Hàm chuyển đổi các số có giá trị lớn từ 999 đến 999.999.999.999

    Args:
        numbers (str): Chuỗi số đầu vào.

    Returns:
        Chuỗi chữ số đầu ra.

    """
    # Chúng ta cần duyệt chuổi số đầu vào từ phải sang trái nhằm phân biệt các giá trị từ nhỏ đến lớn.
    # tương tự như khi chúng ta xữ lý cho hàm n2w_hundreds
    reversed_large_number = numbers[::-1]

    # Chia chuỗi số đầu vào thành các nhóm con có 3 phần tử.
    # vì cứ 3 phần tử số lại tạo thành một lớp giá trị, như lớp trăm, lớp nghìn, lớp triệu...
    reversed_large_number = chunks(reversed_large_number, 3)

    total_number = []
    before_khong_tram = False
    for e in range(0, len(reversed_large_number)):

        if e == 0:
            value_of_hundred = reversed_large_number[0][::-1]
            text_hundred = n2w_hundreds(value_of_hundred)
            if text_hundred == 'không trăm':
                continue
            total_number.append(n2w_hundreds(value_of_hundred))
        if e == 1:
            value_of_thousand = reversed_large_number[1][::-1]
            text_hundred = n2w_hundreds(value_of_thousand)
            if text_hundred == 'không trăm': 
                continue
            total_number.append(text_hundred + random.choice(['-nghìn-', '-ngàn-']))
        if e == 2:
            value_of_million = reversed_large_number[2][::-1]
            text_hundred = n2w_hundreds(value_of_million)
            if text_hundred == 'không trăm': continue
            total_number.append(text_hundred + '-triệu-')
        if e == 3:
            value_of_billion = reversed_large_number[3][::-1]
            text_hundred = n2w_hundreds(value_of_billion)
            # if text_hundred == 'không trăm': continue
            total_number.append(text_hundred + '-tỷ-')
    
    # print(numbers, total_number)
    total_number = total_number[:-1] if total_number[-1] == 'không trăm' else total_number
    return ''.join(total_number[::-1]).strip()


if __name__ == '__main__':

    number = '115205201211'
    print(n2w_large_number(number))
