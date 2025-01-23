from mitmproxy import io
from mitmproxy.websocket import WebSocketMessage
import os
import csv


FLOW_FILE = "path/to/input.flow"  # Replace with your .flow file path
OUTPUT_FILE = "path/to/output.csv"  # Replace with your desired output file path

def extract_websocket_messages_to_csv(flow_file, output_file):
    # Check if the .flow file exists
    if not os.path.exists(flow_file):
        print(f"Error: The file {flow_file} does not exist.")
        return

    # Open the .flow file and write the results to the output CSV file
    try:
        with open(flow_file, "rb") as f, open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            reader = io.FlowReader(f)
            writer = csv.writer(csvfile)

            # Write the CSV header
            writer.writerow(["WebSocket URL", "Direction", "Message Content"])

            for flow in reader.stream():
                if hasattr(flow, "websocket") and flow.websocket is not None:
                    url = f"{flow.request.scheme}://{flow.request.host}:{flow.request.port}"
                    for message in flow.websocket.messages:
                        if isinstance(message, WebSocketMessage):
                            direction = "sent" if message.from_client else "received"
                            writer.writerow([url, direction, message.content.decode('utf-8', errors='ignore')])

        print(f"WebSocket messages saved to {output_file}")
    except Exception as e:
        print(f"Error while processing the file: {e}")

if __name__ == "__main__":
    extract_websocket_messages_to_csv(FLOW_FILE, OUTPUT_FILE)
