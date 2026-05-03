import { agent } from "../../../lib/api/agent";

export const dashboardApi = {
  getDatasetSummary: async () => {
    const response = await agent.get("/dataset/summary");
    return response.data;
  },
  getModels: async () => {
    const response = await agent.get("/models");
    return response.data;
  },
  getTrainingRuns: async () => {
    const response = await agent.get("/training/runs");
    return response.data;
  },
  getActiveModel: async () => {
    const response = await agent.get("/models/active");
    return response.data;
  },
};
