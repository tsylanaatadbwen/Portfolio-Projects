# Automated Meta Lead Acquisition & WhatsApp CRM Pipeline
<img width="2752" height="1536" alt="ss1_lead_pipeline" src="https://github.com/user-attachments/assets/78981860-d2a4-41d6-a300-7ec129a1640c" />

A 24/7 lead capture and automated messaging system that connects Meta Lead Ads to Google Sheets and the WhatsApp Business Cloud API. Built with Python and FastAPI, this system standardizes incoming parent inquiries in real time, logs them into a central CRM spreadsheet, sends a welcome message to applicants, and dispatches actionable alerts to campus staff with a 1-tap follow-up link.

> **Note on Codebase Availability:**  
> The full source code for this project is maintained in a private repository as it contains proprietary business logic, client configurations, and production API integrations currently running live for a commercial education client. This repository documents the system architecture, integration workflows, technical challenges, and verified production execution.

---

## Live System Screenshots

| Google Sheets CRM Ingestion | Instant WhatsApp Admin Alert | Cloud Infrastructure Uptime |
| :---: | :---: | :---: |
| <img width="1917" height="877" alt="ss2_googlesheets" src="https://github.com/user-attachments/assets/84e6176e-0389-4fc3-9468-e2dad34f32b1" /> | <img width="425" height="450" alt="ss3_whatsapp_alert" src="https://github.com/user-attachments/assets/0145406a-3ee0-40f8-b047-26f50184aa13" /> | <img width="1896" height="782" alt="ss4_railway" src="https://github.com/user-attachments/assets/98d5823f-be2e-4357-881d-199fcfc8ffd4" />


---

## System Architecture & Data Flow

```text
[ Parent Submits Meta Lead Form ]
               │
               ▼
   [ FastAPI Webhook on Railway ]
               │
               ├──> Data Cleaning (Slug removal & phone formatting)
               │
               ├──> 1. Log Lead to Google Sheets CRM (gspread API)
               ├──> 2. Send Auto-Welcome Message to Parent (WhatsApp API)
               └──> 3. Dispatch Instant Alert to Principal (WhatsApp API)
                           └──> Includes 1-Tap wa.me Pre-Filled Chat Link
```

## Key Features & Capabilities

Real-Time Webhook Engine: Hosted on Railway for 24/7 cloud reliability without depending on local machines.

Automated Data Cleaning: Custom string cleaning converts raw dropdown API slugs (e.g., primary_school_(1-5)) into clean report text (Primary School (1-5)) and standardizes local phone inputs to 03XX-XXXXXXX format.

1-Tap Parent Follow-up (/chat Endpoint): Includes a custom HTTP redirect endpoint that bypasses Meta link restrictions, allowing school staff to open pre-filled WhatsApp chats directly from their alerts.

Structured CRM Sync: Pushes incoming lead details directly into Google Sheets using gspread with fixed schemas for instant reporting.

Zero-Downtime Authorization: Configured using Meta Admin System User tokens and Lead Access Manager permissions to eliminate 60-day token expiration limits.

## Tech Stack & APIs

Backend Framework: Python 3, FastAPI, Uvicorn

Cloud Hosting: Railway.app

Lead Generation: Meta Graph API, Meta Lead Ads Form v5

Messaging Tier: Meta WhatsApp Business Cloud API

CRM Storage: Google Sheets API (gspread, oauth2client)

## Key Technical Problems Solved

1. Meta CTA Link Restriction Bypass

Meta rejects standard wa.me chat links inside certain CTA buttons and message templates. To work around this, a custom /chat HTTP GET endpoint was added to the FastAPI server. Tapping the link issues an instant 307 redirect straight to https://wa.me/... with pre-filled text, maintaining compliance with Meta's web rules while keeping follow-ups 1-tap for staff.

2. WhatsApp 24-Hour Messaging Window Failover

Standard freeform text API messages are blocked by Meta if the user has not messaged the business in the last 24 hours. To guarantee delivery, the notification script defaults to an approved Utility Template (admin_lead_notification), completely bypassing the 24-hour interaction rule so staff receive alerts around the clock.
Operational Alert Format

When a new lead arrives, the school principal receives this alert on WhatsApp:

🚨 New Admission Inquiry Received!

👤 Name: [Parent Name]
📞 Phone: 0333-XXXXXXX
🏫 Grade: Kindergarten
📍 Area: PECHS / Tariq Road

💬 Click to open chat:
[https://your-domain.up.railway.app/chat?phone=92333XXXXXXX](https://your-domain.up.railway.app/chat?phone=92333XXXXXXX)

