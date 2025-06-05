from openai import OpenAI
import os

def get_description_local(img_base64, file_ext, prompt):
    # 模拟API延迟
    import time
    time.sleep(1)
    tokens = [
        f"根据Prompt: ({prompt}) 生成的描述，",
        f"图片格式: {file_ext.upper()}，",
        "主要对象: 示例对象、",
        "场景: 示例场景、",
        "颜色分析: 示例颜色、",
        "风格: 示例风格。",
        "这是根据用户自定义Prompt生成的模拟响应，实际API会返回更准确的分析结果。"
    ]
    yield "模拟 LLM"
    for token in tokens:
        yield f"data: {token}\n\n"

def get_description_error(img_base64, file_ext, prompt):
    import time
    time.sleep(1)
    raise Exception("模拟 API 错误")

def get_description(img_base64, file_ext, prompt):
    # 使用阿里云百炼API，qwen-vl-max模型
    client = OpenAI(
        api_key = os.getenv("DASHSCOPE_API_KEY"),
        base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    model_name = "qwen-vl-max"

    # 流式输出
    stream = client.chat.completions.create(
        model=model_name,
        stream=True,
        messages=[
            {
                "role": "system", 
                "content": [{"type": "text", "text": "You are a helpful assistant."}]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/{file_ext};base64,{img_base64}"
                        }
                    },
                    {"type": "text", "text": prompt}
                ]
            }
        ]
    )

    yield model_name
    for chunk in stream:
        token = chunk.choices[0].delta.content
        if token:
            yield f"data: {token}\n\n"