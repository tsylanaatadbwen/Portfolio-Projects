## Overview

An automation workflow that fetches the latest tech videos from Marques Brownlee’s YouTube channel, extracts their transcripts, and analyzes them using OpenAI.
The system summarizes each video, scores its ROI (value-for-money relevance), and explains how it aligns with user interests — all sent automatically via email.

### Key Features

- YouTube Data Fetching: Retrieves the newest video using the YouTube Data API.

- Transcript Extraction: Gets video transcripts through a third-party API.

- AI Analysis: Generates a summary, ROI score, and relevance explanation using OpenAI’s chat model.

- Duplicate Filtering: Prevents reprocessing existing videos with Datatable logic.

- Automated Email Delivery: Sends structured insights to a specified Gmail account.

#### Tech Stack

- n8n – Workflow automation

- YouTube Data API – Video data retrieval

- OpenAI API – Transcript summarization and analysis

- Datatable Node – Storage and duplicate checks

- Gmail API – Automated email reports
