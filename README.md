# Flask Azure Deployment Demo

This repository contains a demo Flask application with instructions on how to deploy it on Azure.

### Input Shape - 
PyTorch: (1, 3, 640, 640) BCHW and output shape(s) ((1, 67, 8400), (1, 32, 160, 160)) (350.7 MB)

## Disease
```json
{
    "0": "Caries",
    "1": "Crown",
    "2": "Filling",
    "3": "Implant",
    "4": "Malaligned",
    "5": "Mandibular Canal",
    "6": "Missing teeth",
    "7": "Periapical lesion",
    "8": "Retained root",
    "9": "Root Canal Treatment",
    "10": "Root Piece",
    "11": "impacted tooth",
    "12": "maxillary sinus",
    "13": "Bone Loss",
    "14": "Fracture teeth",
    "15": "Permanent Teeth",
    "16": "Supra Eruption",
    "17": "TAD",
    "18": "abutment",
    "19": "attrition",
    "20": "bone defect",
    "21": "gingival former",
    "22": "metal band",
    "23": "orthodontic brackets",
    "24": "permanent retainer",
    "25": "post - core",
    "26": "plating",
    "27": "wire",
    "28": "Cyst",
    "29": "Root resorption",
    "30": "Primary teeth"
}
```

## Prerequisites

- Python 3.6 or later
- Azure account
- Azure CLI
- Git

## Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/IshuSinghSE/flask_azure_demo.git
    cd flask_azure_demo
    ```

2. **Create a virtual environment and install dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. **Run the Flask app locally:**
    ```bash
    flask run
    ```

## Deploying to Azure

1. **Login to Azure:**
    ```bash
    az login
    ```

2. **Create an Azure App Service plan:**
    ```bash
    az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku FREE
    ```

3. **Create a web app:**
    ```bash
    az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myFlaskApp --runtime "PYTHON|3.8"
    ```

4. **Deploy the app:**
    ```bash
    az webapp up --name myFlaskApp --resource-group myResourceGroup
    ```

## References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Azure App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
