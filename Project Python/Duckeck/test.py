with open('genom.txt', 'r') as f:
    my_dict = dict(line.split() for line in f)  
    # works only if file only contains lines that split into exactly 2 tokens