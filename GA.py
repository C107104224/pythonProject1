import numpy as np
class JAPProblem:
    def __init__(self,job_mechine):
        self.job_mechine = job_mechine
        self.number_of_jobs = len(job_mechine)
    def compute_objective_value(self,jobs):
        total_time = 0
        for i,job in enumerate(jobs):
            total_time += self.job_mechine[job][i]
        return total_time
    def initialize(self):
        self.selected_chrmosomes = np.zeros((self.pop_size,self.number_of_gens))
        self.indexs = np.arrange(self.total_size)
        self.chromosomes = np.zeros((self.total_size,self.number_of_genes),dtype=int)
        for i in range(self.pop_size):
            for j in range(self.number_of_genes):
                self.chromosomes[i][j] = j
            np.random.shuffle(self.chromosomes[i])
        for i in range(self.pop_size,self.total_size):
            for j in range(self.number_of_genes):
                self.chromosomes[i][j] = -1
        self.fitness = np.zeros(self.total_size)
        self.objective = np.zeros(self.total_size)
        self.best_chromosome = np.zeros(self.number_of_genes,dtype=int)
        self.best_fitness = 0
    def perfrom_crossover_operation(self):
        self.shuffle_index(self.pop_size)

        child1_index = self.pop_size
        child2_index = self.pop_size + 1
        count_of_crossover = int(self.crossover_size / 2)
        for i in range(count_of_crossover):
            parent1_index = self.indexs[i]
            parent2_index = self.indexs[i + 1]
            if (self.crossover_type == CrossoverType.PartialMappedCrossover):
                self.PartialMappedCrossover(parent1_index, parent2_index, child1_index, child2_index)
                self.objective_values[child1_index] = self.compute_objective_value(self.chromosomes[child1_index])
                self.objective_values[child2_index] = self.compute_objective_value(self.chromosomes[child2_index])
            child1_index += 2
            child2_index += 2
    def perfrom_mutation_operation(self):
        self.shuffle_index(self.pop_size + self.crossover_size)
        child1_index = self.pop_size + self.crossover_size
        for i in range(self.mutation_size):
            if(self.mutation_type == MutationType.Inversion):
                parent1_index = self.indexs[i]
                self.inversion_mutation(parent1_index, child1_index)
                self.objective_values[child1_index] = self.compute_objective_value(self.chromosomes[child1_index])
                child1_index += 1
    def evaluate_fitness(self):
        for i,chromosome in enumerate(self.chromosomes[:self.pop_size]):
            self.objective_values[i] = self.compute_objective_value(chromosome)

        min_obj_val = np.min(self.objective_values)
        max_obj_val = np.max(self.objective_values)
        range_obj_val = max_obj_val - min_obj_val

        for i,obj in enumerate(self.objective_values):
            self.fitness[i] = max(self.least_fitness_factor*range_obj_val, pow(10, -5) + (max_obj_val - obj))

    def update_best_solution(self):
        best_index = np.argmax(self.fitness)
        if(self.best_fitness<self.fitness[best_index]):
            self.best_fitness = self.fitness[best_index]
            for i,gene in enumerate(self.chromosomes[best_index]):
                self.best_chromosome[i] = gene

    def perform_selection(self):
        if self.selection_type == SelectionType.Deterministic:
            index = np.argsort(self.fitness)[::-1]
        elif self.selection_type == SelectionType.Stochastic:
            index = [self.do_roulette_wheel_seletion(self.fitness) for i in range(self.pop_size)]
        else:
            index = self.shuffle_index(self.total_size)
        for i in range(self.pop_size):
            for j in range(self.number_of_genes):
                self.selected_chrmosomes[i][j] = self.chromosomes[index[i][j]]
        for i in range(self.pop_size):
            for j in range(self.number_of_genes):
                self.chromosomes[i][j] = self.selected_chrmosomes[i][j]







