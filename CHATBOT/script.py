#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能餐廳聊天機器人啟動腳本
Intelligent Restaurant Chatbot Launcher Script

這個腳本提供了多種功能來管理聊天機器人專案：
- 環境檢查和依賴安裝
- 模型下載和驗證提醒
- 服務器啟動
- 功能測試
"""

import os
import sys
import subprocess
import importlib
import argparse
from pathlib import Path

class ChatbotLauncher:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.requirements = [
            'flask',
            'flask-socketio',
            'transformers',
            'torch',
            'spacy',
            'langchain',
            'pyngrok',
            'gevent',
            'python-dotenv',
            'pandas',
            'openpyxl',
            'sentence-transformers',
            'llama-factory',
            'scikit-learn',
            'python-Levenshtein',
            'numpy',
            'langchain-community',
            'langchain-huggingface',
            'requests'
        ]

    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                智能餐廳聊天機器人啟動器                        ║
║              Intelligent Restaurant Chatbot Launcher         ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def check_python_version(self):
        print("🔍 檢查Python版本...")
        if sys.version_info < (3, 8):
            print("❌ 需要Python 3.8或更高版本")
            print(f"   當前版本: {sys.version}")
            return False
        print(f"✅ Python版本檢查通過: {sys.version}")
        return True

    def check_dependencies(self):
        print("\n🔍 檢查依賴套件...")
        missing = []
        for pkg in self.requirements:
            try:
                importlib.import_module(pkg.replace('-', '_'))
                print(f"✅ {pkg}")
            except ImportError:
                print(f"❌ {pkg} - 未安裝")
                missing.append(pkg)
        if missing:
            print(f"\n⚠️  有 {len(missing)} 個未安裝的套件")
            return False
        print("\n✅ 所有依賴套件檢查通過")
        return True

    def install_dependencies(self):
        print("\n📦 安裝依賴套件...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + self.requirements)
            print("✅ 依賴套件安裝完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 安裝失敗: {e}")
            return False

    def download_spacy_model(self):
        print("\n📥 下載SpaCy中文模型...")
        try:
            subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'zh_core_web_sm'])
            print("✅ SpaCy模型下載完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 模型下載失敗: {e}")
            return False

    def check_data_files(self):
        print("\n📁 檢查資料文件...")
        required_files = [
            'data.json',
            'storeinfo_review.json', 
            'tag_embeddings.json',
            'updated_storeinfo_tablesm.json',
            'test_review.txt',
            'config.py'
        ]
        missing = []
        for file in required_files:
            if (self.project_root / file).exists():
                print(f"✅ {file}")
            else:
                print(f"❌ {file} - 文件不存在")
                missing.append(file)
        if missing:
            print(f"\n⚠️  缺少 {len(missing)} 個必要文件")
            return False
        print("\n✅ 所有資料文件檢查通過")
        return True

    def check_model_directories(self):
        print("\n🤖 檢查模型目錄...")
        required_dirs = [
            'CHATBOT/output',
            'CHATBOT/output2_dia_reserve',
            'CHATBOT/output2_dia_recommand', 
            'CHATBOT/output2_dia_map',
            'CHATBOT/new_result',
            'CHATBOT/Is_Collect_or_Function',
            'CHATBOT/NLG_TAIDE',
            'CHATBOT/shibing624_text2vec-base-chinese'
        ]
        missing = []
        for dir_path in required_dirs:
            if (self.project_root / dir_path).exists():
                print(f"✅ {dir_path}")
            else:
                print(f"❌ {dir_path} - 目錄不存在")
                missing.append(dir_path)
        if missing:
            print(f"\n⚠️  缺少 {len(missing)} 個模型目錄")
            print("📥 請從Google Drive下載模型權重：")
            print("   https://drive.google.com/drive/folders/1xt2j6hwjhCDhpAqlXl1bVf1dRDx-EIxc?usp=sharing")
            return False
        print("\n✅ 所有模型目錄檢查通過")
        return True

    def test_imports(self):
        print("\n🧪 測試模組導入...")
        modules = [
            'user_information',
            'classification_function',
            'spacy_function',
            'dp_function',
            'chat_function',
            'use_function',
            'database',
            'config'
        ]
        failed = []
        for m in modules:
            try:
                importlib.import_module(m)
                print(f"✅ {m}")
            except ImportError as e:
                print(f"❌ {m} - 導入失敗: {e}")
                failed.append(m)
        if failed:
            print(f"\n⚠️  有 {len(failed)} 個模組導入失敗")
            return False
        print("\n✅ 所有模組導入成功")
        return True

    def run_quick_test(self):
        print("\n🧪 執行快速功能測試...")
        try:
            from classification_function import NLU
            nlu = NLU()
            print("✅ NLU模組測試通過")
            from spacy_function import NER
            ner = NER()
            print("✅ NER模組測試通過")
            from user_information import User
            user = User()
            print("✅ User類別測試通過")
            from config import NLU_FUNCTION_MODEL, SPACY_STORE_MODEL
            print("✅ Config模組測試通過")
            print("\n✅ 快速測試完成")
            return True
        except Exception as e:
            print(f"❌ 測試失敗: {e}")
            return False

    def start_server(self, host='localhost', port=5000, debug=False, external=False):
        print(f"\n🚀 啟動聊天機器人服務器...")
        print(f"   主機: {host}")
        print(f"   端口: {port}")
        print(f"   調試模式: {'開啟' if debug else '關閉'}")
        print(f"   外部訪問: {'開啟' if external else '關閉'}")
        try:
            os.environ['FLASK_ENV'] = 'development' if debug else 'production'
            if external:
                from pyngrok import ngrok
                public_url = ngrok.connect(port)
                print(f"\n🌐 外部訪問URL: {public_url}")
            from main import app, socketio
            socketio.run(app, host=host, port=port, debug=debug)
        except KeyboardInterrupt:
            print("\n⏹️  服務器已停止")
        except Exception as e:
            print(f"❌ 啟動失敗: {e}")

    def show_status(self):
        print("\n📊 專案狀態報告")
        print("=" * 50)
        print(f"Python版本: {sys.version}")
        print("\n依賴套件狀態:")
        for pkg in self.requirements:
            try:
                module = importlib.import_module(pkg.replace('-', '_'))
                version = getattr(module, '__version__', '未知')
                print(f"  {pkg}: {version}")
            except ImportError:
                print(f"  {pkg}: 未安裝")
        print("\n文件狀態:")
        files = ['main.py', 'data.json', 'storeinfo_review.json', 'config.py']
        for file in files:
            path = self.project_root / file
            if path.exists():
                size = path.stat().st_size
                print(f"  {file}: {size:,} bytes")
            else:
                print(f"  {file}: 不存在")

    def setup_environment(self):
        print("\n🔧 開始環境設定...")
        if not self.check_python_version():
            return False
        if not self.check_dependencies():
            print("\n📦 嘗試安裝缺失的依賴套件...")
            if not self.install_dependencies():
                return False
        if not self.download_spacy_model():
            return False
        if not self.check_data_files():
            print("\n⚠️  請確保所有必要文件存在")
            return False
        if not self.check_model_directories():
            print("\n⚠️  請確保所有模型目錄存在")
            return False
        if not self.test_imports():
            return False
        print("\n✅ 環境設定完成！")
        return True

def main():
    parser = argparse.ArgumentParser(description='智能餐廳聊天機器人啟動器')
    parser.add_argument('action', nargs='?', default='start', 
                       choices=['start', 'setup', 'test', 'status', 'help'],
                       help='執行動作')
    parser.add_argument('--host', default='localhost', help='服務器主機')
    parser.add_argument('--port', type=int, default=5000, help='服務器端口')
    parser.add_argument('--debug', action='store_true', help='開啟調試模式')
    parser.add_argument('--external', action='store_true', help='啟用外部訪問')
    args = parser.parse_args()
    launcher = ChatbotLauncher()
    launcher.print_banner()
    if args.action == 'help':
        parser.print_help()
        return
    elif args.action == 'setup':
        if launcher.setup_environment():
            print("\n🎉 設定完成！現在可以使用 'python script.py start' 啟動服務器")
        else:
            print("\n❌ 設定失敗，請檢查錯誤信息")
            sys.exit(1)
    elif args.action == 'test':
        if launcher.setup_environment():
            launcher.run_quick_test()
        else:
            print("\n❌ 環境檢查失敗，無法執行測試")
            sys.exit(1)
    elif args.action == 'status':
        launcher.show_status()
    elif args.action == 'start':
        print("🔍 執行啟動前檢查...")
        if launcher.setup_environment():
            print("\n🎯 開始啟動聊天機器人...")
            launcher.start_server(
                host=args.host,
                port=args.port,
                debug=args.debug,
                external=args.external
            )
        else:
            print("\n❌ 環境檢查失敗，請先執行 'python script.py setup'")
            sys.exit(1)

if __name__ == '__main__':
    main() 