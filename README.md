### Introduction

This application uses streamlit and the bittensor cli commands to run a website that monitors the last updated blocks of every validator.

## Setup instructions

Ensure you have python 3 installed

```
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt

```

Start the streamlit app using - 
```
streamlit run validatorData.py
```

Navigate to localhost:8051 to see the page