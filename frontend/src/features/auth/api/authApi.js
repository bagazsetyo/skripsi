import { agent } from "../../../lib/api/agent";

export const authApi = {
  login: async (payload) => {
    const response = await agent.post("/auth/login", payload);
    return response.data;
  },
  me: async () => {
    const response = await agent.get("/auth/me");
    return response.data;
  },
};
