# CA model for tumor growth and treatment

This project reproduces the study described in [On a cellular automaton with time delay for modelling cancer tumors](https://iopscience.iop.org/article/10.1088/1742-6596/285/1/012015) as part of Complex System Simulation 2024 course at UvA.

## Description

### Background and Motivation
The dynamics of tumor growth and metastasis represent a critical area of study in the field of oncology and mathematical biology. Understanding the underlying mechanisms driving the proliferation and spread of cancer cells is vital for the development of effective treatments and interventions. Discrete systems like Cellular Automata (CA) provide a robust framework for detailed simulation of complex cellular interactions. The inclusion of time delays in these models is crucial as it reflects the real-time cell division cycles and the variable durations of different cell phases, which are significant in understanding tumor development and progression. Thus, this research seeks to bridge the gap between the micro-level cellular interactions and the macro-level tumor growth patterns, providing insights into the emergent behaviors that contribute to cancer progression.

### Disciplines Utilized
The research is grounded in the following disciplines:
- **Complex Systems**: For the analysis of emergent behaviors from simple interactions between components of the tumor microenvironment.
- **Chaos Theory**: To explore the sensitivity of tumor growth dynamics to initial conditions and parameter changes.
- **Computational Biology**: To simulate tumor growth using discrete and continuous models.
- **Mathematical Oncology**: To provide a theoretical basis for the growth patterns observed in empirical data.
- **Statistical Physics and Percolation Theory**: To study the formation and properties of clusters within the CA as a model for metastasis.

### Problem Addressed
The primary problem being addressed is the predictive modeling of tumor growth and the conditions under which metastasis occurs. This includes determining the critical points within tumor growth models that could correspond to the transition from benign to malignant phases. By identifying such points, the research aims to contribute to the development of targeted therapies that could potentially disrupt or reverse the progression of cancer.

### Research Questions
1. At what point does a growing tumor transition to a metastatic state, and can this transition be predicted by a critical value of a specific parameter in the model? 
2. How does the interplay between cancerous cell proliferation and treatment influence tumor growth dynamics? I.e., how do time delays in tumor growth influence the macroscopic growth patterns of tumors? 


### Model Implementation and Simulation
A two-dimensional stochastic cellular automaton model was implemented to simulate the competition for resources among cancer and normal cells. Percolation theory will be used to calculate the number of clusters. The project incorporate a continuous growth model based on which the CA was designed to analyze fixed points and bifurcations.

### Emergent Phenomenon Focus
The research focuses on two emergent phenomena:
- **Phase transitions** in tumor growth, specifically the transition to metastasis. To detect this, we looked at signs of critical behavior around different parameters of our CA model.
- **Bifurcation** due to the introduction of time delay in the model. Analogous to cancer treatment, time delay leads to oscillatory behavior in the model which can be analyzed through the lense of bifurcation theory.

## Getting Started

### Installing

To install all necessary packages, run the following command:

```
pip install -r requirements.txt
```

### Executing program

All analysis is done in Jupyter Notebooks which utilize functions from python files. The main code and modules are available in the folder `code/functions` as .py files. 

Jupyter notebooks can be opened in JupyterLab or Visual Studio Code and executed by pressing `Run All`.

### Testing and Development Details:

* We have atleast 10% ‘assert’ statements inline
* “pytest .” works and succeeds
* Code is structured as a module with “__init__.py”
* Functions documented in detail through docstrings


## Authors

* Eline van de Lagemaat
* Jiawei Liao
* Kenia Lopez
* Shreya Raghavendra


### References
1. [Iarosz, K. C., Martins, C. C., Batista, A. M., Viana, R. L., Lopes, S. R., Caldas, I. L., & Penna, T. J. P. (2011, March). On a cellular automaton with time delay for modelling cancer tumors. In Journal of Physics: Conference Series (Vol. 285, No. 1, p. 012015). IOP Publishing.](https://iopscience.iop.org/article/10.1088/1742-6596/285/1/012015/meta)
2. [Qi, A. S., Zheng, X., Du, C. Y., & An, B. S. (1993). A cellular automaton model of cancerous growth. Journal of theoretical biology, 161(1), 1-12.](https://www.sciencedirect.com/science/article/pii/S0022519383710350)
3. [Thomlinson, R. H. (1982). Measurement and management of carcinoma of the breast. Clinical Radiology, 33(5), 481-493.](https://www.sciencedirect.com/science/article/pii/S0009926082801530)
