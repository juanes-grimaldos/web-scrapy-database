# Web Scraping Project for Exito, Falabella, Alkosto, and Sodimac

## Summary

This project automates the process of web scraping product data from major e-commerce platforms Exito, Falabella, Alkosto, and Sodimac using Selenium and stores the scraped data in a PostgreSQL database. The project is developed in Python and aims to streamline data collection for market analysis and research.

## Table of Contents

- [Summary](#summary)
- [Project Overview](#project-overview)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Virtual Environment](#virtual-environment)
  - [Installing Dependencies](#installing-dependencies)
- [Usage](#usage)
  - [Running the Scripts](#running-the-scripts)
  - [Execution Time](#execution-time)
- [Technical Details](#technical-details)
  - [Browser Compatibility](#browser-compatibility)
  - [Expected Output](#expected-output)
- [Viewing the Dashboard](#viewing-the-dashboard)


## Project Overview

This project involves developing a PostgreSQL database by web scraping product data from the following e-commerce websites:
- **Exito**
- **Falabella**
- **Alkosto**
- **Sodimac**

The data is collected using Selenium for automation and then processed and stored in a PostgreSQL database. This facilitates market analysis and data-driven decision-making.

## Setup and Installation

### Prerequisites

- Python 3.x
- PostgreSQL
- Google Chrome or Mozilla Firefox

### Virtual Environment

It's recommended to use a virtual environment to manage dependencies. You can create and activate a virtual environment as follows:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment (Windows)
.\venv\Scripts\activate

# Activate the virtual environment (macOS/Linux)
source venv/bin/activate
```


### Installing Dependencies

Install the required packages using the requirements.txt file:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Scripts

You can run the scraping scripts using either Chrome or Firefox. Ensure that the appropriate WebDriver (e.g., chromedriver or geckodriver) is installed and added to your PATH.

Example command to run a script:

```bash
python scrape_exito.py
```

### Execution Time

  Full run: The script may take between 15 minutes to 1 hour to complete.


  Quick run: Scraping about 50 links per store/script takes approximately 5 to 10 minutes.


## Technical Details
### Browser Compatibility

The scraping scripts are compatible with both Google Chrome and Mozilla Firefox. Make sure you have the corresponding WebDriver:

    Chrome: Download Chromedriver
    Firefox: Download Geckodriver

### Expected Output

The scripts will scrape product details such as:

    Product name
    Price
    Availability
    Ratings (if available)
    Product URL

The data is then saved into the PostgreSQL database configured in your setup.
## Viewing the Dashboard

To view the interactive project dashboard:

You can view the interactive dashboard [here](https://app.powerbi.com/view?r=eyJrIjoiNjNhYTBhOTktMDE0YS00Yzg3LTg1ZDctN2JkZjIxNzJiYmE4IiwidCI6ImQ2NDZkM2E4LTdiMTUtNGI1My05ZDkyLTk4MTVmZDYyNzAyYyIsImMiOjR9).

![Dashboard Preview](https://app.powerbi.com/view?r=eyJrIjoiNjNhYTBhOTktMDE0YS00Yzg3LTg1ZDctN2JkZjIxNzJiYmE4IiwidCI6ImQ2NDZkM2E4LTdiMTUtNGI1My05ZDkyLTk4MTVmZDYyNzAyYyIsImMiOjR9)
    
