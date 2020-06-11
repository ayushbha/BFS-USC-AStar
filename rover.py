from operator import attrgetter
file2=open("output.txt","w")
file2.truncate(0)
class Path:
	def __init__(self, cur_pos_x, cur_pos_y, height,cost,parent,f_n):
		self.cur_pos_x = cur_pos_x
		self.cur_pos_y = cur_pos_y
		self.height= height
		self.cost = cost
		self.parent = parent
		self.f_n = f_n

	def check_goals(cur_pos_x,cur_pos_y,target_site_x,target_site_y):
		if cur_pos_x==target_site_x and cur_pos_y==target_site_y:
			return 1
		else:
			return 0	

	def check_goals1(cur_pos_x,cur_pos_y,target_site_x,target_site_y,goal_filled):
		o=0
		count=0
		while o<len(target_site_x):
			if cur_pos_x==target_site_x[o] and cur_pos_y==target_site_y[o] and goal_filled[o]==0:
				goal_filled[o]=1
				count=1
			o=o+1
		if count==0:
			return 0
		else:
			return 1

	def printpath(c,path):
		while c.parent!=[]:
			path=str(c.cur_pos_y)+','+str(c.cur_pos_x)+' '+path
			c=c.parent
		path=str(c.cur_pos_y)+','+str(c.cur_pos_x)+' '+path
		file2.write(path)
		return 0

	def printpath1(c,path,count,target_site_x,target_site_y,no_of_targets,list_path):
		o=0
		k=[]
		while o<len(target_site_x):
			if c.cur_pos_x==target_site_x[o] and c.cur_pos_y==target_site_y[o]:
				k.append(o)
			o=o+1
		a=len(k)
		while c.parent!=[]:
			path=str(c.cur_pos_y)+','+str(c.cur_pos_x)+' '+path
			c=c.parent
		path=str(c.cur_pos_y)+','+str(c.cur_pos_x)+' '+path
		i=0
		while i<a:
			list_path[k[i]]=path
			i=i+1
		return count+a,list_path

	def Heuristic_function(pos_x,pos_y,target_site_x,target_site_y):
		h_d = min(abs(pos_x-target_site_x),abs(pos_y-target_site_y))
		h_s = abs(pos_x-target_site_x) + abs(pos_y-target_site_y)
		return 14 * h_d + 10 * (h_s - 2*h_d)

	def getAdjacentSpaces(x, y):
		spaces=[]
		spaces.append([x-1, y-1])
		spaces.append([x+1, y+1])  
		spaces.append([x+1, y-1])  
		spaces.append([x-1, y+1])
		spaces.append([x-1, y])
		spaces.append([x+1, y])  
		spaces.append([x, y-1])  
		spaces.append([x, y+1])
		return spaces

