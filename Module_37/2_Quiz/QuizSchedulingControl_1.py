from gekko import GEKKO
m = GEKKO(remote=False)
paper_width = 8.5     # width of paper
paper_length = 11     # length of paper
x = m.Var(lb=0)       # cut out length
box_width  = m.Intermediate(paper_width - 2 * x)
box_length = m.Intermediate(paper_length - 2 * x)
box_height = m.Intermediate(x)
Volume = m.Intermediate(box_width * box_length * box_height)
# lower constraint for box width with tabs
m.Equations([box_width > 0,box_length > 0,Volume > 0.01])
m.Maximize(Volume)
m.solve(disp=False)
print('width = ' + str(box_width.value[0]))
print('length = ' + str(box_length.value[0]))
print('height = ' + str(box_height.value[0]))
print('volume = ' + str(Volume.value[0]))