#!/usr/bin/env python
# coding: utf-8

# # Name: Xiangyu Huang
# 
# # Problem Set 10
# 
# ### Learning Objective:
# 
# - Create Python code to automate a given task.
# - Formulate linear optimization models to inform a business decision.
# 
# ### Overview:
# 
# This problem set assesses your ability to turn an abstract formulation into reusable optimization software, as discussed in Week 12.
# 
# ### Grading
# 
# There are three possible scores you can get from submitting this assignment on time (submitting a blank file or one without any apparent effort does not count). Note that the rubric is designed to incentivize you to go for 100% mastery of the material, as the little details matter a lot in business analytics. 
# 
# | Grade | Description |
# |--|--|
# | 5 out of 5 | Perfect submission with no significant errors. | 
# | 4 out of 5 | Near perfect submission with one or more significant errors. |
# | 2 out of 5 | Apparent effort but far from perfect. |

# ## Q1. Reusable Software for Assortment Planning
# 
# Create a function called "optimizeAssortment" with two input arguments:
# 
# - inputFile: filename of the input file. See the attached "PS10-books-input-1.xlsx" and "PS10-books-input-2.xlsx" for examples of the sample input.
# - outputFile: filename of the output file that the function will create. 
# 
# The function should implement the abstract formulation for Problem 9.2 and produce the outputFile. See the attached "PS10-books-sampleOutput-1.xlsx" for the desired output file format corresponding to the "PS10-books-input-1.xlsx" input file. The abstract formulation is reproduced below for your convenience.
# 
# **Data:**
# 
# - $B$: the set of books.
# - $G$: the set of genres.
# - $a_{bg}$: whether book $b$ is in genre $g$.
# - $q_g$: how many books we need of genre $g$.
# 
# **Decision Variables:** Let $x_b$ deibite whether to carry book $b$. (Binary)
# 
# **Objective and constraints:**
# 
# $$\begin{aligned}
# \text{Minimize:} && \sum_{b \in B} x_b \\
# \text{subject to:} \\
# \text{(Enough books in genre)} && \sum_{b \in B} a_{bg}x_b & \ge q_g & \text{ for each genre $g \in G$.}
# \end{aligned}$$
# 

# In[242]:


# Write your code here
import pandas as pd
from gurobipy import Model, GRB


# In[243]:


def optimizeAssortment(inputFile, outputFile):
    genres = pd.read_excel( inputFile, sheet_name = 'genres', index_col = 0 ).                isnull().replace({True: 0, False: 1})
    G = list(genres.columns)
    B = list(genres.index)
    a = genres
    q = pd.read_excel(inputFile , sheet_name = 'requirements', index_col = 0 )['required']
    mod = Model()
    x = mod.addVars(B, name = 'x', vtype = GRB.BINARY)
    mod.setObjective(sum(x[b] for b in B), GRB.MINIMIZE)
    for g in G:
        mod.addConstr(sum( x[b]*a.loc[b,g] for b in B) >= q[g]) 
    mod.setParam('outputflag',False)
    mod.optimize()
    
    
    writer=pd.ExcelWriter(outputFile)
    df = pd.DataFrame( columns = ['books'])
    i = 0
    for b in B:
        if x[b].x == 1:
            df.loc[i] = b
            i = i + 1
    df.to_excel(writer, sheet_name = 'optimal_decision', index = True)
    pd.DataFrame( [mod.objVal],columns = ['books_needed']).to_excel(writer, sheet_name = 'objective', index = False)
    
    writer.save()
    print('minimum book needed:', mod.objVal)


# In[74]:


# Test code (will create two output files for the two input files)
optimizeAssortment('PS10-books-input-1.xlsx','PS10-books-output-1.xlsx') 
optimizeAssortment('PS10-books-input-2.xlsx','PS10-books-output-2.xlsx') 


