export default function handler(req, res) {
    const { address, time } = req.query;
  
    // Mock prediction logic, in reality, you would fetch from MongoDB and apply ARIMAX
    const mockPrediction = Math.floor(Math.random() * 100);
  
    res.status(200).json({ prediction: mockPrediction });
  }
  