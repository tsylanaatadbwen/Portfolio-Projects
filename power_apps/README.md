# Microsoft Teams Document Tracker

![Automated Teams Document Tracking System](<Automated Teams Document Tracking System.png>)

## Overview
This project automates how file uploads are tracked in Microsoft Teams. Instead of manually copying file names and links into a spreadsheet, an automated workflow logs every document dropped into Teams, records who sent it and when, and displays the activity on a live Power BI dashboard.

## How It Works
1. **File Uploaded:** A user uploads a document into a Microsoft Teams chat.
2. **Automatic Capture:** Power Automate picks up the new file, checks for duplicates, and pulls the uploader details.
3. **Excel Storage:** The file name, uploader, date, and direct file link are saved into a central Excel sheet.
4. **Power BI Reporting:** Power BI reads the Excel sheet and updates the dashboard visual on a set schedule.

## Key Features
* **Zero Manual Data Entry:** Eliminates the need to manually track incoming documents.
* **Duplicate Prevention:** Skips files that were already recorded so the log stays clean.
* **Direct File Links:** Clickable links inside the report allow users to open the uploaded file directly.
* **Scheduled Data Refresh:** Uses a Power BI Gateway to keep the cloud report updated without manual refreshes.

## Tools Used
* **Microsoft Teams:** Intake point for documents
* **Power Automate:** Workflow and automation logic
* **Microsoft Excel:** Central table for storing document logs
* **Power BI Desktop & Service:** Visual dashboard and reporting
* **Power BI Gateway (Personal Mode):** Automated cloud data refreshes
