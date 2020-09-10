# Quoter Model and Contagion
This repository is the codebase for our paper [1]: [Complex contagion features without social reinforcement in a model of social information flow](https://www.mdpi.com/1099-4300/22/3/265) as well as much of my master's thesis [2].

This research studies the properties of -- and provides validation for -- the *quoter model* as a model for social information flow. The quoter model, recently proposed in [3], offers an idealistic mechanism for how people communicate written information in online social contexts (i.e. tweets on Twitter or posts on Facebook). The model runs on a social network: each node (user) takes turns generating a sequence of words by one of two mechanisms: (i) copying a segment of a random neighbor's past text, (ii) randomly generating new text according to a vocabulary distribution. We can then apply the *cross-entropy* (an information-theoretic measure which satisfies temporal precedence) to quantify information flow between each pair of users text. 

Here our main objective was to understand how network structure (density, clustering, etc.) impacts information flow in the quoter model. We compare with other traditional models for social contagion (namely the *threshold model*) and find interesting results. In particular, although the quoter model does not include a threshold or specify a social reinforcement mechanism explicitly -- we find that the quoter model depends on network structure in similar ways to traditional social contagion models. Two commonalities are that density inhibits information flow and clustering promotes information flow. This suggests that a more nuanced, information-theoretic, measure of information flow -- in conjuction with a simple model (the quoter model) can lead to realistic outcomes.

Every immediate directory in this repository corresponds to one set of "experiments" in which we ran many (thousands) of quoter model simulations. Although the organization here is not great, generally the files are organized as follows. 
- `sims_scripts/` contains scripts for simulating the quoter model and calculating cross-entropy on the VACC (Vermont Advanced Computing Core). `.sh` files are for submitting jobs. 
- `processing/` contains scripts for computing summary statistics of the previously computed cross-entropies. For experiments that were ultimately used to create figures for the paper, you can also find plotting scripts here. For example `small_world/processing/small_world-processing.py` and `small_world/processing/small_world-plot.py`.

The data from the simulations has been omitted as it is ~100GB raw. However, the `.csv` files containing the summary statistics of the data (and which were used to make the figures) is included. Scripts for generating the exact figures in the paper are presented below, e.g. `quoter-model-and-contagion/figure1-QM-complex-simple.py`.

# Requirements
Works with
+ Python 3.6.1
+ Networkx 1.11
Untested with newer versions. Python 3 required.

# References
[1] Pond, T., Magsarjav, S., South, T., Mitchell, L., & Bagrow, J. P. (2020). Complex contagion features without social reinforcement in a model of social information flow. *Entropy*, 22(3), 265.
[2] Pond, T. C. (2020). Measuring and Modeling Information Flow on Social Networks (Doctoral dissertation, The University of Vermont and State Agricultural College).
[3] Bagrow, J. P., & Mitchell, L. (2018). The quoter model: A paradigmatic model of the social flow of written information. *Chaos: An Interdisciplinary Journal of Nonlinear Science*, 28(7), 075304.