# ## Q2. Assigning of Final Grades
# 
# This question asks you to create software that can help a professor assign final grades in such a way so that the average GPA rounds to 3.5, while obtaining an assignment in which there are gaps in scores between consecutive grade levels, and no particular grade is assigned to disproportionally many students.
# 
# **Data:** 
# 
# - $I$: the set of students.
# - $n$: the number of students.
# - $J=\{0,1,\cdots\}$: numerical indices used to denote the various grade levels.
# - $s_i$: the overall score of student $i\in I$ (between 0 and 100). 
# - $g_j$: the GPA corresponding to grade level $j \in J$.
# 
# **Decision Variables:**
# 
# - $x_{ij}$: whether to assign student $i$ to grade level $j$. (Binary)
# - $t_j$: the number of students assigned to grade level $j$. (Continuous)
# - $L_j$: the score cutoff for grade level $j$. (Continuous)
# - $U_j$: the maximum score in grade level $j$. (Continuous)
# 
# $$\begin{aligned}
# \text{Min} && \sum_{j \in J}(U_j-L_j) + 0.1 \sum_{j \in J} t_j \times t_j \\
# \text{s.t.} \\
# \text{(Average GPA)} && 3.495n \le \sum_{i \in I}\sum_{j \in J} x_{ij}g_{j} & \le 3.505n \\
# \text{(Assignment)} && \sum_{j \in J} x_{ij} & = 1 && \text{for each $i \in I$.}\\
# \text{(Max score)} && s_i x_{ij} & \le U_j && \text{for each $i \in I$, $j \in J$.}\\
# \text{(Min score)} && 100(1-x_{ij}) + s_i x_{ij} & \ge L_j && \text{for each $i \in I$, $j \in J$.}\\
# \text{(Correct totals)} && \sum_{i \in I} x_{ij} & = t_j && \text{for each $j \in J$.}\\
# \text{(Bounds)} && L_j & \le U_j && \text{for each $j \in J$.} \\
# \text{(Ordering)} && U_j & \le L_{j-1} && \text{for each $j \in J$ with $j \ge 1$.}
# \end{aligned}$$
# 
# The input data is contained in an Excel file named `PS10-grade-input.xlsx` with two sheets. The first sheet, named "Scores", contains the score of each student. The first five entries look like:
# 
# ![Sample Scores Sheet](PS10-grade1.png)
# 
# The second sheet, named "Levels", is as follows
# 
# ![Sample Levels Sheet](PS10-grade2.png)
# 
# The output data should be an Excel file named `PS10-grade-output.xlsx` that contains the cutoff ($L_j$) for each grade level $j$. It should look like
# 
# ![Sample Output](PS10-grade3.png)
# 
# 

# In[245]:


# Write your code here
scores = pd.read_excel('PS10-grade-input.xlsx', sheet_name = 'Scores', index_col = 0)
levels = pd.read_excel('PS10-grade-input.xlsx', sheet_name = 'Levels', index_col = 0)
I = list(scores.index)
n = len(I)
J = list(levels.index)
J
s = scores['s_i']
g = levels['g_j']
g_name = levels['Letter']
mod = Model()
x = mod.addVars(I, J, name = 'x', vtype = GRB.BINARY)
t = mod.addVars(J, name = 't')
L =  mod.addVars(J, name = 'L')
U =  mod.addVars(J, name = 'U')
mod.setObjective(sum(U[j] - L[j] for j in J) + 0.1*sum(t[j]* t[j] for j in J))
for i in I:
    mod.addConstr(sum(x[i,j] for j in J) == 1)
for i in I:
    for j in J:
        mod.addConstr( s[i]*x[i,j] <= U[j])
        mod.addConstr( 100*(1-x[i,j]) + s[i]*x[i,j]  >= L[j])
for j in J:
    mod.addConstr(sum(x[i,j] for i in I) == t[j])
    mod.addConstr(L[j] <= U[j])
    if j >= 1:
        mod.addConstr(U[j] <= L[j-1])
mod.addConstr(sum(sum(x[i,j]*g[j] for j in J) for i in I) <= 3.505*n)
mod.addConstr(sum(sum(x[i,j]*g[j] for j in J) for i in I) >= 3.495*n)
mod.setParam('outputflag',False)
mod.optimize()

df = pd.DataFrame(columns = ['Letter', 'Cutoff'])
for i in range(len(g)):
    df.loc[i] = [g_name[i], L[i].x]
df


# In[275]:


