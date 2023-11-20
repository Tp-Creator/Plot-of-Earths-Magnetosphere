def remove_chars(string:str, chars:str):
    for char in chars:
        string = string.replace(char, "")
        
    return string

color = input()

print(color)

if color[0] == "#":
    print("Color was valid.")

if len(color) == 7:
    print("me")
    
if remove_chars(color, "0123456789abcdef ") == "#":
    print("good")
    
print(remove_chars(color, "0123456789abcdef "))