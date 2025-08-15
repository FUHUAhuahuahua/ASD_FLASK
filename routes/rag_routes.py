from flask import Blueprint, request, jsonify
import os
import dashscope  # 阿里云官方SDK
from dotenv import load_dotenv

# 初始化蓝图
rag_bp = Blueprint('rag', __name__, url_prefix='/api/rag')
load_dotenv()  # 加载.env环境变量

@rag_bp.route('/query', methods=['POST'])
def rag_query():
    try:
        # 1. 解析前端请求
        request_data = request.json
        if not request_data or 'message' not in request_data:
            return jsonify({'error': '请求缺少message字段'}), 400
        
        user_message = request_data['message'].strip()
        if not user_message:
            return jsonify({'error': '问题内容不能为空'}), 400

        # 2. 加载并验证环境变量
        api_key = os.getenv("ALIYUN_API_KEY")
        knowledge_id = os.getenv("ALIYUN_KNOWLEDGE_ID")
        
        # 打印配置信息（调试用）
        print(f"API_KEY加载状态: {'成功' if api_key else '失败'}")
        print(f"KNOWLEDGE_ID加载状态: {'成功' if knowledge_id else '失败'}")
        
        if not api_key or not knowledge_id:
            return jsonify({'error': '阿里云API配置不完整（检查.env文件）'}), 500

        # 3. 配置阿里云SDK
        dashscope.api_key = api_key

        # 4. 调用RAG接口（移除task参数，适配SDK最新版本）
        print(f"开始调用RAG接口，问题: {user_message}")
        response = dashscope.Generation.call(
            model="qwen-plus",  # 模型名称（必填）
            messages=[
                {"role": "user", "content": f"请基于提供的自闭症检测知识库回答：{user_message}"}
            ],
            retrieval={
                "enable": True,
                "knowledge_id": knowledge_id  # 知识库ID
            },
            timeout=60  # 超时时间（秒）
        )

        # 5. 处理API响应
        print(f"RAG接口响应状态: {response.status_code}")
        print(f"响应内容: {response}")

        if response.status_code == 200:
            # 提取回答内容
            answer = response.output.get('text', '')
            if answer:
                return jsonify({'answer': answer})
            else:
                return jsonify({'error': 'API返回为空，未获取到答案'}), 500
        else:
            # 处理API错误
            error_msg = f"阿里云API调用失败: {response.message}"
            if hasattr(response, 'code'):
                error_msg += f" (错误码: {response.code})"
            return jsonify({'error': error_msg}), 500

    except Exception as e:
        # 捕获所有其他异常
        error_detail = f"服务器处理错误: {str(e)}"
        print(error_detail)  # 打印详细错误日志
        return jsonify({'error': error_detail}), 500
    