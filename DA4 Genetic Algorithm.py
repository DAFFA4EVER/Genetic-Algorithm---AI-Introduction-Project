import struct # used for decode and encode (important)
import random # used for generate random value (important)
import math # used for function h formula (important)
import time # used for check how long this program take
import matplotlib.pyplot as plt # used for visualization

def generatePhenotype(min, max): 
    return random.uniform(min,max)

def float_to_bin(num):
    global precision
    return bin(struct.unpack('!I', struct.pack('!f', num))[0])[2:].zfill(int(precision/2))

def bin_to_float(binary):
    return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]
    
def to_chromosomeXY(x, y): # combine binary x and y into one
    return x+y

def createPopulation(population_, max, minRange, maxRange): # generate random population
    i = len(population_)
    while(i != max):
        d = dict()
        d['x'] = generatePhenotype(minRange,maxRange)
        d['y'] = generatePhenotype(minRange,maxRange)
        d['c'] = to_chromosomeXY(float_to_bin(d['x']),float_to_bin(d['y']))
        d['v'] = 5
        population_.append(d)
        i += 1
    return population_

def crossover(population, max_population): 
    list_cross = stochasticWheel(max_population, 2) # population already sorted
    while(len(list_cross) < 2):
        list_cross.append(stochasticWheel(max_population, 2)[0]) # in case list_cross only return 1 value

    length = len(population[0]['c'])
    a = random.randint(0, (length-1))
    b = random.randint(a+1, (length-1))
    buffer1 = population[list_cross[0]]['c'][a:b] # target1
    buffer2 = population[list_cross[1]]['c'][a:b] # target2
    population[list_cross[0]]['c'] = population[list_cross[0]]['c'][:a] + buffer2 + population[list_cross[0]]['c'][b:]
    population[list_cross[1]]['c'] = population[list_cross[1]]['c'][:a] + buffer1 + population[list_cross[1]]['c'][b:]
    return population
    
def mutation(population, max_population):
    list_cross = stochasticWheel(max_population, 1)
    length = len(population[0]['v'])
    for i in range(0, length):
        if((random.randint(0,1)) == 1):
            population[list_cross[0]][i] = random.randint(0,1)

    return population


def stochasticWheel(length, k_value): # probability with sthochastic wheel
    weight = []
    priority = []
    for i in range(1, length+1):
        weight.append((i/length))
        priority.append(i-1)
    # weight will be looks like this [1/length,2/length,3/length,......,n/length]
    # priority will be looks like this [0, 1, 2, 3, 4,...., length]
    return list(set(random.choices(priority, weights=weight, k=k_value)))

def fitness(popu, max_pop, minRange, maxRange): # enters value x, y to get function h result
    global precision
    for i in range(0, max_pop):
        data = popu[i]['c']
        x = data[:int(precision/2)]
        y = data[int(precision/2):precision]
        x = bin_to_float(x), bin_to_float(y)
        if((x not in range(-5,6) and (y not in range(-5,6)))):
            data = to_chromosomeXY(float_to_bin(generatePhenotype(minRange, maxRange)),float_to_bin(generatePhenotype(minRange, maxRange)))
            x = data[:int(precision/2)]
            y = data[int(precision/2):precision]
            x, y = bin_to_float(x), bin_to_float(y)

        d = dict()
        d['v'] = (((math.cos(x) + math.sin(y))*(math.cos(x) + math.sin(y)))/((x*x) + (y*y) + 0.00000000000000001)) # 0.00000000000000001 to avoid division by 0
        d['c'] = data
        d['x'] = x
        d['y'] = y
        popu[i] = d
    return popu

def sorting_value(value): # sort from lowest/nearest
    value = sorted(value, key=lambda i: abs(i['v'])-0.0)
    return value

