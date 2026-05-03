import { agent } from "../../../lib/api/agent";

export const predictionApi = {
  getActiveModel: async () => {
    const response = await agent.get("/models/active");
    return response.data;
  },
  predictImage: async ({ file, scoreThreshold }) => {
    const formData = new FormData();
    formData.append("file", file);
    const response = await agent.post("/predict", formData, {
      params: { score_threshold: scoreThreshold },
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  },
};
