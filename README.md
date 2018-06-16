
使用方法
	
	1. pyinstaller -F qiangchang_UI.py  (-w 可不顯示cmd)

	2. 使用不帶界面的script，文件在script下


注意事項：
1.選擇目錄下你對應的Chrome版本chromedriver.exe解壓到當前文件夾目錄下。
(必須要版本兼容，如果是64-66可能在66版本會出問題，請下最新的chromedriver 65-67)
2.如果沒有你driver的版本(目前只有下兩種版本)，請去這個網址下載對應版本。（64位下WIN32即可）
  https://sites.google.com/a/chromium.org/chromedriver/downloads
3.直接執行qiangchang_UI.exe 然後直接點開始搶場進入test mode。
4.通過testmode後即可正常輸入使用。！
											Edit_By_Fook 2018.04.07

											
出現process_metrics.cc not implemented的問題原因：
Chrome 版本是63，升級到其他版本（以上應該就好了。）
感謝RenDe Chen的測試數據，bug 反饋
											Edit_By_Fook 2018.04.24
