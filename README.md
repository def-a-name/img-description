# Image Description


img-description 是一个基于 `Python Flask` 框架开发的 Web 应用。用户上传一张图片后，应用将通过 API 把图片发送给大语言模型（LLM），请求其进行理解与描述，然后返回描述结果。


## 主要特性

- 支持多种图片格式上传`（png | jpg | jpeg | jpe | tif | tiff | webp | bmp | heic）`；
- 调用阿里云百炼 API，使用 `QWEN-VL` 系列模型；
- 流式输出结果，并按照 `Markdown` 样式渲染；
- 自定义 prompt，支持 prompt 历史记录的保存、查看和管理；
- 保存 `用户请求` 和 `模型回应` 记录到数据库中，制作了展示页面；

## 本地运行

1. **克隆项目**

   ```bash
   git clone https://github.com/def-a-name/img-description.git
   cd img-description
   ```

2. **安装依赖**

   建议新建 python 虚拟环境：
   ```bash
   python -m venv venv
   # Linux
   source venv/bin/activate
   # Windows
   source venv/Script/activate
   ```
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **添加 API-Key**

   将 [阿里云百炼平台](https://bailian.console.aliyun.com/#/home) 的 API-Key 添加到 **环境变量**`DASHSCOPE_API_KEY` 中，或者直接在 [api.py](https://github.com/def-a-name/img-description/blob/main/service/api.py#L28) 里替换。

4. **启动应用**

   ```bash
   python app.py
   ```
   应用将默认以 debug 模式在本地运行，可访问 [http://127.0.0.1:5000](http://127.0.0.1:5000)。

## 部署

- 关闭 `Flask` 的 `Debug` 模式`（app.py 中 app.run(debug=False)）`；
- 使用 `Gunicorn` 或 `uWSGI` 等 `WSGI` 服务器运行 `Flask`：
     ```bash
     # gunicorn 示例 
     gunicorn -w 4 -b 127.0.0.1:8000 app:app --timeout 0
     ```
- 使用 `Nginx` 等工具反向代理；
