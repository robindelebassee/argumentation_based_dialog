import matplotlib.pyplot as plt


x = [10, 20, 30, 40, 50, 100]
scores = [1.254901961, 1.157422969, 0.633333333, 0.704682899, 0.273284314, 0.173274971]

plt.plot(x, scores, 'b', color='blue')
plt.xlabel('Number of items in the corpus')
plt.ylabel('Average score on 17 experiments')
plt.title('Scores depending on the number of items in the corpus')
plt.savefig('figures/average_scores_on_item_number.jpg')
plt.show()