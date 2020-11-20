import csv
import numpy as np
import math
import matplotlib.pyplot as plt

def fileRead(file):
    with open(file) as csvDataFile:
        csvReader = csv.reader(csvDataFile, delimiter= ',')
        next(csvReader)
        X = []
        for row in csvReader:
            temp = [float(i) for i in row[1:18]]
            temp.append(-1)
            X.append(temp)

    return np.asarray(X)

def randomCentroids(k, n):
    return np.random.uniform(size=(k, n))

def euclidDist(fileData, centroid):
    sum = 0

    for i in range(len(centroid)):
        sum+= (fileData[i] - centroid[i]) ** 2

    return math.sqrt(sum)


if __name__=="__main__":
    fileData = fileRead('College.csv')
    kMeans = int(input("k = "))
    print("\nIntances per Cluster:")

    J = []
    for k in range(1, kMeans + 1):
        centroid = randomCentroids(k, len(fileData[0]) - 1)

        reallocatedCount = len(fileData) * 0.005 + 1

        while(reallocatedCount > len(fileData) * 0.005):
            reallocatedCount = 0

            distArray = []
            for x in fileData:
                min = cent = 100000

                for i in range(len(centroid)):
                    dist = euclidDist(x, centroid[i])
                    if dist <= min:
                        min = dist
                        cent = i

                distArray.append(min)
                if x[len(x) - 1] != cent:
                    reallocatedCount+= 1
                    x[len(x) - 1] = cent


            for i in range(len(centroid)):
                temp = []
                for x in fileData:
                    if x[len(x) - 1] == i:
                        temp.append(x[:len(x) - 1])

                for j in range(len(centroid)):
                    sum = 0
                    for t in temp:
                        sum+= t[j]

                    if len(temp) > 0:
                        centroid[i][j] = sum/len(temp)


        clusters = [0 for i in range(k)]
        for x in fileData:
            clusters[int(x[len(x) - 1])]+= 1
        print(clusters)

        distSum = 0
        for dist in distArray:
            distSum+= dist
        J.append([k, distSum/len(distArray)])


    maxDist = 0
    bestK = 1
    print("\nCurvature:")
    for i in range(len(J) - 1):
        dist = J[i][1] - J[i + 1][1]
        print(dist)
        if dist > maxDist:
            maxDist = dist
            bestK = i + 2

    print("\nBest K=", bestK)
    J = np.transpose(J)
    plt.plot(J[0], J[1], '-ro',  markevery=[bestK - 1])
    plt.xlabel('K')
    plt.ylabel('Avg. Distance to Centroid')
    plt.title('Best K= %s' % bestK)
    plt.show()