def survival(value, max_popu,x ,last, minRange, maxRange): # survival
    y = []
    y = createPopulation(y,1, minRange, maxRange)
    y = fitness(y,1, minRange, maxRange)
    value[max_popu-1] = y[0] # replace the last one with the new another one
        # target harus 
    value = sorted(value, key=lambda i: abs(i['v'])-0)
    result = value[0]
    if(x != 0):
        a = result['v'] # Current Smallest Result
        b = last['v'] # Last Smallest Result
        if(a < b):
            print(f"Take CURRENT : {a} < Dump LAST : {b}")
            print("Rounded => Take CURRENT : {0:.15f} <".format(float(a)),end="")
            print(" Dump LAST : {0:.15f}".format(float(b)))
            value[0] = result # assigned the first index to result
            last = result
        elif(a > b ):
            print(f"Take LAST : {b} < Dump CURRENT : {a}")
            print("Rounded => Take LAST : {0:.15f} <".format(float(b)),end="")
            print(" Dump CURRENT : {0:.15f}".format(float(a)))
            value[0] = last # assigned the first index to min
            last = last
        #print(f'FIX : {evaluate[0]}\n')
    
    return value

def evolution(initial_population, max_population : int, max_generation : int, minRange : int, maxRange :int): # For running the simulation
    global total_simulation
    evaluate = initial_population
    for x in range(0, max_generation):
        print(f'Evolution Generation {x+1}')
        #print(f'UNFIX : {evaluate[0]}')
        evaluate = fitness(evaluate, max_population, minRange, maxRange) 
        evaluate = sorting_value(evaluate) # sort from lowest
        choosing = random.choices([0,1], weights=[0.85,0.15], k=1) # Crossover 0.85 Mutation 0.15
        if(choosing == 1):
            print("Crossover")
            evaluate = crossover(evaluate, max_population)
        elif(choosing == 0):
            print("Mutation")
            evaluate = mutation(evaluate, max_population)
        if(x == 0):
            last = evaluate[0]
        evaluate = survival(evaluate, max_population, x, last, minRange, maxRange)
        result = evaluate[0]
        total_simulation.append(result)
        print(f'Result Generation {x+1} : \n{result}\n')
        last = result

    return evaluate

def visualization_2d(): # visualize the generation growth in 2d
    global total_simulation
    #x =[]
    #for i in total_simulation: x.append(i['x'])
    #y =[]
    #for i in total_simulation: y.append(i['y'])
    z =[]
    for i in total_simulation: z.append(i['v'])
    i = []
    for v in range(0, max_gen): i.append(v+1)

    xdata = i
    ydata = z
    plt.plot(xdata, ydata)
    plt.title("Fitness Growth")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.annotate('Minimum', xy=(xdata[-1],ydata[-1]), arrowprops=dict(facecolor='black', shrink=0.05))
    plt.show()

# Main Program
if __name__=="__main__":
    start = time.time() # how long this will take (starting time)
    total_simulation = []
    population = []
    precision = 64 # bits for binary
    if(precision % 2 != 0):
        precision += 1
    max_pop = 6 # max kromosom in one populasi
    max_gen = 120 # max generasi
    minRange = -5 # min domain
    maxRange = 5 # max domain
    population = createPopulation(population, max_pop, minRange, maxRange) # Create initial population
    print('--------------------SIMULATION BEGIN!--------------------------')

    final_generation = evolution(population, max_pop, max_gen, minRange, maxRange)
    final = final_generation[0] # Final Result
    end = time.time() # how long this will take (ending time)
    round_value = '{0:.15f}'.format(final['v'])
    length = final['c']
    print('--------------------SIMULATION STOP!---------------------------')

    print(f'Data Representation Example :\n{final}\nv = Heuristic value\nc = Chromosome\nx = X Value\ny = Y value')
    print(f"""\nConfiguration Details :
The amount of population per-generation = {max_pop}
Total Generation = {max_gen}
Domain Range = ({minRange} to {maxRange})
Binary Precision = {precision}bits""")
    print(f"""--------------------Smallest is-------------------------------
X = {final['x']} Y = {final['y']}
Binary : {final['c']}
Value : {final['v']}\nValue Rounded : {round_value} \n\nTime Duration = {end-start}s""")

    visualization_2d() # 2d representation of each generation