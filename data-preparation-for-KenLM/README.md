# Pre-processing text using KenLM

I used the KenLM model to pre-process text. I first created an ARPA file based on texts from the CORE, FTD and EN-GINCO datasets. The original text file (*data-preparation-for-KenLM/English-data-for-KenLM.txt*) consists of around 3M sentences, each in their own line. Markup language was removed prior to creating the ARPA file. Based on the KenLM information, the file consists of 62,475,695 unigram tokens and 1,459,185 types.

I built a 5-gram KenLM model.

KenLM scores for "non-textual" texts (those that remained after new preparation of texts):

|       |   KenLM-score |
|:------|--------------:|
| count |         5     |
| mean  |      -765.833 |
| std   |       367.754 |
| min   |     -1249.58  |
| 25%   |     -1048.26  |
| 50%   |      -594.898 |
| 75%   |      -570.265 |
| max   |      -366.167 |

KenLM scores for "suitable" texts:

|       |   KenLM-score |
|:------|--------------:|
| count |        87     |
| mean  |     -1079.45  |
| std   |      1094.04  |
| min   |     -6294.92  |
| 25%   |     -1189.48  |
| 50%   |      -682.453 |
| 75%   |      -461.512 |
| max   |      -283.303 |