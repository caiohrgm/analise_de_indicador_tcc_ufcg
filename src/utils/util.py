def format_string(data_list):
    cmps = ''
    size = len(data_list)
    for i in range(size):
        if i == 0:
            cmps = cmps + str(data_list[i])
        elif i == (size-1):
            cmps = cmps + " e " + str(data_list[i])
        else:
            cmps = cmps + " , " + str(data_list[i])
    
    return cmps