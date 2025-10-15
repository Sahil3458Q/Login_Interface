
def cap(st):
    result = "".join([st[k].upper() if  k%2 == 0 else st[k].lower()  for k in range(0,len(st))])
    return result

def add_space(text, index):
    text = [char for char in text]
    for k in range(0,len(index)):
        text.insert(index[k]," ")
    text = "".join(text)
    return text

def main():
    text = input("Enter your string : ")    
    if  all(char.isalpha() or char.isspace()for char in text) :
        if " " in text:
            space_index = []
            text = [char for char in text]
            space_constant = 0
            while " " in text:
                space_position = text.index(" ")
                space_index.append(space_position+space_constant)
                del text[space_position]
                space_constant+=1
            text = "".join(text)
            text = cap(text)
            text = add_space(text,space_index)
            print(text)
        else :
            print(cap(text))
    elif text == "":
        print("No string entered")
    else:
        print("Your sentence contains character than alphabets")

if  __name__ == "__main__":
    main()