def gpa_cutoff(inputFile, outputFile):
    scores = pd.read_excel(inputFile, sheet_name = 'Scores', index_col = 0)
    levels = pd.read_excel(inputFile, sheet_name = 'Levels', index_col = 0)
    I = list(scores.index)
    n = len(I)
    J = list(levels.index)
    s = scores['s_i']
    g = levels['g_j']
    g_name = levels['Letter']
    mod = Model()
    x = mod.addVars(I, J, name = 'x', vtype = GRB.BINARY)
    t = mod.addVars(J, name = 't')
    L =  mod.addVars(J, name = 'L')
    U =  mod.addVars(J, name = 'U')
    mod.setObjective(sum(U[j] - L[j] for j in J) + 0.1*sum(t[j]* t[j] for j in J))
    for i in I:
        mod.addConstr(sum(x[i,j] for j in J) == 1)
    for i in I:
        for j in J:
            mod.addConstr( s[i]*x[i,j] <= U[j])
            mod.addConstr( 100*(1-x[i,j]) + s[i]*x[i,j]  >= L[j])
    for j in J:
        mod.addConstr(sum(x[i,j] for i in I) == t[j])
        mod.addConstr(L[j] <= U[j])
        if j >= 1:
            mod.addConstr(U[j] <= L[j-1])
    mod.addConstr(sum(sum(x[i,j]*g[j] for j in J) for i in I) <= 3.505*n)
    mod.addConstr(sum(sum(x[i,j]*g[j] for j in J) for i in I) >= 3.495*n)
    mod.setParam('outputflag',False)
    mod.optimize()

    writer = pd.ExcelWriter(outputFile)
    df = pd.DataFrame(columns = ['Letter', 'Cutoff'])
    for i in range(len(g)):
        df.loc[i] = [g_name[i], L[i].x]
    df.to_excel(writer, sheet_name = 'sheet1', index = False)
    writer.save()


# ## Q3. Team Assignment
# 
# The following MIP can used to assign students into project teams to balance the overall characteristics of each team.
# 
# **Data:**
# 
# - $I$: set of students.
# - $n$: number of teams
# - $J=\{1,2,\cdots,n\}$ : set of teams.
# - $K$: set of characteristics.
# - $a_{ik}$: student $i$'s value for characteristics $k$.
# - $w_k$: the weight for characteristics $k$ in the objective.
# - $L_k$: the ideal lower bound for the sum of characteristic $k$ for any team. 
# - $U_k$: the ideal upper bound for the sum of characteristics $k$ for any team.
# 
# You should assume that the data is given in a excel file with the same format as the `PS10-Team-input-1.xlsx` and `PS10-Team-input-2.xlsx` files attached to this assignment. 
# 
# The sheet named "Students" encodes $I$, $K$ and $a_{ik}$'s. In the below screenshot of `PS10-Team-input-1.xlsx`, $I=\{A,B,C,D,E,F\}$, and $K=\{Person, Male, Programmer, Math, Speaking\}$.
# 
# ![](PS10-Team1.png)
# 
# 
# The sheet named "Parameters" encodes the $w_k$, $L_k$ and $U_k$ for each characteristic $k$.
# 
# ![](PS10-Team2.png)
# 
# **Decision variables:**
# 
# - $x_{ij}$ : whether to assign student $i$ to team $j$. (Binary)
# - $s_k$ : maximum deviation below the ideal lower bound $L_k$ for characteristic $k$. (Continuous)
# - $t_k$ : maximum deviation above the ideal upper bound $U_k$ for characteristic $k$. (Continuous)
# 
# **Objective and constraints:**
# 
# $$\begin{aligned}
# \text{Minimize:} && \sum_{k \in K} w_k(s_k+t_k) \\
# \text{subject to:} && \\
# \text{(Every person assigned)} && \sum_{j \in J} x_{ij} & = 1 && \text{For each person $i \in I$.}\\
# \text{(Team balance)} && L_k - s_k \le \sum_{i \in I} a_{ik}x_{ij} & \le U_k + t_k && \text{For each team $j \in J$ and each $k \in K$.} \\
# \text{(Non-negativity)} && s_k, t_k & \ge 0 && \text{for all $k$.}
# \end{aligned}$$
# 
# **Write a function called "assignTeams" with the following input arguments:**
# 
# - **inputFile:** path to the input spreadsheet.
# - **n:** the number of teams to divide students into.
# 
# **The function should return two variables:**
# 
# - **df:** a DataFrame with one column called "Team". The index should be the name of each individual, and the column "Team" should specify the number $j$ to which the person is assigned.
# - **objval:** the optimal objective value.
# 
# For the test runs, you should download the input files attached to this exercise into the same directory as the Jupyter notebook.

# In[296]:


