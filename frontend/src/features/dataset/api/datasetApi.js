import { agent } from "../../../lib/api/agent";

export const datasetApi = {
  getClasses: async () => {
    const response = await agent.get("/dataset/classes");
    return response.data;
  },
  getSummary: async () => {
    const response = await agent.get("/dataset/summary");
    return response.data;
  },
  getValidation: async () => {
    const response = await agent.get("/dataset/validation");
    return response.data;
  },
  refreshCache: async () => {
    const response = await agent.post("/dataset/refresh");
    return response.data;
  },
  getImages: async ({ split, classLabel, page = 1, perPage = 30 }) => {
    const response = await agent.get("/dataset/images", {
      params: { split, class_label: classLabel, page, per_page: perPage },
    });
    return response.data;
  },
};
