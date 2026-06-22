# heart_disease_detection
# Description
Heart disease remains one of the leading causes of death worldwide, emphasizing the need for early and accurate diagnosis. This project, “Heart Disease Detection Using Neuro-Fuzzy Approach,” presents a hybrid intelligent system that combines the learning capabilities of Artificial Neural Networks (ANN) with the human-like reasoning power of Fuzzy Logic. The proposed model, based on the Adaptive Neuro-Fuzzy Inference System (ANFIS), analyzes key clinical parameters such as age, blood pressure, cholesterol, chest pain type, and ECG results to predict the likelihood of heart disease. 
The system first preprocesses medical data to handle missing values, normalize inputs, and encode categorical features. It then employs the Neuro-Fuzzy framework to learn fuzzy membership functions and optimize decision rules through neural learning techniques. This hybrid approach effectively handles uncertainties and imprecise medical data, leading to higher prediction accuracy compared to conventional machine learning models.
A user-friendly interface is developed to allow doctors and healthcare professionals to input patient data and instantly view the predicted heart disease risk level (Low, Medium, or High) along with a confidence score. The model’s performance is evaluated using metrics such as accuracy, precision, recall, and F1-score, demonstrating reliable diagnostic support.
By integrating adaptive learning with interpretable fuzzy reasoning, the proposed Neuro-Fuzzy system provides a robust, intelligent decision-support tool for early heart disease detection, thereby contributing to improved clinical outcomes and preventive healthcare.
# Features
1. Hybrid Neuro-Fuzzy Model
•	Combines the learning ability of Neural Networks with the reasoning capability of Fuzzy Logic.
•	Automatically tunes fuzzy membership functions and rules using the ANFIS (Adaptive Neuro-Fuzzy Inference System) framework.
•	Provides adaptive and intelligent decision-making even with uncertain or noisy data.

 2. Intelligent Data Analysis
•	Analyzes key medical attributes such as age, blood pressure, cholesterol, ECG results, and heart rate.
•	Identifies complex patterns and correlations that may not be easily detected through manual analysis.
•	Supports data normalization, feature selection, and correlation-based filtering for improved model performance.

3. High Prediction Accuracy
•	The hybrid approach improves accuracy, precision, recall, and F1-score compared to traditional methods (like logistic regression or SVM).
•	Learns from large datasets and refines predictions over time through adaptive learning.

4. Fuzzy Logic-Based Decision Making
•	Handles imprecise, linguistic, or uncertain data using fuzzy sets (e.g., “low,” “medium,” “high”).
•	Mimics human-like reasoning for medical conditions that are not strictly defined numerically.

5. User-Friendly Interface
•	Provides an easy-to-use Graphical User Interface (GUI) — can be implemented as a Web App or Android App.
6
•	Allows users (patients or doctors) to input medical data and view real-time predictions.
•	Displays output such as:
o	Prediction: Heart Disease: Yes/No
o	Risk Level: Low / Medium / High
o	Confidence Score (%)

6. Performance Evaluation and Visualization
•	Evaluates the system using metrics like Accuracy, Precision, Recall, F1-Score, and Confusion Matrix.
•	Provides graphical visualization of model performance through charts and plots for better understanding.

7. Database Integration
•	Stores and retrieves patient data using MySQL or Firebase, enabling record management and future reference.
•	Facilitates future model retraining or trend analysis.

8. Scalability and Extensibility
•	Can be extended to integrate with IoT-based health sensors for real-time data collection (e.g., wearable devices).
•	Can support additional AI models for comparative analysis or ensemble predictions.
