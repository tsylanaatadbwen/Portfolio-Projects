Steps

1. Created a Datatable inside n8n to serve as the project’s internal database.

2. Added a Scheduled Trigger node to run the workflow automatically at set intervals.

3. Configured an HTTP Request Node connected to the YouTube API to fetch the latest video data.

4. Added a Code Node to extract and structure the specific variables needed (e.g., video URL, title, channel name, etc.).

5. Inserted a Limit Node to reduce the results from 10 items to 1 (fetching only the latest video).

6. Used a Set Node to align the variables with the Datatable’s column names for consistency.

7. Added a Datatable Node to filter duplicate URLs, ensuring no video is processed twice (with “Always Output Data” enabled).

8. Inserted an IF Node to check whether new data exists (branching logic based on empty/non-empty results).

9. Added Another Datatable Node to insert the new video’s metadata (excluding the transcript for now).

10. Used a Third-Party API to retrieve YouTube video transcripts via HTTP request.

11. Configured a GET HTTP Request Node to fetch the transcript using cURL or a public transcript API.

12. Inserted a Datatable Node again to store the transcript data into the database.

13. Integrated Root Cause GPT to perform a 5 Whys Analysis on the video transcript for deeper insight.

14. Added an AI Agent Node, providing full context and instructions through its system memory.

15. Defined a Structured Output Parser to ensure the AI response aligns with the desired output format.

16. Connected an OpenAI Chat Model as the main LLM to power the agent’s reasoning.

17. Added a Gmail Node to send the AI agent’s summary or insights to a specific email via API.