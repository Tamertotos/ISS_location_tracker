def read(path):
    credentials_dict = {}
    with open(path) as read_file:
        for line in read_file:
            line = line.strip()
            key,value = line.split("=",1)
            credentials_dict[key.strip()] = value.strip()
    return credentials_dict