import base64
import traceback
from playwright.async_api import async_playwright
from schemas import Node, Edge
from typing import List, Dict
# from config import VIEWPORT
from strategies import get_strategy 
from strategies.base import BaseStrategy

# 简单的原子操作兜底 (防止 forgot to register strategy)
class AtomicStrategy(BaseStrategy):
    async def execute(self, page, params, logs):
        pass # 暂时不做兜底，依靠 Registry

async def execute_task(nodes: List[Node], edges: List[Edge], cdp_url: str):
    # 1. 图结构映射
    node_map = {n.id: n for n in nodes}
    adjacency = {e.source: e.target for e in edges}
    
    start_node = next((n for n in nodes if n.data.get('nodeType') == 'start'), None)
    if not start_node:
        return {"status": "error", "message": "未找到 Start 节点"}

    print(f"--- 引擎启动，连接: {cdp_url} ---")
    
    # === 循环计数器 { 'node_id': current_count } ===
    loop_counters: Dict[str, int] = {} 

    async with async_playwright() as p:
        try:
            # 2. 连接浏览器
            # 尝试连接，如果失败则提示用户
            try:
                browser = await p.chromium.connect_over_cdp(cdp_url)
            except Exception as e:
                 return {"status": "error", "message": f"无法连接浏览器，请检查是否开启了9222端口: {str(e)}"}

            # 获取上下文
            context = browser.contexts[0] if browser.contexts else await browser.new_context()
            if context.pages:
                page = context.pages[0] # 使用当前激活的页面
            else:
                page = await context.new_page()
            
            # await page.set_viewport_size(VIEWPORT)

            # 3. 开始遍历执行
            current_node_id = start_node.id
            logs = []

            while current_node_id:
                node = node_map.get(current_node_id)
                if not node: break

                node_type = node.data.get('nodeType')
                
                # ==========================================
                # 🔄 核心循环控制逻辑
                # ==========================================
                if node_type == 'loop_start':
                    # 获取设定的最大循环次数 (默认为1)
                    max_loops = int(node.data.get('loop_count', 1))
                    
                    # 初始化或获取当前计数
                    current_count = loop_counters.get(node.id, 0)
                    
                    # 判断逻辑
                    if current_count < max_loops:
                        # 次数未满，计数+1，继续执行
                        loop_counters[node.id] = current_count + 1
                        logs.append(f"🔄 [循环控制] 进入第 {loop_counters[node.id]} / {max_loops} 次循环")
                    else:
                        # 次数已满，终止路径
                        logs.append(f"🛑 [循环控制] 循环次数已达上限 ({max_loops})，跳出循环。")
                        # 在当前的单线逻辑中，跳出循环意味着切断 Next 指针
                        # 如果未来支持多分支，这里应该跳转到 'False' 路径
                        current_node_id = None 
                        break # 退出 while
                # ==========================================

                # 4. 执行具体策略
                strategy = get_strategy(node_type)
                
                if strategy:
                    try:
                        await strategy.run(page, node.data, logs)
                    except Exception as e:
                        logs.append(f"❌ [执行错误] 节点 {node_type} 报错: {str(e)}")
                        traceback.print_exc()
                elif node_type != 'start':
                    logs.append(f"⚠️ 未知节点类型: {node_type}")

                # 5. 寻找下一个节点
                current_node_id = adjacency.get(current_node_id)

            # 6. 任务结束：截图证明
            try:
                screenshot = await page.screenshot()
                b64_img = base64.b64encode(screenshot).decode('utf-8')
            except:
                b64_img = None # 可能会出现页面已关闭的情况

            # 断开连接 (注意：connect_over_cdp 时不要用 browser.close() 关闭进程，而是断开 socket)
            await browser.close()

            return {
                "status": "success", 
                "logs": logs, 
                "screenshot": f"data:image/png;base64,{b64_img}" if b64_img else None
            }

        except Exception as e:
            traceback.print_exc()
            return {"status": "error", "message": f"引擎内部错误: {str(e)}"}