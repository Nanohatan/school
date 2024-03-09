import matplotlib.pyplot as plt
import fish
import json
 
# Opening JSON file
f = open('params//params.json')
data = json.load(f)
f.close()
school = fish.school()

params1 = data[0]
school.create_fish(params1,2)
params2 = data[1]
school.create_fish(params2,6)

fig,ax = plt.subplots()
xy = school.get_position()
ax.scatter(xy[:,0],xy[:,1])

for i in range(100):
    school.update()

hist_matrix = school.get_history()
print(hist_matrix.shape)
for ind in range(8):
    ax.plot(hist_matrix[ind,:,0],hist_matrix[ind,:,1])
    ax.text(hist_matrix[ind,-1,0],hist_matrix[ind,-1,1],ind)
plt.show()
