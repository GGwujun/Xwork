#!/usr/bin/env python3
"""
OpenCode集成功能测试脚本
"""

import asyncio
import json
from app.opencode_integration import OpenCodeSpecGenerator, OpenCodeError
from app.schemas import Requirement

async def test_opencode_integration():
    """测试OpenCode集成功能"""
    print("开始测试OpenCode集成功能...")

    # 创建测试需求
    test_requirement = Requirement(
        summary="创建一个简单的计算器应用",
        description="开发一个基于Web的计算器应用，支持基本的四则运算（加减乘除），具有清晰的用户界面和响应式设计。",
        acceptance_criteria=[
            "支持加法、减法、乘法、除法运算",
            "具有清除和重置功能",
            "界面美观且响应式",
            "支持键盘输入"
        ]
    )

    print(f"测试需求: {test_requirement.summary}")
    print(f"详细描述: {test_requirement.description}")

    # 创建OpenCode生成器实例
    generator = OpenCodeSpecGenerator("http://127.0.0.1:4096")

    try:
        print("\n开始生成OpenSpec...")

        # 生成规范
        spec = await generator.generate_spec(test_requirement)

        print("OpenSpec生成成功!")
        print(f"项目名称: {spec.project_name}")
        print(f"任务数量: {len(spec.tasks)}")

        if spec.design:
            print(f"架构概述长度: {len(spec.design.architecture_overview)} 字符")
            print(f"API端点数量: {len(spec.design.api_endpoints)}")
            print(f"数据模型数量: {len(spec.design.data_models)}")

        print("\n任务列表:")
        for i, task in enumerate(spec.tasks, 1):
            print(f"  {i}. {task.title}")
            print(f"     状态: {task.status}")
            if task.file_changes:
                print(f"     文件变更: {', '.join(task.file_changes)}")

        # 保存测试结果
        result_file = "test_opencode_result.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(spec.dict(), f, ensure_ascii=False, indent=2)
        print(f"\n测试结果已保存到: {result_file}")

        return True

    except OpenCodeError as e:
        print(f"OpenCode服务错误: {e}")
        print("请确保OpenCode服务正在运行在 http://127.0.0.1:4096")
        return False

    except Exception as e:
        print(f"未知错误: {e}")
        return False

async def test_api_endpoint():
    """测试API端点"""
    print("\n测试API端点...")

    import httpx

    test_data = {
        "requirement": {
            "summary": "创建一个简单的待办事项应用",
            "description": "开发一个基于Web的待办事项管理应用，用户可以添加、编辑、删除和标记完成待办事项。",
            "acceptance_criteria": [
                "用户可以添加新的待办事项",
                "用户可以编辑现有的待办事项",
                "用户可以删除待办事项",
                "用户可以标记待办事项为完成"
            ]
        }
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                "http://127.0.0.1:8000/spec/generate-via-opencode",
                json=test_data
            )

            if response.status_code == 200:
                result = response.json()
                print("API端点测试成功!")
                print(f"项目名称: {result.get('project_name', 'N/A')}")
                print(f"任务数量: {len(result.get('tasks', []))}")
                return True
            else:
                print(f"API端点测试失败: HTTP {response.status_code}")
                print(f"错误信息: {response.text}")
                return False

    except httpx.ConnectError:
        print("无法连接到后端服务 (http://127.0.0.1:8000)")
        print("请确保后端服务正在运行")
        return False
    except Exception as e:
        print(f"API测试错误: {e}")
        return False

async def main():
    """主测试函数"""
    print("OpenCode集成功能测试")
    print("=" * 50)

    # 测试1: 直接测试OpenCode集成
    success1 = await test_opencode_integration()

    # 测试2: 测试API端点
    success2 = await test_api_endpoint()

    print("\n" + "=" * 50)
    print("测试结果总结:")
    print(f"  OpenCode集成测试: {'通过' if success1 else '失败'}")
    print(f"  API端点测试: {'通过' if success2 else '失败'}")

    if success1 and success2:
        print("\n所有测试通过! OpenCode集成功能正常工作。")
    else:
        print("\n部分测试失败，请检查相关服务状态。")

if __name__ == "__main__":
    asyncio.run(main())