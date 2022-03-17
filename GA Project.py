import random
import math

def generateChromosome():
    return [(random.randint(-10,10)), (random.randint(-10,10))]

def to_binary(n):
    t = n
    chromosome = []
    n = bin(abs(n)).replace("0b", "")
    for _ in range(0, len(n)+ 1):
        chromosome.append(0)
    i = len(n)
    g = len(chromosome)
    while(i != 0):
        chromosome[g-1] = int(n[i-1])
        i -= 1
        g -= 1
    if(t < 0): chromosome[0] = 1
    return chromosome

def to_decimal(chromosome):
    n = 0
    total = 0
    for q in range(-(len(chromosome)-1), 1):
        o = 2**n
        q = abs(q)
        if((q == len(chromosome)-1) and chromosome[q] == 1): total += 1
        else:
            if((q == 0) and chromosome[q] == 1): total *= -1
            else:
                if(chromosome[q] == 1): total += o
        n += 1
    return int(total)

def ChromosomeCombine(chromosome1,chromosome2): #nyatuin chromosome x dan y
    p = []
    if(len(chromosome1) > len(chromosome2)):
        r = len(chromosome1) - len(chromosome2)
        for _ in range(0, r):
            p.append(0)
        if(chromosome2[0]==1):
            chromosome2[0] = 0
            chromosome2 = p + chromosome2
            chromosome2[0] = 1
        else : chromosome2 = p + chromosome2
    elif(len(chromosome2) > len(chromosome1)):
        r = len(chromosome2) - len(chromosome1)
        for _ in range(0, r):
            p.append(0)
        if(chromosome1[0]==1):
            chromosome1[0] = 0
            chromosome1 = p + chromosome1
            chromosome1[0] = 1
        else : chromosome1 = p + chromosome1
        
    return chromosome1 + chromosome2

def ChromosomeSplit(chromosome): #misahin chromosome xy
    return chromosome[:len(chromosome)//2], chromosome[len(chromosome)//2:]

def generatePopulation(n): #buat banyak jenis chromosom
    populate = []
    for _ in range(n):
        x, y = generateChromosome()
        populate.append(ChromosomeCombine(to_binary(x),to_binary(y)))

    return populate

def selection():
    return 0

def crossover():
    return 0

def mutation():
    return 0

def formula(x : int, y : int): #Implementasi Formula yang ada di pdf
    return (((math.cos(x) + math.sin(y))**2)/((x**2) + (y**2)))

def fitness(populate):
    return

#Main
for i in range(0, 10):
    print(f'{i}---------------------')
    x, y = generateChromosome()
    print(x, y)
    chromosome_x = to_binary(x)
    chromosome_y = to_binary(y)
    print(chromosome_x, chromosome_y)
    chromosome_xy = ChromosomeCombine(chromosome_x, chromosome_y)
    print(chromosome_xy)
    chromosome_x, chromosome_y = ChromosomeSplit(chromosome_xy)
    print(chromosome_x, chromosome_y)
    x = to_decimal(chromosome_x)
    y = to_decimal(chromosome_y)
    print(x, y)