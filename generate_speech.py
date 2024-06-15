import os
import edge_tts
import asyncio
from flask import Flask, request, jsonify
from datetime import datetime
app = Flask(__name__)
# 可调参数：音量volume，语速rate，picth频率 可以保存文件到mp3格式，可以保存字幕
# 生成：edge-tts 重播：edge-playback
# 在前端，通过<audio controls>
#   <source src="音频位置">
# </audio>可以播放。前提是音频文件在服务器或者前端的本地。可以把绝对路径写好
# 还要注意的是 文件只生成一遍 如果要修改已经生成的文件的速度，可以在前端改
# 后端要实现的基本功能：根据选择的语音种类+输入的文本，提前设定好音量和语速，生成音频文件
# 前端：输入文本，选择语音种类，点击生成，点击试听，重播，倍速 这些基本通过autio可以实现
# 前端参考：https://blog.csdn.net/superKM/article/details/88687774
async def amain(VOICE,TEXT,OUTPUT_FILE) -> None:
    """Main function"""
    communicate = edge_tts.Communicate(TEXT, VOICE)#同步生成文件
    await communicate.save(OUTPUT_FILE)#异步保存
    print('音频文件已生成')
#创建一个列表，它包含各个template的文件名
voice_list=['zh-CN-XiaoxiaoNeural','zh-HK-HiuGaaiNeural','zh-CN-liaoning-XiaobeiNeural',
            'zh-HK-WanLungNeural','zh-CN-YunxiNeural','zh-CN-YunjianNeural']
#生成的文件所存放的路径
output_dir='D:/vs_temp/news-front/news/src/assets/output'
@app.route("/get-speech", methods=['POST'])
def get_speech():
    print(1)
    response = {
        "response": {
            "isError": True,
            "msg": "", }
    }
    try:
        data = request.get_json()
        text = data.get('text')
        # 如果没有接收到voice_type，默认选择第一个
        voice_type=data.get('voice_type')==None and 0 or data.get('voice_type')
        voice=voice_list[int(voice_type)]
        print(f"接收到post请求{text},{voice}")

        # 文件相关
        # 如果没有output_dir这个文件夹，就创建一个
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        file_prefix = datetime.now().strftime('%H_%M_%S')
        output_filename = output_dir+'/'+file_prefix + '.mp4'
        asyncio.run(amain(voice,text,output_filename))
        print('音频文件已生成')
        response['response']['data'] = file_prefix + '.mp4'
        response['response']['isError'] = False
    except Exception as e:
        response['response']['msg'] = str(e)
    return jsonify(response)

if __name__ == '__main__':
    print("已经进入main函数")
    app.run(
        host='0.0.0.0',
        port=9000,
        debug=True
    )
    # asyncio.run(amain())#异步执行