class AI:
	def extract(k):
		i=0
		n=len(k)
		x=''
		y=''
		while ' '!=k[i]:
			x = x + k[i]
			i=i+1
		i=i+1
		while i<n:
			y = y + k[i]
			i=i+1
		x=int(x)
		y=int(y)
		return x,y

	def A_star(grid_row,grid_column,landing_site_x,landing_site_y,height_Diff,no_of_targets,graph,target_site_x,target_site_y):
		q=Path(landing_site_x,landing_site_y,graph[landing_site_x][landing_site_y],0,[],Path.Heuristic_function(landing_site_x,landing_site_y,target_site_x,target_site_y))
		paths=""
		queue=[]
		closed=[]
		f=[]
		child_queue=[]
		visited=[[0 for i in range(grid_column)] for j in range(grid_row)]
		temp_visited=[[0 for i in range(grid_column)] for j in range(grid_row)]
		l=Path.check_goals(q.cur_pos_x,q.cur_pos_y,target_site_x,target_site_y)
		if l==1:
			paths=str(q.cur_pos_y)+','+str(q.cur_pos_x)
			return paths
		else:
			queue.append(q)
			temp_visited[q.cur_pos_x][q.cur_pos_y]=1
			while queue:
				f=queue[0]
				del queue[0]
				l=Path.check_goals(f.cur_pos_x,f.cur_pos_y,target_site_x,target_site_y)
				if l==1:
					return Path.printpath(f,paths)
				child_queue.clear()
				child_queue=Path.getAdjacentSpaces(f.cur_pos_x,f.cur_pos_y)
				while child_queue:
					if child_queue[0][0]<grid_row and child_queue[0][1]<grid_column and child_queue[0][0]>=0 and child_queue[0][1]>=0 and abs(f.height-graph[child_queue[0][0]][child_queue[0][1]])<=height_Diff and visited[child_queue[0][0]][child_queue[0][1]]==0:
						g=child_queue[0][0]
						h=child_queue[0][1]
						if g!=f.cur_pos_x and h!=f.cur_pos_y:
							q=Path(g,h,graph[g][h],f.cost+abs(f.height-graph[g][h])+14,f,0)
						else:
							q=Path(g,h,graph[g][h],f.cost+abs(f.height-graph[g][h])+10,f,0)
						h_n=Path.Heuristic_function(q.cur_pos_x,q.cur_pos_y,target_site_x,target_site_y)
						q.f_n=h_n+q.cost
						o=0
						if temp_visited[g][h]==0:
							queue.append(q)
							temp_visited[g][h]=1
						elif temp_visited[g][h]==1:
							u=len(queue)	
							while o<u:
								if g==queue[o].cur_pos_x and h==queue[o].cur_pos_y:
									if q.cost<queue[o].cost:
										del queue[o]
										queue.append(q)
									break
								o=o+1
					del child_queue[0]
				closed.append(f)
				visited[f.cur_pos_x][f.cur_pos_y]=1
				queue.sort(key = attrgetter('f_n'))
		return "FAIL"		

	def UCS(grid_row,grid_column,landing_site_x,landing_site_y,height_Diff,no_of_targets,graph,target_site_x,target_site_y):
		q=Path(landing_site_x,landing_site_y,graph[landing_site_x][landing_site_y],0,[],0)
		paths=""
		queue=[]
		closed=[]
		count=0
		goal_filled=[]
		goal_filled=[0 for i in range(no_of_targets)]
		f=[]
		list_path=[]
		list_path=["" for i in range(no_of_targets)]
		child_queue=[]
		visited=[[0 for i in range(grid_column)] for j in range(grid_row)]
		temp_visited = [[0 for i in range(grid_column)] for j in range(grid_row)]
		l=Path.check_goals1(q.cur_pos_x,q.cur_pos_y,target_site_x,target_site_y,goal_filled)
		if l==1:
			count,list_path=Path.printpath1(q,paths,count,target_site_x,target_site_y,no_of_targets,list_path)
		if count<no_of_targets:
			queue.append(q)
			temp_visited[q.cur_pos_x][q.cur_pos_y]=1
			while queue and count!=no_of_targets:
				f=queue[0]
				del queue[0]
				l=Path.check_goals1(f.cur_pos_x,f.cur_pos_y,target_site_x,target_site_y,goal_filled)
				if l==1:
					count,list_path=Path.printpath1(f,paths,count,target_site_x,target_site_y,no_of_targets,list_path)
					if count==no_of_targets:
						break
				child_queue.clear()
				child_queue=Path.getAdjacentSpaces(f.cur_pos_x,f.cur_pos_y)
				while child_queue:
					if child_queue[0][0]<grid_row and child_queue[0][1]<grid_column and child_queue[0][0]>=0 and child_queue[0][1]>=0 and abs(f.height-graph[child_queue[0][0]][child_queue[0][1]])<=height_Diff and visited[child_queue[0][0]][child_queue[0][1]]==0:
						g=child_queue[0][0]
						h=child_queue[0][1]
						if g!=f.cur_pos_x and h!=f.cur_pos_y:
							q=Path(g,h,graph[g][h],f.cost+14,f,0)
						else:
							q=Path(g,h,graph[g][h],f.cost+10,f,0)
						if temp_visited[g][h]==0:
							queue.append(q)
							temp_visited[g][h]=1
						elif temp_visited[g][h]==1:
							for u in queue:
								if g==u.cur_pos_x and h==u.cur_pos_y:
									if q.cost<u.cost:
										del u
										queue.append(q)
									break
					del child_queue[0]
				visited[f.cur_pos_x][f.cur_pos_y]=1
				closed.append(f)
				queue.sort(key = attrgetter('cost'))
		o=0
		while o<no_of_targets:
			if list_path[o]=="":
				list_path[o]="FAIL"
			o=o+1
		o=0
		while o<no_of_targets-1:
			file2.write(list_path[o]+"\n")
			o=o+1
		file2.write(list_path[o])
		return 0

	def BFS(grid_row,grid_column,landing_site_x,landing_site_y,height_Diff,no_of_targets,graph,target_site_x,target_site_y):
		q=Path(landing_site_x,landing_site_y,graph[landing_site_x][landing_site_y],0,[],0)
		paths=""
		queue=[]
		goal_filled=[]
		goal_filled=[0 for i in range(no_of_targets)]
		f=[]
		count=0
		list_path=[]
		child_queue=[]
		list_path=["" for i in range(no_of_targets)]
		visited=[[0 for i in range(grid_column)] for j in range(grid_row)]
		l=Path.check_goals1(q.cur_pos_x,q.cur_pos_y,target_site_x,target_site_y,goal_filled)
		if l==1:
			count,list_path=Path.printpath1(q,paths,count,target_site_x,target_site_y,no_of_targets,list_path)
		if count<no_of_targets:
			visited[q.cur_pos_x][q.cur_pos_y]=1
			queue.append(q)
			while queue and count!=no_of_targets:
				f=queue[0]
				del queue[0]
				child_queue.clear()
				child_queue=Path.getAdjacentSpaces(f.cur_pos_x,f.cur_pos_y)
				while child_queue:
					if child_queue[0][0]<grid_row and child_queue[0][1]<grid_column and child_queue[0][0]>=0 and child_queue[0][1]>=0 and abs(f.height-graph[child_queue[0][0]][child_queue[0][1]])<=height_Diff and visited[child_queue[0][0]][child_queue[0][1]]==0:
						g=child_queue[0][0]
						h=child_queue[0][1]
						q=Path(g,h,graph[g][h],f.cost+1,f,0)
						l=Path.check_goals1(g,h,target_site_x,target_site_y,goal_filled)
						if l==1:
							count,list_path=Path.printpath1(q,paths,count,target_site_x,target_site_y,no_of_targets,list_path)
							if count==no_of_targets:
								break
						else:
							queue.append(q)
							visited[g][h]=1
					del child_queue[0]
		o=0
		while o<no_of_targets:
			if list_path[o]=="":
				list_path[o]="FAIL"
			o=o+1
		o=0
		while o<no_of_targets-1:
			file2.write(list_path[o]+"\n")
			o=o+1
		file2.write(list_path[o])
		return 0

	if __name__ == "__main__":
		graph=[]
		file1 = open("input6.txt","r")
		a=file1.readlines()
		file1.close()
		a=[x.rstrip('\n') for x in a]
		target_site_x=[]
		target_site_y=[]
		method = a[0]
		grid_column , grid_row=extract(a[1])
		landing_site_y,landing_site_x = extract(a[2])
		height_Diff = int(a[3])
		no_of_targets = int(a[4])
		j=0
		while j<no_of_targets:
			target_site_y_,target_site_x_ =extract(a[5+j])
			target_site_x.append(target_site_x_)
			target_site_y.append(target_site_y_)
			j=j+1
		z=5+j
		j=0
		graph_=[]
		while j<grid_row:
			graph.append(a[z+j].split())
			j=j+1
		j=0
		k=0
		while j<grid_row:
			k=0
			while k<grid_column:
				graph[j][k]=int(graph[j][k])
				k=k+1
			j=j+1
		if method == 'BFS':
			z=BFS(grid_row,grid_column,landing_site_x,landing_site_y,height_Diff,no_of_targets,graph,target_site_x,target_site_y)

		elif method == 'UCS':
			z=UCS(grid_row,grid_column,landing_site_x,landing_site_y,height_Diff,no_of_targets,graph,target_site_x,target_site_y)

		elif method == 'A*':
			i=0
			while no_of_targets!=0 and i<no_of_targets:
				if target_site_x[i]<grid_row and target_site_y[i]<grid_column:
					path_ = A_star(grid_row,grid_column,landing_site_x,landing_site_y,height_Diff,no_of_targets,graph,target_site_x[i],target_site_y[i])
					if path_!=0:
						file2.write(path_)
					if i<no_of_targets-1:
						file2.write("\n")
				else:
					if i<no_of_targets-1:
						file2.write("FAIL\n")
					else:
						file2.write("FAIL")
				i=i+1