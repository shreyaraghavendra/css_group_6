### Introduction

* Cancerous tumor dynamics include their growth, propagation, and treatment  
* Cell division states: G1, G2, S, M. Each have different durations. Most cancerous cells in G1-phase -> the mean time is important.  
* CA models can demonstrate how global (macroscopic) behavior of cell assemblies as tumors are affected by changes in local (microscopic) properties of cell interaction.  
* This model focuses on these macroscopic properties:  
(a) Metastasis - the ability to migrate to other parts of the body through the lymphatic system or the bloodstream, causing secondary tumors in other organs.  
(b) Cytotoxic effect of the immune system  
(c) Mechanical pressure inside the tumor  
* Time delay in the model represents the time it takes for a cancer cell to undergo mitosis. This enables metastasis.  

### Continuous Model

### Cellular Automaton Model

#### Types of cells modelled:

N: normal cells  
C: cancerous (abnormal) cells  
D: dead cancerous cells  
E: effector (cytotoxic) cells (macrophages, etc)   
E_{0): complexes produced by the cytotoxic process  

#### Reaction Equations:

$C \xrightarrow{k'_1(t)} 2C$  
Represents the proliferation of cancerous cells at time `t`.

$C + E_0 \xrightarrow{k_2} E \xrightarrow{k_3} E_0 + D$  
The first part is a cytotoxic process where an effector cell `E_0` binds to a cancerous cell `C`, becoming an activated effector cell `E`.   The second part denotes the dissolution of the effector cell complex, resulting in the reversion of the effector cell to its original state `E_0` and a dead cell `D`. This sequence implies that the effector cell attacks the cancerous cell, which eventually dies.

$D \xrightarrow{k_4} \text{normal}$  
Represents revertion of a dead cell to a normal cell.  

 
| Parameter | Value (day^-1) | Description                                                                                      |
|-----------|----------------|--------------------------------------------------------------------------------------------------|
| k1        |  0.58-0.89     | Rate of proliferation, depends on the total number of cancerous cells `N_C` and a constant `\phi`. The rate decreases as `N_C` approaches `\phi`. |      
| k2        | 0.2-0.4        | Activation rate of the immune response against the cancerous cell.                               |
| k3        | 0.2-0.65       | Completion rate of the cytotoxic process where the cancer cell is destroyed.                     |
| k4        | 0.1-0.4        | Rate of a cell's return to a non-cancerous state.                                                |




### Results
