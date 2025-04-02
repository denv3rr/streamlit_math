# Streamlit Math

[seperet.com](https://seperet.com)

An interactive web application for exploring Pre-calculus and Calculus concepts.

Using: Streamlit, SymPy, NumPy, and Plotly.

## Features

- Interactive Unit Circle
- Trigonometric Function Graphing
- Trigonometric Identity Exploration & Verification
- Triangle Solver (SSS, SAS, ASA, AAS) with Visualization
- Geometric Application Solver (Bearings, Elevation/Depression) with Visualization
- Function Plotting & Analysis
- Logarithmic & Exponential Tools
- Limit & Derivative Calculation
- Integration (Definite & Indefinite)
- Sequence & Series Exploration (Basic)
- General Expression Simplifier & Equality Checker

## Setup

1.  **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate

    # On Windows use:
    venv\Scripts\activate
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

The streamlit application should open in your default web browser.

## Project Structure

- `app.py`: Main Streamlit application entry point.
- `requirements.txt`: Python package dependencies.
- `README.md`: This file.
- `pages/`: Contains the Python scripts for each page/section of the app. Streamlit automatically creates navigation from files in this directory.
- `utils/`: Helper modules for mathematical logic, plotting, and parsing.
- `assets/`: Optional directory for static files like CSS.
