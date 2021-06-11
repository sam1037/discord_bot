def get_arr(input_list, arr):
    result_list = []
    result = None
    for i, word in enumerate(input_list):
        if word == arr:
            for sub_word in input_list[i+1:]:
                if sub_word.startswith("-"):
                    break
                result_list.append(sub_word)
            result = " ".join(result_list) 
            return result


a = get_arr(["-o1", "o1", "o11", "-o2", "o2", "o22", "o23", "-o3"], "-o3")
print(a)
print("sdfsdf")