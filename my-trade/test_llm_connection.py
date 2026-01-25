#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
测试本地大模型连接
"""
import requests
import json

# 本地模型配置
API_URL = "http://10.56.88.6:1234/v1/chat/completions"
MODEL = "google/gemma-3-27b"

def test_local_model():
    """测试本地模型是否正常工作"""
    print("=" * 80)
    print("测试本地大模型连接")
    print("=" * 80)
    print(f"API URL: {API_URL}")
    print(f"模型: {MODEL}")
    print()

    # 构建请求
    request_data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "你是一个有帮助的助手。"},
            {"role": "user", "content": "你好，请简单介绍一下自己。"}
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    print("发送请求...")
    print(f"请求数据: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
    print()

    try:
        response = requests.post(
            url=API_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(request_data),
            timeout=60
        )

        print(f"响应状态码: {response.status_code}")
        print()

        if response.status_code == 200:
            result = response.json()
            print("✅ 连接成功！")
            print()
            print("完整响应:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print()

            if 'choices' in result and len(result['choices']) > 0:
                message = result['choices'][0].get('message', {})
                content = message.get('content', '')
                print("=" * 80)
                print("模型回答:")
                print("=" * 80)
                print(content)
                print()

                # 检查是否支持 reasoning
                if 'reasoning_details' in message:
                    print("✅ 本地模型支持 reasoning 功能")
                else:
                    print("⚠️  本地模型不支持 reasoning 功能（这是正常的）")

                return True
            else:
                print("❌ 响应格式异常")
                return False
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ 连接失败！")
        print()
        print("请确保:")
        print("1. 本地模型服务已启动")
        print("2. 服务运行在 http://10.56.88.6:1234")
        print("3. 防火墙没有阻止连接")
        return False
    except requests.exceptions.Timeout:
        print("❌ 请求超时！")
        print("本地模型可能需要更长的处理时间，或者服务未响应")
        return False
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return False


def test_streaming():
    """测试流式响应"""
    print("\n" + "=" * 80)
    print("测试流式响应")
    print("=" * 80)

    request_data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": "数到5"}
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": True
    }

    print("发送流式请求...")

    try:
        response = requests.post(
            url=API_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(request_data),
            stream=True,
            timeout=60
        )

        if response.status_code == 200:
            print("✅ 流式连接成功！")
            print("\n收到的数据流:")
            print("-" * 80)

            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]  # 移除 'data: ' 前缀
                        if data_str.strip() != '[DONE]':
                            try:
                                data = json.loads(data_str)
                                if 'choices' in data and len(data['choices']) > 0:
                                    delta = data['choices'][0].get('delta', {})
                                    content = delta.get('content', '')
                                    if content:
                                        print(content, end='', flush=True)
                            except json.JSONDecodeError:
                                pass

            print("\n" + "-" * 80)
            print("✅ 流式响应测试完成")
            return True
        else:
            print(f"❌ 流式请求失败: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ 流式测试失败: {e}")
        return False


if __name__ == "__main__":
    print("\n🚀 本地大模型连接测试\n")

    # 测试基本连接
    basic_ok = test_local_model()

    # 测试流式响应（如果基本连接成功）
    stream_ok = False
    if basic_ok:
        stream_ok = test_streaming()

    print("\n" + "=" * 80)
    print("测试总结")
    print("=" * 80)
    print(f"基本连接: {'✅ 通过' if basic_ok else '❌ 失败'}")
    if basic_ok:
        print(f"流式响应: {'✅ 通过' if stream_ok else '❌ 失败'}")

    if basic_ok:
        print("\n✅ 本地模型配置正确，可以使用投资顾问了！")
    else:
        print("\n❌ 请检查本地模型服务是否正常运行")
        print("\n启动建议:")
        print("1. 确保 LM Studio 或其他本地模型服务已启动")
        print("2. 确认服务监听在 10.56.88.6:1234")
        print("3. 确认模型名称为 'google/gemma-3-27b'")
