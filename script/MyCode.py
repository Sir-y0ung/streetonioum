from code_runner_files.AbstractCodeRunner import AbstractCodeRunner
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import pandas as pd

class MyCode(AbstractCodeRunner):
    def run_code(self):

        #Read data 
        #Please, do not edit this line of code.
        data = pd.read_csv("datafile.csv")

        #Code to run
        #Add here the code to run. You can create different functions and the results should be clear stated.
        #clustered_data, reduced_clustered_data, cluster_centers = cluster_data(data=data)
        #clusters_figure = plot_clusters_figure(data=reduced_clustered_data, centroids=cluster_centers)

        #Gather results
        #The results variable should be a list of dicts. Each dict element must have the following elements:
        # "data": the results, "name": name of the results (will be used a the filename in which this resuls will be stored),
        # and "format": the format in which you want to store the results (fig, csv, txt for the moment)
        results = [
            {
                "data": data,
                "name": "clustered_data",
                "format": "csv"
            }
        ]
        return results


def preprocess_data(data):
    # get categorical attributes
    categorical_vars = data.select_dtypes(include=["object","category"])

    # label encoder each categorical attribute
    for c in categorical_vars.columns.tolist():
        categorical_vars[c] = LabelEncoder().fit_transform(categorical_vars[c])

    # one-hot encode categorical variables
    onehot_encoder_x = OneHotEncoder()
    x_cat = onehot_encoder_x.fit_transform(categorical_vars).toarray()

    # standardize numerical variables
    numerical_vars = data.select_dtypes(include=["int64", "float64"])
    x_num = StandardScaler().fit_transform(numerical_vars)

    # return the standardized numerical attributes stacked with the one-hot encoded categorical attributes
    return np.column_stack((x_num, x_cat))    


def cluster_data(data):
    data_scaled = preprocess_data(data)
    tsne = TSNE(n_components=2, random_state=42)
    data_reduced = tsne.fit_transform(data_scaled)
    kmeans = KMeans(n_init=10, n_clusters=3, random_state=42).fit(data_reduced)
    data["cluster"] = kmeans.predict(data_reduced)
    reduced_data = pd.DataFrame(data=data_reduced, index=list(range(0,data_reduced.shape[0])), columns=["PC1","PC2"])
    reduced_data["cluster"] = data["cluster"]
    return data, reduced_data, kmeans.cluster_centers_


def plot_clusters_figure(data, centroids):
    fig = plt.figure(figsize=(8, 6))
    colors = ["tab:blue", "tab:orange", "tab:green"]

    for cluster_label, centroid in enumerate(centroids):
        cluster_data = data[data['cluster'] == cluster_label].drop('cluster', axis=1)
        plt.scatter(cluster_data["PC1"], cluster_data["PC2"], color=colors[cluster_label], label=f'Cluster {cluster_label}', marker='o', s=10, alpha=0.2)
        plt.scatter(centroid[0], centroid[1], marker="*", s=100, color=colors[cluster_label], label=f'Centroid of cluster {cluster_label}', zorder=100)
    
    plt.title('t-SNE for clustered data with K-Means')
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), fancybox=True, ncol=cluster_label+1)
    plt.tight_layout()
    return fig
