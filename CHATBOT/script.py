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
        # 修正套件名稱映射 - 套件名:模組名
        self.requirements = {
            'flask': 'flask',
            'flask-socketio': 'flask_socketio',
            'transformers': 'transformers',
            'torch': 'torch',
            'spacy': 'spacy',
            'langchain': 'langchain',
            'pyngrok': 'pyngrok',
            'gevent': 'gevent',
            'python-dotenv': 'dotenv',
            'pandas': 'pandas',
            'openpyxl': 'openpyxl',
            'sentence-transformers': 'sentence_transformers',
            'scikit-learn': 'sklearn',
            'python-Levenshtein': 'Levenshtein',
            'numpy': 'numpy',
            'langchain-community': 'langchain_community',
            'langchain-huggingface': 'langchain_huggingface',
            'requests': 'requests',
            'jieba': 'jieba',
            'bitsandbytes': 'bitsandbytes'
        }
        
        # 可選的依賴套件（如果沒有也不會阻止啟動）
        self.optional_requirements = {
            'llama-factory': 'llamafactory'
        }

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
        optional_missing = []
        
        # 檢查必需套件
        for pkg_name, module_name in self.requirements.items():
            try:
                importlib.import_module(module_name)
                print(f"✅ {pkg_name}")
            except ImportError:
                print(f"❌ {pkg_name} - 未安裝")
                missing.append(pkg_name)
        
        # 檢查可選套件
        for pkg_name, module_name in self.optional_requirements.items():
            try:
                importlib.import_module(module_name)
                print(f"✅ {pkg_name} (可選)")
            except ImportError:
                print(f"⚠️  {pkg_name} - 未安裝 (可選)")
                optional_missing.append(pkg_name)
        
        if missing:
            print(f"\n⚠️  有 {len(missing)} 個必需套件未安裝")
            return False
        
        if optional_missing:
            print(f"\n💡 有 {len(optional_missing)} 個可選套件未安裝，但不影響基本功能")
        
        print("\n✅ 所有必需依賴套件檢查通過")
        return True

    def install_dependencies(self):
        print("\n📦 安裝依賴套件...")
        try:
            # 使用 requirements.txt 安裝
            if (self.project_root / 'requirements.txt').exists():
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
                ])
                print("✅ 從 requirements.txt 安裝依賴套件完成")
            else:
                # 如果沒有 requirements.txt，則安裝核心套件
                core_packages = list(self.requirements.keys())
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install'
                ] + core_packages)
                print("✅ 核心依賴套件安裝完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 安裝失敗: {e}")
            print("💡 建議手動執行: pip install -r requirements.txt")
            return False

    def download_spacy_model(self):
        print("\n📥 下載SpaCy中文模型...")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'spacy', 'download', 'zh_core_web_sm'
            ])
            print("✅ SpaCy模型下載完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"⚠️  SpaCy模型下載失敗: {e}")
            print("�� 可以稍後手動執行: python -m spacy download zh_core_web_sm")
            return True  # 不阻止啟動

    def check_data_files(self):
        print("\n📁 檢查資料文件...")
        # 修正檔案路徑檢查
        required_files = [
            'data.json',
            'storeinfo_review.json', 
            'tag_embeddings.json',
            'updated_storeinfo_tablesm.json',
            'config.py'
        ]
        
        missing = []
        for file in required_files:
            file_path = self.project_root / file
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"✅ {file} ({size:,} bytes)")
            else:
                print(f"❌ {file} - 文件不存在")
                missing.append(file)
        
        if missing:
            print(f"\n⚠️  缺少 {len(missing)} 個必要文件")
            print("📥 請確保已解壓縮所有數據檔案到 CHATBOT/data/ 目錄")
            return False
        
        print("\n✅ 所有資料文件檢查通過")
        return True

    def check_model_directories(self):
        print("\n🤖 檢查模型目錄...")
        # 修正模型目錄路徑檢查
        model_dirs = [
            'model',
            'output',
            'output2_dia_reserve',
            'output2_dia_recommand', 
            'output2_dia_map',
            'new_result',
            'Is_Collect_or_Function',
            'NLG_TAIDE',
            'shibing624_text2vec-base-chinese'
        ]
        
        missing = []
        for dir_name in model_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                print(f"✅ {dir_name}")
            else:
                print(f"❌ {dir_name} - 目錄不存在")
                missing.append(dir_name)
        
        if missing:
            print(f"\n⚠️  缺少 {len(missing)} 個模型目錄")
            print("📥 請從Google Drive下載模型權重：")
            print("   https://drive.google.com/drive/folders/1xt2j6hwjhCDhpAqlXl1bVf1dRDx-EIxc?usp=sharing")
            print("💡 如果只是測試基本功能，可以暫時跳過此檢查")
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
            print("💡 這可能是因為缺少模型檔案或數據檔案")
            return False
        
        print("\n✅ 所有模組導入成功")
        return True

    def run_quick_test(self):
        print("\n🧪 執行快速功能測試...")
        try:
            # 測試基本模組
            import config
            print("✅ Config模組測試通過")
            
            # 嘗試測試其他模組（如果可用）
            try:
                from classification_function import NLU
                nlu = NLU()
                print("✅ NLU模組測試通過")
            except Exception as e:
                print(f"⚠️  NLU模組測試失敗: {e}")
            
            try:
                from spacy_function import NER
                ner = NER()
                print("✅ NER模組測試通過")
            except Exception as e:
                print(f"⚠️  NER模組測試失敗: {e}")
            
            try:
                from user_information import User
                user = User()
                print("✅ User類別測試通過")
            except Exception as e:
                print(f"⚠️  User類別測試失敗: {e}")
            
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
                try:
                    from pyngrok import ngrok
                    public_url = ngrok.connect(port)
                    print(f"\n🌐 外部訪問URL: {public_url}")
                except Exception as e:
                    print(f"⚠️  外部訪問設置失敗: {e}")
                    print("💡 將使用本地模式啟動")
            
            from main import app, socketio
            socketio.run(app, host=host, port=port, debug=debug)
            
        except KeyboardInterrupt:
            print("\n⏹️  服務器已停止")
        except Exception as e:
            print(f"❌ 啟動失敗: {e}")
            print("💡 請檢查錯誤信息並確保所有依賴已正確安裝")

    def show_status(self):
        print("\n📊 專案狀態報告")
        print("=" * 50)
        print(f"Python版本: {sys.version}")
        print(f"專案路徑: {self.project_root}")
        
        print("\n依賴套件狀態:")
        for pkg_name, module_name in self.requirements.items():
            try:
                module = importlib.import_module(module_name)
                version = getattr(module, '__version__', '未知')
                print(f"  {pkg_name}: {version}")
            except ImportError:
                print(f"  {pkg_name}: 未安裝")
        
        print("\n文件狀態:")
        files = ['main.py', 'data.json', 'storeinfo_review.json', 'config.py']
        for file in files:
            path = self.project_root / file
            if path.exists():
                size = path.stat().st_size
                print(f"  {file}: {size:,} bytes")
            else:
                print(f"  {file}: 不存在")

    def setup_environment(self, strict_mode=False):
        print("\n🔧 開始環境設定...")
        
        # Python版本檢查
        if not self.check_python_version():
            return False
        
        # 依賴套件檢查
        if not self.check_dependencies():
            print("\n📦 嘗試安裝缺失的依賴套件...")
            if not self.install_dependencies():
                if strict_mode:
                    return False
                else:
                    print("⚠️  依賴安裝失敗，但繼續進行其他檢查...")
        
        # SpaCy模型下載（非阻塞）
        self.download_spacy_model()
        
        # 數據文件檢查
        if not self.check_data_files():
            if strict_mode:
                return False
            else:
                print("⚠️  數據文件檢查失敗，但繼續進行其他檢查...")
        
        # 模型目錄檢查（非阻塞）
        self.check_model_directories()
        
        # 模組導入測試
        if not self.test_imports():
            if strict_mode:
                return False
            else:
                print("⚠️  模組導入測試失敗，但繼續進行...")
        
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
    parser.add_argument('--strict', action='store_true', help='嚴格模式檢查')
    
    args = parser.parse_args()
    launcher = ChatbotLauncher()
    launcher.print_banner()
    
    if args.action == 'help':
        parser.print_help()
        return
    elif args.action == 'setup':
        if launcher.setup_environment(strict_mode=args.strict):
            print("\n🎉 設定完成！現在可以使用 'python script.py start' 啟動服務器")
        else:
            print("\n❌ 設定失敗，請檢查錯誤信息")
            if not args.strict:
                print("💡 嘗試使用 --strict 參數進行更嚴格的檢查")
            sys.exit(1)
    elif args.action == 'test':
        if launcher.setup_environment(strict_mode=False):
            launcher.run_quick_test()
        else:
            print("\n❌ 環境檢查失敗，無法執行測試")
            sys.exit(1)
    elif args.action == 'status':
        launcher.show_status()
    elif args.action == 'start':
        print("🔍 執行啟動前檢查...")
        if launcher.setup_environment(strict_mode=False):
            print("\n🎯 開始啟動聊天機器人...")
            launcher.start_server(
                host=args.host,
                port=args.port,
                debug=args.debug,
                external=args.external
            )
        else:
            print("\n❌ 環境檢查失敗")
            print("💡 嘗試執行 'python script.py setup' 進行完整設定")
            print("💡 或使用 'python main.py' 直接啟動（跳過檢查）")
            sys.exit(1)

if __name__ == '__main__':
    main()