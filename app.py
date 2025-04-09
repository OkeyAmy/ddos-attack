from fastapi import FastAPI
from pydantic import BaseModel, Field
import pandas as pd
import joblib
import yaml
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
) 

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

# Define the input schema with aliases for special characters
class InputData(BaseModel):
    tcp_srcport: int = Field(..., alias="tcp.srcport")
    tcp_dstport: int = Field(..., alias="tcp.dstport")
    ip_proto: int = Field(..., alias="ip.proto")
    frame_len: int = Field(..., alias="frame.len")
    tcp_flags_syn: int = Field(..., alias="tcp.flags.syn")
    tcp_flags_reset: int = Field(..., alias="tcp.flags.reset")
    tcp_flags_push: int = Field(..., alias="tcp.flags.push")
    tcp_flags_ack: int = Field(..., alias="tcp.flags.ack")
    ip_flags_mf: int = Field(..., alias="ip.flags.mf")
    ip_flags_df: int = Field(..., alias="ip.flags.df")
    ip_flags_rb: int = Field(..., alias="ip.flags.rb")
    tcp_seq: int = Field(..., alias="tcp.seq")
    tcp_ack: int = Field(..., alias="tcp.ack")
    packets: int = Field(..., alias="Packets")
    bytes: int = Field(..., alias="Bytes")
    tx_packets: int = Field(..., alias="Tx Packets")
    tx_bytes: int = Field(..., alias="Tx Bytes")
    rx_packets: int = Field(..., alias="Rx Packets")
    rx_bytes: int = Field(..., alias="Rx Bytes")

    class Config:
        populate_by_name = True

# Load your trained model once during startup
model = joblib.load('models/model.pkl')

# Define your class label mapping
class_label_mapping = {
    0: "Benign",
    1: "DDoS-ACK",
    2: "DDoS-PSH-ACK"
}

@app.get("/")
async def read_root():
    return {
        "Role": 'Network Traffic Prediction',
        "Model Name": config['model'][3]['name'],
        "health_check": "OK", 
        "model_version": 3
        }

@app.post("/predict")
async def predict(input_data: InputData):
    # Convert input data to a DataFrame
    data_dict = input_data.model_dump(by_alias=True)
    df = pd.DataFrame([data_dict])

    # Make a prediction
    predicted_class = int(model.predict(df)[0])
    class_label = class_label_mapping.get(predicted_class, "Unknown")

    return {
        "predicted_class": predicted_class,
        "class_label": class_label
    } 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)