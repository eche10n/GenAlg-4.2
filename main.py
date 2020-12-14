import random


def getList(dict):
    list = []
    for key in dict.keys():
        list.append(key)

    return list


def initBackpack():
    backpack = list()
    f = open("25.txt")

    # считываю грузоподъемность и вместимость
    firstline = f.readline()
    weight = firstline[0:firstline.index(" ")]
    capacity = firstline[firstline.index(" ") + 1:]
    f.close()

    # построчно считываю остаток файла
    f = open("25.txt")
    for line in f:
        if line == weight + ' ' + capacity:
            continue
        backpack.append(line.split())
    f.close()
    return int(weight), float(capacity), backpack


population_size = 200
weight, capacity, backpack = initBackpack()

population = dict()


# Возвращает один код, полученный жадным алгоритмом
def Greedy(backpack):
    randomNum = random.randint(0, len(backpack))
    current_backpack_weight = 0
    current_backpack_capacity = 0
    gen = dict()
    for i in range(0, len(backpack)):
        gen[i] = 0
    for i in range(randomNum, len(backpack)):
        # Если помещается — берем
        if current_backpack_weight + int(backpack[i][0]) < weight and \
                current_backpack_capacity + float(backpack[i][1]) < capacity:
            current_backpack_weight += int(backpack[i][0])
            current_backpack_capacity += float(backpack[i][1])
            gen[i] = 1
        # Иначе берем сколько можно и выходим
    for i in range(0, len(backpack)):
        # Если помещается — берем
        if current_backpack_weight + int(backpack[i][0]) < weight and \
                current_backpack_capacity + float(backpack[i][1]) < capacity:
            current_backpack_weight += int(backpack[i][0])
            current_backpack_capacity += float(backpack[i][1])
            gen[i] = 1
        # Иначе берем сколько можно и выходим
    return gen


# Создает популяцию
def PopulationCreator(population):
    for i in range(0, population_size):
        population[i] = Greedy(backpack)


PopulationCreator(population)


# population_weight = dict()
# for i in range(0, population_size):
#    population_weight[i] = 0

# Выбор 20% самых самых (по ценности)
def CrossoverSelection(population_weight):
    for i in range(0, population_size):
        for j in range(0, 30):
            if population[i][j] == 1:
                population_weight[i] += int(backpack[j][2])
    population_weight = dict(sorted(population_weight.items(), key=lambda kv: kv[1], reverse=True)[:int(200 * 0.2)])
    return population_weight


# population_weight = CrossoverSelection(population_weight)

# Равномерное скрещивание через случайных родителей
def Crossover():
    parents_copy = population_weight.copy()
    parents = getList(parents_copy)
    newGens = list()
    while parents_copy:
        can_be_parent = getList(parents_copy)
        parent1 = 0
        parent2 = 0
        # Определение родителей
        while (parent1 == parent2):
            parent1 = random.choice(can_be_parent)
            parent2 = random.choice(can_be_parent)

        newGen = dict()
        for genxd in range(0, 2):
            # Создание маски для однородного скрещивания
            mask = dict()
            for i in range(0, 30):
                mask[i] = random.randint(1, 2)

            # Выбор гена с помощью маски
            for i in range(0, 30):
                if mask[i] == 1:
                    newGen[i] = population[parent1][i]
                else:
                    newGen[i] = population[parent2][i]

            newGens.append(newGen)
        del parents_copy[parent1]
        del parents_copy[parent2]

    dictOfGens = {i: newGens[i] for i in range(0, len(newGens))}
    return dictOfGens, parents


# CrossoverRes, CurrentParents = Crossover()


# Мутация инвертированием битов случайной особи
def Mutation(CrossoverResult):
    MutationRes = CrossoverResult.copy()
    randX = random.randint(0, 39)
    for i in CrossoverResult[randX]:
        if MutationRes[randX][i] == 1:
            MutationRes[randX][i] = 0
        else:
            MutationRes[randX][i] = 1
    return MutationRes


# MutationRes = Mutation(CrossoverRes)


# Новая популяция через замену старых родителей потомками
def NewPopulation(parents, MutationRes, population):
    for i in parents:
        counter = 0
        population[i] = MutationRes[counter]
        counter += 1
    return population


# newPop = NewPopulation(CurrentParents, MutationRes, population)

# Самый низкий по цене груз
def cheapest(backpack):
    max_weight = 1000000
    for i in range(0, len(backpack)):
        if int(backpack[i][2]) < max_weight:
            max_weight = int(backpack[i][2])
    return max_weight


# Возвращает лучшего из популяции
def Best(newPopulation):
    forBestWeight = dict()
    for i in range(0, population_size):
        forBestWeight[i] = 0

    for i in range(0, population_size):
        for j in range(0, 30):
            if population[i][j] == 1:
                forBestWeight[i] += int(backpack[j][2])
    forBestWeight = dict(sorted(forBestWeight.items(), key=lambda kv: kv[1], reverse=True)[:1])

    return (forBestWeight)


# Список лучших особей для каждого нового поколения
ListOfBest = list()


# bestInPop = Best(newPop)
# current_best = getList(bestInPop)[0]
# ListOfBest.append(newPop[current_best])

# Возвращает ценность
def getW(gen):
    sum = 0
    for j in range(0, 30):
        if gen[j] == 1:
            sum += int(backpack[j][2])
    return sum


# Возвращает вес
def getVES(gen):
    sum = 0
    for j in range(0, 30):
        if gen[j] == 1:
            sum += int(backpack[j][0])
    return sum


# Возвращает объем
def getP(gen):
    sum = 0
    for j in range(0, 30):
        if gen[j] == 1:
            sum += float(backpack[j][1])
    return sum


# Проверка листа с лучшими
def Check(ListofBest, cheap):
    listofSums = list()
    if len(ListOfBest) >= 2:
        for i in ListofBest:
            listofSums.append(getW(i))
        for i in listofSums:
            for j in listofSums:
                if i != j:
                    if abs(i - j) <= cheap:
                        return 1

    return 0

# Основной цикл, который активирует генетический алгоритм
counter = 0
mostCh = cheapest(backpack)
while (counter <= 500):

    print("Поколение: ", counter)

    population_weight = dict()
    for i in range(0, population_size):
        population_weight[i] = 0

    population_weight = CrossoverSelection(population_weight)

    CrossoverRes, CurrentParents = Crossover()

    MutationRes = Mutation(CrossoverRes)

    newPop = NewPopulation(CurrentParents, MutationRes, population)

    bestInPop = Best(newPop)
    current_best = getList(bestInPop)[0]
    ListOfBest.append(newPop[current_best])

    # Условие выхода из цикла - отличие в лучших меньше или равно самому менее ценному предмету
    if Check(ListOfBest, mostCh) == 1:
        break

    counter += 1

best = 0
bestID = 0

# Выбор лучшего результата из всех (обычно их 1-2)
for i in range(0, len(ListOfBest)):
    if getW(ListOfBest[i]) > best and getP(ListOfBest[i]) < 12 and getVES(ListOfBest[i]) < 13000:
        best = getW(ListOfBest[i])
        bestID = i
        bestIndivid = ListOfBest[i]
        print(bestID)

print("Лучший индивид - ", bestIndivid)
print("Ценность - ", best)

sumOfValue = 0
sumOfW = 0
for i in range(0, 30):
    if bestIndivid[i] == 1:
        sumOfW += int(backpack[i][0])
        sumOfValue += float(backpack[i][1])

print("Объем ", sumOfValue)
print("Вес ", sumOfW)