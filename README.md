# smsem project


### Prerequisites

- Python 3.x
- Flask
- Required Python packages (listed in `requirements.txt`)

### Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/Taiwrash/smsem.git
   cd smsem


pip install -r requirements.txt

python app.py

curl -X POST -H "Content-Type: application/json" -d '{"message": "Your message here"}' http://127.0.0.1:5000/predict

{
  "message": "Your message here"
}