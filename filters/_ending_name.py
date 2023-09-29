def ending_name(cnt):
    if cnt % 100 in [11, 12, 13, 14]:
        return f'{cnt} файлов'
    elif cnt % 10 == 1:
        return f'{cnt} файл'
    elif cnt % 10 in [2, 3, 4]:
        return f'{cnt} файла'
    else:
        return f'{cnt} файлов' 