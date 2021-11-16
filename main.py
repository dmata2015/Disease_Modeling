import turtle
import random
import tkinter as tk
import time
population_list=[]
infection_chance=9
gap=25
incubation_time=5
lookup={}
size_of_population=23
percent_vaccinated=20
infected_timer=5


class Person(turtle.RawTurtle):
    def __init__(self,screen,infected_timer,incubation_time,infection_chance,rn,cn):
        turtle.RawTurtle.__init__(self,screen)
        self.infected=False
        self.vaccinated=False
        self.dead=False
        self.exposed=False
        self.infectious=False
        self.infected_timer=infected_timer
        self.icounter=0
        self.vaccination_sucess_rate=75
        self.intelligence=75
        self.pen_color='black'
        screen.tracer(0)
        self.infection_chance=infection_chance

        self.shape('turtle')
        self.rn=rn
        self.cn=cn
        lookup[(self.rn,self.cn)]=self


        self.incubation_timer=0
        self.incubation_time=incubation_time
        def infectme (x,y):
            self.infected = True
        self.onclick(infectme)

    def update_person(self):

        if not self.infected:
            self.check_neighbors()


        if self.infected:
            self.infected_timer -= 1
            if self.infected_timer >= 0:
                self.infectious=True
            else:
                self.infectious=False
            if self.pen_color!='red':
                self.draw_1()
            else:
                return


        elif self.vaccinated:
            chance=random.randint(1,100)
            if chance<=self.vaccination_sucess_rate:
                self.infected=False


        elif self.exposed:

            self.incubation_timer+=1
            if self.incubation_timer>=self.incubation_time:
                self.infected=True




    def draw_1(self):

        self.color(self.pen_color)
        self.down()
        if self.infected:
            self.pen_color='red'
            self.color(self.pen_color)
        if self.exposed:
            self.pen_color='orange'
            self.color(self.pen_color)
        if self.vaccinated:
            self.pen_color='green'
            self.color(self.pen_color)
        if self.incubation_timer >= self.incubation_time:
            self.exposed=False
        self.stamp()
    def check_neighbors(self):
        if self.exposed:
            return
        self.neighbors=[
        lookup.get((self.rn+1,self.cn)),
        lookup.get((self.rn-1,self.cn)),
        lookup.get((self.rn,self.cn-1)),
        lookup.get((self.rn,self.cn+1))]
        for neighbor in self.neighbors:
            if neighbor:

                if neighbor.infectious:

                    chance=random.randint(1,100)
                    if chance<=self.infection_chance:

                        self.exposed=True
                        self.draw_1()
                        return
class Settings:
    def __init__(self):
        self.size_of_population=25
        self.infection_chance = 100
        self.incubation_time = 5
        self.percent_vaccinated = 20
        self.infected_timer = 5

class Gt(turtle.RawTurtle):
    def __init__(self,screen):
        turtle.RawTurtle.__init__(self, screen)
        self.penup()
        self.goto(-400,-100)
        self.pendown()

    def update(self,num_infected):
        x,y=self.pos()
        print(num_infected)
        self.goto(x+1,num_infected)

