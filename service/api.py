def get_test_description(base64_image, file_ext, prompt):
    # 模拟API延迟
    import time
    time.sleep(1)
    return {
        'model': '模拟LLM',
        'description': \
            f"""根据Prompt:「{prompt}」生成的描述:

                图片格式: {file_ext.upper()}
                模拟生成内容:
                - 主要对象: 示例对象
                - 场景: 示例场景
                - 颜色分析: 示例颜色
                - 风格: 示例风格

                详细描述:
                这是根据用户自定义Prompt生成的模拟响应。实际API会返回更准确的分析结果。""",
        'prompt_used': prompt
    }