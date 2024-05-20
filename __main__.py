import matplotlib.pyplot as plt
import fish
import json
 
# Opening JSON file
f = open('params//params.json')
data = json.load(f)
f.close()
school = fish.school()
n = 8
n_params1 = 2
steps_between_random_movement = 5 # todo:ランダムな動きを追加する
params1 = data[0]
school.create_fish(params1,n_params1)
params2 = data[1]
school.create_fish(params2,n-n_params1)

fig,ax = plt.subplots()
ax.grid()
xy = school.get_position()
for name in ["AR1","AR2"]:
    ax.scatter(xy[name][:,0],xy[name][:,1])


for i in range(100):
    school.update()

hist_matrix = school.get_history()

for ind in range(n):
    ax.plot(hist_matrix[ind,:,0],hist_matrix[ind,:,1])
    ax.text(hist_matrix[ind,-1,0],hist_matrix[ind,-1,1],ind)
plt.show()
