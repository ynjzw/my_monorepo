from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# Step 1: 定义 State
class SimpleState(TypedDict):
    message: str
    processed: bool

# Step 2: 定义节点函数
def greet_node(state: SimpleState) -> dict:
    """欢迎节点：生成问候语"""
    print(f"[greet_node] 收到消息: {state['message']}")
    return {"message": f"你好！{state['message']}"}

def process_node(state: SimpleState) -> dict:
    """处理节点：标记为已处理"""
    print(f"[process_node] 处理消息: {state['message']}")
    return {"processed": True}

def test_node(state: SimpleState) -> dict:
    """测试节点：标记为已处理"""
    print(f"[test_node] 测试消息: {state['message']}")
    return {"message": f"test！{state['message']}"}

def route_after_greet(state: SimpleState) -> str:
    """
    路由函数：根据 LLM 的最新输出决定走哪条路径
    返回值必须是已注册节点名称或 END
    """
    last_message = state["message"][-1]
    
    # 如果 LLM 请求使用工具
    if "test" in last_message:
        return "test"
    
    # 否则结束
    return END


# Step 3: 构建图
builder = StateGraph(SimpleState)

# 添加条件边
builder.add_conditional_edges(
    "greet",              # 源节点
    route_after_greet,    # 路由函数
    {
        "test": "test"
    }
)
# 添加节点
builder.add_node("greet", greet_node)
builder.add_node("process", process_node)
builder.add_node("test", test_node)

# 添加边
builder.add_edge(START, "greet")
builder.add_edge("greet", "test")
builder.add_edge("greet", "process")
builder.add_edge("process", END)
builder.add_edge("test", END)

# Step 4: 编译图
graph = builder.compile()

# Step 5: 运行
result = graph.invoke({
    "message": "世界",
    "processed": False
})

print(f"\n最终结果: {result}")