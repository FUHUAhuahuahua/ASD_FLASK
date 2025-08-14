from flask import Blueprint, request, jsonify
import requests
from dotenv import load_dotenv
import os

rag_bp = Blueprint('rag', __name__, url_prefix='/api/rag')
load_dotenv()  # 加载.env文件

@rag_bp.route('/query', methods=['POST'])
def rag_query():
    try:
        data = request.json
        user_message = data.get('message', '')
        if not user_message:
            return jsonify({'error': '请输入问题'}), 400

        # 构造阿里云API请求
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.getenv("ALIYUN_API_KEY")}'
        }
        payload = {
            "model": "qwen-plus",
            "messages": [
                {"role": "user", "content": user_message},
                {"role": "system", "content": "请基于提供的自闭症检测知识库回答问题"}
            ],
            "retrieval": {
                "enable": True,
                "knowledge_id": os.getenv("ALIYUN_KNOWLEDGE_ID")
            }
        }

        # 调用阿里云API
        response = requests.post(
            'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation',
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        # 解析并返回结果
        answer = response.json()['output']['text']
        return jsonify({'answer': answer})

    except Exception as e:
        return jsonify({'error': str(e)}), 500