# YourEyes-API

YourEyes-API is the server-side component for processing live video streams received from clients. This repository handles video streams using advanced computer vision techniques to detect and analyze objects in real-time. It leverages gRPC for communication and integrates with the YOLO (You Only Look Once) model for efficient object detection.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

The YourEyes-API serves as a backend for real-time video analysis. It receives video frames from various clients, processes them to detect and analyze objects using the YOLO model, and provides insights back to the client. This is particularly useful for applications requiring real-time object detection and analysis, such as surveillance systems, autonomous vehicles, and augmented reality.

## Features

- **Real-time Video Processing**: Efficiently handles streaming video frames for real-time analysis.
- **Object Detection**: Uses the YOLO model to detect and classify objects within the video frames.
- **Flexible Deployment**: Containerized using Docker for easy deployment and integration with CI/CD pipelines.
- **gRPC Communication**: Utilizes gRPC for high-performance and scalable client-server communication.
- **Extensible**: Designed to be easily extended with additional features or support for other models and services.
# Task List

This document lists tasks and features we plan to work on in the future. Community contributions are welcome! If you're interested in any task, please comment on the relevant issue or create a new one.

## High Priority

- [ ] **Support for multiple video formats**: Extend support for additional video formats beyond YUV420.
- [ ] **Implement video frame caching**: Add a mechanism to cache video frames for better performance.
- [ ] **Fix Docker containerization**: Resolve the issues with containerizing the application using Docker.

## Medium Priority

- [ ] **Integrate Word2Vec for semantic matching**: Enhance the function that processes user questions to use Word2Vec for better semantic matching. This will allow the system to understand and map synonyms or related terms (e.g., mapping "television" to "tvmonitor").
- [ ] **Add unit tests for gRPC services**: Enhance test coverage by adding unit tests for the `StreamVideo` and `SetupDetection` services.
- [ ] **Improve error handling**: Refactor the codebase to provide more robust error handling and logging.

## Low Priority

- [ ] **Enhance documentation**: Add more detailed documentation for developers and users.
- [ ] **Create examples for different clients**: Provide sample code for clients written in different languages (e.g., Python, JavaScript, Go).

## Future Features

- [ ] **Web-based admin dashboard**: Develop a web interface for managing and monitoring the video processing.

---

If you want to pick up a task, please comment on the relevant issue or create a new one. We look forward to your contributions!

## Architecture

The system architecture includes the following key components:

1. **gRPC Server**: Manages the communication with clients and streams video frames to the processing pipeline.
2. **YOLO Model Integration**: Processes frames using the YOLO model to detect and classify objects.
3. **Configuration Service**: Allows dynamic setup of detection criteria based on user input.
4. **Shared Storage**: Stores configuration and session data for ongoing video processing sessions.


## Prerequisites

Before setting up the YourEyes-API, ensure you have the following installed:

- **Python 3.8+**: The core processing is implemented in Python.
- **Docker**: For containerizing the application.
- **gRPC**: Required for communication between client and server.
- **OpenCV**: For image and video processing tasks.
- **Ultralytics YOLO**: YOLO model for object detection.

## Installation

To set up the YourEyes-API locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Your-Eyes-Project/YourEyes-API.git
   cd YourEyes-API
2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. **Install Dependencies** 
    ```bash
    pip install -r requirements.txt
4. **Build and Run with Docker (if using Docker)**
    ```bash
    docker build -t youreyes-api .
    docker run -p 5270:5270 youreyes-api
## Usage

### Run the Server

If not using Docker, start the server with (from root directory):

    python -m app.main

### Test The Server
Use a gRPC client to send video frames to the server. Refer to the API documentation for the expected request format.

### Send Video Frames
Implement a client (e.g., using Python or another language that supports gRPC) to send video frames for processing.

## Contributing

We welcome contributions to the YourEyes-API! Here’s how you can get involved:

1. **Fork the Repository**: Create a fork of this repository on GitHub.
2. **Create a Feature Branch**: Develop your feature or bug fix on a new branch.
3. **Submit a Pull Request**: Open a pull request with a detailed description of your changes.

Please read our [Contributing Guidelines](CONTRIBUTING.md) before making any contributions. <!-- Create and link to your contributing guidelines -->

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions, feedback, or support, please contact us at:

- **Email**: [Link](mailto:issa.albawwab.yes@gmail.com)
- **GitHub Issues**: [YourEyes-API Issues](https://github.com/Your-Eyes-Project/YourEyes-API/issues)