I = list(student.index)
K = list(student.columns)
a = student
w = parameter.loc['Weights']
L = parameter.loc['L']
U = parameter.loc['U']

n = 10
J = [1,2,3,4,5,6,7,8,9,10]


mod = Model()
x = mod.addVars(I,J, name = 'x' ,vtype = GRB.BINARY)
s = mod.addVars(K, name = 's', lb = 0)
t = mod.addVars(K, name = 't', lb = 0)
mod.setObjective(sum(w[k]*(s[k] + t[k]) for k in K), GRB.MINIMIZE)
for i in I:
    mod.addConstr(sum(x[i,j] for j in J) == 1)
for j in J:
    for k in K:
        mod.addConstr(sum(a.loc[i,k] * x[i,j] for i in I) >= L[k] - s[k])
        mod.addConstr(sum(a.loc[i,k] * x[i,j] for i in I) <= U[k] + t[k]) 
mod.setParam('OutputFlag',False)
mod.optimize()
mod.objVal


# In[284]:


## Write your final code here

student = pd.read_excel('PS10-Team-input-2.xlsx', sheet_name = 'Students', index_col = 0)
parameter = pd.read_excel('PS10-Team-input-2.xlsx', sheet_name = 'Parameters', index_col = 0)
I = list(student.index)
K = list(student.columns)
a = student
w = parameter.loc['Weights']
L = parameter.loc['L']
U = parameter.loc['U']
n = 10
J = [1,2,3,4,5,6,7,8,9,10]
    
mod = Model()
X = mod.addVars(I,J, vtype = GRB.BINARY)
s = mod.addVars(K, name = 's')
t = mod.addVars(K, name = 't')
mod.setObjective(sum(w[k]*(s[k] + t[k]) for k in K))
for i in I:
    mod.addConstr(sum(X[i,j] for j in J) == 1)
for j in J:
    for k in K:
        mod.addConstr(sum(a.loc[i,k] * X[i,j] for i in I) >= L[k] - s[k])
        mod.addConstr(sum(a.loc[i,k] * X[i,j] for i in I) <= U[k] + t[k]) 
mod.setParam('OutputFlag',False)
mod.optimize()


# In[271]:



df = pd.DataFrame(columns = ['Names', 'Team'])
index = 0
for i in I:
for j in J:
    if X[i,j].x == 1:
        df.loc[index] = [i,j] 
        index = index + 1
    else:
        continue
df = df.set_index('Names')
df


# In[297]:



def assignTeams(inputfile, n):
    student = pd.read_excel( inputfile, sheet_name = 'Students', index_col = 0)
    parameter = pd.read_excel( inputfile , sheet_name = 'Parameters', index_col = 0)
    I = list(student.index)
    K = list(student.columns)
    a = student
    w = parameter.loc['Weights']
    L = parameter.loc['L']
    U = parameter.loc['U']
    n = n
    J = range(1,n+1)
    
    mod = Model()
    X = mod.addVars(I,J, vtype = GRB.BINARY)
    s = mod.addVars(K, name = 's')
    t = mod.addVars(K, name = 't')
    mod.setObjective(sum(w[k]*(s[k] + t[k]) for k in K))
    for i in I:
        mod.addConstr(sum(X[i,j] for j in J) == 1)
    for j in J:
        for k in K:
            mod.addConstr(sum(a.loc[i,k] * X[i,j] for i in I) >= L[k] - s[k])
            mod.addConstr(sum(a.loc[i,k] * X[i,j] for i in I) <= U[k] + t[k]) 
    mod.setParam('OutputFlag',False)
    mod.optimize()
    
    df = pd.DataFrame(columns = ['Names', 'Team'])
    index = 0
    for i in I:
        for j in J:
            if X[i,j].x == 1:
                df.loc[index] = [i,j] 
                index = index + 1
            else:
                continue
    df = df.set_index('Names')
    return df, mod.objVal


# In[298]:


# Test run 1
# It is okay if your team numbers are different from what's below, as there are multiple optimal solutions
df,objval=assignTeams('PS10-Team-input-1.xlsx',2)
print('Optimal objective value:',objval)
df


# In[301]:


# Test run 2
# It is okay if your team numbers are different from what's below, as there are multiple optimal solutions
df,objval=assignTeams('PS10-Team-input-2.xlsx',10)
print('Optimal objective value:',objval)
df.sort_values(by='Team')

