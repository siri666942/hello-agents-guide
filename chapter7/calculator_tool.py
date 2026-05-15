"""简单计算器工具"""
from hello_agents.tools.base import Tool, ToolParameter

class CalculatorTool(Tool):
    """计算器工具 - 支持基础数学运算"""

    def __init__(self):
        super().__init__(
            name="calculator",
            description="执行基础数学运算（加、减、乘、除）",
        )

    def run(self, params: dict) -> str:
        expression = params.get("expression", "")
        try:
            # 安全计算：只允许数字和运算符
            allowed = set("0123456789.+-*/() ")
            if not all(c in allowed for c in expression):
                return "错误：表达式包含非法字符"
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"计算错误: {e}"

    def get_parameters(self) -> list:
        """返回参数定义"""
        return [
            ToolParameter(name="expression", type="string", description="数学表达式，如 '15 * 8 + 32'"),
        ]


def calculate(expression: str) -> str:
    """便捷函数"""
    tool = CalculatorTool()
    return tool.run({"expression": expression})
