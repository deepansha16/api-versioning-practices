## Notebooks

 1 Classification-BR:NBR.ipynb : deals with classification into breaking and non-breaking changes, extraction of type of breaking changes, segmentation of API's according to age,breaking and non breaking changes over major, minor and patch releases

 2 Cluster.ipynb: ran clustering on diff type of algorithms: K-Means, Agglomerative Clustering, DBSCAN Clustering, Decision Tree Classifier

 3 Feature-selection.ipynb : Feature selection using different types of estimators(XGBClassifier,ExtraTreesClassifier,GradientBoostingClassifier), Select K best method for feature importance, Mutual information implemented for same, cosine similarity calculation, Clustering using Gaussian Mixture Model and Spectral Clustering, confusion matrix for both, network graphs protoypes

 4 Graphs.ipynb: Study of API's, filtered by label, type of change, Age, Total API changes and total breaking changes. Boxplots for all the releases over the years ( major,minor,patch,unlabeled)

 5 PCA-Loadings.ipynb: extract loadings for all features, PCA Loadings plots for young and old API's, PCA on all nine subsets of predicted and true labels

 6 breaking.ipynb: count of features changing across major, minor, patch and no label releases, Breaking and Non breaking for Major, minor, patch over the years

 7 network.ipynb : Network graphs for the entire dataset, as well as all the years present in the data

 8 oversample.ipynb : Oversmapling of gaussian mixture trained model using SMOTE, calculation of accuracy, precision, recall etc for dataframes subset by Year's

 9 plot.ipynb: 9x9 matrix for labels vs predicted labels (using TSNE, PCA and UMAP), visualization of clusters

 10 prep_db.py : Extracts data from MongoDB, converts to df, then extracts all the features from the diff column

 11 semver.ipynb: Few examples of API : info-versions vs label( major, minor,patch, major.minor, etc..)

 12 subset.ipynb:  Calculation of accuracy, precision, recall for all Years without oversampling

 13 version-label.ipynb: labels all verison identifiers according to their info version fields

 14 sunburst.ipynb: generates hierarchy of each api for plotting sunburst graphs