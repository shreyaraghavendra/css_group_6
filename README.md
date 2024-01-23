## Tumor Growth and Metastasis - a Continuous and Discrete Analysis

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
1. How does the interplay between cancerous cell proliferation and immune response influence tumor growth dynamics?
2. At what point does a growing tumor transition to a metastatic state, and can this transition be predicted by a critical value of a specific parameter in the model?
3. How do time delays in cell division cycles influence the macroscopic growth patterns of tumors?
4. How does the number of clusters observed in the CA vary with the proliferation rate, and what implications does this have for the onset of metastasis?

### Model Implementation and Simulation
A two-dimensional stochastic cellular automaton model will be implemented to simulate the competition for resources among cancer and normal cells. Percolation theory will be used to calculate the number of clusters. If time allows, the research will incorporate a continuous growth model based on which the CA was designed to analyze fixed points and bifurcations.

### Emergent Phenomenon Focus
The research will focus on the emergent phenomenon of **phase transitions** in tumor growth, specifically the transition to metastasis. To detect this, we will analyze the model for signs of critical behavior, such as power-law scaling indicative of **self-organized criticality**. We will also study the **oscillatory behavior** of tumor cell populations as a potential emergent phenomenon and how time delays can influence these dynamics, potentially leading to oscillatory behavior or stability within the modeled system.

### References
1. K C Iarosz et al 2011 J. Phys.: Conf. Ser. 285 012015
2. Qi A -S, Zheng X, Du C -Y and An B -S, A cellular automaton model of cancerous growth, 1993 Journal of Theoretical Biology 161 1.
3. Thomlinson R, Measurement and management of carcinoma of the breast, 1982 Clinical Radiology 33 481.
