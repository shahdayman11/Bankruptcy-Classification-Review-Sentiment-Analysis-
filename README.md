**AI-Based Bankruptcy Prediction & Customer Review Analysis**

* Developed an end-to-end **bankruptcy prediction system** using financial ratios from the Company Bankruptcy Prediction dataset. Performed feature engineering, anomaly detection with Isolation Forest, feature selection using Boruta, and trained multiple machine learning models (Logistic Regression, XGBoost, and AdaBoost) with hyperparameter optimization using Optuna. Selected Logistic Regression with a tuned decision threshold to maximize recall for bankruptcy detection.
* Built a **customer sentiment analysis pipeline** using classical NLP techniques, including Bag of Words, TF-IDF, and bigrams with Logistic Regression, and compared their performance for review classification.
* Designed a **deep learning sentiment analysis model** using Word2Vec/GloVe embeddings and a Bidirectional LSTM to classify customer reviews, incorporating text preprocessing, tokenization, padding, class weighting, and early stopping for improved generalization.
* Developed a **web scraping pipeline** to automatically collect customer reviews from Trustpilot for Amazon using Python, enabling the creation of a real-world review dataset for sentiment analysis.
* Applied comprehensive data preprocessing, feature engineering, model evaluation, threshold optimization, and performance analysis using metrics such as ROC-AUC, Precision, Recall, and F1-score.
* **Technologies:** Python, Pandas, NumPy, Scikit-learn, TensorFlow/Keras, XGBoost, AdaBoost, Logistic Regression, Optuna, NLTK, Gensim, BeautifulSoupa, Word2Vec/GloVe.
