## Notebooks

### Classification-BR:NBR.ipynb
Deals with classification into breaking and non-breaking changes, extraction of type of breaking changes, segmentation of API's according to age, breaking and non-breaking changes over major, minor and patch releases

### Cluster.ipynb
Ran clustering on different types of algorithms: K-Means, Agglomerative Clustering, DBSCAN Clustering, Decision Tree Classifier

### Feature-selection.ipynb
Feature selection using different types of estimators (XGBClassifier, ExtraTreesClassifier, GradientBoostingClassifier), Select K best method for feature importance, Mutual information implemented for the same, cosine similarity calculation, Clustering using Gaussian Mixture Model and Spectral Clustering, confusion matrix for both, network graphs prototypes

### Graphs.ipynb
Study of API's, filtered by label, type of change, Age, Total API changes and total breaking changes. Boxplots for all the releases over the years (major, minor, patch, unlabeled)

### PCA-Loadings.ipynb
Extract loadings for all features, PCA Loadings plots for young and old API's, PCA on all nine subsets of predicted and true labels

### breaking.ipynb
Count of features changing across major, minor, patch, and no label releases, Breaking and Non breaking for Major, minor, patch over the years

### network.ipynb
Network graphs for the entire dataset, as well as all the years present in the data

### oversample.ipynb
Oversampling of Gaussian mixture trained model using SMOTE, calculation of accuracy, precision, recall, etc. for dataframes subset by Year's

### plot.ipynb
9x9 matrix for labels vs predicted labels (using TSNE, PCA, and UMAP), visualization of clusters

### prep_db.py
Extracts data from MongoDB, converts to df, then extracts all the features from the diff column

### semver.ipynb
Few examples of API: info-versions vs label (major, minor, patch, major.minor, etc..)

### subset.ipynb
Calculation of accuracy, precision, recall for all Years without oversampling

### version-label.ipynb
Labels all version identifiers according to their info version fields

### sunburst.ipynb
Generates hierarchy of each API for plotting sunburst graphs
