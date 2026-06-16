// export const BASE_API_URL = 'http://localhost:8000/api/v1';
// export const BASE_API_URL = '/adoru-world/api/v1';

// let base_api_url: string;

// if (import.meta.env.NODE_ENV === 'development') {
//     base_api_url = 'http://localhost:8000/api/v1';
// }
// else {
//     base_api_url = '/adoru-world/api/v1';
// }

// export const BASE_API_URL = base_api_url;

export const BASE_API_URL = import.meta.env.DEV
  ? '/api/v1'              // 开发模式 → Vite proxy
  : '/adoru-world/api/v1'; // 生产模式 → nginx