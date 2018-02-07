from math import trunc
import pdb

def logic_puzzle_solve():
	trace_on=False
	finishup="N"
	dimxdim=raw_input("Enter puzzle dimension, categories x instances, e.g. 3x4  ")
	groups=int(dimxdim[0:1])
	numcases=int(dimxdim[2:3])
	labels=[]
	##load quantitative labels
	raw_quant=raw_input("Enter quantitative labels, e.g. 12,14,16,18 or NO  ")
	if raw_quant=="NO":
		do_something=True
	else:
		quants = raw_quant.split(",")
		i_quants=[]
		for s in quants:
			i_quants.append(int(s))
		##labels.append(i_quants)
		labels.append(quants)
		q_increment=int(labels[0][1])-int(labels[0][0])

	labelgroup="initialize"
	while labelgroup!="STOP":
		labelgroup=raw_input("Enter label group, e.g. dog,cat,fish,bird or STOP  ")
		lg=labelgroup.split(",")
		print ([lg,labelgroup])
		if labelgroup!="STOP":
			labels.append(lg)
	print[labels]
	flatlabels  = [val for sublist in labels for val in sublist]
	numlabels=groups*numcases
	## create grid now
	onerow=[]
	for i in range(0,numcases): onerow.append("-")
	onesquare=[]
	for i in range(0,numcases): onesquare.append(onerow)
	squares=groups*(groups-1)/2
	squarelabels=[]
	for i in range(0,groups):
		for j in range(i+1,groups):
			squarelabels.append([i,j])
	numsquares=len(squarelabels)
	grid=[]
	for i in range(0,numsquares):
		grid.append([])
		for j in range(0,numcases):
			grid[i].append([])
			for k in range(0,numcases):
				grid[i][j].append("-")
	rules=[]
	simple_equality=[]
	rule="initialize"
	while rule!="STOP":
		rule=raw_input("Enter rule or STOP ")
		wellformed=False
		## check rule types
		## simple equality O=3
		if ("=" in rule):
			if ("+" in rule) or ("-" in rule):
				## quantitative equality
				## turn - into +
				qe_elements=rule.split("=")
				if ("+" in qe_elements[0]):
					q_split=qe_elements[0].split("+")
					store=["qe",int(q_split[1]),q_split[0],qe_elements[1]]
				if ("+" in qe_elements[1]):
					q_split=qe_elements[1].split("+")
					store=["qe",int(q_split[1]),q_split[0],qe_elements[0]]
				if ("-" in qe_elements[0]):
					q_split=qe_elements[0].split("-")
					store=["qe",int(q_split[1]),qe_elements[1],q_split[0]]
				if ("-" in qe_elements[1]):
					q_split=qe_elements[1].split("-")
					store=["qe",int(q_split[1]),qe_elements[0],q_split[0]]
				rules.append(store)
				qe_ind=labelstoindex([store[2],store[3]],labels,squarelabels)
				if qe_ind[4]!=-1:
					grid[qe_ind[4]][qe_ind[0]][qe_ind[1]]="X"
				i_quants=[]
				for s in labels[0]:
					i_quants.append(int(s))
				min_q=min(i_quants)
				max_q=max(i_quants)
				for j in i_quants:
					if j < (min_q+store[1]):
						qe_ind=labelstoindex([store[3],str(j)],labels,squarelabels)
						if qe_ind[4]!=-1:
							grid[qe_ind[4]][qe_ind[0]][qe_ind[1]]="X"
					if j > (max_q-store[1]):
						qe_ind=labelstoindex([store[2],str(j)],labels,squarelabels)
						if qe_ind[4]!=-1:
							grid[qe_ind[4]][qe_ind[0]][qe_ind[1]]="X"
			else:  
				## simple equality
				eq_elements=rule.split("=")
				eq_ind=labelstoindex(eq_elements,labels,squarelabels)
			
				grid=writeo(grid,eq_ind[4],eq_ind[0],eq_ind[1])
				printgrid(grid,labels,squarelabels)	
				
		## exclusive set O<>S<>3<>dog
		if ("<>" in rule):
			ex_elements=rule.split("<>")
			print(ex_elements)
			for i in range(0,len(ex_elements)):
				print("i="+str(i))
				for j in range(i+1,len(ex_elements)):
					## i<>j
					simple_ex=[ex_elements[i],ex_elements[j]]
					ex_ind=labelstoindex(simple_ex,labels,squarelabels)
					print(ex_ind)
					
					## write X
					if ex_ind[4]!=-1:
						grid[ex_ind[4]][ex_ind[0]][ex_ind[1]]="X"
						printgrid(grid,labels,squarelabels)			

		store=["clear"]
		## quantitative inequality O>Z or O<Z
		if (">" in rule) and not("<>" in rule):
			gt_elements=rule.split(">")
			store=["gt",gt_elements[0],gt_elements[1]]
			rules.append(store)
			
		if ("<" in rule) and not("<>" in rule):
			gt_elements=rule.split("<")
			store=["gt",gt_elements[1],gt_elements[0]]
			rules.append(store)

		if store[0]=="gt":
			if q_increment>0:
				## minimum value is in [0].  gt_elements[0] cannot be min value
				min_label=labels[0][0]
				max_label=labels[0][numcases-1]
			else:
				max_label=labels[0][0]
				min_label=labels[0][numcases-1]
			gt_ind=labelstoindex([min_label,store[1]],labels,squarelabels)
			if gt_ind[4]!=-1:
				grid[gt_ind[4]][gt_ind[0]][gt_ind[1]]="X"
			gt_ind=labelstoindex([max_label,store[2]],labels,squarelabels)
			if gt_ind[4]!=-1:
				grid[gt_ind[4]][gt_ind[0]][gt_ind[1]]="X"
			gt_ind=labelstoindex([store[1],store[2]],labels,squarelabels)
			if gt_ind[4]!=-1:
				grid[gt_ind[4]][gt_ind[0]][gt_ind[1]]="X"


			
		## choice 3in(dog,S) or (3,7)in(dog,S)
		if (")in(") in rule:
			minus_parens=rule[1:len(rule)-1]
			step1=minus_parens.split(")in(")
			store=["inc",step1[0].split(","),step1[1].split(",")]
			store_it=False
			##rules.append(store)
			if len(store[1])==2:
				inc_ind=labelstoindex(store[1],labels,squarelabels)
				if inc_ind[4]!=-1:
					grid[inc_ind[4]][inc_ind[0]][inc_ind[1]]="X"
					store_it=True
				else:
					for x in labels[inc_ind[2]]:
						if x not in store[1]:
							for y in store[2]:
								grid=labelx(grid,labels,squarelabels,x,y)
			if len(store[2])==2:
				inc_ind=labelstoindex(store[2],labels,squarelabels)
				if inc_ind[4]!=-1:
					grid[inc_ind[4]][inc_ind[0]][inc_ind[1]]="X"
					store_it=True
				else:
					for x in labels[inc_ind[2]]:
						if x not in store[2]:
							for y in store[1]:
								grid=labelx(grid,labels,squarelabels,x,y)
			if store_it:
				rules.append(store)
					
		printgrid(grid,labels,squarelabels)
		flatgrid1  = [val for sublist in grid for val in sublist]
		flatgrid = [val for sublist in flatgrid1 for val in sublist]
		ocount=flatgrid.count("O")
		if ocount==len(flatgrid1):
			print("Let me stop you right there.")
			printlist(grid,labels)
			rule="STOP"

	for unattached_counter in range(0,20):
		# print("--------------UAC "+str(unattached_counter))
		# if unattached_counter==2:
			# printgrid(grid,labels,squarelabels)
			# print (rules)
			# dummy=raw_input("loop begin")
		## cycle through rule stack
		for rule in rules:
		##	## choices are qe (A+7=B), gt (A>B), and inc(A in (B,C))
			if unattached_counter==2:
				print("pre inc, rule "+str(rule))
				printgrid(grid,labels,squarelabels)
			if rule[0]=="inc":
				## first check if possibilities have been ruled out
				ruleout=False
				if len(rule[1])==2 and len(rule[2])==2:
					inc1=labelstoindex([rule[1][0],rule[2][0]],labels,squarelabels)
					inc2=labelstoindex([rule[1][1],rule[2][1]],labels,squarelabels)					
					if grid[inc1[4]][inc1[0]][inc1[1]]=="X" or grid[inc2[4]][inc2[0]][inc2[1]]=="X":
						grid=labelo(grid,labels,squarelabels,rule[1][0],rule[2][1])
						grid=labelo(grid,labels,squarelabels,rule[2][0],rule[1][1])
						ruleout=True
					inc1=labelstoindex([rule[1][0],rule[2][1]],labels,squarelabels)
					inc2=labelstoindex([rule[1][1],rule[2][0]],labels,squarelabels)					
					if grid[inc1[4]][inc1[0]][inc1[1]]=="X" or grid[inc2[4]][inc2[0]][inc2[1]]=="X":
						grid=labelo(grid,labels,squarelabels,rule[1][0],rule[2][0])
						grid=labelo(grid,labels,squarelabels,rule[2][1],rule[1][1])
						ruleout=True
					if not ruleout:
						## find rule[1] intersection
						int_ind=labelstoindex(rule[1],labels,squarelabels)
						if int_ind[4]!=-1:
							##check horizontals
							for j in range(0,numcases):
								if grid[int_ind[4]][int_ind[0]][j]=="X" and j!=int_ind[1]:
									top_check=labels[squarelabels[int_ind[4]][1]][j]
									grid=labelx(grid,labels,squarelabels,top_check,rule[2][0])
									grid=labelx(grid,labels,squarelabels,top_check,rule[2][1])
							for i in range(0,numcases):
								if grid[int_ind[4]][i][int_ind[1]]=="X" and i!=int_ind[0]:
									left_check=labels[squarelabels[int_ind[4]][0]][i]
									grid=labelx(grid,labels,squarelabels,left_check,rule[2][0])
									grid=labelx(grid,labels,squarelabels,left_check,rule[2][1])
						## find rule[2] intersection
						int_ind=labelstoindex(rule[2],labels,squarelabels)
						if int_ind[4]!=-1:
							##check horizontals
							for j in range(0,numcases):
								if grid[int_ind[4]][int_ind[0]][j]=="X" and j!=int_ind[1]:
									top_check=labels[squarelabels[int_ind[4]][1]][j]
									grid=labelx(grid,labels,squarelabels,top_check,rule[1][0])
									grid=labelx(grid,labels,squarelabels,top_check,rule[1][1])
							for i in range(0,numcases):
								if grid[int_ind[4]][i][int_ind[1]]=="X" and i!=int_ind[0]:
									left_check=labels[squarelabels[int_ind[4]][0]][i]
									grid=labelx(grid,labels,squarelabels,left_check,rule[1][0])
									grid=labelx(grid,labels,squarelabels,left_check,rule[1][1])
					if ruleout:
						rules.remove(rule)
				else:
					if len(rule[1])==1:
						single=rule[1]
						double=rule[2]
					if len(rule[2])==1:
						single=rule[2]
						double=rule[1]
					inc1=labelstoindex([single[0],double[0]],labels,squarelabels)
					if grid[inc1[4]][inc1[0]][inc1[1]]=="X":
						grid=labelo(grid,labels,squarelabels,single[0],double[1])
						ruleout=True
					inc2=labelstoindex([single[0],double[1]],labels,squarelabels)
					if grid[inc2[4]][inc2[0]][inc2[1]]=="X":
						grid=labelo(grid,labels,squarelabels,single[0],double[0])
						ruleout=True
					if not ruleout:
						print(rule)
						int_ind=labelstoindex(double,labels,squarelabels)
						for j in range(0,numcases):
							if grid[int_ind[4]][int_ind[0]][j]=="X" and j!=int_ind[1]:
								top_check=labels[squarelabels[int_ind[4]][1]][j]
								grid=labelx(grid,labels,squarelabels,top_check,single[0])
						for i in range(0,numcases):
							if grid[int_ind[4]][i][int_ind[1]]=="X" and i!=int_ind[0]:
								left_check=labels[squarelabels[int_ind[4]][0]][i]
								grid=labelx(grid,labels,squarelabels,left_check,single[0])
			if unattached_counter==2:
				print("pre gt, rule "+str(rule))
				printgrid(grid,labels,squarelabels)
								
			if rule[0]=="gt":
				solved=False
				## look at maximum value of Greater, X out any equal or higher from Lesser
				max_greater=0
				gt_ind=labelstoindex([min_label,rule[1]],labels,squarelabels)
				for i in range(0,numcases):
					if grid[gt_ind[4]][i][gt_ind[1]]=="-":
						max_greater=i
					if grid[gt_ind[4]][i][gt_ind[1]]=="O":
						max_greater=i
						solved=True
						break
				gt_ind=labelstoindex([max_label,rule[2]],labels,squarelabels)
				for i in range(max_greater,numcases):
					grid[gt_ind[4]][i][gt_ind[1]]="X"
				## look at minimum value of Lesser, X out any equal or lower from Greater
				min_lesser=numcases-1
				gt_ind=labelstoindex([max_label,rule[2]],labels,squarelabels)
				for i in range(numcases-1,-1,-1):
					if grid[gt_ind[4]][i][gt_ind[1]]=="-":
						min_lesser=i
					if grid[gt_ind[4]][i][gt_ind[1]]=="O":
						min_lesser=i
						solved=True
						break
				gt_ind=labelstoindex([max_label,rule[1]],labels,squarelabels)
				for i in range(min_lesser,-1,-1):
					grid[gt_ind[4]][i][gt_ind[1]]="X"
				if solved:
					rules.remove(rule)
			if unattached_counter==2:
				print("pre qe, rule "+str(rule))
				printgrid(grid,labels,squarelabels)
					
			if rule[0]=="qe":
				for j in i_quants:
					if (j + rule[1]) in i_quants:
						qe1=labelstoindex([rule[2],str(j)],labels,squarelabels)
						qe2=labelstoindex([rule[3],str(j+rule[1])],labels,squarelabels)
						if (grid[qe1[4]][qe1[0]][qe1[1]]=="O") or (grid[qe2[4]][qe2[0]][qe2[1]]=="O"):
							writeo(grid,qe1[4],qe1[0],qe1[1])
							writeo(grid,qe2[4],qe2[0],qe2[1])
							rules.remove(rule)
						if (grid[qe1[4]][qe1[0]][qe1[1]]=="X") or (grid[qe2[4]][qe2[0]][qe2[1]]=="X"):
							grid[qe1[4]][qe1[0]][qe1[1]]="X"
							grid[qe2[4]][qe2[0]][qe2[1]]="X"

		## geometry checks, in the rule loop
		for h in range(0,numsquares):
			for i in range(0,numcases):
				if grid[h][i].count("O")==1:
					j=grid[h][i].index("O")
					grid=geometry(h,i,j,grid,labels,squarelabels)
			
		## exclusive checks, in the rule loop
		for h in range(0,numsquares):
			## check horizontal exclusives
			for i in range(0,numcases):
				if (not ("O" in grid[h][i])) and (grid[h][i].count("X")+1==numcases):
						##grid[h][i][grid[h][i].index("-")]="O"
						grid=writeo(grid,h,i,grid[h][i].index("-"))
			## check vertical exclusives
			for j in range(0,numcases):
				tempcol=[]
				for i in range(0,numcases):
					tempcol.append(grid[h][i][j])
				if (not ("O" in tempcol)) and (tempcol.count("X")+1==numcases):
					##grid[h][tempcol.index("-")][j]="O"
					grid=writeo(grid,h,tempcol.index("-"),j)

					## sudoku checks
		print("New sudoku check")
		printgrid(grid,labels,squarelabels)
		for h in range(0,numsquares):
			## first horizontal
			for i in range(0,numcases):
				if grid[h][i].count("O")==0:
					dashcount=grid[h][i].count("-")
					dlist=[]
					xlist=[]
					for j in range(0,numcases):
						if grid[h][i][j]=="-":dlist.append(j)
						if grid[h][i][j]=="X":xlist.append(j)
					if dashcount==2:
						## which two?
						## dash pattern established in dlist
						## now look for a match within the same square
						irange=range(0,numcases)
						irange.remove(i)
						for i2 in irange:
							if grid[h][i2].count("-")==2 and grid[h][i2][dlist[0]]=="-" and grid[h][i2][dlist[1]]=="-":
								## rows i and i2 in square h have a matching 2x2 square of empties.  X out those empties in other rows.
								xrange=range(0,numcases)
								xrange.remove(i)
								xrange.remove(i2)
								for i3 in xrange:
									for j in range(0,numcases):
										if j in dlist:  grid[h][i3][j]="X"
					##print(["h",h,i,dashcount])
					##printgrid(grid,labels,squarelabels)
					##if grid[0][0][1]=="X":dummy=raw_input("cont?")
					if dashcount==3:
						## which three?
						## dash pattern established in dlist
						## now look for a match within the same square
						irange=range(0,numcases)
						irange.remove(i)
						matchlist=[i]
						for i2 in irange:
							if grid[h][i2].count("-")<=3:
								match=True
								for j in xlist:
									if grid[h][i2][j]!="X":
										match=False
								if match:matchlist.append(i2)
						if len(matchlist)==3:
							for curs in range(0,numcases):
								if curs not in matchlist:
									for j in dlist:
										grid[h][curs][j]="X"
					##print(["h",h,i,dashcount])
					##printgrid(grid,labels,squarelabels)
					##if grid[0][0][1]=="X":dummy=raw_input("cont?")
					## compare dlist, which is horizontal, with xlists from squares matching second index
					dlist_label=labels[squarelabels[h][0]][i]
					targetsquares=range(numsquares)
					targetsquares.remove(h)
					for target_h in targetsquares:
						if squarelabels[h][1]==squarelabels[target_h][0]:
							## target match will be vertical
							for j in range(numcases):
								v_list=[]
								fit=True
								for i2 in dlist:
									if grid[target_h][i2][j]!="X":fit=False
								if fit:
									target_label=labels[squarelabels[target_h][1]][j]
									grid=labelx(grid,labels,squarelabels,dlist_label,target_label)
						if squarelabels[h][1]==squarelabels[target_h][1]:
							## target match will be horizontal	
							for i2 in range(numcases):
								fit=True
								for j in dlist:
									if grid[target_h][i2][j]!="X":fit=False
								if fit:
									target_label=labels[squarelabels[target_h][0]][i2]
									grid=labelx(grid,labels,squarelabels,dlist_label,target_label)
			for j in range(0,numcases):
				v_list=[]
				for i in range(numcases):
					v_list.append(grid[h][i][j])
				if v_list.count("O")==0:
					dashcount=v_list.count("-")
					dlist=[]
					xlist=[]
					for i in range(0,numcases):
						if v_list[i]=="-":dlist.append(i)
						if v_list[i]=="X":xlist.append(i)
					if dashcount==2:
						## which two?
						## dash pattern established in dlist
						## now look for a match within the same square
						jrange=range(0,numcases)
						jrange.remove(j)
						for j2 in jrange:
							v2_list=[]
							for i in range(numcases):
								v2_list.append(grid[h][i][j2])
							if v2_list.count("-")==2 and v2_list[dlist[0]]=="-" and v2_list[dlist[1]]=="-":
								## rows i and i2 in square h have a matching 2x2 square of empties.  X out those empties in other rows.
								xrange=range(0,numcases)
								xrange.remove(j)
								xrange.remove(j2)
								for j3 in xrange:
									for i2 in range(0,numcases):
										if i2 in dlist:  grid[h][i2][j3]="X"
					##print(["v",h,j,dashcount])
					##printgrid(grid,labels,squarelabels)
					##if grid[0][0][1]=="X":dummy=raw_input("cont?")
					if dashcount==3:
						## which three?
						## dash pattern established in dlist
						## now look for a match within the same square
						jrange=range(0,numcases)
						jrange.remove(j)
						matchlist=[j]
						for j2 in jrange:
							v2_list=[]
							for i in range(numcases):
								v2_list.append(grid[h][i][j2])
							if v2_list.count("-")<=3:
								match=True
								for i2 in xlist:
									if v2_list[i2]!="X":
										match=False
								if match:matchlist.append(j2)
						if len(matchlist)==3:
							for curs in range(0,numcases):
								if curs not in matchlist:
									for i in dlist:
										grid[h][i][curs]="X"		
					##print(["v",h,j,dashcount])
					##printgrid(grid,labels,squarelabels)
					##if grid[0][0][1]=="X":dummy=raw_input("cont?")
					## compare dlist, which is vertical, with xlists from squares matching first index
					dlist_label=labels[squarelabels[h][1]][j]
					targetsquares=range(numsquares)
					targetsquares.remove(h)
					for target_h in targetsquares:
						if squarelabels[h][0]==squarelabels[target_h][0]:
							## target match will be vertical
							for j2 in range(numcases):
								v_list=[]
								fit=True
								for i in dlist:
									if grid[target_h][i][j2]!="X":fit=False
								if fit:
									target_label=labels[squarelabels[target_h][1]][j2]
									grid=labelx(grid,labels,squarelabels,dlist_label,target_label)
						if squarelabels[h][0]==squarelabels[target_h][1]:
							## target match will be horizontal	
							for i in range(numcases):
								fit=True
								for j2 in dlist:
									if grid[target_h][i][j2]!="X":fit=False
								if fit:
									target_label=labels[squarelabels[target_h][0]][i]
									grid=labelx(grid,labels,squarelabels,dlist_label,target_label)

		print("End sudoku check")
		printgrid(grid,labels,squarelabels)
		
		## cross reference quantitative equalities
		## build qerules from rules
		qerules=[]
		for rule in rules:
			if rule[0]=='qe':
				qerules.append(rule)
		if len(qerules)>1:
			newqerules=[]
			for h in range(numsquares):
				for i in range(numcases):
					for j in range(numcases):
						if grid[h][i][j]=="O":
							ilabel=labels[squarelabels[h][0]][i]
							jlabel=labels[squarelabels[h][1]][j]
							for rule in qerules:
								if rule[2]==ilabel:newqerules.append([rule[0],rule[1],jlabel,rule[3]])
								if rule[2]==jlabel:newqerules.append([rule[0],rule[1],ilabel,rule[3]])
								if rule[3]==ilabel:newqerules.append([rule[0],rule[1],rule[2],jlabel])
								if rule[3]==jlabel:newqerules.append([rule[0],rule[1],rule[2],ilabel])
							for rule in newqerules:
								newiiggs=labelstoindex([rule[2],rule[3]],labels,squarelabels)
								if not ((rule in qerules) or (rule[2] in labels[0] and rule[3] in labels[0])):qerules.append(rule)
			##if finishup!="Y":
				##print(newqerules)
				##print(qerules)
				##finishup=raw_input("Y to finish1")
			## we should now have a comprehensive qerules
			numqe=len(qerules)
			## check each qerule for other qerules which are A) same step B) rule[2] or rule[3] in same group
			for x in range(numqe):
				rule=qerules[x]
				targets=range(numqe)
				targets.remove(x)
				for target in targets:
					trule=qerules[target]
					if rule[1]==trule[1]:
						iiggs2=labelstoindex([rule[2],trule[2]],labels,squarelabels)
						iiggs3=labelstoindex([rule[3],trule[3]],labels,squarelabels)
						if iiggs2[4]==-1 and iiggs2[0]!=iiggs2[1]:
							grid=labelx(grid,labels,squarelabels,rule[3],trule[3])
							##if finishup!="Y":
								##print([2,iiggs2,iiggs3,rule,trule])
								##finishup=raw_input("Y to finish2")
						if iiggs3[4]==-1 and iiggs3[0]!=iiggs3[1]:
							## index 3s are same category.  X out index 2s
							grid=labelx(grid,labels,squarelabels,rule[2],trule[2])
							##if finishup!="Y":
								##print([3,iiggs2,iiggs3,rule,trule])
								##finishup=raw_input("Y to finish3")
					## check each qerule for other qerules which A) have the same label B) are different steps
					if rule[2]==trule[2]:
						if rule[1]==trule[1]:
							grid=labelo(grid,labels,squarelabels,rule[3],trule[3])
						else:
							grid=labelx(grid,labels,squarelabels,rule[3],trule[3])
					if rule[3]==trule[3]:
						if rule[1]==trule[1]:
							grid=labelo(grid,labels,squarelabels,rule[2],trule[2])
						else:
							grid=labelx(grid,labels,squarelabels,rule[2],trule[2])
					if rule[2]==trule[3]:
						grid=labelx(grid,labels,squarelabels,rule[3],trule[2])
					if rule[3]==trule[2]:
						grid=labelx(grid,labels,squarelabels,rule[2],trule[3])
				## check rules where both labels are in the same category for exclusions
				iiggs=labelstoindex([rule[2],rule[3]],labels,squarelabels)
				if iiggs[4]==-1:
					# if finishup!="Y":
						# printgrid(grid,labels,squarelabels)
						# print(qerules)
						# print(iiggs)
						# finishup=raw_input("Y to finish4")
					## same label group
					h=squarelabels.index([0,iiggs[2]])
					## check if there are only two possibilities
					vlist=[]
					dlist=[]
					for i in range(numcases):
						vlist.append(grid[h][i][iiggs[0]])
						if grid[h][i][iiggs[0]]=="-":dlist.append(i)
					if vlist.count("-")==2:
						int1=int(labels[0][dlist[0]])
						int2=int(labels[0][dlist[1]])
						if int2-int1==rule[1]:
							## X out row i==dlist[0]
							for j in range(numcases):
								if not (j in [iiggs[0],iiggs[1]]):grid[h][dlist[0]][j]="X"
					# if finishup!="Y":
						# printgrid(grid,labels,squarelabels)
						# print(iiggs)
						# print(rule)
						# print(unattached_counter)
						# finishup=raw_input("Y to finish5")
												
		printgrid(grid,labels,squarelabels)
		flatgrid1  = [val for sublist in grid for val in sublist]
		flatgrid = [val for sublist in flatgrid1 for val in sublist]
		ocount=flatgrid.count("O")
		if ocount==len(flatgrid1):
			print("Let me stop you right there.")
			printlist(grid,labels)
			rule="STOP"
			break
				
	printgrid(grid,labels,squarelabels)

