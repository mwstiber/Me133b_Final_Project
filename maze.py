import tkinter as tk
import tkinter.simpledialog
import D_star as DS

board = [ [None]*7 for _ in range(6) ]

press = 0
counter = 0
obstacles = []
root = tk.Tk()


def on_Return(event):
    global press
    global r
    press += 1
    if press == 1:
        r = DS.DStar(goal, start, 7,  6, obstacles)
        print("Running...")
        path = r.initPlan()
        for elem in path:
            color = "blue"
            event.widget.config(bg=color)
            board[elem[0]][elem[1]] = color

        gameframe.destroy()
        redraw()
    press += 1
    if press == 4:
        for i in range(6):
            for j in range(7):
                if board[i][j] == "blue":
                    color = "grey"
                    event.widget.config(bg=color)
                    board[i][j] = color
        path = r.run2()
        for e in path:
            color = "blue"
            event.widget.config(bg=color)
            board[e[0]][e[1]] = color

        gameframe.destroy()
        redraw()
        
def on_click(i,j,event):
    global counter
    global goal
    global start
    global obstacles
    if press == 0 and board[i][j] == None:
        if counter == 0:
            color = "green"
            start = (i, j)
        elif counter == 1:
            color = "red"
            goal = (i, j)
        else:
            color = "black"
            obstacles.append((i, j))
        counter += 1
        event.widget.config(bg=color)
        board[i][j] = color
        gameframe.destroy()
        redraw()
        
    elif press == 2 and (board[i][j] == None or board[i][j] == "blue"):
        color = "black"
        obstacles.append((i, j))
        event.widget.config(bg=color)
        board[i][j] = color
        gameframe.destroy()
        redraw()

def redraw():
    global gameframe
    gameframe = tk.Frame(root)
    gameframe.pack()

    for i,row in enumerate(board):
        for j,column in enumerate(row):
            name = str(i)+str(j)
            L = tk.Label(gameframe,text='    ',bg= "grey" if board[i][j] == None else board[i][j])
            L.grid(row=i,column=j,padx='1',pady='1')
            L.bind('<Button-1>',lambda e,i=i,j=j:on_click(i,j,e))
    

tk.messagebox.showinfo("Instructions", "Click: \n" 
                                            "1) Start \n"
                                            "2) End \n"
                                          "3) Click as many times for obstacles \n"
      "4) Hit return when done adding obstacles to run D* star")
redraw()
root.bind('<Return>', lambda e: on_Return(e))
root.mainloop()
