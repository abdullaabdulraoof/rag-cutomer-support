

const axios = require("axios");

exports.handleChat = async (req, res) => {
  try {
    const { question } = req.body;

    if (!question) {
      return res.status(400).json({ error: "Question is required" });
    }

    // Call FastAPI RAG
    const response = await axios.post("http://127.0.0.1:8000/ask", {
      question: question
    });

    // Return response
    res.json({
      success: true,
      data: response.data
    });

  } catch (error) {
    console.error("Error:", error.message);

    res.status(500).json({
      success: false,
      error: "Something went wrong"
    });
  }
};