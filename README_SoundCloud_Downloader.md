
# SoundCloud Downloader

## Project Description

The **SoundCloud Downloader** is a web application that allows users to download audio tracks from SoundCloud by simply entering the track's URL. The application is built using Python's FastAPI framework for the backend, and the frontend is designed with a simple HTML/CSS layout. This project is containerized using Docker, making it easy to deploy and run on any environment that supports Docker.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Docker Deployment](#docker-deployment)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- Download SoundCloud audio tracks directly by entering the URL.
- Responsive and user-friendly interface.
- Supports multiple audio formats.
- Backend built with FastAPI, providing a fast and scalable API.
- Containerized with Docker for easy deployment.

## Installation

### Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Clone the Repository

```bash
git clone https://github.com/amrmarey/scdl.git
cd scdl
```

### Install Dependencies

If you prefer running the project locally without Docker, you can install the necessary Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running Locally

To run the project locally:

1. Start the FastAPI server:

    ```bash
    uvicorn server:app --reload
    ```

2. Open `index.html` in your browser to access the downloader interface.

### Docker Deployment

To deploy the project using Docker:

1. Build and run the Docker container:

    ```bash
    docker-compose up --build
    ```

2. Access the application in your web browser at `http://localhost:8000`.

### Accessing the Web Interface

1. Enter the SoundCloud URL of the track you wish to download.
2. Click the **Download** button.
3. The application will process the URL and download the track to your device.

## API Endpoints

The following API endpoints are available:

- `GET /download`: Downloads a SoundCloud track. Requires a `url` query parameter with the SoundCloud track URL.

Example usage:

```bash
curl -X GET "http://localhost:8000/download?url=https://soundcloud.com/artistname/trackname"
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any features, enhancements, or bugs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
