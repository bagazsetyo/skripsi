import { agent } from "../../../lib/api/agent";

export const trainingApi = {
  getConfig: async () => {
    const response = await agent.get("/training/config");
    return response.data;
  },
  getRuns: async () => {
    const response = await agent.get("/training/runs");
    return response.data;
  },
  createRun: async (payload) => {
    const response = await agent.post("/training/runs", payload);
    return response.data;
  },
  getModels: async () => {
    const response = await agent.get("/models");
    return response.data;
  },
  getActiveModel: async () => {
    const response = await agent.get("/models/active");
    return response.data;
  },
  activateModel: async (modelId) => {
    const response = await agent.post(`/models/${modelId}/activate`);
    return response.data;
  },
};
