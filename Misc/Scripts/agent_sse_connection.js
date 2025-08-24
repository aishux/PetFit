const apiUrl = "http://127.0.0.1:8000/run_sse";

// Example request data, replace with your own payload if needed
const data = {
  "appName": "petfit_agent",
  "userId": "user122323343",
  "sessionId": "session3241234124",
  "newMessage": {
    "parts": [
      {
        "text": "My pet dog (id: DOG12345) seems to have dark circles under his eyes and also looks he is breathing heavily, I'm concerned, can you please tell me how is he?"
      }
    ],
    "role": "user"
  },
  "streaming": true
}


fetch(apiUrl, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Accept": "text/event-stream"
  },
  body: JSON.stringify(data)
}).then(response => {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  function read() {
    reader.read().then(({done, value}) => {
      if (done) {
        console.log("Stream ended.");
        return;
      }
      buffer += decoder.decode(value, { stream: true });
      // Extract SSE event lines
      const lines = buffer.split(/\r?\n/).filter(line => line.startsWith("data:"));
      lines.forEach(line => {
        // Remove "data:" prefix and parse JSON
        const json = line.replace(/^data:\s*/, "");
        try {
          const parsed = JSON.parse(json);
          console.log(parsed);
        } catch (e) {
          // Ignore incomplete JSON chunks
        }
      });
      buffer = "";
      read();
    });
  }

  read();
}).catch(err => {
  console.error("Error:", err);
});
