import random
import time

decompose = False
main_memory_size = (2**10)*int(input("Please choose the Main memory size in KO: "))
cache_size = (2**10)*int(input("Please choose Cache size in  KO: "))
block_size = int(input("Please choose block size: "))
cache_lines_number = int(input("Please, choose the set associative type: "))

main_memory_blocks_number = int(cache_size / block_size)
main_memory_lines_number = int(main_memory_size/main_memory_blocks_number)

cpu_requests_num = int(input("Please set cpu requests number: "))
number_of_testing_phases = int(input("Please set testing phases number: "))
replacement_algorithm = input("select a replacement algorithm 'lru' or 'random' :")
writing_algorithm = input("select a writing algorithm write through 'WT' or write back 'WB' :")
print("Informations...")
print("main memory size: ", int(main_memory_size/(2**10)), " ko")
print("cache size: ", int(cache_size/(2**10)), "ko")
print("block size: ", block_size, " word")
print("blocks number: ", main_memory_blocks_number)
print("main memory lines number: ", main_memory_lines_number)
print("cache-", cache_lines_number, "- set associative")
print("cpu requests number: ", cpu_requests_num)
print("Number of testing phases: ", number_of_testing_phases)
print("Replacement algorithm: ", replacement_algorithm)
print("Writing algorithms: ", writing_algorithm)
time.sleep(4)
print("Start execution...")
time.sleep(5)


# Creating Main Memory and fill it
print("Main memory generating...")
time.sleep(4)
main_memory = [[random.randint(1, 100) for j in range(main_memory_blocks_number)] for i in range(main_memory_lines_number)]
print("main memory :")
for row in main_memory:
    print("")
    for col in row:
        print(col, end=" ")
print("")
time.sleep(4)
# Creating cache and fill it
print("Cache generating...")
time.sleep(4)
cache = [[[0 for k in range(2)] for j in range(main_memory_blocks_number)] for i in range(cache_lines_number)]
for row in cache:
    c = 0
    for col in row:
        v = random.randint(0, main_memory_lines_number-1)
        col[0] = v
        col[1] = main_memory[v][c]
        c += 1
# printing cache
print("Cache:(Initial)")
for row in cache:
    print("")
    for col in row:
        print(col, end=" ")
print("")
time.sleep(4)
print("Generating CPU requests...")
# Generating CPU requests randomly
cpu_requests = []
for i in range(cpu_requests_num):
    if decompose:
        address = range(main_memory_blocks_number*main_memory_lines_number)
    cpu_requests.append(address)
# Printing CPU requests
print("CPU requests: ")
for r in range(len(cpu_requests)):
    print("CPU request num ", r, " is: ", cpu_requests[r])
time.sleep(4)
# Setting up lru buffer
lru = []
for x in range(main_memory_blocks_number):
    tab2= []
    for l in range(cache_lines_number):
        tab2.append(l)
    lru.append(tab2)

# Executing and testing in 5 phases
for i in range(1, number_of_testing_phases+1):
    print("EXE phase number ", i)
    time.sleep(2)
    h = 0
    main_memory_lines_number = 0
    for req in range(0, cpu_requests_num):
        hit = False
        requested_address_tag = cpu_requests[req][0]
        requested_address_column = cpu_requests[req][1]

        if decompose:
            requested_address_tag = address / (main_memory_blocks_number * block_size)
            requested_address_column = divmod(address, (main_memory_blocks_number * block_size)) / block_size
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
                changes = random.randrange(1, number_of_testing_phases+1)
                print("CPU will change the value: ", changes, "times")
                if (writing_algorithm == 'WT'):
                    print("Using write through algorithm...")
                    for change in range(changes):
                        word = random.randrange(100)
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
                    print("Error")
                    break
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
                randomly = random.randint(0, main_memory_blocks_number)
                cache[randomly][requested_address_column][0] = requested_address_tag
                cache[randomly][requested_address_column][1] = main_memory[requested_address_tag][requested_address_column]
            else:
                print("Error")
                break
            main_memory_lines_number= main_memory_lines_number + 1
            print("Cache:(After update)")
            for row in cache:
                print("")
                for col in row:
                    print(col, end=" ")
            print("")


    hits_rate = (h / (h + main_memory_lines_number) * 100)
    print("Hit: ", h)
    print("Miss: ", main_memory_lines_number)
    print("Hits rate: ", hits_rate, "%   -----------------------------------------------------------------------------------------------------------")
time.sleep(5)




