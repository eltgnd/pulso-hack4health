import agentpy as ap
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import random as rand
import streamlit as st
import base64
import os

matplotlib.rcParams['animation.embed_limit'] = 2**128


# Streamlit form for parameters
st.title("Infection Simulation Model 🧬")

with st.expander("Parameters", expanded=True):
    with st.form(key='parameters_form'):
        population_density = st.slider('Population Density', 0.0, 1.0, 0.65)
        size = st.number_input('Size', min_value=1, max_value=100, value=50)
        steps = st.number_input('Steps', min_value=1, value=300)
        initial_infected = st.number_input('Initial Infected', min_value=1, value=3)
        infection_probability = st.slider('Infection Probability', 0.0, 1.0, 0.3)
        recovery_probability = st.slider('Recovery Probability', 0.0, 1.0, 0.1)
        resusceptibility_probability = st.slider('Resusceptibility Probability', 0.0, 1.0, 0.02)
        vaccination_speed = st.number_input('Vaccination Speed', min_value=0, value=20)
        vaccination_start = st.number_input('Vaccination Start', min_value=0, value=100)

        submit_button = st.form_submit_button(label='Run Simulation')

parameters = {
    'Population Density': population_density,
    'size': size,
    'steps': steps,
    'Initial Infected': initial_infected,
    'Infection Probability': infection_probability,
    'Recovery Probability': recovery_probability,
    'Resusceptibility Probability': resusceptibility_probability,
    'Vaccination Speed': vaccination_speed,
    'Vaccination Start': vaccination_start
}

class InfectionModel(ap.Model):
    def setup(self):
        nPersons = int(self.p['Population Density'] * (self.p.size**2))
        persons = self.agents = ap.AgentList(self, nPersons)
        
        self.city = ap.Grid(self, [self.p.size]*2, track_empty=True)
        self.city.add_agents(persons, random=True, empty=True)
        
        self.agents.condition = 0
        self.agents.random(self.p['Initial Infected']).condition = 1

        self.timeStep = 0
        
    def update(self):
        pop = 0
        for i in range(0,5):
            pop += len(self.agents.select(self.agents.condition == i))
        self['S'] = len(self.agents.select(self.agents.condition == 0))/pop
        self['I'] = (len(self.agents.select(self.agents.condition == 1)) + len(self.agents.select(self.agents.condition == 2)))/pop
        self['R'] = len(self.agents.select(self.agents.condition == 3))/pop
        self['V'] = len(self.agents.select(self.agents.condition == 4))/pop
        self.record('S')
        self.record('I')
        self.record('R')
        self.record('V')
        
        
    def step(self):
        susceptible_population = self.agents.select(self.agents.condition == 0)
        infected_Population = self.agents.select(self.agents.condition == 1)
        infected_Population += self.agents.select(self.agents.condition == 2)
        recently_Infected = self.agents.select(self.agents.condition == 1)
        recovered_Population = self.agents.select(self.agents.condition == 3)

        #Start of Vaccination
        if self.timeStep >= self.p['Vaccination Start']:
            susceptible_population = self.agents.select(self.agents.condition == 0)
            recovered_population = self.agents.select(self.agents.condition == 3)
            num_vaccinated = min(self.p['Vaccination Speed'], len(susceptible_population) + len(recovered_population))
            
            for _ in range(num_vaccinated):
                susceptible_population = self.agents.select(self.agents.condition == 0)
                recovered_Population = self.agents.select(self.agents.condition == 3)
                
                if len(susceptible_population) == 0:
                    recovered_population.random(1, replace=True).condition = 4
                elif len(recovered_population) == 0:
                    susceptible_population.random(1, replace=True).condition = 4
                else:
                    rng = rand.randint(0,1)
                    if rng == 0:
                        recovered_population.random(1, replace=True).condition = 4
                    else: 
                        susceptible_population.random(1, replace=True).condition = 4
                
        
        for inf in infected_Population:
            for neighbor in self.city.neighbors(inf):
                if neighbor.condition == 0:
                    if rand.uniform(0,1) < self.p['Infection Probability']:
                        neighbor.condition = 1
                        
        for inf in recently_Infected:
            inf.condition = 2
        
        for inf in infected_Population:
            if rand.uniform(0,1) < self.p['Recovery Probability']:
                inf.condition = 3
            
        for rec in recovered_Population:
            if rand.uniform(0,1) < self.p['Resusceptibility Probability']:
                rec.condition = 0
        
        if(len(infected_Population) == 0):
            self.stop()

        self.timeStep +=1 
    
    def end(self):
        recovered_population = len(self.agents.select(self.agents.condition == 3))
        vaccinated_population = len(self.agents.select(self.agents.condition == 4))
    
        print(f"\nNumber of Susceptible: {len(self.agents.select(self.agents.condition == 0))}")
        print(f"Number of Infected: {len(self.agents.select(self.agents.condition == 2))}")
        print(f"Number of Recovered: {recovered_population}")
        print(f"Number of Vaccinated: {vaccinated_population}")
    
        self.report('Percentage of recovered population', recovered_population / len(self.agents))

