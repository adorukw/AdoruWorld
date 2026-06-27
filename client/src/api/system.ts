import { request } from "@/utils";
export const systemApi = {
  systemInfo: () => request<any>("/system/info"),
};