def writeo(grid,square,ind1,ind2):
	numcases=len(grid[0][0])
	## write O
	grid[square][ind1][ind2]="O"
	## write Xs
	for i in range(0,numcases):
		if i<>ind1:grid[square][i][ind2]="X"
	for i in range(0,numcases):
		if i<>ind2:grid[square][ind1][i]="X"
	outvec=[square,ind1,ind2]
	print("--- wrote O to h,i,j "+ str(outvec))
	return grid
	
def labelo(grid,labels,squarelabels,label1,label2):
	numcases=len(grid[0][0])
	ltoi=labelstoindex([label1,label2],labels,squarelabels)
	## write O
	grid[ltoi[4]][ltoi[0]][ltoi[1]]="O"
	## write Xs
	for i in range(0,numcases):
		if i<>ltoi[0]:grid[ltoi[4]][i][ltoi[1]]="X"
	for i in range(0,numcases):
		if i<>ltoi[1]:grid[ltoi[4]][ltoi[0]][i]="X"
	outvec=[ltoi[4],ltoi[0],ltoi[1]]
	print("--- wrote O to h,i,j "+ str(outvec))
	return grid

	
def labelx(grid,labels,squarelabels,label1,label2):
	ltoi=labelstoindex([label1,label2],labels,squarelabels)
	if ltoi[4]!=-1:
		grid[ltoi[4]][ltoi[0]][ltoi[1]]="X"
	return grid

	
