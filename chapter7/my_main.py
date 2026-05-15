# my_main.py
from dotenv import load_dotenv
from my_llm import MyLLM
from stepfun_llm import StepfunLLM

# 加载环境变量
load_dotenv()

# 创建LLM实例（使用StepfunLLM适配器）
llm = StepfunLLM()

# 准备消息
messages = [{"role": "user", "content": "你好，请介绍一下你自己。"}]

# 发起调用，think等方法都已从父类继承，无需重写
response_stream = llm.think(messages)

# 打印响应
print("Stepfun Response:")
for chunk in response_stream:
    # chunk在my_llm库中已经打印过一遍，这里只需要pass即可
    # print(chunk, end="", flush=True)
    pass