class Display:
    def __init__(self):
        self.settings=Settings()
        self.screen_size = '1920x1080'
        self.entry_list=[]
        self.settings_str_list=['size of population(make this a square root)','infection chance','incubation time',
                            'percent vaccinated','infected timer']
        self.settings_list=[]
        self.root = tk.Tk()
        self.root.geometry(self.screen_size)
        self.simulation_canvas = tk.Canvas(master=self.root,width=960,height=1080)
        self.simulation_canvas.grid(row=1,column=15,rowspan=2,)
        self.config_frame=tk.Frame(self.root)
        self.config_frame.grid(row=1,column=1)
        self.gt_screen = tk.Canvas(master=self.root, width=960, height=1080)
        self.gt_screen.grid(row=2, column=1, rowspan=2, )
        counter=-1
        print(self.settings_list)
        for i in range(5):
            counter+=1
            self.label = tk.Label(self.config_frame, text=self.settings_str_list[counter])
            self.label.grid(row= counter + 1, column=1)
            entry=tk.Entry(self.config_frame,width=10)
            entry.grid(row=counter + 1, column=2)
            self.entry_list.append(entry)
        self.run_button=tk.Button(master=self.config_frame,text='run',command=self.change_settings)
        self.run_button.grid(row=counter+2,column=2)
        self.reset_button=tk.Button(master=self.config_frame,text='reset',command=self.reset)
        self.reset_button.grid(row=counter+3,column=2)
        self.reset_button=tk.Button(master=self.config_frame,text='reset',command=self.reset)
        self.reset_button.grid(row=counter+3,column=2)

        self.screen = turtle.TurtleScreen(self.simulation_canvas)
        self.screen.bgcolor('blue')
        self.gt_screen= turtle.TurtleScreen(self.gt_screen)

    def run(self):

        self.simulation.make_population()
        self.simulation.for_loop()
        self.screen.ontimer(self.simulation.update_turtles, 1)
    def change_settings(self):
        self.screen.clear()
        self.screen.bgcolor('blue')
        for entry in self.entry_list:
            entry=entry.get()
            self.settings_list.append(entry)
        self.settings.size_of_population=int(self.settings_list[0])
        self.settings.infection_chance=int(self.settings_list[1])
        self.settings.infected_timer=int(self.settings_list[4])
        self.settings.incubation_time=int(self.settings_list[2])
        self.settings.percent_vaccinated=int(self.settings_list[3])
        self.simulation = Simulation(self.settings, self.screen,self.gt_screen)
        self.simulation.writer.num_text()

        self.run()
    def reset(self):
        self.simulation.clear_turltes()
        while self.settings_list:
            self.settings_list.pop()
class Writer(turtle.RawTurtle):
    def __init__(self,screen,simulation):
        self.simulation=simulation
        turtle.RawTurtle.__init__(self, screen)
        screen.tracer(0)
        self.screen=screen
        self.y=200
        self.update_time=1000
        self.num_infected=0
        self.x=0
        self.counter=0
        self.running=True
    def num_text(self):
        self.penup()
        self.goto(self.x,self.y)
        self.pendown()
        self.counter+=1
        if self.counter==10:
            self.counter=0
            self.x+=20
            self.y=210
        time_completed=str(self.update_time/1000)
        self.write(self.num_infected)
        self.y-=10
        #print((self.simulation.num_infected,'people were infected in',time_completed))
        if self.running:
            self.screen.ontimer(self.num_text,self.update_time)



class Simulation:
    def __init__(self,settings,screen,gt_screen):
        self.screen=screen
        self.settings=settings
        self.gap = 25
        self.running=True
        self.gt_screen=gt_screen
        self.gt=Gt(gt_screen)
        self.num_infected = 0
        self.writer=Writer(gt_screen,self)

    def make_population(self):
        #size of population is the square root of the total population
        x=-300
        y=-400
        print(self.settings.size_of_population)

        for row_number in range(self.settings.size_of_population):
            for column_number in range(self.settings.size_of_population):

                p=Person(self.screen,self.settings.infected_timer,self.settings.incubation_time,self.settings.infection_chance,row_number,column_number)
                p.setheading(90)
                p.penup()
                p.goto(x+(gap*column_number),(y+(row_number*gap)))
                p.pendown()
                population_list.append(p)
        patient_0=random.randint(0,(self.settings.size_of_population*self.settings.size_of_population))
        population_list[patient_0].infected=True

        people_vaccinated=((self.settings.percent_vaccinated/100)*(self.settings.size_of_population*self.settings.size_of_population))

        for i in range(int(people_vaccinated)):
            smart_guy = random.randint(0, ((self.settings.size_of_population * self.settings.size_of_population)-1))

            population_list[smart_guy].vaccinated = True


    def update_turtles (self):
        counter=0
        #print('Update turtles')
        s = time.time()
        num_infected=0

        num_infected=0
        for p in population_list:
            p.update_person()
            if p.infected:
                num_infected+=1
        self.y=num_infected
        self.writer.num_infected=self.y
        self.gt.update(self.y)
        self.screen.update()

        #print('Completed in',time.time()-s,self.num_infected,'out of',len(population_list))
        if self.running:
            self.screen.ontimer(self.update_turtles,1)

    def for_loop(self):
        for p in population_list:
            p.draw_1()
    def clear_turltes(self):

        print(population_list)
        for p in population_list:
            p.hideturtle()
            p.clear()
        while population_list:
            population_list.pop()
        self.writer.running=False

        self.running = False
        self.gt_screen.clear()
        self.gt_screen.update()
        self.screen.update()


display=Display()
display.screen.mainloop()
display.root.mainloop()