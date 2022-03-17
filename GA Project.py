import random
import math

def generateChromosome():
    return [(random.randint(-5,5)), (random.randint(-5,5))]

def to_binary(n):
    chromosome = [0,0,0,0]
    if(n < 0): chromosome[0] = 1
    n = bin(abs(n)).replace("0b", "")
    i = len(n)
    g = len(chromosome)
    while(i != 0):
        chromosome[g-1] = int(n[i-1])
        i -= 1
        g -= 1
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
        for i in range(0, r+1):
            p.append(0)
        if(chromosome2[0]==1):chromosome2 = chromosome2[:0] + p + chromosome2[1:len(chromosome2)]
        else : p + chromosome2
    if(len(chromosome2) > len(chromosome1)):
        r = len(chromosome2) - len(chromosome1)
        for i in range(0, r+1):
            p.append(0)
        if(chromosome1[0]==1):chromosome1 = chromosome1[:0] + p + chromosome1[1:len(chromosome1)]
        else : p + chromosome1
        
    return chromosome1 + chromosome2

def ChromoseSplit(chromosome): #misahin chromosome xy
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
