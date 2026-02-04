"""
测试OpenWork桥接功能
验证后端能否从OpenWork获取OpenCode服务URL
"""

import asyncio
import httpx
from app.openwork_bridge import get_openwork_bridge
from app.opencode_integration import get_opencode_generator


async def test_openwork_bridge():
    """测试OpenWork桥接功能"""
    print("=" * 60)
    print("OpenWork桥接功能测试")
    print("=" * 60)

    # 1. 测试桥接器
    print("\n1. 测试OpenWork桥接器...")
    bridge = get_openwork_bridge()
    service_info = bridge.get_service_info()

    if service_info:
        print(f"✅ 成功从OpenWork获取服务信息:")
        print(f"   - 运行状态: {service_info.get('running')}")
        print(f"   - 服务URL: {service_info.get('base_url')}")
        print(f"   - 端口: {service_info.get('port')}")
        print(f"   - 项目目录: {service_info.get('project_dir')}")
        print(f"   - 更新时间: {service_info.get('updated_at')}")
    else:
        print("⚠️  无法从OpenWork获取服务信息")
        print("   请确保OpenWork正在运行")

    # 2. 测试OpenCode生成器
    print("\n2. 测试OpenCode生成器初始化...")
    generator = get_opencode_generator()
    print(f"   OpenCode服务URL: {generator.opencode_url}")

    # 3. 测试连接
    print("\n3. 测试OpenCode服务连接...")
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{generator.opencode_url}/health")
            if response.status_code == 200:
                print(f"✅ OpenCode服务连接成功")
                health_data = response.json()
                print(f"   健康状态: {health_data}")
            else:
                print(f"❌ OpenCode服务响应异常: {response.status_code}")
    except httpx.ConnectError:
        print(f"❌ 无法连接到OpenCode服务: {generator.opencode_url}")
        print("   请确保OpenCode服务正在运行")
    except Exception as e:
        print(f"❌ 连接测试失败: {str(e)}")

    # 4. 测试后端API
    print("\n4. 测试后端API...")
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get("http://127.0.0.1:8000/opencode/status")
            if response.status_code == 200:
                print(f"✅ 后端API响应成功")
                status_data = response.json()
                print(f"   状态: {status_data.get('status')}")
                print(f"   来源: {status_data.get('source')}")
                if status_data.get('service_info'):
                    print(f"   服务信息: {status_data.get('service_info')}")
            else:
                print(f"❌ 后端API响应异常: {response.status_code}")
    except httpx.ConnectError:
        print(f"❌ 无法连接到后端服务: http://127.0.0.1:8000")
        print("   请确保后端服务正在运行")
    except Exception as e:
        print(f"❌ API测试失败: {str(e)}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_openwork_bridge())
