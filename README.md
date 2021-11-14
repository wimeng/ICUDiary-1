# ICUDiary-1

## Introduction
This is a website which designed for users to write or speak messages to their loved ones in the ICU, and for patients to read and hear said messages. The website allows its users to create profiles for themselves, and associate themselves with patients by entering their specific code.

## Prerequisites
In order to properly run our software, you need to have python (>=3.6) and npm (>=8.0.0) installed onto your system. This website works best on Google Chrome, however it will still run on other browsers. This software will run on any modern operating system.

## Steps to run
1. Open up ICUDiary-1 folder in terminal
2. Run the following commands in order:
```bash
python3 -m venv env
```
```bash
source env/bin/activate
```
```bash
pip install -r requirements.txt
```
```bash
pip install -e .
```
```bash
npm ci . 
```
```bash
npx webpack
```
```bash
./bin/ICUDiarydb create
```
```bash
./bin/ICUDiaryrun
```
3. Open up localhost:8000 on your browser

