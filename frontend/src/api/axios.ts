import axios from "axios";
import { getCookie } from "cookies-next";
import { toast } from "react-toastify";

axios.defaults.baseURL = `${process.env.NEXT_PUBLIC_BACKEND_URL}${process.env.NEXT_PUBLIC_API_V1_STR}`;

axios.interceptors.request.use((config) => {
  const authToken = getCookie("token");
  if (authToken) {
    config.headers.Authorization = `Bearer ${authToken}`;
  }
  return config;
});

axios.interceptors.response.use(
  (response) => response,
  (error) => {
    toast.error(error.response.data.detail || "Something going wrong!");
    return Promise.reject(error);
  }
);

export default axios;
