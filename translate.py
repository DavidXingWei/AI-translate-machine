import argparse
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
import openai

def setup_client():
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set it in a .env file or export it in your environment.")
        sys.exit(1)
    return OpenAI(api_key=api_key,
    base_url = "https://api.deepseek.com"
    )
def translate(client,text,target_language="中文"):
    prompt = (f"""请将以下文本翻译成{target_language}。只输出翻译结果，不要加任何解释或前缀。原文：{text}"""
    )
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-pro",
            max_tokens=99999,
            messages=[
            {"role":"user","content":prompt}
        ]
        )
        return response.choices[0].message.content
    except openai.AuthenticationError:
        print("错误：认证失败，请检查您的 API 密钥是否正确。")
        sys.exit(1) 
    except openai.RateLimitError:
        print("错误：请求频率超过限制或余额不足，请稍后再试。")
        sys.exit(1)
    except openai.APIconnectionError:
        print("错误：无法连接到 DeepSeek API，请检查您的网络连接。")
        sys.exit(1)
    except openai.APIError as e:
        print(f"错误：API 调用失败，错误信息：{e}")
        sys.exit(1)

def main():
    parser=argparse.ArgumentParser(
        description="CLI翻译工具-使用 DeepSeek AI 进行翻译",
        epilog="示例用法:python translate.py -t 'Hello, how are you?' -l '中文'"   
    )
    parser.add_argument(
        "--text", "-t",
        help="要翻译的文本内容"
    )      
    parser.add_argument(
        "--file", "-f",
        help="要翻译的文本文件路径"
    )
    parser.add_argument(
        "--to", "-l",
        default="中文",
        dest="target_language", 
        help="目标语言（默认：中文）"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="启用详细输出，显示翻译过程中的调试信息"
    )
    args=parser.parse_args()
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                args.text = f.read()
        except FileNotFoundError:
            print(f"错误：文件 '{args.file}' 未找到，请检查路径是否正确。")
            sys.exit(1)
        except IOError as e:
            print(f"错误：无法读取文件 '{args.file}'，错误信息：{e}")
            sys.exit(1)
    else:
       text_to_translate = args.text

    if not args.text.strip():
        print("错误：输入文本不能为空")
        sys.exit(1)
    if args.verbose:
        print(f"原文：{args.text}")
        print(f"目标语言：{args.target_language}")
        print("正在翻译...")
    client=setup_client()
    result=translate(client,args.text,args.target_language)
    print(result)
if __name__ == "__main__":
    main()
