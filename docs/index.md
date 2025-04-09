# Network Traffic Prediction 📶📊
[![GitHub](https://img.shields.io/badge/GitHub-code-blue?style=flat&logo=github&logoColor=white&color=red)](https://github.com/prsdm/network-traffic-prediction) [![Medium](https://img.shields.io/badge/Medium-view_article-green?style=flat&logo=medium&logoColor=white&color=green)](https://medium.com/@yourusername/network-traffic-prediction-for-beginners) [![X (formerly Twitter)](https://img.shields.io/badge/X-@okeyamy-1DA1F2?style=flat&logo=twitter&logoColor=white&color=blue)](https://x.com/okey_amy)

Welcome to the **Network Traffic Prediction** project! This project leverages machine learning to classify network traffic for improved traffic management and security. It includes data ingestion, model training, FastAPI deployment, and monitoring using Evidently AI for data drift detection.

## Project Diagram
The architecture diagram below outlines the flow from data ingestion to model deployment and monitoring:

![Architecture Diagram](mlops.jpg)

## Project Structure
Here’s an overview of the project’s key files and folders:
```plaintext
.
├── app.py                  # FastAPI app for model inference
├── config.py               # Configuration for MLflow tracking
├── data/                   # Folder containing training and test datasets
├── Dockerfile              # Docker configuration
├── main.py                 # Main script for data processing and model training
├── models/                 # Folder where trained model files are saved
├── monitor.py              # Script for monitoring model performance
├── requirements.txt        # Python dependencies
├── webpage.html            # Frontend HTML for submitting predictions
└── README.md               # Project documentation
```

## Getting Started
Follow these steps to set up, train, deploy, and monitor the model.

### 1. Clone the Repository
Clone the project repository from GitHub and navigate into the project directory:
```bash
git clone https://github.com/prsdm/network-traffic-project.git
cd network-traffic-project
```

### 2. Set Up the Environment
Make sure Python 3.8+ is installed. Set up a virtual environment and install the required dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Alternatively, use the Makefile command:
```bash
make setup
```

### 3. Data Preparation
Ensure your training and test datasets are in the `data` folder. If you have DVC set up, you can pull the data as follows:
```bash
dvc pull
```

### 4. Train the Model
To train the model, execute:
```bash
python main.py
```
Alternatively, you can use the Makefile:
```bash
make run
```
This will load, preprocess, and train the model, saving it to the `models/` directory.

### 5. Start the FastAPI Server
To serve model predictions, start the FastAPI application:
```bash
uvicorn app:app --reload
```
This hosts the API at `http://127.0.0.1:8000`, where you can make prediction requests.

### 6. Dockerize the Application
1. **Build the Docker image**:
   ```bash
   docker build -t network_traffic_api .
   ```
2. **Run the Docker container**:
   ```bash
   docker run -p 80:80 network_traffic_api
   ```
3. **Push to Docker Hub** for deployment on cloud platforms:
   ```bash
   docker tag network_traffic_api your-dockerhub-username/network_traffic_api
   docker push your-dockerhub-username/network_traffic_api
   ```

### 7. Frontend (HTML)
This project includes an HTML frontend (`webpage.html`) for entering network packet data and submitting it to the FastAPI backend for predictions.

1. Open `webpage.html` in your browser.
2. Enter the necessary network traffic data.
3. Submit the form to see the prediction on the page.

Ensure the FastAPI server is running to process requests from the HTML form.

### 8. Model Monitoring with Evidently AI
For monitoring the model’s performance and detecting data drift, use the `monitor.py` script:
```bash
python monitor.py
```
This script uses Evidently AI to generate reports on data drift, model quality, and other metrics, saved as HTML files (`data_drift_report.html` and `classification_tests.html`).

## Configuration Details
### `app.py` - FastAPI Setup
The FastAPI app handles incoming requests for predictions. It uses the model stored in `models/model.pkl` and defines input data schemas for network packet attributes like `tcp.srcport`, `ip.proto`, and `frame.len`.

### `monitor.py` - Model Monitoring
This script integrates Evidently AI to check for data drift, ensuring model predictions stay reliable over time. It loads reference data, applies preprocessing, and runs diagnostic reports on model quality and drift.

### `main.py` - Model Training
The `main.py` script ingests, cleans, and trains on network traffic data. It logs model metrics to MLflow and saves the trained model, which is then used for FastAPI predictions.

## API Endpoints
### `POST /predict`
- **Request**: JSON payload containing network packet attributes like `tcp.srcport`, `tcp.dstport`, `ip.proto`, etc.
- **Response**: Returns the predicted class label (e.g., "Benign" or "DDoS-ACK").

Example request:
```json
{
  "tcp.srcport": 52332,
  "tcp.dstport": 8000,
  "ip.proto": 6,
  "frame.len": 66,
  "tcp.flags.syn": 0,
  "tcp.flags.reset": 0,
  "tcp.flags.push": 0,
  "tcp.flags.ack": 1,
  "ip.flags.mf": 0,
  "ip.flags.df": 1,
  "ip.flags.rb": 0,
  "tcp.seq": 1,
  "tcp.ack": 1,
  "Packets": 10,
  "Bytes": 1144,
  "Tx Packets": 6,
  "Tx Bytes": 560,
  "Rx Packets": 4,
  "Rx Bytes": 584
}
```

Example response:
```json
{
  "predicted_class": 1,
  "class_label": "DDoS-ACK"
}
```

## License
This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.

---

Happy coding! If you encounter any issues, feel free to open an issue in the repository.