const axios = require("axios");

exports.handleChat = async (req, res) => {
  try {
    const { question, sessionId } = req.body;

    const response = await axios({
      method: "post",
      url: "http://127.0.0.1:8000/ask-stream",
      data: {
        question,
        session_id: sessionId || "user1",
      },
      responseType: "stream",
    });

    res.setHeader("Content-Type", "text/plain");

    response.data.on("data", (chunk) => {
      res.write(chunk.toString());
    });

    response.data.on("end", () => {
      res.end();
    });

  } catch (error) {
    console.error(error.message);
    res.status(500).send("Error");
  }
};