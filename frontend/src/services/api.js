import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

export const indexCode = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post("/index", formData);

  return response.data;
};

export const askCode = async (question, topK = 5) => {
  const response = await api.post("/ask", {
    question,
    top_k: topK,
  });

  return response.data;
};

export const debugCode = async (question, topK = 5) => {
  const response = await api.post("/debug", {
    question,
    top_k: topK,
  });

  return response.data;
};

export const analyzeCode = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post("/analyze", formData);

  return response.data;
};