# EPAM homework: Microservices exchange rates from API
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-blue.svg)](https://www.python.org) [![made-with-flask](https://img.shields.io/badge/Made%20with-Flask-white.svg)](https://flask.palletsprojects.com/en/1.1.x/) [![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/ab24db?icon=github)](https://github.com/xistadi/homework/edit/main/PythonMicroservicesApp) [![saythanks](https://img.shields.io/badge/say-thanks-ff69b4.svg)](https://www.donationalerts.com/c/xistadi)


## About
Microservices app using Docker / docker-compose
- Reaper (service 1): scrapes exchange rates from API [nbrb.by](https://www.nbrb.by), parses data, stores date using Keeper, provides API to Master to start scraping
- Keeper (service 2): manages DB that stores date provided by Reaper, provides interface for Master in order to retrieve data
- Master (service 3): gets data from Keeper, provides API to get the data, forces Reaper to run web scrapper

![gif](https://github.com/xistadi/homework/blob/main/PythonMicroservicesApp/images/start.gif)

## How to start

1. Clone project from github
    ```
    git clone https://github.com/xistadi/homework
    ```
2. Go to `PythonMicroservicesApp`
    ```bash
    cd PythonMicroservicesApp
    ```
3. Run docker-compose
    ```bash
    docker-compose up
    ```
4. Open your web browser http://localhost:3100

## Useful links

- [Docker Documentation](https://docs.docker.com)
- [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/)
- [SOLID](https://gist.github.com/pavel-loginov-dev/8f3ef63e265c15763d169eff4627265d)
- [Design patterns in test automation](https://habr.com/ru/company/jugru/blog/338836/)
- [Refactoring guru](https://refactoring.guru)
