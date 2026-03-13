"""
CrewAI配置模块

该模块负责配置CrewAI的核心功能，包括创建代理、任务和团队。
"""

from crewai import Agent, Task, Crew, Process
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.outputs import LLMResult
import ollama
import os

# 从环境变量获取模型配置
DEFAULT_MODEL_NAME = os.getenv('DEFAULT_MODEL_NAME', 'llama2:latest')


class OllamaLLM(LLM):
    """
    自定义Ollama LLM类，直接使用ollama Python客户端
    """
    model: str = DEFAULT_MODEL_NAME
    
    def _call(
        self,
        prompt: str,
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs
    ) -> str:
        """
        调用Ollama模型
        
        Args:
            prompt: 提示文本
            stop: 停止词列表
            run_manager: 回调管理器
            **kwargs: 其他参数
            
        Returns:
            模型生成的文本
        """
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            stop=stop,
            **kwargs
        )
        return response['response']
    
    @property
    def _identifying_params(self) -> dict:
        """
        获取标识参数
        
        Returns:
            标识参数字典
        """
        return {"model": self.model}
    
    @property
    def _llm_type(self) -> str:
        """
        获取LLM类型
        
        Returns:
            LLM类型
        """
        return "ollama"


def get_ollama_llm(model_name=DEFAULT_MODEL_NAME):
    """
    获取Ollama LLM实例
    
    Args:
        model_name: 模型名称
        
    Returns:
        LLM实例
    """
    # 使用自定义的Ollama LLM
    return OllamaLLM(model=model_name)


def create_research_agent():
    """
    创建研究代理
    
    Returns:
        研究代理实例
    """
    return Agent(
        role="研究分析师",
        goal="深入研究用户提出的问题，提供全面、准确的信息",
        backstory="你是一位专业的研究分析师，擅长收集、分析和整理信息，能够快速理解复杂问题并提供有见地的分析。",
        llm=get_ollama_llm(),
        verbose=True
    )


def create_writer_agent():
    """
    创建写作代理
    
    Returns:
        写作代理实例
    """
    return Agent(
        role="专业作家",
        goal="将研究结果转化为清晰、结构化、易于理解的内容",
        backstory="你是一位经验丰富的专业作家，擅长将复杂的信息转化为简洁明了的文字，能够制作出高质量的报告和文章。",
        llm=get_ollama_llm(),
        verbose=True
    )


def create_editor_agent():
    """
    创建编辑代理
    
    Returns:
        编辑代理实例
    """
    return Agent(
        role="内容编辑",
        goal="检查内容的准确性、一致性和流畅性，确保最终输出质量",
        backstory="你是一位专业的内容编辑，具有敏锐的眼光和丰富的编辑经验，能够发现并纠正内容中的错误和不足之处。",
        llm=get_ollama_llm(),
        verbose=True
    )


def create_research_task(agent, topic):
    """
    创建研究任务
    
    Args:
        agent: 执行任务的代理
        topic: 研究主题
        
    Returns:
        任务实例
    """
    return Task(
        description=f"深入研究关于 '{topic}' 的信息，收集相关数据和事实，分析不同角度的观点",
        expected_output="一份详细的研究报告，包含关键信息、数据支持和分析结论",
        agent=agent
    )


def create_writing_task(agent, research_output):
    """
    创建写作任务
    
    Args:
        agent: 执行任务的代理
        research_output: 研究结果
        
    Returns:
        任务实例
    """
    return Task(
        description=f"基于研究结果撰写一份结构清晰、内容丰富的文章，确保信息准确且易于理解",
        expected_output="一篇高质量的文章，包含引言、主体内容和结论",
        agent=agent,
        context=[research_output]
    )


def create_editing_task(agent, writing_output):
    """
    创建编辑任务
    
    Args:
        agent: 执行任务的代理
        writing_output: 写作结果
        
    Returns:
        任务实例
    """
    return Task(
        description=f"检查并编辑文章，确保内容准确、逻辑连贯、语言流畅",
        expected_output="一份经过编辑和优化的最终版本",
        agent=agent,
        context=[writing_output]
    )


def create_crew(topic):
    """
    创建AI代理团队
    
    Args:
        topic: 研究和写作主题
        
    Returns:
        团队实例
    """
    # 创建代理
    research_agent = create_research_agent()
    writer_agent = create_writer_agent()
    editor_agent = create_editor_agent()
    
    # 创建任务
    research_task = create_research_task(research_agent, topic)
    writing_task = create_writing_task(writer_agent, research_task)
    editing_task = create_editing_task(editor_agent, writing_task)
    
    # 创建团队
    crew = Crew(
        agents=[research_agent, writer_agent, editor_agent],
        tasks=[research_task, writing_task, editing_task],
        process=Process.sequential,
        verbose=True
    )
    
    return crew
