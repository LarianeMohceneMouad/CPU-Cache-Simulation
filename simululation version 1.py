import random
cpu_requests_num = 15
main_memory_blocks_number = 4
m = 32
replacement_algorithm = input("select a replacement algorithm 'lru' or 'random' :")
writing_algorithm = input("select a writing algorithm write through 'WT' or write back 'WB' :")

add = 1
block_size = 1
nombre_col = 1
# Creating Main Memory and fill it
main_memory = [[random.randint(1, 100) for j in range(main_memory_blocks_number)] for i in range(m)]
print("main memory :")
for row in main_memory:
    print("")
    for col in row:
        print(col, end=" ")
print("")
# Creating cache and fill it
cache = [[[random.randint(0, m), random.randint(1, 100)], [random.randint(0, m), random.randint(1, 100)], [random.randint(0, m), random.randint(1, 100)], [random.randint(0, m), random.randint(1, 100)]],
         [[random.randint(0, m), random.randint(1, 100)], [random.randint(0, m), random.randint(1, 100)], [random.randint(0, m), random.randint(1, 100)], [random.randint(0, m), random.randint(1, 100)]],
         [[random.randint(0, m), random.randint(1, 100)], [random.randint(0, m), random.randint(1, 100)], [random.randint(0, m), random.randint(1, 100)], [random.randint(0, m), random.randint(1, 100)]],
         [[random.randint(0, m), random.randint(1, 100)], [random.randint(0, m), random.randint(1, 100)], [random.randint(0, m), random.randint(1, 100)], [random.randint(0, m), random.randint(1, 100)]]]
# printing cache
print("Cache:(Initial)")
for row in cache:
    print("")
    for col in row:
        print(col, end=" ")

print("")
# Generating CPU requests randomly
cpu_requests= []
for i in range(0, cpu_requests_num):
    address = [random.randint(0, 15), random.randint(0, 3)]
    cpu_requests.append(address)
# Printing CPU requests
print("CPU requests: ")
for r in range(len(cpu_requests)):
    print("CPU request num ", r, " is: ", cpu_requests[r])
# Setting up lru buffer
lru = []
for x in range(4):
    tab2= []
    for l in range(4):
        tab2.append(l)
    lru.append(tab2)


# Executing and testing in 2 phases
for i in range(0, 2):
    h = 0
    m = 0
    for req in range(0, cpu_requests_num):
        hit = False
        dec = False


        requested_address_tag = cpu_requests[req][0]
        requested_address_column = cpu_requests[req][1]

        if dec:
            requested_address_tag = add / (nombre_col * block_size)
            requested_address_column = divmod(add, (nombre_col * block_size)) / block_size
        print("Requested address, line/tag: ", requested_address_tag, "block: ", requested_address_column)

        for cache_row in cache:
            if(cache_row[requested_address_column][0] == requested_address_tag):
                hit = True
                word = cache_row[requested_address_column][1]
                word_cache_row = cache_row

        if(hit):
            print("Hit, Returned word to the CPU is:", word)

            h = h+1
            modify = random.choice([True, False])
            if (modify== False):
                print("cpu won't modify the word")
            else:
                print("CPU need to update the returned value...")
                changes = random.randrange(1, 5)
                print("CPU will change the value: ", changes, "times")
                if (writing_algorithm == 'WT'):
                    print("Using write through algorithm...")
                    for change in range(changes):
                        word = random.randrange(0, 100)
                        print("cpu changed the word value to :", word)
                        print("Updating word in cache...")
                        word_cache_row[requested_address_column][1] = word
                        print("word update in cache : Done")
                        print("Cache:(After update)")
                        for row in cache:
                            print("")
                            for col in row:
                                print(col, end=" ")
                        print("")
                        print("Updating word in main memory...")
                        main_memory[requested_address_tag][requested_address_column] = word
                        print("word update in main memory : Done")
                elif (writing_algorithm == 'WB'):
                    print("Using write back algorithm...")
                    for change in range(changes):
                        print("cpu changed the word value")
                        word = random.randrange(0, 100)
                        print("Updating word in cache...")
                        word_cache_row[requested_address_column][1] = word
                        print("word update in cache : Done")
                        print("Cache:(After update)")
                        for row in cache:
                            print("")
                            for col in row:
                                print(col, end=" ")
                        print("")
                    print("Updating word in main memory...")
                    main_memory[requested_address_tag][requested_address_column] = word
                    print("word update in main memory : Done")
        else:
            if (replacement_algorithm == "lru") :
                print("Miss, Updating cache for address(line/column/word) using 'LRU' : ", "(", requested_address_tag, "/", requested_address_column, "/", main_memory[requested_address_tag][requested_address_column], ")")
                case = lru[requested_address_column]
                value = case[0]
                lru[requested_address_column].pop(0)
                lru[requested_address_column].append(value)
                cache[value][requested_address_column][0] = requested_address_tag
                cache[value][requested_address_column][1] = main_memory[requested_address_tag][requested_address_column]
            elif (replacement_algorithm == "random"):
                print("Miss, Updating cache for address(line/column/word) using 'Randomly' : ", "(", requested_address_tag, "/", requested_address_column, "/", main_memory[requested_address_tag][requested_address_column], ")")
                randomly = random.randint(0, 3)
                cache[randomly][requested_address_column][0] = requested_address_tag
                cache[randomly][requested_address_column][1] = main_memory[requested_address_tag][requested_address_column]
            m= m + 1
            print("Cache:(After update)")
            for row in cache:
                print("")
                for col in row:
                    print(col, end=" ")
            print("")


    hits_rate = (h / (h + m) * 100)
    print("Hit: ", h)
    print("Miss: ", m)
    print("Hits rate: ", hits_rate, "%   -----------------------------------------------------------------------------------------------------------")




