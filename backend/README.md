# Flask Backend for Christian Advice App

This is the Flask backend for the Christian Advice App, which handles the integration with the ChatGPT API and applies a filter to provide Christian audience-specific advice.

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [Built With](#built-with)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Getting Started

These instructions will help you set up and run the Flask backend on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
git clone https://github.com/yourusername/christian-advice-app-backend.git
2. Change directory to the cloned repository:
cd christian-advice-app-backend
3. Create a virtual environment:
python -m venv venv
4. Activate the virtual environment:
- Windows:
.\venv\Scripts\activate
- macOS/Linux:
source venv/bin/activate
5. Install the required packages:
pip install -r requirements.txt

### Configuration

To configure the backend, create a `.env` file in the root directory of the project and add the following environment variables:

FLASK_APP=app.py
FLASK_ENV=development
CHATGPT_API_KEY=your_api_key_here

Replace `your_api_key_here` with your ChatGPT API key.

### Running the Application

To run the Flask backend in development mode, execute the following command:

flask run

The application should be accessible at http://localhost:5000.

### Running Tests

To run tests, execute the following command:

pytest

### Deployment

For deploying the Flask backend to a production environment, follow the [official Flask deployment documentation](https://flask.palletsprojects.com/en/2.1.x/deploying/index.html).

## Built With

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [OpenAI's ChatGPT](https://beta.openai.com/docs/api-reference/chat/create) - API for generating advice

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- [OpenAI](https://www.openai.com/) for providing the ChatGPT API
