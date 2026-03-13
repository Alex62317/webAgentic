"""
LangChain配置模块

该模块负责配置LangChain的基础设置，包括模型连接、向量存储等。
"""

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# 从环境变量获取模型配置
DEFAULT_MODEL_NAME = os.getenv('DEFAULT_MODEL_NAME', 'llama2:latest')
DEFAULT_MODEL_API_KEY = os.getenv('DEFAULT_MODEL_API_KEY', 'ollama')
DEFAULT_MODEL_BASE_URL = os.getenv('DEFAULT_MODEL_BASE_URL', 'http://localhost:11434/v1')


def get_ollama_llm(model_name=DEFAULT_MODEL_NAME):
    """
    获取Ollama LLM实例
    
    Args:
        model_name: 模型名称
        
    Returns:
        Ollama LLM实例
    """
    return Ollama(
        model=model_name
    )


def create_chat_chain(model_name=DEFAULT_MODEL_NAME):
    """
    创建聊天链
    
    Args:
        model_name: 模型名称
        
    Returns:
        聊天链实例
    """
    # 创建提示模板
    prompt = ChatPromptTemplate.from_template(
        """
        你是一个智能助手，需要根据用户的问题提供准确、详细的回答。
        
        问题: {question}
        回答:
        """
    )
    
    # 获取LLM实例
    llm = get_ollama_llm(model_name)
    
    # 创建输出解析器
    output_parser = StrOutputParser()
    
    # 构建链
    chain = prompt | llm | output_parser
    
    return chain