def labelstoindex(elements,labels,squarelabels):
	flatlabels  = [val for sublist in labels for val in sublist]
	numcases=len(labels[0])
	if (elements[0] in flatlabels) and (elements[1] in flatlabels):
		el_index=[flatlabels.index(elements[0]),flatlabels.index(elements[1])]
		el_index.sort()
		ind1=el_index[0]%numcases
		ind2=el_index[1]%numcases
		grp1=trunc(el_index[0]/numcases)
		grp2=trunc(el_index[1]/numcases)
		squareindex=[grp1,grp2]
		if squareindex in squarelabels:
			square=squarelabels.index(squareindex)
		else:
			square=-1
		outputs=[ind1,ind2,grp1,grp2,square]
		return outputs
	else: return []

	
def indextolabels(h,i,j,labels,squarelabels):
	numcases=len(labels[0])
	h1=squarelabels[h][0]
	h2=squarelabels[h][1]
	label1=labels[h1][i]
	label2=labels[h2][j]
	return [label1,label2]
	
	
def geometry(h,i,j,grid,labels,squarelabels):
	flatlabels  = [val for sublist in labels for val in sublist]
	groups=len(labels)
	##pdb.set_trace()
	numcases=len(labels[0])
	h1=squarelabels[h][0]
	h2=squarelabels[h][1]
	squarelist=[]
	for x in range(0,groups):
		if not(x in squarelabels[h]):
			target=[h1,x]
			target.sort()
			intersect=[h2,x]
			intersect.sort()
			target_h=squarelabels.index(target)
			intersect_h=squarelabels.index(intersect)
			for curs in range(0,numcases):
				if h1==target[0]:  ##target_h,i,curs
					if h2==intersect[0]:  ##intersect_h,j,curs
						if grid[target_h][i][curs]=="O" or grid[intersect_h][j][curs]=="O":
							grid=writeo(grid,target_h,i,curs)
							grid=writeo(grid,intersect_h,j,curs)
						if grid[target_h][i][curs]=="X" or grid[intersect_h][j][curs]=="X":
							grid[target_h][i][curs]="X" 
							grid[intersect_h][j][curs]="X"
					else:  ##intersect_h,curs,j
						if grid[target_h][i][curs]=="O" or grid[intersect_h][curs][j]=="O":
							grid=writeo(grid,target_h,i,curs)
							grid=writeo(grid,intersect_h,curs,j)
						if grid[target_h][i][curs]=="X" or grid[intersect_h][curs][j]=="X":
							grid[target_h][i][curs]="X" 
							grid[intersect_h][curs][j]="X"
				else:  ##target_h,curs,i
					if h2==intersect[0]:  ##intersect_h,j,curs
						if grid[target_h][curs][i]=="O" or grid[intersect_h][j][curs]=="O":
							grid=writeo(grid,target_h,curs,i)
							grid=writeo(grid,intersect_h,j,curs)
						if grid[target_h][curs][i]=="X" or grid[intersect_h][j][curs]=="X":
							grid[target_h][curs][i]="X" 
							grid[intersect_h][j][curs]="X"
					else:  ##intersect_h,curs,j
						if grid[target_h][curs][i]=="O" or grid[intersect_h][curs][j]=="O":
							grid=writeo(grid,target_h,curs,i)
							grid=writeo(grid,intersect_h,curs,j)
						if grid[target_h][curs][i]=="X" or grid[intersect_h][curs][j]=="X":
							grid[target_h][curs][i]="X" 
							grid[intersect_h][curs][j]="X"
				
			
	return grid
							
					
def printgrid(grid, labels, squarelabels):
	##print(grid)
	print(squarelabels)
	print(labels)
	numsquares=len(grid)
	numcases=len(grid[0])
	for h in range(0,numsquares):
		leftindex=squarelabels[h][0]
		topindex=squarelabels[h][1]
		setwidth_l=max(len(str(s)) for s in labels[leftindex])
		toptext=" "*setwidth_l
		for j in range(0,numcases):
			toptext=toptext+" |"+labels[topindex][j]
		print(toptext)
		print("-"*len(toptext))
		for i in range(0,numcases):
			outtext="%*s"%(setwidth_l,labels[leftindex][i])
			for j in range(0,numcases):
				setwidth_t=len(labels[topindex][j])
				nexttext="%*s"%(setwidth_t,grid[h][i][j])
				outtext=outtext + " |" + nexttext
				
			print (outtext)
		print ("")

		
def printlist(grid,labels):
	numcases=len(grid[0])
	groups=len(labels)
	for i in range(0,numcases):
		lineout=str(labels[0][i])
		for g in range(1,groups):
			lineout=lineout+" "
			lineout=lineout+str(labels[g][grid[g-1][i].index("O")])
		print lineout
		
logic_puzzle_solve()