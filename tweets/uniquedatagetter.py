file= open("Albany_AB.txt", "r").readlines()
content_set=set(file)
data = open("Raw_data_unique.txt","w")
for line in content_set:
    data.write(line)