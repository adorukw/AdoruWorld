规范做法如下：
    ```markdown
    方案一：后端返回完整 URL                                                                                                                                             
                                                                                                                                                                        
    思路： 后端在返回 coverImage 时，加上部署的子路径前缀 /blog。                                                                                                        
                                                                                                                                                                        
    ### 后端改法                                                                                                                                                         
                                                                                                                                                                        
    在 server/app/config.py 里加一个配置：                                                                                                                               
                                                                                                                                                                        
    ```python                                                                                                                                                            
    # 部署的子路径，如果是裸域名就是空字符串，如果在 /blog/ 下就是 /blog                                                                                               
    DEPLOY_SUB_PATH: str = os.getenv("DEPLOY_SUB_PATH", "/blog")                                                                                                       
    ```                                                                                                                                                                  
                                                                                                                                                                        
    然后在 main.py 里找一个公共的地方（比如写个工具函数）：                                                                                                              
                                                                                                                                                                        
    ```python                                                                                                                                                            
    from app.config import DEPLOY_SUB_PATH                                                                                                                             
                                                                                                                                                                        
    def asset_url(path: str) -> str:                                                                                                                                   
        """给资源路径加上部署子路径前缀"""                                                                                                                             
        if path and path.startswith("/"):                                                                                                                              
            return f"{DEPLOY_SUB_PATH}{path}"                                                                                                                          
        return path                                                                                                                                                    
    ```                                                                                                                                                                  
                                                                                                                                                                        
    然后在每个返回 coverImage 的 API 路由里，返回之前套一层 asset_url()。或者更干净的做法——写个 Pydantic 的字段验证器：                                                  
                                                                                                                                                                        
    ```python                                                                                                                                                            
    from pydantic import field_validator                                                                                                                               
                                                                                                                                                                        
    class PostResponse(BaseModel):                                                                                                                                     
        # ... 其他字段                                                                                                                                                 
        cover_image: str | None = None                                                                                                                                 
                                                                                                                                                                        
        @field_validator('coverImage')                                                                                                                                 
        @classmethod                                                                                                                                                   
        def add_prefix(cls, v):                                                                                                                                        
            if v and v.startswith('/'):                                                                                                                                
                return f"/blog{v}"                                                                                                                                     
            return v                                                                                                                                                   
    ```                                                                                                                                                                  
                                                                                                                                                                        
    这样每次返回的 coverImage 都是 /blog/uploads/... 格式，前端拿来直接用。                                                                                              
                                                                                                                                                                        
    优点： 前端什么都不用改                                                                                                                                              
    缺点： 部署环境变了（子路径变了或变成裸域名）还得改配置或加判断                                                                                                      
                                                                                                                                                                        
    ────────────────────────────────────────────────────────────────────────────────                                                                                     
                                                                                                                                                                        
    方案二：前端统一处理（咱推荐的）                                                                                                                                     
                                                                                                                                                                        
    在 src/utils/index.ts 里加一个通用函数：                                                                                                                             
                                                                                                                                                                        
    ```ts                                                                                                                                                                
    import { BASE_API_URL } from '@/config'                                                                                                                            
                                                                                                                                                                        
    // 把资源路径转成完整 URL                                                                                                                                          
    export function assetUrl(path?: string): string {                                                                                                                  
        if (!path) return ''                                                                                                                                             
        if (path.startsWith('http://') || path.startsWith('https://')) return path  // 已经是完整 URL                                                                    
        // 从 BASE_API_URL 里提取部署路径前缀                                                                                                                            
        // BASE_API_URL = '/blog/api/v1' → 前缀就是 /blog                                                                                                                
        const prefix = BASE_API_URL.replace('/api/v1', '')                                                                                                               
        return `${prefix}${path}`                                                                                                                                        
    }                                                                                                                                                                  
    ```                                                                                                                                                                  
                                                                                                                                                                        
    然后在组件里：                                                                                                                                                       
                                                                                                                                                                        
    ```vue                                                                                                                                                               
    <img :src="assetUrl(coverImage)" />                                                                                                                                
    ```                                                                                                                                                                  
                                                                                                                                                                        
    优点： BASE_API_URL 改了就自动适配，前后端路径是一致的                                                                                                               
    缺点： 每个 <img> 的地方都要手动套一下   
    ```