def virus_lineplot(data, ax):
    x = data.index.get_level_values('t')
    y = [data[var] for var in ['I', 'S', 'R', 'V']]
    
    ax.plot(x, y[0], 'purple', label="Infected")
    ax.plot(x, y[1], 'green', label="Susceptible")
    ax.plot(x, y[2], 'blue', label="Recovered")
    ax.plot(x, y[3], 'orange', label="Vaccinated")
    
    ax.legend()
    ax.set_xlim(0, max(1, len(x) - 1))
    ax.set_ylim(0, 1)
    ax.set_xlabel("Time steps")
    ax.set_ylabel("Population")

def virus_stackplot(data, ax):
    x = data.index.get_level_values('t')
    y = [data[var] for var in ['I', 'S', 'R','V']]

    sns.set()
    ax.stackplot(x, y, labels=['Infected', 'Susceptible', 'Recovered', 'Vaccinated'],
                 colors = ['purple', 'g', 'b', 'orange'])

    ax.legend()
    ax.set_xlim(0, max(1, len(x)-1))
    ax.set_ylim(0, 1)
    ax.set_xlabel("Time steps")
    ax.set_ylabel("Percentage of population")

def animation_plot(model, axz):
    ax1, ax2, ax3 = axz
    attr_grid = model.city.attr_grid('condition')
    color_dict = {0: 'white', 1: '#f6ff00', 2: '#bd00bd', 3: '#0095ff', 4: 'green', None: '#000000'}
    ap.gridplot(attr_grid, ax=ax1, color_dict=color_dict, convert=True)
    ax1.set_title(f"Simulation of an infection\n"
                  f"Time-step: {model.t} S: ["
                  f"{len(model.agents.select(model.agents.condition == 0))}] "
                  "I: ["
                  f"{len(model.agents.select(model.agents.condition == 1))+len(model.agents.select(model.agents.condition == 2))}] "
                  "R: ["
                  f"{len(model.agents.select(model.agents.condition == 3))}] "
                  "V: ["
                  f"{len(model.agents.select(model.agents.condition == 4))}]"
                  )

    virus_lineplot(model.output.variables.InfectionModel, ax2)

    virus_stackplot(model.output.variables.InfectionModel, ax3)


model = InfectionModel(parameters)
if submit_button:
    with st.spinner('Simulating...'):
        results = model.run()
    fig1, ax = plt.subplots()
    virus_lineplot(results.variables.InfectionModel, ax)
    
    fig2, ax = plt.subplots()
    virus_stackplot(results.variables.InfectionModel, ax)
    
    st.subheader(body = 'Virus Plot 📊', divider = 'grey')
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(fig1)

    with col2:
        st.pyplot(fig2)

    fig, axs = plt.subplots(1, 3, figsize=(20, 6))
    model = InfectionModel(parameters)
    animation = ap.animate(model, fig, axs, animation_plot)
    animation.save(os.path.join('images/', 'animation1.gif'), writer="imagemagick", fps=30)

    st.subheader(body = 'SIR-V Simulation 📉', divider = 'grey')
    file_ = open("images/animation1.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    # Display the GIF in the center with altered size
    st.markdown(
        f'''
        <div style="display: flex; justify-content: center;">
            <img src="data:image/gif;base64,{data_url}" alt="SIRV Simulation" style="width: 150%; height: auto;">
        </div>
        ''',
        unsafe_allow_html=True,
    )

else:
    st.subheader(body = 'Virus Plot 📊', divider = 'grey')
    col1, col2 = st.columns(2)
    with col1:
        st.image('images/virus_lineplot.png')

    with col2:
        st.image('images/virus_stackplot.png')

    st.subheader(body = 'SIR-V Simulation 📉', divider = 'grey')
    # gif_url = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWYxbm9lM2U2bXE5Zng2cTY2OGZ1Y2t3OXo4OWV1eW9sczEwM2cwaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/KgvCoKoHCG0v2UTmTU/giphy.gif"
    # st.image(gif_url, caption='SIR-V Animation', use_column_width=True)

    @st.cache_data
    def view_animation():
        file_ = open("model_train_notebook/animation.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        # Display the GIF in the center with altered size
        st.markdown(
            f'''
            <div style="display: flex; justify-content: center;">
                <img src="data:image/gif;base64,{data_url}" alt="SIRV Simulation" style="width: 150%; height: auto;">
            </div>
            ''',
            unsafe_allow_html=True,
        )
    
    view_animation()