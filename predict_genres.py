# install the libraries necessary for data wrangling, prediction and result analysis
import json
import numpy as np
import pandas as pd
import time
#import matplotlib.pyplot as plt
#from sklearn import metrics
#from sklearn.metrics import classification_report, confusion_matrix, f1_score,precision_score, recall_score
#import torch
from numba import cuda

# Install transformers
#!pip install -q transformers

# Install the simpletransformers
#!pip install -q simpletransformers
from simpletransformers.classification import ClassificationModel

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Install wandb
#!pip install -q wandb
#import wandb

# Login to wandb
#wandb.login()

# Initialize Wandb
#run = wandb.init(project="X-GENRE classifiers", entity="tajak", name="testing-trained-model")

# Load the trained model from Wandb
#model_name = "tajak/X-GENRE classifiers/X-GENRE-classifier"
# Use the latest version of the model
#model_at = run.use_artifact(model_name + ":latest")
# Download the directory
#model_dir = model_at.download()

# Loading a local save
model = ClassificationModel(
    "xlmroberta", "artifacts/X-GENRE-classifier:v0/")

# Open csv file

# MaCoCu-sl-en
#corpus_path = "Macocu-sl-en-doc-format-filtered.csv"

# MaCoCu-is-en
#corpus_path = "MaCoCu-is/Macocu-is-en-doc-format.csv"

# MaCoCu-mt-en
#corpus_path = "MaCoCu-mt/Macocu-mt-en-doc-format-filtered.csv"

# MaCoCu-mk-en
corpus_path = "MaCoCu-mk/Macocu-mk-en-doc-format-filtered.csv"

corpus_df = pd.read_csv(corpus_path, sep = "\t", index_col= 0)

def predict(dataframe, file_path):
    """
    This function takes the dataframe with English documents in the en_doc column, prepared in previous notebooks, and applies the trained model on it to infer predictions. It prints the time that it took to predict to all instances. It saves the results as a new column in the dataframe and returns the dataframe.

    Args:
    - dataframe (pandas DataFrame)
    - file_path: the path to the new CSV file with predictions
    """
    # Define the label list
    labels = ["Other", "Information/Explanation", "News", "Instruction", "Opinion/Argumentation", "Forum", "Prose/Lyrical", "Legal", "Promotion"]
    
    # Split the dataframe into batches
    # Create batches of text
    from itertools import islice

    def chunk(arr_range, arr_size):
        arr_range = iter(arr_range)
        return iter(lambda: tuple(islice(arr_range, arr_size)), ())

    batches_list = list(chunk(dataframe.en_doc, 8))

    batches_list_new = []

    for i in batches_list:
        batches_list_new.append(list(i))

    print("The dataset is split into {} batches of {} texts.".format(len(batches_list_new),len(batches_list_new[0])))

    # Apply softmax to the raw outputs
    def softmax(x):
    #Compute softmax values for each sets of scores in x.
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    y_pred = []
    y_distr = []
    most_probable = []
    batch_counter = 0

    print("Prediction started.")
    start_time = time.time()

    for i in batches_list_new:
        output = model.predict(i)
        current_y_pred = output[0]
        current_y_distr = output[1]
        current_y_distr_softmax = []
        current_y_distr_most_probable = []
        for i in current_y_distr:
            distr = softmax(i)
            distr_dict = {labels[i]: round(distr[i],4) for i in range(len(labels))}
            current_y_distr_softmax.append(distr_dict)
            # Also add the information for the softmax of the most probable category ("certainty")
            distr_sorted = np.sort(distr)
            current_y_distr_most_probable.append(distr_sorted[-1])

        for i in current_y_pred:
            y_pred.append(i)
        
        for i in current_y_distr_softmax:
            y_distr.append(i)
        
        for i in current_y_distr_most_probable:
            most_probable.append(i)
        
        batch_counter += 1
        print("Batch {} predicted.".format(batch_counter))
        
        json_backup = [batch_counter,y_pred, y_distr, most_probable]

        # Save y_pred and y_distr just in case
        with open("batch-backup-predictions.json","w") as backup:
            json.dump(json_backup, backup)

    prediction_time = round((time.time() - start_time)/60,2)

    print("Prediction completed. It took {} minutes for {} instances - {} minutes per one instance.".format(prediction_time, dataframe.shape[0], prediction_time/dataframe.shape[0]))
    
    dataframe["X-GENRE"] = y_pred
    dataframe["label_distribution"] = y_distr
    dataframe["chosen_category_distr"] = most_probable

    # Save the new dataframe which contains the y_pred values as well
    dataframe.to_csv("{}".format(file_path), sep="\t")

    return dataframe


# Try prediction on a sample
sample = corpus_df.sample(n=30)
predict(sample, "MaCoCu-mk/sample-prediction-test.csv")

predict(corpus_df, "MaCoCu-mk/Macocu-mk-en-predicted.csv")
