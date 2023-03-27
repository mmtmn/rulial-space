import matplotlib.pyplot as plt
from itertools import product
import networkx as nx
import matplotlib.animation as animation


class TuringMachine:
    def __init__(self, rules, initial_state, initial_position, tape):
        self.rules = rules
        self.state = initial_state
        self.position = initial_position
        self.tape = tape

    def step(self):
        current_symbol = self.tape[self.position]
        rule_key = (self.state, current_symbol)
        if rule_key in self.rules:
            new_state, new_symbol, move = self.rules[rule_key]
            self.state = new_state
            self.tape[self.position] = new_symbol
            self.position += move
        else:
            raise Exception("Undefined transition for state: {}, symbol: {}".format(self.state, current_symbol))

def generate_turing_machines(num_states, num_symbols):
    turing_machines = []
    state_space = range(num_states)
    symbol_space = range(num_symbols)
    move_space = [-1, 1]
    
    for rule_combination in product(product(state_space, symbol_space, move_space), repeat=num_states*num_symbols):
        rules = {(state, symbol): rule for (state, symbol), rule in zip(product(state_space, symbol_space), rule_combination)}
        turing_machines.append(TuringMachine(rules, 0, 0, [0] * 100))
    
    return turing_machines
  
tm_list = generate_turing_machines(1, 2)



def create_rulial_space_graph(turing_machines, steps, step_limit):
    rulial_space_graph = nx.DiGraph()
    rulial_space_graph.add_nodes_from(turing_machines)
    
    for tm1 in turing_machines:
        for tm2 in turing_machines:
            tm1_copy = TuringMachine(tm1.rules, tm1.state, tm1.position, tm1.tape.copy())
            tm2_copy = TuringMachine(tm2.rules, tm2.state, tm2.position, tm2.tape.copy())
            
            for _ in range(step_limit):
                try:
                    tm1_copy.step()
                    tm2_copy.step()
                except Exception:
                    break
                
            if tm1_copy.state == tm2_copy.state and tm1_copy.tape == tm2_copy.tape:
                rulial_space_graph.add_edge(tm1, tm2)
                
    return rulial_space_graph


def visualize_rulial_space_animation(turing_machines, steps):
    fig, ax = plt.subplots()
    ani = animation.FuncAnimation(fig, update_rulial_space, frames=steps, fargs=(turing_machines, ax), interval=1000, blit=False)
    plt.show()

def update_rulial_space(step, turing_machines, ax):
    ax.clear()
    rulial_space = create_rulial_space_graph(turing_machines, step, step)
    pos = nx.spring_layout(rulial_space)
    nx.draw(rulial_space, pos, node_size=50, with_labels=False, node_color="blue", font_size=8, ax=ax)
    ax.set_title("Step: {}".format(step))

while True:
    steps = int(input("Enter the number of steps: "))
    visualize_rulial_space_animation(tm_list, steps)

    exit = input("Do you want to exit? (y/n): ")
    if exit == "y":
        break