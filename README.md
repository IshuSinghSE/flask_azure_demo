# Flask Azure Deployment Demo

This repository contains a demo Flask application with instructions on how to deploy it on Azure.

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
