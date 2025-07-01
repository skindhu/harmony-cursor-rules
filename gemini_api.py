import os
from dotenv import load_dotenv
from google import genai  # 使用新的导入方式
from google.genai import types

class GeminiAPI:
    """Google Gemini API封装，使用Google Gen AI SDK"""

    def __init__(self, api_key=None):
        """
        初始化Google Gemini API

        Args:
            api_key (str, optional): API密钥，如果为None则从环境变量中读取
        """
        # 加载环境变量
        load_dotenv()

        # 从环境变量或参数获取API密钥
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("未提供Gemini API密钥，也未在环境变量中找到GEMINI_API_KEY")

        # 默认模型和配置
        self.model_name = "gemini-2.5-flash"
        self.temperature = 0.7  # 默认温度参数

        # 设置API选项并初始化客户端
        self._configure_gemini_api()


    def _configure_gemini_api(self):
        """配置Google Gemini API客户端"""
        # 创建客户端实例
        proxy_url = os.getenv('GEMINI_BASE_URL')
        self.client = genai.Client(api_key=self.api_key, http_options=types.HttpOptions(api_version='v1beta', base_url=proxy_url))

        print(f"已初始化Gemini API客户端，使用模型: {self.model_name}")

    def generate_text(self, prompt):
        """
        使用Gemini API生成文本

        Args:
            prompt (str): 提示词

        Returns:
            str: 生成的文本
        """
        try:
            # 使用新的SDK调用方式
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(temperature= self.temperature)
            )

            # 提取并返回生成的文本
            if hasattr(response, 'text'):
                return response.text
            elif hasattr(response, 'parts'):
                return ''.join([part.text for part in response.parts if hasattr(part, 'text')])
            else:
                raise RuntimeError("API响应格式异常，无法提取生成的文本")

        except Exception as e:
            raise RuntimeError(f"Gemini API调用失败: {str(e)}")